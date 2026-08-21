# -*- coding: utf-8 -*-
"""
日历数据生成器 —— 撕纸风插画风日历 skill 配套脚本

用法:
    python scripts/calendar.py 2026 3          # 单月
    python scripts/calendar.py 2026 3-5        # 连续多月
    python scripts/calendar.py 2026 all        # 整年
    python scripts/calendar.py 2026 3 --no-lunar   # 无农历依赖降级模式

输出:
    CALENDAR_TEXT  —— 嵌入生图 prompt 的日期网格文本（逐字排版用）
    控制台月历块   —— 供 agent 自查

依赖:
    pip install lunardate   # 农历转换；--no-lunar 可跳过
    节气由内置天文近似公式计算（21世纪精度约±1天，个别年份需人工核对）
"""
import sys
import datetime
import calendar as pycal

# ---------- 节气 ----------
# 21世纪 C 值（通寿星公式），按年内出现顺序
TERMS_C = [
    ("小寒", 5.4055), ("大寒", 20.12),
    ("立春", 3.87), ("雨水", 18.73),
    ("惊蛰", 5.63), ("春分", 20.646),
    ("清明", 4.81), ("谷雨", 20.1),
    ("立夏", 5.52), ("小满", 21.04),
    ("芒种", 5.678), ("夏至", 21.37),
    ("小暑", 7.108), ("大暑", 22.83),
    ("立秋", 7.5), ("处暑", 23.13),
    ("白露", 7.646), ("秋分", 23.042),
    ("寒露", 8.318), ("霜降", 23.438),
    ("立冬", 7.438), ("小雪", 22.36),
    ("大雪", 7.18), ("冬至", 21.94),
]
TERM_MONTH = {  # 每个节气大致所在月份
    "小寒": 1, "大寒": 1, "立春": 2, "雨水": 2, "惊蛰": 3, "春分": 3,
    "清明": 4, "谷雨": 4, "立夏": 5, "小满": 5, "芒种": 6, "夏至": 6,
    "小暑": 7, "大暑": 7, "立秋": 8, "处暑": 8, "白露": 9, "秋分": 9,
    "寒露": 10, "霜降": 10, "立冬": 11, "小雪": 11, "大雪": 12, "冬至": 12,
}

def solar_term_day(year: int, term: str, c: float) -> int:
    """通寿星公式：Y*D+C - Y/4 （21世纪）"""
    y = year % 100
    d = int(y * 0.2422 + c) - int(y / 4)
    return d

def terms_of_year(year: int):
    out = {}
    for term, c in TERMS_C:
        d = solar_term_day(year, term, c)
        m = TERM_MONTH[term]
        out[(m, d)] = term
    return out

# ---------- 农历 ----------
CN_NUM = "一二三四五六七八九十"
LUNAR_DAY = {
    1: "初一", 2: "初二", 3: "初三", 4: "初四", 5: "初五", 6: "初六", 7: "初七",
    8: "初八", 9: "初九", 10: "初十", 11: "十一", 12: "十二", 13: "十三",
    14: "十四", 15: "十五", 16: "十六", 17: "十七", 18: "十八", 19: "十九",
    20: "二十", 21: "廿一", 22: "廿二", 23: "廿三", 24: "廿四", 25: "廿五",
    26: "廿六", 27: "廿七", 28: "廿八", 29: "廿九", 30: "三十",
}
LUNAR_MONTH = {1: "正月", 2: "二月", 3: "三月", 4: "四月", 5: "五月", 6: "六月",
               7: "七月", 8: "八月", 9: "九月", 10: "十月", 11: "冬月", 12: "腊月"}
LUNAR_FESTIVAL = {(1, 1): "春节", (1, 15): "元宵", (5, 5): "端午",
                  (7, 7): "七夕", (8, 15): "中秋", (9, 9): "重阳"}
SOLAR_FESTIVAL = {(1, 1): "元旦", (5, 1): "劳动节", (10, 1): "国庆节",
                  (10, 2): "国庆节", (10, 3): "国庆节", (3, 8): "妇女节",
                  (5, 4): "青年节", (6, 1): "儿童节", (9, 10): "教师节"}

def get_lunar(y, m, d):
    """返回 (农历小字, 是否节日)。无 lunardate 时返回 (None, False)。"""
    try:
        from lunardate import LunarDate
    except ImportError:
        return None, False
    from_solar = getattr(LunarDate, "from_solar_date", None) or LunarDate.fromSolarDate
    ld = from_solar(y, m, d)
    key = (ld.month, ld.day)
    if key in LUNAR_FESTIVAL:
        return LUNAR_FESTIVAL[key], True
    if ld.day == 1:
        is_leap = getattr(ld, "isLeapMonth", getattr(ld, "isLeap", False))
        label = LUNAR_MONTH[ld.month] + ("闰" if is_leap else "")
        return label, False
    return LUNAR_DAY[ld.day], False

# ---------- 月历生成 ----------
WEEK_CN = ["日", "一", "二", "三", "四", "五", "六"]

def month_grid(year, month, terms):
    """返回 weeks: List[List[cell|None]]，cell=(day, sub, is_red)"""
    cal = pycal.Calendar(firstweekday=6)  # 周日开头
    weeks = []
    for week in cal.monthdatescalendar(year, month):
        row = []
        for dt in week:
            if dt.month != month:
                row.append(None)
                continue
            sub, is_festival = get_lunar(dt.year, dt.month, dt.day)
            term = terms.get((dt.month, dt.day))
            # 优先级: 公历节日 > 节气 > 农历
            sf = SOLAR_FESTIVAL.get((dt.month, dt.day))
            if sf:
                sub, is_festival = sf, True
            elif term:
                sub, is_festival = term, True
            is_red = dt.weekday() in (5, 6) or is_festival
            row.append((dt.day, sub, is_red))
        weeks.append(row)
    return weeks

def render_prompt_text(year, month, weeks):
    """生图 prompt 用的 CALENDAR_TEXT：逐周一行"""
    lines = []
    for row in weeks:
        parts = []
        for cell in row:
            if cell is None:
                parts.append("□")
            else:
                d, sub, red = cell
                s = f"{d}({sub})" if sub else f"{d}"
                parts.append(s + ("红" if red else ""))
        lines.append("  ".join(parts))
    return "\n".join(lines)

def render_console(year, month, weeks):
    """控制台月历块（agent 自查）"""
    head = f"{year}年{month}月"
    lines = [head, " ".join(WEEK_CN)]
    for row in weeks:
        lines.append(" ".join(
            "--" if c is None else f"{c[0]:2d}" + (("*" if c[2] else " "))
            for c in row))
    return "\n".join(lines)

def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    year = int(sys.argv[1])
    mspec = sys.argv[2]
    no_lunar = "--no-lunar" in sys.argv

    if mspec == "all":
        months = list(range(1, 13))
    elif "-" in mspec:
        a, b = mspec.split("-")
        months = list(range(int(a), int(b) + 1))
    else:
        months = [int(mspec)]

    try:
        from lunardate import LunarDate  # noqa
        has_lunar = True
    except ImportError:
        has_lunar = False

    terms = terms_of_year(year)
    print(f"=== {year} 年日历数据 ===")
    if not has_lunar and not no_lunar:
        print("[警告] 未安装 lunardate（pip install lunardate），农历列将为空。")
        print("[警告] agent 需自行补全农历并提醒用户核对，或使用 --no-lunar 明确降级。")
    if no_lunar:
        print("[提示] --no-lunar 降级模式：仅公历+节气+固定节日。")

    for m in months:
        weeks = month_grid(year, m, terms)
        print(f"\n--- {year}-{m:02d} ---")
        print(render_console(year, m, weeks))
        print(f"\nCALENDAR_TEXT ({year}年{m}月, 嵌入prompt, 格子=数字(小字)红字标记):")
        print(render_prompt_text(year, m, weeks))
    print("\n[核对提示] 节气为天文近似计算，个别年份可能偏差1天，重要日期请人工核对。")

if __name__ == "__main__":
    main()

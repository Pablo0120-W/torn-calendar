# Torn-Calendar 📅✂️

**撕纸风插画风日历 Skill** —— 把你的照片撕成一张日历：法国插画家 Kaen 风格的高饱和撞色插画，贴在做旧纸张上，再叠一张带农历、节气、节日的撕纸日历卡片。

Turn your photos into Kaen-style, candy-colored, torn-paper collage calendars — with Chinese lunar calendar, solar terms, and holidays baked in.

![skill](https://img.shields.io/badge/skill-SKILL.md-blue) ![style](https://img.shields.io/badge/style-Kaen%20torn--paper-orange) ![calendar](https://img.shields.io/badge/calendar-%E5%86%9C%E5%8E%86%20%2B%20%E8%8A%82%E6%B0%94%20%2B%20%E8%8A%82%E6%97%A5-green) ![model](https://img.shields.io/badge/image-gpt--image--2-purple) ![license](https://img.shields.io/badge/license-MIT-lightgrey)

---

## ✨ 效果展示

2026 年 1~12 月全流程验证案例（原图 → 撕纸风插画风日历成品），左列为用户照片，右列为生成结果：

| 月份 | 原图 | 生成图 |
|---|---|---|
| 1 月 | <img src="examples/01-photo.jpg" width="280"> | <img src="examples/01-calendar.png" width="280"> |
| 2 月 | <img src="examples/02-photo.jpg" width="280"> | <img src="examples/02-calendar.png" width="280"> |
| 3 月 | <img src="examples/03-photo.jpg" width="280"> | <img src="examples/03-calendar.png" width="280"> |
| 4 月 | <img src="examples/04-photo.jpg" width="280"> | <img src="examples/04-calendar.png" width="280"> |
| 5 月 | <img src="examples/05-photo.jpg" width="280"> | <img src="examples/05-calendar.png" width="280"> |
| 6 月 | <img src="examples/06-photo.jpg" width="280"> | <img src="examples/06-calendar.png" width="280"> |
| 7 月 | <img src="examples/07-photo.jpg" width="280"> | <img src="examples/07-calendar.png" width="280"> |
| 8 月 | <img src="examples/08-photo.jpg" width="280"> | <img src="examples/08-calendar.png" width="280"> |
| 9 月 | <img src="examples/09-photo.jpg" width="280"> | <img src="examples/09-calendar.png" width="280"> |
| 10 月 | <img src="examples/10-photo.jpg" width="280"> | <img src="examples/10-calendar.png" width="280"> |
| 11 月 | <img src="examples/11-photo.jpg" width="280"> | <img src="examples/11-calendar.png" width="280"> |
| 12 月 | <img src="examples/12-photo.jpg" width="280"> | <img src="examples/12-calendar.png" width="280"> |

## 🎯 它能做什么

- 📷 **照片 → Kaen 插画**：人物/风景/城市整体转为高饱和撞色（钴蓝、樱桃红、蜂蜜黄、薄荷绿）扁平插画风，保留人物可辨识特征
- ✂️ **撕纸拼贴**：插画做成"撕下来的纸"，毛边、纤维丝、翘角、投影
- 🗓️ **真·可用日历**：公历 + 农历 + 24 节气 + 中外节日，周末红字，可圈纪念日
- 🔢 **灵活生成**：单月 / 连续多月 / 整年，任选年份
- 🤖 **多智能体可用**：标准 SKILL.md 格式，Claude Code、Codex、WorkBuddy 等均可加载

## 🚀 快速开始

### 方式一：直接对话使用（需先加载 skill，见下方安装）

加载后对智能体说：

> 帮我把这张照片做成 2026 年 3 月的撕纸风插画风日历，3 月 8 号圈出来

或整年：

> 用这张照片生成 2026 全年 12 张撕纸风日历

**零参数也行** —— 不上传照片、不指定时间，直接说：

> 给我来一张撕纸风日历

skill 会自动随机想象一个风景场景（不出现人物）并默认生成下个月的日历。

### 🎨 生图模型建议

| 推荐度 | 模型 | 说明 |
|---|---|---|
| ⭐⭐⭐ | **香蕉模型（nano-banana）** | 日历小字清晰、撕纸质感还原最好 |
| ⭐⭐⭐ | **gpt-image-2** | 同样优秀，prompt 模板即按其设计 |
| ⭐⭐ | 其他图像模型 | 可用，文字精度可能下降 |

skill 默认**只生成 1 次**；自检发现日历文字错误或画面问题才会用内置修正话术重试，不做多余生成。

### 方式二：只用日历数据（不生图）

```bash
python scripts/calendar_gen.py 2026 3      # 单月
python scripts/calendar_gen.py 2026 3-5    # 3~5月
python scripts/calendar_gen.py 2026 all    # 整年
python scripts/calendar_gen.py 2026 3 --no-lunar  # 无农历降级
```

## 📦 安装到智能体

### Claude Code

```bash
# 克隆到 skills 目录
git clone https://github.com/Pablo0120-W/torn-calendar.git
mkdir -p ~/.claude/skills && mv torn-calendar ~/.claude/skills/

# 安装农历依赖
pip install lunardate
```

### Codex

```bash
git clone https://github.com/Pablo0120-W/torn-calendar.git
```

将仓库目录作为 Codex 的工作区（或在其上下文中引用 `SKILL.md`），对话时自动生效。

### WorkBuddy

1. 下载技能包：[release/torn-calendar.zip](release/torn-calendar.zip)
2. 打开 WorkBuddy → 技能市场 → **上传技能**
3. 拖入 zip 文件，完成导入
4. 之后对话直接说"帮我把这张照片做成日历"即可调用

> 💡 农历功能需要 Python 依赖 `pip install lunardate`；未安装时 skill 会自动降级为公历 + 节气模式。

## 🔄 工作流程

```
用户照片（可选）          年份/月份（可选）
      │                      │
      ▼                      ▼
 ┌─────────┐          ┌─────────────┐
 │ 人物规则 │          │ calendar_gen │
 │ 有人→保脸 │          │ 公历+农历+节气 │
 │ 无人→不加 │          │ +节日+红字   │
 └────┬────┘          └──────┬──────┘
      │                     │
      ▼                     ▼
 ┌───────────────────────────────┐
 │  prompt-template.md 组装生图 prompt │
 │  随机排版 L1~L6 + 随机梦境元素      │
 └──────────────┬────────────────┘
                ▼
        gpt-image-2（竖版 1024×1536）
                ▼
 ┌───────────────────────────────┐
 │  逐字校验日历文字，出错则用      │
 │  内置修正话术重新生成            │
 └───────────────────────────────┘
```

## 📁 仓库结构

```
├── SKILL.md                    # skill 主文件（工作流程）
├── references/
│   ├── style-guide.md          # Kaen × 撕纸 风格规范与色板
│   ├── prompt-template.md      # gpt-image-2 生图模板 + 修正话术
│   ├── layouts.md              # 6 种排版结构（L1~L6）
│   └── calendar-spec.md        # 日历排版规范 + 月份主题表
├── scripts/
│   └── calendar_gen.py         # 日历数据（公历/农历/节气/节日）
├── examples/                   # 12 个月效果示例
└── release/
    └── torn-calendar.zip       # WorkBuddy 等智能体的技能包
```

## ⚠️ 已知限制

- 节气采用天文近似公式，个别年份可能偏差 1 天，重要日期请人工核对
- 生图模型的日历文字渲染可能出错，本 skill 已内置逐字校验与修正话术
- 风格受法国插画家 Kaen 启发，仅学习其色彩语言与画面氛围，不复制其具体作品

## 📄 License

MIT

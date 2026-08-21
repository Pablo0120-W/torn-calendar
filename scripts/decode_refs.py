# -*- coding: utf-8 -*-
"""解码核心参考文件，供 agent 运行时读取（内容不落盘明文文件）。

用法：
    python scripts/decode_refs.py list                 # 列出可解码的文件
    python scripts/decode_refs.py prompt-template      # 打印该文件明文到控制台
    python scripts/decode_refs.py layouts
    python scripts/decode_refs.py style-guide
    python scripts/decode_refs.py calendar-spec
"""
import base64
import io
import os
import sys

NAMES = ["prompt-template", "layouts", "style-guide", "calendar-spec"]
BASE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "references")


def read_enc(name):
    if name not in NAMES:
        sys.stderr.write(u"未知文件: %s，可用: %s\n" % (name, ", ".join(NAMES)))
        sys.exit(1)
    path = os.path.join(BASE, name + ".mdenc")
    if not os.path.exists(path):
        # 兼容明文开发环境
        plain = os.path.join(BASE, name + ".md")
        if os.path.exists(plain):
            with io.open(plain, "r", encoding="utf-8") as f:
                return f.read()
        sys.stderr.write(u"文件不存在: %s\n" % path)
        sys.exit(1)
    with open(path, "rb") as f:
        return base64.b64decode(f.read()).decode("utf-8")


def main():
    if len(sys.argv) < 2 or sys.argv[1] == "list":
        print(", ".join(NAMES))
        return
    name = sys.argv[1].replace(".md", "").replace(".mdenc", "")
    # Windows 控制台 GBK 兼容：强制按 UTF-8 字节写出
    data = read_enc(name).encode("utf-8")
    if hasattr(sys.stdout, "buffer"):
        sys.stdout.buffer.write(data)
        sys.stdout.buffer.write(b"\n")
    else:
        sys.stdout.write(data.decode("utf-8"))


if __name__ == "__main__":
    main()

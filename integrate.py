#!/usr/bin/env python3
"""
根据标记注释，将 tab.css 和 tab.js 的内容插入到 tab.html 中对应位置。

思路:
1. 读取整个 HTML 文件到内存
2. 读取 CSS 和 JS 文件内容
3. 用正则匹配 (start) ... (end) 之间的所有内容
4. 替换为: start标记 + <style>CSS</style> + end标记 (CSS块)
          start标记 + <script>JS</script> + end标记 (JS块)
5. 写入输出文件
"""
import re
import sys
from pathlib import Path


def main():
    # 默认路径
    src_path = Path('src/tab.html')
    css_path = Path('src/tab.css')
    js_path = Path('src/tab.js')
    out_path = Path('tab.browser.iWonder.html')

    # 检查文件存在
    for f in [src_path, css_path, js_path]:
        if not f.exists():
            print(f'error: {f} not found', file=sys.stderr)
            sys.exit(1)

    # 读取文件内容
    html = src_path.read_text(encoding='utf-8')
    css = css_path.read_text(encoding='utf-8')
    js = js_path.read_text(encoding='utf-8')

    # 正则替换 CSS 块: 匹配 (start) 到 (end) 之间的所有内容
    # 保留 start/end 标记，中间插入 <style>...</style>
    def css_replacer(m):
        return f'{m.group(1)}\n<style>\n{css}\n</style>\n{m.group(2)}'

    html = re.sub(
        r'(<!--.*?tab\.css.*?\(start\).*?-->).*?(<!--.*?tab\.css.*?\(end\).*?-->)',
        css_replacer,
        html,
        flags=re.DOTALL | re.IGNORECASE
    )

    # 正则替换 JS 块: 匹配 start 到 end 之间的所有内容
    def js_replacer(m):
        return f'{m.group(1)}\n<script>\n{js}\n</script>\n{m.group(2)}'

    html = re.sub(
        r'(<!--.*?tab\.js\s+start.*?-->).*?(<!--.*?tab\.js\s+end.*?-->)',
        js_replacer,
        html,
        flags=re.DOTALL | re.IGNORECASE
    )

    # 写入输出文件
    out_path.write_text(html, encoding='utf-8')
    print(f'Created {out_path}')


if __name__ == '__main__':
    main()

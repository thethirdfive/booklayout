import os
import math
import markdown
from bs4 import BeautifulSoup

# 设定每个section能显示的字符数量
max_chars_per_section = 410

# 读取Markdown文件
with open("contents.md", "r", encoding="utf-8") as f:
    md_content = f.read()

# 将Markdown转换为HTML
html_content = markdown.markdown(md_content)

# 使用BeautifulSoup处理HTML
soup = BeautifulSoup(html_content, "html.parser")

# 拆分section的递归函数
def split_sections(content_str, max_chars):
    sections = []

    start = 0
    while start < len(content_str):
        end = start + max_chars
        if end < len(content_str) and content_str[end:end + 4] == '</h2':
            end = content_str.rfind('<h2', start, end)
        sections.append(content_str[start:end])
        start = end

    return sections

# 将内容拆分为sections
content_str = str(soup)
sections = split_sections(content_str, max_chars_per_section)

# 生成section模板
section_template = '''
<div style="width: 50%; height: 50%; float: left; box-sizing: border-box; padding: 5px;">
    <section style="border: 1px solid black; width: 100%; height: 100%; position: relative;">
        <div style="position: absolute; bottom: 0; width: 100%; text-align: center;">
            <span>{section_number}</span>
        </div>
        <div style="padding: 10px;">
            {section_content}
        </div>
    </section>
</div>
'''

# 创建输出的HTML文件
output_html = "<!DOCTYPE html><html><head><meta charset='UTF-8'></head><body>"

# A4 paper size in pixels, assuming 96 DPI
a4_width = 794
a4_height = 1123

page_template = '''
<div style="width: {width}px; height: {height}px; position: relative; page-break-after: always;">
    {page_content}
</div>
'''

page_content = ''
for idx, section in enumerate(sections):
    page_content += section_template.format(section_number=idx+1, section_content=section)

    if (idx+1) % 4 == 0:
        output_html += page_template.format(width=a4_width, height=a4_height, page_content=page_content)
        page_content = ''

if page_content:
    output_html += page_template.format(width=a4_width, height=a4_height, page_content=page_content)

output_html += "</body></html>"

# 将生成的HTML写入文件
with open("output.html", "w", encoding="utf-8") as f:
    f.write(output_html)


import pdfkit

# ... (previous script code) ...

# 将生成的HTML写入文件
with open("output.html", "w", encoding="utf-8") as f:
    f.write(output_html)

# Convert the HTML file to a PDF
pdfkit.from_file("output.html", "output.pdf")

"""
Converts a Homebrewery-formatted markdown input to a libris-compatible one

usage: homebrewery-to-libris <input string>
"""
import sys
import markdown2

def main():
    """
    Converts a Homebrewery-formatted markdown input to a libris-compatible one.
    """
    text = sys.stdin.read()
    lines = text.split('\n')
    output = ''
    for line in lines:
        line = line.replace('\r', '')
        if line.startswith('{{'):
            line_output = parse_double_curly_brace_start(line)
        elif line.startswith('}}'):
            line_output = '</div>'
        elif line == ':':
            line_output = ''
        elif '::' in line:
            line_output = parse_stats(line)
        elif line == '\\page':
            # line_output = '<div style="page-break-after: always" markdown="1"></div>'
            line_output = ''
        else:
            line_output = line
        output += f'{line_output}\n'
    print(output)

def parse_double_curly_brace_start(line: str) -> str:
    """
    Converts double curly brace Homebrewery format to a div tag.

    Args:
        line (str): Input line to be processed.

    Returns:
        str: Modified output with double curly brace correctly interpreted
    """
    line = line[2:]
    if line.endswith('}}'):
        return ''
    if ':' in line:
        return f'<div style="{line}" markdown="1">'
    class_list = line.split(',')
    class_list.append('block')
    class_string = ' '.join(class_list)
    return f'<div class="{class_string}" markdown="1">'

def parse_stats(line: str) -> str:
    """
    Converts double colon notation in Homebrewery to <dl> tag

    Args:
        line (str): Input line to be processed.

    Returns:
        str: Modified output with double colon correctly interpreted
    """
    line = markdown2.markdown(line, extras=['fenced-code-blocks', 'markdown-in-html', 'tables'])
    line = line.replace('<p>', '')
    line = line.replace('</p>', '')
    line = f'<dl>\n<dt>\n{line}\n</dd>\n</dl>'
    line = line.replace('::', '\n</dt>\n<dd>\n')
    return line

if __name__ == '__main__':
    main()

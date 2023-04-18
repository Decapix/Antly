from django import template

register = template.Library()

@register.filter
def format_description(value):
    lines = value.split('\n')
    result = []

    inside_list = False

    for line in lines:
        stripped_line = line.strip()

        if stripped_line.startswith(('–', '-', '•')):
            if not inside_list:
                inside_list = True
                result.append('<ul>')
            result.append(f'<li>{stripped_line[1:].strip()}</li>')
        else:
            if inside_list:
                inside_list = False
                result.append('</ul>')
            if stripped_line:
                result.append(f'<p>{stripped_line}</p>')

    if inside_list:
        result.append('</ul>')

    return ''.join(result)
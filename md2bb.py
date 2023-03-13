import markdown2
import re


#build godot: E:\Godot\Godot_v4.0-stable_win64.exe --rendering-driver opengl3 --path E:\SourceCode\Ebook --export-release "Windows Desktop" "E:\SourceCode\Ebook\Ebook.exe"

# Define your Markdown input
markdown_input = "This is some **bold** text."

# Convert Markdown to HTML
html_output = markdown2.markdown(markdown_input)

# Define a regular expression pattern to match HTML tags
pattern = re.compile(r'<(.*?)>')

# Define a dictionary mapping HTML tags to BBCode markup
html_to_bbcode = {
    'strong': 'b',
    'em': 'i',
    'code': 'code',
    'a': 'url',
    'img': 'img',
    'ul': 'list',
    'ol': 'list',
    'li': '*',
    'blockquote': 'quote',
    'hr': 'hr',
    'br': 'br'
}

# Define a function to replace HTML tags with BBCode markup
def replace_tags(match):
    tag = match.group(1)
    if tag.startswith('/'):
        bbcode = f'[/{html_to_bbcode.get(tag[1:], tag[1:])}]'
    else:
        bbcode = f'[{html_to_bbcode.get(tag, tag)}]'
    return bbcode

# Convert HTML to BBCode using the replace_tags function
bbcode_output = pattern.sub(replace_tags, html_output)

# Print the output
print(bbcode_output)


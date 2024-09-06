from markdown_it import MarkdownIt

def markdown_to_html(markdown_text):
    md = MarkdownIt()
    md.renderer.rules['heading_open'] = lambda tokens, idx, options, env, self: f'<h{tokens[idx].tag}>{tokens[idx + 1].content}'
    html_content = md.render(markdown_text)
    return html_content


def markdown_to_qml(markdown_text):
    md = MarkdownIt()

    # Parse Markdown
    tokens = md.parse(markdown_text, {})
    qml_code = ""

    # Convert Markdown tokens to QML
    for i, token in enumerate(tokens):
        #print("token", token.type)
        if token.type == 'heading_open':
            level = int(token.tag[1])
            qml_code += "Text {\n\tfont.pixelSize: " + str(36 - 6 * level) + "\n\ttext: "
            
        elif token.type == "heading_close":
            qml_code += "\n}\n"
            
        elif token.type == "paragraph_open":
            qml_code += "Text {\n\tfont.pixelSize: 14\n\ttext: "
            
        elif token.type == "paragraph_close":
            qml_code += "\n}\n"
            
        # elif token.type == 'bullet_list_open':
        #     qml_code += "Item {/n"

        # elif token.type == 'list_item_open':
        #     qml_code += "/tText { text: '"
        
        # elif token.type == 'list_item_close':
        #     qml_code += "' }/n"
        
        # elif token.type == 'bullet_list_close':
        #     qml_code += "}/n"

        # elif token.type == 'strong_open':
        #     qml_code += "/tText { text: '"
        
        # elif token.type == 'strong_close':
        #     qml_code += "' font.bold: true }/n"

        # elif token.type == 'em_open':
        #     qml_code += "/tText { text: '"
        
        # elif token.type == 'em_close':
        #     qml_code += "' font.italic: true }/n"

        # elif token.type == 'link_open':
        #     link_text = tokens[i + 1].content
        #     link_url = next(attr[1] for attr in tokens[i + 1].attrs if attr[0] == 'href')
        #     qml_code += f"/tMouseArea {{ onClicked: Qt.openUrlExternally('{link_url}')/n/t/tText {{ text: '{link_text}' }}/n/t}}/n"

        elif token.type == 'inline':
            qml_code += '"' + token.content + '"'
            
        else:
            print(token.type + " not implemented")

    return qml_code


if __name__ == "__main__":
    markdown_text = "# Heading 1\n## Heading 2\nTest\n```javascript\na = 5\n```\nTest with **bold** word"

    qml_output = markdown_to_qml(markdown_text)
    print(qml_output)
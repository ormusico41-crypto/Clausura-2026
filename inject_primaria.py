import re

def inject_file(html_path):
    print(f"Injecting into {html_path}...")
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Read table content
    with open('primaria_table.html', 'r', encoding='utf-8') as f:
        table_html = f.read().strip()

    # Read cards content
    with open('primaria_cards.html', 'r', encoding='utf-8') as f:
        cards_html = f.read().strip()

    # Replace table body
    table_start_tag = '<tbody id="minutoPrimariaTableBody">'
    table_end_tag = '</tbody>'
    
    start_idx = content.find(table_start_tag)
    if start_idx == -1:
        print("Error: Could not find table start tag in", html_path)
        return False
        
    end_idx = content.find(table_end_tag, start_idx)
    if end_idx == -1:
        print("Error: Could not find table end tag in", html_path)
        return False
        
    # Replace table rows
    content = content[:start_idx + len(table_start_tag)] + "\n" + table_html + "\n                            " + content[end_idx:]

    # Replace cards container
    cards_start_tag = '<div class="minuto-cards-container" id="minutoPrimariaCardsContainer">'
    
    start_idx = content.find(cards_start_tag)
    if start_idx == -1:
        print("Error: Could not find cards start tag in", html_path)
        return False
    
    # We find the 5 closing divs from the end of the file
    body_idx = content.find("</body>")
    if body_idx == -1:
        print("Error: Could not find body end tag in", html_path)
        return False
        
    div_modal_wrapper = content.rfind("</div>", 0, body_idx)
    div_modal_overlay = content.rfind("</div>", 0, div_modal_wrapper)
    div_modal_content = content.rfind("</div>", 0, div_modal_overlay)
    div_minuto_body = content.rfind("</div>", 0, div_modal_content)
    div_cards_container = content.rfind("</div>", 0, div_minuto_body)
    
    if div_cards_container == -1:
        print("Error: Could not trace closing divs in", html_path)
        return False
        
    # Replace content inside the container
    content = content[:start_idx + len(cards_start_tag)] + "\n" + cards_html + "\n                    " + content[div_cards_container:]
    
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(content)
        
    print(f"Successfully injected into {html_path}!")
    return True

if __name__ == "__main__":
    inject_file("presentacion_consejo_clausura.html")
    inject_file("index.html")

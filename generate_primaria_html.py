import docx

doc = docx.Document("CEREMONIA DE PRIMARIA/Minuto a Minuto - Primaria Ohana.docx")
table = doc.tables[1]

rows_html = []
cards_html = []

def clean_text(t):
    return t.strip().replace("\n", " ").replace('"', '&quot;')

for r_idx in range(1, len(table.rows)):
    row = table.rows[r_idx]
    cells = [clean_text(cell.text) for cell in row.cells]
    
    # Check cells list length just in case
    if len(cells) < 3:
        continue
        
    idx = cells[0]
    
    # Check if this row is a transition or technical note (no numeric ID in column 0)
    is_trans = not idx.isdigit()
    
    if is_trans:
        idx_str = f"trans-{r_idx}"
        hora = ""
        actividad = cells[2]
        intervienen = cells[3]
        responsable = cells[4]
        utileria = cells[5] if len(cells) > 5 else ""
    else:
        idx_str = idx
        hora = cells[1]
        actividad = cells[2]
        intervienen = cells[3]
        responsable = cells[4]
        utileria = cells[5] if len(cells) > 5 else ""
        
    # Clean up redundant text in merged cells
    if intervienen == actividad:
        intervienen = ""
    if responsable == actividad or responsable == intervienen:
        responsable = ""
    if utileria == actividad:
        utileria = ""
    if hora == actividad:
        hora = ""
        
    # Categorization logic
    act_lower = actividad.lower()
    
    if "teatro" in act_lower:
        role = "actrices"
        row_cls = "row-actrices"
        card_cls = "card-actrices"
    elif any(x in act_lower for x in ["danza", "hula", "hawaiian", "kahiko", "aloha", "komo", "sway", "devil in disguise"]):
        role = "danza"
        row_cls = "row-danza"
        card_cls = "card-danza"
    elif any(x in act_lower for x in ["música", "musica", "heartbreak", "stuck", "burning", "orquesta"]):
        role = "musica"
        row_cls = "row-musica"
        card_cls = "card-musica"
    elif any(x in act_lower for x in ["video", "stop motion", "captura"]):
        role = "acto"
        row_cls = "row-acto"
        card_cls = "card-acto"
    else:
        role = "protocolo"
        row_cls = "row-protocolo"
        card_cls = "card-protocolo"
        
    # Build search terms for multi-word real-time filtering
    search_terms = f"{idx_str} {hora} {actividad} {intervienen} {responsable} {utileria} {role}".lower()
    # Normalize spaces
    search_terms = " ".join(search_terms.split())
    
    # Generate Table Row HTML
    act_content = f"<strong>{actividad}</strong>"
    if utileria:
        act_content += f'<br><span style="font-size: 0.8rem; color: #64748b; font-weight: 500;"><i class="fa-solid fa-wand-magic-sparkles" style="margin-right: 4px; color: #94a3b8;"></i>Utilería: {utileria}</span>'
        
    if is_trans:
        action_td = '<span style="font-size: 0.8rem; color: #64748b; font-weight: 600;"><i class="fa-solid fa-circle-info" style="margin-right: 4px; color: #94a3b8;"></i>Nota</span>'
        num_td = '<i class="fa-solid fa-gears" style="color: #94a3b8;" title="Transición / Nota Técnica"></i>'
    else:
        action_td = f"""<button class="btn-live-track" onclick="setLivePrimariaActividad({idx_str})"><i class="fa-solid fa-play"></i> En Vivo</button>
                                    <span class="live-badge"><i class="fa-solid fa-satellite-dish"></i> En Vivo</span>"""
        num_td = idx_str

    tr_html = f"""                            <tr class="minuto-row {row_cls}" id="primaria-row-{idx_str}" data-role="{role}" data-search="{search_terms}">
                                <td>{num_td}</td>
                                <td>{hora}</td>
                                <td>{act_content}</td>
                                <td>{intervienen}</td>
                                <td>{responsable}</td>
                                <td>
                                    {action_td}
                                </td>
                            </tr>"""
    rows_html.append(tr_html)
    
    # Generate Mobile Card HTML
    utileria_field = ""
    if utileria:
        utileria_field = f'\n                        <div class="card-field"><strong>Utilería / Obs:</strong> {utileria}</div>'
        
    if is_trans:
        time_row = f"""<div class="card-time-row">
                            <span class="card-time" style="display: none;"></span>
                            <span class="card-number" style="color: #475569; font-weight: bold;"><i class="fa-solid fa-gears"></i> Transición / Nota</span>
                        </div>"""
        fields_html = f'<h3 class="card-title" style="margin-top: 4px;">{actividad}</h3>'
        if intervienen:
            fields_html += f'\n                        <div class="card-field"><strong>Detalle:</strong> {intervienen}</div>'
        if responsable:
            fields_html += f'\n                        <div class="card-field"><strong>Responsable:</strong> {responsable}</div>'
        fields_html += utileria_field
        
        card_html = f"""                    <div class="minuto-card {card_cls}" id="primaria-card-{idx_str}" data-role="{role}" data-search="{search_terms}">
                        {time_row}
                        {fields_html}
                    </div>"""
    else:
        time_row = f"""<div class="card-time-row">
                            <span class="card-time">{hora}</span>
                            <span class="card-number">Actividad #{idx_str}</span>
                        </div>"""
        card_html = f"""                    <div class="minuto-card {card_cls}" id="primaria-card-{idx_str}" data-role="{role}" data-search="{search_terms}">
                        {time_row}
                        <h3 class="card-title">{actividad}</h3>
                        <div class="card-field"><strong>Intervienen:</strong> {intervienen}</div>
                        <div class="card-field"><strong>Responsable:</strong> {responsable}</div>{utileria_field}
                        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 8px;">
                            <button class="btn-live-track" onclick="setLivePrimariaActividad({idx_str})"><i class="fa-solid fa-play"></i> En Vivo</button>
                            <span class="live-badge"><i class="fa-solid fa-satellite-dish"></i> En Vivo</span>
                        </div>
                    </div>"""
    cards_html.append(card_html)

# Save output
with open("primaria_table.html", "w") as f:
    f.write("\n".join(rows_html))

with open("primaria_cards.html", "w") as f:
    f.write("\n".join(cards_html))

print("Success! Generated html for primaria table and cards.")

from docx import Document
import aspose.words as aw
from dotenv import load_dotenv
import os
load_dotenv()


path_file_doc = os.getenv("PATH_FILE_DOC")
pdf_file_path = os.getenv("PATH_FILE_PDF")

def convert(duree1, duree2, versement, vers_mens, cotis_total, cap_acquis, plus_value ):
    doc = Document(path_file_doc)
    # Supposons que le premier tableau est celui que tu veux parcourir
    table = doc.tables[0]  # Accède au premier tableau

    # Parcourir les lignes et les cellules du tableau
    for row in table.rows:
        for cell in row.cells:
            print(cell.text)  # Affiche le texte de chaque cellule

            # Exemple : si tu veux remplacer un texte spécifique
            if "{{duree1}}" in cell.text:
                cell.text = cell.text.replace("{{duree1}}", duree1)
            elif "{{Duree2}}" in cell.text:
                cell.text = cell.text.replace("{{duree2}}", duree2)
            elif "{{versement}}" in cell.text:
                cell.text = cell.text.replace("{{versement}}", versement)
            elif "{{cotis_total}}" in cell.text:
                cell.text = cell.text.replace("{{cotis_total}}", cotis_total)
            elif "{{cap_acquis}}" in cell.text:
                cell.text = cell.text.replace("{{cap_acquis}}", cap_acquis)
            elif "{{plus_value}}" in cell.text:
                cell.text = cell.text.replace("{{plus_value}}", plus_value)
            elif "{{vers_mens}}" in cell.text:
                cell.text = cell.text.replace("{{vers_mens}}", vers_mens)
            else:
                print("Il n' ya pas ce placeholde")
    doc_aspose = doc.save('./doc/retraite_prestige.docx')
    pdf_save = aw.Document('./doc/retraite_prestige.pdf')

    # Sauvegarder le document modifié
    return pdf_save
from docx import Document
import aspose.words as aw
from dotenv import load_dotenv
import os

load_dotenv()

path_file_doc = os.getenv("PATH_FILE_DOC")  # Chemin du fichier Word
pdf_file_path = os.getenv("PATH_FILE_PDF")  # Chemin pour sauvegarder le PDF


def convert(duree1, duree2, versement, vers_mens, cap_acquis, plus_value):
    doc = Document(path_file_doc)

    # Supposons que le premier tableau est celui que vous souhaitez modifier
    table = doc.tables[0]  # Accède au premier tableau du document

    # Parcourir les lignes et les cellules du tableau
    for row in table.rows:
        for cell in row.cells:
            # Remplacement des placeholders par les valeurs dynamiques
            if "{{duree1}}" in cell.text:
                cell.text = cell.text.replace("{{duree1}}", duree1)
            elif "{{duree2}}" in cell.text:
                cell.text = cell.text.replace("{{duree2}}", duree2)
            elif "{{versement}}" in cell.text:
                cell.text = cell.text.replace("{{versement}}", versement)
            # elif "{{cotis_total}}" in cell.text:
            #     cell.text = cell.text.replace("{{cotis_total}}", str(cotis_total))
            elif "{{cap_acquis}}" in cell.text:
                cell.text = cell.text.replace("{{cap_acquis}}", cap_acquis)
            elif "{{plus_value}}" in cell.text:
                cell.text = cell.text.replace("{{plus_value}}", plus_value)
            elif "{{vers_mens}}" in cell.text:
                cell.text = cell.text.replace("{{vers_mens}}", vers_mens)
            else:
                print(f"Pas de placeholder trouvé dans cette cellule : {cell.text}")

    # Sauvegarder le document modifié sous un nouveau nom
    output_word_file = './doc/retraite_prestige_modifie.docx'
    doc.save(output_word_file)

    # Conversion du fichier Word modifié en PDF avec aspose.words
    doc_aspose = aw.Document(output_word_file)  # Charger le document modifié avec Aspose
    doc_aspose.save(pdf_file_path)  # Sauvegarder en tant que PDF

    return pdf_file_path  # Retourner le chemin du PDF généré

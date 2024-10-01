from docx import Document
import aspose.words as aw
from dotenv import load_dotenv
import os

load_dotenv()

path_file_doc = os.getenv("PATH_FILE_DOC", './doc/RETRAITE_PRESTIGE.docx')  # Chemin du fichier Word
pdf_file_path = os.getenv("PATH_FILE_PDF", './pdf/retraite_prestige.pdf')  # Chemin pour sauvegarder le PDF


def convert(duree1, duree2, versement   , vers_mens, cotis_total, cap_acquis, plus_value):
    try:
        # Vérifier que le fichier Word existe
        if not os.path.exists(path_file_doc):
            print(f"Erreur : Le fichier Word '{path_file_doc}' est introuvable.")
            return None

        # Charger le document Word
        doc = Document(path_file_doc)

        # Parcourir les paragraphes et remplacer les placeholders par les valeurs fournies
        for paragraph in doc.paragraphs:
            if "{{duree1}}" in paragraph.text:
                paragraph.text = paragraph.text.replace("{{duree1}}", duree1)
            if "{{duree2}}" in paragraph.text:
                paragraph.text = paragraph.text.replace("{{duree2}}", duree2)
            if "{{versement1}}" in paragraph.text:
                paragraph.text = paragraph.text.replace("{{versement1}}", versement)
            if "{{verse_mens}}" in paragraph.text:
                paragraph.text = paragraph.text.replace("{{verse_mens}}", vers_mens)
            if "{{cotis_total}}" in paragraph.text:
                paragraph.text = paragraph.text.replace("{{cotis_total}}", cotis_total)
            if "{{cap_acquis}}" in paragraph.text:
                paragraph.text = paragraph.text.replace("{{cap_acquis}}", cap_acquis)
            if "{{plus_value}}" in paragraph.text:
                paragraph.text = paragraph.text.replace("{{plus_value}}", plus_value)

        # Sauvegarder le document modifié sous un nouveau nom
        output_word_file = './doc/retraite_prestige_modifie.docx'
        doc.save(output_word_file)

        # Conversion du fichier Word modifié en PDF avec aspose.words
        try:
            doc_aspose = aw.Document(output_word_file)  # Charger le document modifié avec Aspose
            doc_aspose.save(pdf_file_path)  # Sauvegarder en tant que PDF
        except Exception as e:
            print(f"Erreur lors de la conversion en PDF : {e}")
            return None

    except Exception as e:
        print(f"Erreur lors de la lecture du document : {e}")
        return None

    return pdf_file_path  # Retourner le chemin du PDF généré

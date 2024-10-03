from file_doc import convert
from calculation import calculate_results


# Fonction pour générer et envoyer un PDF
def generate_and_send_pdf(bot, chat_id, user_data):
    # Vérifier si les données utilisateur sont disponibles
    if not user_data:
        bot.send_message(chat_id, "Erreur : données utilisateur introuvables.")
        return

    # Calculer les résultats
    results = calculate_results(user_data)

    # Vérifier que les résultats ne contiennent pas d'erreur
    if 'error' in results:
        bot.send_message(chat_id, results['error'])
        return

    # Vérification des résultats de calcul
    required_keys = ['capi_acquis_one', 'plus_value_one', 'total_cotis_one',
                     'capi_acquis_two', 'plus_value_two', 'total_cotis_two']

    for key in required_keys:
        if key not in results or results[key] is None:
            bot.send_message(chat_id, f"Erreur lors du calcul des résultats : {key} est introuvable.")
            return

    # Appeler la fonction pour générer le PDF
    pdf_file = convert(
        duree1=results['duree_1'],
        duree2=results['duree_2'],
        versement=results['coti_libre'],
        vers_mens=results['cotis_mens'],

        cotis_total_one=results['total_cotis_one'],
        cap_acquis_one=results['capi_acquis_one'],
        plus_value_one=results['plus_value_one'],

        cotis_total_two=results['total_cotis_two'],
        cap_acquis_two=results['capi_acquis_two'],
        plus_value_two=results['plus_value_two'],
    )

    # Vérifier si la génération du PDF a réussi
    if pdf_file is None:
        bot.send_message(chat_id, "Erreur lors de la génération du PDF.")
        return

    # Envoyer le fichier PDF à l'utilisateur
    with open(pdf_file, 'rb') as pdf:
        bot.send_document(chat_id, pdf)

    bot.reply_to(chat_id, "Votre avis de situation en PDF a été envoyé.")







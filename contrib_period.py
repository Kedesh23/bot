from calculation import calculate_results, calcul_prestation
from utils import user_states, set_user_state, validate_and_store_contribution_period, simulator

REQUIRED_FIELDS = ['cotis_mens', 'coti_libre', 'frais_gestion', 't_it', 'duree_1', 'duree_2']
REQUIRED_FIELDS_PRESTATION = ['frais_gestion', 't_it', 'duree_1', 'duree_2', 'capi_souhaite']

def handle_contribution_period(bot, message, state, duration_key, next_state, is_final=False):
    try:
        duration = validate_and_store_contribution_period(message.chat.id, message.text)
        if duration is not None:
            user_states[message.chat.id][duration_key] = duration
            set_user_state(message.chat.id, next_state)

            if is_final:
                user_data = user_states[message.chat.id]
                if all(field in user_data for field in REQUIRED_FIELDS):
                    results = calculate_results(user_data)
                    if results:
                        bot.reply_to(message, results['results_one'])
                        bot.reply_to(message, results['results_two'])
                        bot.send_message(message.chat.id, "Souhaitez-vous recevoir l'avis de situation en version PDF ? \nRépondez par 'oui' ou 'non'.")
                        user_states[message.chat.id]['state'] = 'generateur_pdf'
                    else:
                        bot.reply_to(message, "Une erreur s'est produite lors du calcul des résultats de la cotisation.")
                elif all(field in user_data for field in REQUIRED_FIELDS_PRESTATION):
                    result = calcul_prestation(user_data)
                    if result:
                        bot.reply_to(message, result['results_one'])
                        bot.reply_to(message, result['results_two'])
                        bot.send_message(message.chat.id, "Souhaitez-vous recevoir l'avis de situation en version PDF ? \nRépondez par 'oui' ou 'non'.")
                        user_states[message.chat.id]['state'] = 'generateur_pdf'
                    else:
                        bot.reply_to(message, "Une erreur s'est produite lors du calcul des résultats de la prestation.")
                else:
                    bot.reply_to(message, "Données manquantes. Veuillez vérifier que toutes les étapes ont été complétées.")
            else:
                bot.reply_to(message, "Entrez la durée de cotisation suivante.")
        else:
            bot.reply_to(message, "Entrez une durée entre 1 et 40")
    except (TypeError, ValueError):
        bot.reply_to(message, "Veuillez entrer un nombre valide.")
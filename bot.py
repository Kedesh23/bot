import os
import telebot
from dotenv import load_dotenv
from calculation import calculate_results, calcul_prestation
from contrib_period import handle_contribution_period
from pdf_generate_pres import generate_and_send_pdf_prestige
from utils import set_user_state, user_states, frais_gestion, validate_and_store_contribution_period, \
handler_frais_gestion, handler_interet_technique, simulator
from pdf_generate import generate_and_send_pdf
load_dotenv()



# Récupérer le token depuis les variables d'environnement
token = os.getenv("TOKEN")  # Assurez-vous d'avoir défini la variable d'environnement TOKEN
path_file_pptx = os.getenv("PATH_FILE_PPTX")
pdf_file_path = os.getenv("PATH_FILE_PDF")
bot = telebot.TeleBot(token)


# Produits disponibles
product = {
    1: "Epargne",
    2: "Etudes",
    3: "Emprunteur",
    4: "Epargne Plus"
}



# Début de la messagerie
@bot.message_handler(commands=['start'])
def start_message(message):
    # Proposer les produits à l'utilisateur
    bot.reply_to(message, "Bonjour M. / Mme\nVous souhaitez faire une simulation pour quel produit ?\n" +
                 "\n".join([f"{key}- {value}" for key, value in product.items()]))
    set_user_state(message.chat.id, 'choosing_product')

# Gestionnaire pour la sélection du produit
@bot.message_handler(
    func=lambda message: user_states.get(message.chat.id, {}).get('state') == 'choosing_product' and message.text.isdigit())
def handle_product_selection(message):
    selected_product = int(message.text)

    if selected_product == 1:
        bot.reply_to(message, "Souhaitez-vous faire une simulation sur la base d'une :\n" +
                     "\n".join([f"{key}- {value}" for key, value in simulator.items()]))
        set_user_state(message.chat.id, 'choosing_simulator')
    else:
        bot.reply_to(message, "Sélection invalide. Veuillez choisir un chiffre entre 1 et 4.")



"""
    Parcours Epargne  pour la cotisation définie
"""
# Gestionnaire pour la sélection du simulateur
@bot.message_handler(
    func=lambda message: user_states.get(message.chat.id, {}).get('state') == 'choosing_simulator' and message.text.isdigit())
def handle_simulator_selection(message):
    selected_simulator = int(message.text)

    if selected_simulator == 1:
        user_states[message.chat.id]['simulator'] = 'Cotisation definie'  # Ajouter la clé pour Cotisation définie
        bot.reply_to(message, "Entrez la cotisation mensuelle.")
        set_user_state(message.chat.id, 'choosing_cotis_mensuelle')
    elif selected_simulator == 2:
        user_states[message.chat.id]['simulator'] = 'Prestation definie'  # Ajouter la clé pour Cotisation définie
        bot.reply_to(message, "Entrez le capital souhaité.")
        set_user_state(message.chat.id, "choosing_capital_souhaite")
    else:
        bot.reply_to(message, "Sélection invalide. Veuillez choisir un chiffre valide pour le simulateur.")

# Gestionnaire pour la cotisation mensuelle
@bot.message_handler(
    func=lambda message: user_states.get(message.chat.id, {}).get('state') == 'choosing_cotis_mensuelle')
def cotis_mensuelle(message):
    try:
        cotis_mens = float(message.text)
        user_states[message.chat.id]['cotis_mens'] = cotis_mens  # Stocker la cotisation mensuelle
        bot.reply_to(message, "Entrez le premier versement libre.")
        set_user_state(message.chat.id, 'choosing_versement_libre')
    except ValueError:
        bot.reply_to(message, "Veuillez entrer un nombre valide.")

# Gestionnaire de versement libre
@bot.message_handler(func=lambda message: user_states.get(message.chat.id, {}).get('state') == 'choosing_versement_libre')
def versement_libre(message):
    try:
        coti_libre = float(message.text)
        user_states[message.chat.id]['coti_libre'] = coti_libre  # Stocker le versement libre
        set_user_state(message.chat.id, 'choosing_frais_gestion')  # Changer d'état

        bot.reply_to(message, "A quel frais de gestion ?\n" +
                     "\n".join([f"{key}- {value * 100:.1f} %" for key, value in frais_gestion.items()]))
    except ValueError:
        bot.reply_to(message, "Veuillez entrer un nombre valide.")

# Gestionnaire frais de gestion
@bot.message_handler(func=lambda message: user_states.get(message.chat.id, {}).get('state') == 'choosing_frais_gestion')
def frais_gestionnaire(message):
    handler_frais_gestion(bot, message, 'choosing_interet_technique')

# Gestionnaire d'intérêts techniques
@bot.message_handler(func=lambda message: user_states.get(message.chat.id, {}).get('state') == 'choosing_interet_technique')
def interet_technique(message):
    handler_interet_technique(bot, message, 'contribution')

@bot.message_handler(func=lambda message: user_states.get(message.chat.id, {}).get('state') == 'contribution')
def contribution_period_one(message):
    handle_contribution_period(bot, message, 'contribution', 'duree_1', 'contribution_two')


@bot.message_handler(func=lambda message: user_states.get(message.chat.id, {}).get('state') == 'contribution_two')
# Après avoir calculé les résultats, demander si l'utilisateur souhaite recevoir un PDF
@bot.message_handler(func=lambda message: user_states.get(message.chat.id, {}).get('state') == 'contribution_two')
def contribution_period_two(message):
    handle_contribution_period(bot, message, 'contribution_two', 'duree_2', "generateur_pdf", is_final=True)

    # Appel à la fonction de calcul appropriée selon le simulateur choisi
    user_data = user_states.get(message.chat.id)

    if user_data['simulator'] == 'Cotisation definie':
        calculate_results(user_data)
    elif user_data['simulator'] == "Prestation definie":
        calcul_prestation(user_data)
    else:
        bot.send_message(message.chat.id,"Données manquantes. Veuillez vérifier que toutes les étapes ont été complétées.")


@bot.message_handler(func=lambda message: user_states.get(message.chat.id, {}).get('state') == 'generateur_pdf')
def pdf_generator(message):
    response = message.text.lower()

    # Vérification de la variable simulator
    simulator = user_states.get(message.chat.id, {}).get('simulator')
    print(simulator)
    if not simulator:
        bot.send_message(message.chat.id, "Erreur : simulateur non défini.")
        return

    if response in ["oui", "yes"]:
        # Récupérer les données utilisateur pour générer le PDF
        user_data = user_states.get(message.chat.id)

        if not user_data:
            bot.send_message(message.chat.id, "Erreur : données utilisateur introuvables.")
            return

        # Vérifier quel simulateur est utilisé
        if simulator == "Cotisation definie":
            generate_and_send_pdf(bot, message.chat.id, user_data)
        elif simulator == "Prestation definie":
            generate_and_send_pdf_prestige(bot, message.chat.id, user_data)
        else:
            bot.send_message(message.chat.id, "Erreur : simulateur inconnu.")
    elif response in ['non', 'no']:
        bot.send_message(message.chat.id, "NSIA vous remercie pour votre confiance.")
    else:
        bot.send_message(message.chat.id, "Veuillez répondre par 'oui' ou 'non'.")

    # Terminer la conversation (ne pas répéter pour 'non')
    if response not in ['non', 'no']:
        bot.send_message(message.chat.id, "NSIA vous remercie pour votre confiance.")



"""
    Parcours Epargne pour la prestation définie
"""

@bot.message_handler(func=lambda message: user_states.get(message.chat.id, {}).get('state') == "choosing_capital_souhaite")
def capital_souhaite(message):
    try:
        capi_souhaite = float(message.text)
        user_states[message.chat.id]['capi_souhaite'] = capi_souhaite  # Stocker le capital souhaité
        set_user_state(message.chat.id, 'choosing_frais_gestion')  # Changer d'état
        bot.reply_to(message, "A quel frais de gestion ?\n" +
                     "\n".join([f"{key}- {value * 100:.1f} %" for key, value in frais_gestion.items()]))
        set_user_state(message.chat.id, 'choosing_frais_gestion')  # Passer à l'étape suivante
    except ValueError:
        bot.reply_to(message, "Entrez un montant pour le capital souhaité.")



# Lancer le bot
bot.polling()

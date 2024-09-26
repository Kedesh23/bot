import os
from os import getenv
import telebot
from dotenv import load_dotenv
from read_db import get_data

# Charger les variables d'environnement
load_dotenv()

# Récupérer le token depuis les variables d'environnement
token = os.getenv("TOKEN")  # Assurez-vous d'avoir défini la variable d'environnement TOKEN
bot = telebot.TeleBot(token)

# Dictionnaire pour stocker l'état des utilisateurs
user_states = {}

# Produits disponibles
product = {
    1: "Epargne",
    2: "Etudes",
    3: "Emprunteur",
    4: "Epargne Plus"
}

# Simulateurs disponibles
simulator = {
    1: "Cotisation définie",
    2: "Prestation définie"
}

# Frais de gestion
frais_gestion = {
    1: 0.05,
    2: 0.045,
    3: 0.04,
    4: 0.035,
    5: 0.03,
    6: 0.025
}

# Taux d'intérêt technique
interet_tech = {
    1: 0.035,
    2: 0.04,
    3: 0.045,
    4: 0.05
}

# Début de la messagerie
@bot.message_handler(commands=['start'])
def start_message(message):
    # Proposer les produits à l'utilisateur
    bot.reply_to(message, "Bonjour M. / Mme\nVous souhaitez faire une simulation pour quel produit ?\n" +
                 "\n".join([f"{key}- {value}" for key, value in product.items()]))

    # Stocker l'étape de sélection du produit
    user_states[message.chat.id] = 'choosing_product'


# Gestionnaire pour la sélection du produit
@bot.message_handler(
    func=lambda message: user_states.get(message.chat.id) == 'choosing_product' and message.text.isdigit())
def handle_product_selection(message):
    selected_product = int(message.text)

    if selected_product == 1:
        # Passer à la sélection du simulateur
        bot.reply_to(message, "Souhaitez-vous faire une simulation sur la base d'une :\n" +
                     "\n".join([f"{key}- {value}" for key, value in simulator.items()]))
        user_states[message.chat.id] = 'choosing_simulator'
    else:
        bot.reply_to(message, "Sélection invalide. Veuillez choisir un chiffre entre 1 et 4.")


# Gestionnaire pour la sélection du simulateur
@bot.message_handler(
    func=lambda message: user_states.get(message.chat.id) == 'choosing_simulator' and message.text.isdigit())
def handle_simulator_selection(message):
    selected_simulator = int(message.text)

    if selected_simulator == 1:
        bot.reply_to(message, "Entrez la cotisation mensuelle.")
        user_states[message.chat.id] = 'choosing_cotis_mensuelle'
    else:
        bot.reply_to(message, "Sélection invalide. Veuillez choisir un chiffre valide pour le simulateur.")


# Gestionnaire pour la cotisation mensuelle
@bot.message_handler(
    func=lambda message: user_states.get(message.chat.id) == 'choosing_cotis_mensuelle')
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'choosing_cotis_mensuelle')
def cotis_mensuelle(message):
    try:
        cotis_mens = float(message.text)
        user_states[message.chat.id] = 'choosing_versement_libre'
        user_states['cotis_mens'] = cotis_mens
        bot.reply_to(message, "Entrez le premier versement libre.")
    except ValueError:
        bot.reply_to(message, "Veuillez entrer un nombre valide.")


# Gestionnaire de versement libre
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'choosing_versement_libre')
def versement_libre(message):
    try:
        coti_libre = float(message.text)
        user_states[message.chat.id] = "choosing_frais_gestion"  # Change state to choosing frais de gestion

        bot.reply_to(message, "A quel frais de gestion ?\n" +
                     "\n".join([f"{key}- {value * 100:.1f}" for key, value in frais_gestion.items()]))
    except ValueError:
        bot.reply_to(message, "Veuillez entrer un nombre valide.")


# Gestionnaire frais de gestion
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'choosing_frais_gestion')
def frais_gestionnaire(message):
    try:
        fg = int(message.text)

        if fg in frais_gestion:
            # Stocker les frais de gestion dans user_states
            user_states[message.chat.id] = 'choosing_interet_technique'
            user_states['fg'] = fg  # Enregistrez les frais de gestion ici

            bot.reply_to(message, "A quel taux d'intérêts techniques ?\n" +
                          "\n".join([f"{key}- {value * 100:.1f} %" for key, value in interet_tech.items()]))
        else:
            bot.reply_to(message, "Sélection invalide. Veuillez choisir un chiffre valide pour les frais de gestion.")
    except ValueError:
        bot.reply_to(message, "Veuillez entrer un nombre valide.")



# Gestionnaire d'intérêts techniques
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'choosing_interet_technique')
def interet_technique(message):
    try:
        t_it = int(message.text)

        if t_it in interet_tech:
            # Stocker le taux d'intérêt technique dans user_states avec l'ID de l'utilisateur
            user_states[message.chat.id] = "contribution"
            user_states[message.chat.id] = {'t_it': t_it}  # Stocker correctement t_it pour cet utilisateur
            bot.reply_to(message, "Entrez la durée de cotisation 1")
        else:
            bot.reply_to(message, "Sélection invalide. Veuillez choisir un chiffre valide pour le taux d'intérêts technique.")
    except ValueError:
        bot.reply_to(message, "Veuillez entrer un nombre valide.")



@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "contribution")
def contribution_period_one(message):
    try:
        duree_1 = int(message.text)
        if 1 <= duree_1 <= 40:
            user_states[message.chat.id] = "contribution_two"  # Changer l'état pour contribution_two
            bot.reply_to(message, "Entrez la durée de cotisation 2")
        else:
            bot.reply_to(message, "Entrez une durée entre 1 et 40")
    except ValueError:
        bot.reply_to(message, "Veuillez entrer un nombre valide.")


@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "contribution_two")
def contribution_period_two(message):
    try:
        duree_2 = int(message.text)
        if 1 <= duree_2 <= 40:
            # Récupérer les données précédemment stockées par l'utilisateur
            cotis_mens = float(user_states.get('cotis_mens', 0))
            coti_libre = float(user_states.get('coti_libre', 0))
            fg = frais_gestion.get(int(user_states.get('fg')))
            t_it = interet_tech.get(int(user_states.get('t_it')))
            duree_1 = int(user_states.get('duree_1'))

            # Calcul des cotisations et du capital pour la première période
            coti_total_1 = 12 * duree_1 * cotis_mens + coti_libre
            capi_acquis_1 = cotis_mens * (1 - fg) + coti_libre * (1 + t_it) ** duree_1 * (1 - fg)
            plus_value_1 = capi_acquis_1 - coti_total_1

            # Calcul des cotisations et du capital pour la deuxième période
            coti_total_2 = 12 * duree_2 * cotis_mens + coti_libre
            capi_acquis_2 = cotis_mens * (1 - fg) + coti_libre * (1 + t_it) ** duree_2 * (1 - fg)
            plus_value_2 = capi_acquis_2 - coti_total_2

            # Réponse avec les résultats
            bot.reply_to(message, f"Après {duree_1} année(s), vous aurez cotisé : {coti_total_1:.2f} F CFA\n"
                                  f"Capital acquis : {capi_acquis_1:.2f} F CFA\n"
                                  f"Plus-value : {plus_value_1:.2f} v\n\n"
                                  f"Après {duree_2} année(s), vous aurez cotisé : {coti_total_2:.2f} F CFA\n"
                                  f"Capital acquis : {capi_acquis_2:.2f} F CFA\n"
                                  f"Plus-value : {plus_value_2:.2f} F CFA")
        else:
            bot.reply_to(message, "Entrez une durée entre 1 et 40")
    except ValueError:
        bot.reply_to(message, "Veuillez entrer un nombre valide.")


# Démarrer le bot
bot.infinity_polling()

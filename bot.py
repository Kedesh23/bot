import os
import telebot
from dotenv import load_dotenv
from calcul import calculate_results
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

# Fonction pour définir l'état de l'utilisateur
def set_user_state(chat_id, state):
    if chat_id not in user_states:
        user_states[chat_id] = {}  # Créez un dictionnaire vide si l'utilisateur n'existe pas
    user_states[chat_id]['state'] = state

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

    if selected_product in product:
        bot.reply_to(message, "Souhaitez-vous faire une simulation sur la base d'une :\n" +
                     "\n".join([f"{key}- {value}" for key, value in simulator.items()]))
        set_user_state(message.chat.id, 'choosing_simulator')
    else:
        bot.reply_to(message, "Sélection invalide. Veuillez choisir un chiffre entre 1 et 4.")

# Gestionnaire pour la sélection du simulateur
@bot.message_handler(
    func=lambda message: user_states.get(message.chat.id, {}).get('state') == 'choosing_simulator' and message.text.isdigit())
def handle_simulator_selection(message):
    selected_simulator = int(message.text)

    if selected_simulator == 1:
        bot.reply_to(message, "Entrez la cotisation mensuelle.")
        set_user_state(message.chat.id, 'choosing_cotis_mensuelle')
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
    try:
        fg = int(message.text)

        if fg in frais_gestion:
            user_states[message.chat.id]['frais_gestion'] = frais_gestion[fg]  # Stocker les frais de gestion
            set_user_state(message.chat.id, 'choosing_interet_technique')  # Changer l'état
            bot.reply_to(message, "A quel taux d'intérêts techniques ?\n" +
                          "\n".join([f"{key}- {value * 100:.1f} %" for key, value in interet_tech.items()]))
        else:
            bot.reply_to(message, "Sélection invalide. Veuillez choisir un chiffre valide pour les frais de gestion.")
    except ValueError:
        bot.reply_to(message, "Veuillez entrer un nombre valide.")

# Gestionnaire d'intérêts techniques
@bot.message_handler(func=lambda message: user_states.get(message.chat.id, {}).get('state') == 'choosing_interet_technique')
def interet_technique(message):
    try:
        t_it = int(message.text)
        if t_it in interet_tech:
            user_states[message.chat.id]['t_it'] = interet_tech[t_it]  # Stocker le taux d'intérêt technique
            set_user_state(message.chat.id, 'contribution')  # Changer l'état
            bot.reply_to(message, "Entrez la durée de cotisation 1")
        else:
            bot.reply_to(message, "Sélection invalide. Veuillez choisir un chiffre valide pour le taux d'intérêts technique.")
    except ValueError:
        bot.reply_to(message, "Veuillez entrer un nombre valide.")

@bot.message_handler(func=lambda message: user_states.get(message.chat.id, {}).get('state') == 'contribution')
def contribution_period_one(message):
    try:
        duree_1 = int(message.text)
        if 1 <= duree_1 <= 40:
            user_states[message.chat.id]['duree_1'] = duree_1  # Stocker la première durée
            set_user_state(message.chat.id, 'contribution_two')  # Changer d'état
            bot.reply_to(message, "Entrez la durée de cotisation 2")
        else:
            bot.reply_to(message, "Entrez une durée entre 1 et 40")
    except ValueError:
        bot.reply_to(message, "Veuillez entrer un nombre valide.")


@bot.message_handler(func=lambda message: user_states.get(message.chat.id, {}).get('state') == 'contribution_two')
def contribution_period_two(message):
    try:
        duree_2 = int(message.text)
        if 1 <= duree_2 <= 40:
            user_states[message.chat.id]['duree_2'] = duree_2  # Stocker la deuxième durée

            # Vérification des données utilisateur avant d'appeler calculate_results
            user_data = user_states[message.chat.id]
            required_fields = ['cotis_mens', 'coti_libre', 'frais_gestion', 't_it', 'duree_1', 'duree_2']
            if all(field in user_data for field in required_fields):
                results = calculate_results(user_data)

                # Vérifiez que results n'est pas None
                if results:
                    bot.reply_to(message, results['results_one'])
                    bot.reply_to(message, results['results_two'])
                else:
                    bot.reply_to(message, "Une erreur s'est produite lors du calcul des résultats.")
            else:
                bot.reply_to(message, "Données manquantes. Veuillez vérifier que toutes les étapes ont été complétées.")
        else:
            bot.reply_to(message, "Entrez une durée entre 1 et 40")
    except ValueError:
        bot.reply_to(message, "Veuillez entrer un nombre valide.")



# Lancer le bot
bot.polling()

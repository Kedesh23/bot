# Frais de gestion
from pyexpat.errors import messages

frais_gestion = {
    1: 0.05,
    2: 0.045,
    3: 0.04,
    4: 0.035,
    5: 0.03,
    6: 0.025
}


# Simulateurs disponibles
simulator = {
    1: "Cotisation définie",
    2: "Prestation définie"
}

# Taux d'intérêt technique
interet_tech = {
    1: 0.035,
    2: 0.04,
    3: 0.045,
    4: 0.05
}

# Dictionnaire pour stocker l'état des utilisateurs
user_states = {}

# separateur de millier
def format_separator(value):
    return "{:,.2f}".format(value).replace(',', " ")


def get_frais_gestion(key):
    return frais_gestion.get(key, None)

def get_interet_tech(key):
    return interet_tech.get(key, None)


# Fonction pour définir l'état de l'utilisateur
def set_user_state(chat_id, state):
    if chat_id not in user_states:
        user_states[chat_id] = {}  # Créez un dictionnaire vide si l'utilisateur n'existe pas
    user_states[chat_id]['state'] = state
    return user_states[chat_id]['state']


# Fonction pour valider et enregistrer une période de contribution
def validate_and_store_contribution_period(chat_id, period, min_value=1, max_value=40):
    try:
        period_value = int(period)
        if min_value <= period_value <= max_value:
            return period_value
        else:
            return None
    except ValueError:
        return None

# Fonction de frais de gestion

def handler_frais_gestion(bot, message, next_state):
    try:
        fg = int(message.text)
        frais = get_frais_gestion(fg)
        if fg is not frais:
            user_states[message.chat.id]['frais_gestion'] = frais  # Stocker les frais de gestion
            set_user_state(message.chat.id, next_state)  # Changer l'état
            bot.reply_to(message, "A quel taux d'intérêts techniques ?\n" +
                          "\n".join([f"{key}- {value * 100:.1f} %" for key, value in interet_tech.items()]))
        else:
            bot.reply_to(message, "Sélection invalide. Veuillez choisir un chiffre valide pour les frais de gestion.")
    except ValueError:
        bot.reply_to(message, "Veuillez entrer un nombre valide.")


def handler_interet_technique(bot, message, next_state):
    try:
        t_it = int(message.text)
        interet = get_interet_tech(t_it)
        if t_it is not interet:
            user_states[message.chat.id]['t_it'] = interet  # Stocker le taux d'intérêt technique
            set_user_state(message.chat.id, next_state)  # Changer l'état
            bot.reply_to(message, "Entrez la durée de cotisation 1")
        else:
            bot.reply_to(message,
                         "Sélection invalide. Veuillez choisir un chiffre valide pour le taux d'intérêts technique.")
    except ValueError:
        bot.reply_to(message, "Veuillez entrer un nombre valide.")



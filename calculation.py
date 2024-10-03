from read_db import get_data
from utils import format_separator

def calculate_results(user_data):
    try:
        cotis_mens = user_data['cotis_mens']
        coti_libre = user_data['coti_libre']
        fg = user_data['frais_gestion']
        t_it = user_data['t_it']
        duree_1 = user_data['duree_1']
        duree_2 = user_data['duree_2']

        col_duree_1 = "var" + str(duree_1)
        col_duree_2 = "var" + str(duree_2)

        # print(col_duree_1)
        # print(col_duree_2)
        # print(t_it)

        # Récupération des taux depuis la base de données
        table_taux_one = get_data(t_it, col_duree_1)
        table_taux_two = get_data(t_it, col_duree_2)
        print(table_taux_one)

        # Vérifiez que les données sont valides avant les calculs
        if table_taux_one is None or table_taux_two is None:
            error_message = "Erreur : Impossible de récupérer les données du taux pour les colonnes sélectionnées."
            print(error_message)
            return {"results_one": error_message, "results_two": error_message}  # Message d'erreur retourné

        # Calcul des cotisations totales 1
        total_cotis_one = 12 * duree_1 * cotis_mens + coti_libre
        total_cotis_one = round(total_cotis_one, 1)

        # Calcul du capital acquis 1
        capi_acquis_one = table_taux_one * cotis_mens * (1 - fg) + coti_libre * (1 + t_it) ** duree_1 * (1 - fg)
        capi_acquis_one = round(capi_acquis_one, 1)

        # Calcul de la plus value 1
        plus_value_one = capi_acquis_one - total_cotis_one
        plus_value_one = round(plus_value_one, 1)

        # Calcul des cotisations totales 2
        total_cotis_two = 12 * duree_2 * cotis_mens + coti_libre
        total_cotis_two = round(total_cotis_two, 1)

        # Calcul du capital acquis 2
        capi_acquis_two = table_taux_two * cotis_mens * (1 - fg) + coti_libre * (1 + t_it) ** duree_2 * (1 - fg)
        capi_acquis_two = round(capi_acquis_two, 1)

        # Calcul de la plus value 2
        plus_value_two = capi_acquis_two - total_cotis_two
        plus_value_two = round(plus_value_two, 1)

        # Formatage des résultats
        results_one = (
            f"Après {duree_1} années de cotisation, le client aura :\n\n"
            f"Cotisé : {format_separator(total_cotis_one)} F CFA\n"
            f"Acquis au capital de : {format_separator(capi_acquis_one)} F CFA\n"
            f"Réalisé une plus-value de : {format_separator(plus_value_one)} F CFA\n"
        )

        results_two = (
            f"Après {duree_2} années de cotisation, le client aura :\n\n"
            f"Cotisé : {format_separator(total_cotis_two)} F CFA\n"
            f"Acquis au capital de : {format_separator(capi_acquis_two)} F CFA\n"
            f"Réalisé une plus-value de : {format_separator(plus_value_two)} F CFA\n"
        )

        return {
            "results_one": results_one,
            "results_two": results_two,

            "duree_1": duree_1,
            "duree_2": duree_2,
            "coti_libre": coti_libre,
            "cotis_mens": cotis_mens,

            "total_cotis_one": total_cotis_one,
            "capi_acquis_one": capi_acquis_one,
            "plus_value_one": plus_value_one,

            "total_cotis_two": total_cotis_two,
            "capi_acquis_two": capi_acquis_two,
            "plus_value_two": plus_value_two,

        }

    except Exception as e:
        error_message = f"Erreur lors du calcul : {e}"
        print(error_message)
        return {"results_one": error_message, "results_two": error_message}


def calcul_prestation(user_data):
    try:
        # Vérification des clés dans user_data
        required_keys = ['frais_gestion', 't_it', 'duree_1', 'duree_2', 'capi_souhaite']
        for key in required_keys:
            if key not in user_data:
                raise ValueError(f"Clé manquante dans user_data : {key}")

        # Récupérer ou initialiser coti_libre à 0 si non fourni par l'utilisateur
        coti_libre = user_data.get('coti_libre', 0)
        fg = user_data['frais_gestion']
        t_it = user_data['t_it']
        duree_1 = user_data['duree_1']
        duree_2 = user_data['duree_2']
        capi_souhaite = user_data['capi_souhaite']

        col_duree_1 = "var" + str(duree_1)
        col_duree_2 = "var" + str(duree_2)

        # Récupération des taux depuis la base de données
        table_taux_one = get_data(t_it, col_duree_1)
        table_taux_two = get_data(t_it, col_duree_2)

        if table_taux_one is None or table_taux_two is None:
            raise ValueError("Impossible de récupérer les taux de la base de données")

        # Calcul de la cotisation mensuelle si non fournie par l'utilisateur
        cotis_mens = user_data.get('cotis_mens')
        if cotis_mens is None:
            cotis_mens = capi_souhaite / (table_taux_one * (1 - fg))  # Calcul basé sur le capital souhaité et les taux

        # Calcul des cotisations totales 1
        total_cotis_one = 12 * duree_1 * cotis_mens
        total_cotis_one = round(total_cotis_one, 1)

        # Calcul du capital acquis 1
        capi_acquis_one = 0.0
        capi_acquis_one = round(capi_acquis_one, 1)

        # Calcul de la plus-value 1
        plus_value_one = capi_souhaite - total_cotis_one
        plus_value_one = round(plus_value_one, 1)

        # Calcul de la cotisation mensuelle pour la deuxième durée
        coti_mens_two = capi_souhaite / (table_taux_two * (1 - fg))

        # Calcul des cotisations totales 2
        total_cotis_two = 12 * duree_2 * coti_mens_two
        total_cotis_two = round(total_cotis_two, 1)

        # Calcul du capital acquis 2
        capi_acquis_two = 0.0
        capi_acquis_two = round(capi_acquis_two, 1)

        # Calcul de la plus-value 2
        plus_value_two = capi_souhaite - total_cotis_two
        plus_value_two = round(plus_value_two, 1)

        results_one = (
            f"Afin d'obtenir {format_separator(capi_souhaite)} après {duree_1} année(s) de cotisation :\n\n"
            f"Votre cotisation mensuelle sera de : {format_separator(cotis_mens)} F CFA\n"
            f"Cotisation totale : {format_separator(total_cotis_one)} F CFA\n"
            f"Réalisé une plus-value de : {format_separator(plus_value_one)} F CFA\n"
        )

        results_two = (
            f"Afin d'obtenir {format_separator(capi_souhaite)} après {duree_2} année(s) de cotisation :\n\n"
            f"Votre cotisation mensuelle sera de : {format_separator(coti_mens_two)} F CFA\n"
            f"Cotisation totale : {format_separator(total_cotis_two)} F CFA\n"
            f"Réalisé une plus-value de : {format_separator(plus_value_two)} F CFA\n"
        )

        return {"results_one": results_one, "results_two": results_two}

    except Exception as e:
        error_message = f"Erreur lors du calcul : {e}"
        print(error_message)
        return {"results_one": error_message, "results_two": error_message}

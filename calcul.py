from read_db import get_data

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

        print(col_duree_1)
        print(col_duree_2)
        print(t_it)

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
        total_cotis_one_sep = f"{total_cotis_one:,.3}".replace(',', " ")

        # Calcul du capital acquis 1
        capi_acquis_one = table_taux_one * cotis_mens * (1 - fg) + coti_libre * (1 + t_it) ** duree_1 * (1 - fg)
        capi_acquis_one_sep = f"{capi_acquis_one:,.3}".replace(",", " ")

        # Calcul de la plus value 1
        plus_value_one = capi_acquis_one - total_cotis_one
        plus_value_one_sep = f"{plus_value_one:,.3}".replace(',', " ")

        # Calcul des cotisations totales 2
        total_cotis_two = 12 * duree_2 * cotis_mens + coti_libre
        total_cotis_two_sep = f"{total_cotis_two:,.3}".replace(',', " ")

        # Calcul du capital acquis 2
        capi_acquis_two = table_taux_two * cotis_mens * (1 - fg) + coti_libre * (1 + t_it) ** duree_2 * (1 - fg)
        capi_acquis_two_sep = f"{capi_acquis_two:,.3}".replace(",", " ")

        # Calcul de la plus value 2
        plus_value_two = capi_acquis_two - total_cotis_two
        plus_value_two_sep = f"{plus_value_two:,.3}".replace(',', " ")

        # Formatage des résultats
        results_one = (
            f"Après {duree_1} années de cotisation, le client aura :\n\n"
            f"Cotisé : {total_cotis_one_sep} F CFA\n"
            f"Acquis au capital de : {capi_acquis_one_sep} F CFA\n"
            f"Réalisé une plus-value de : {plus_value_one_sep} F CFA\n"
        )

        results_two = (
            f"Après {duree_2} années de cotisation, le client aura :\n\n"
            f"Cotisé : {total_cotis_two_sep} F CFA\n"
            f"Acquis au capital de : {capi_acquis_two_sep} F CFA\n"
            f"Réalisé une plus-value de : {plus_value_two_sep} F CFA\n"
        )

        return {
            "results_one": results_one,
            "results_two": results_two,

            "duree_1": duree_1,
            "duree_2": duree_2,
            "total_cotis": total_cotis_one,
            "capi_acquis": capi_acquis_one,
            "total_cotis": total_cotis_one,
            "capi_acquis": capi_acquis_one,
            "plus_value": plus_value_one,
        }

    except Exception as e:
        error_message = f"Erreur lors du calcul : {e}"
        print(error_message)
        return {"results_one": error_message, "results_two": error_message}

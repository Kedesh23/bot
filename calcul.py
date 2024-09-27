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

        # Récupération des taux depuis la base de données
        table_taux_one = get_data(t_it, col_duree_1)
        table_taux_two = get_data(t_it, col_duree_2)

        # Vérifiez que les données sont valides avant les calculs
        if table_taux_one is None or table_taux_two is None:
            error_message = "Erreur : Impossible de récupérer les données du taux pour les colonnes sélectionnées."
            print(error_message)
            return {"results_one": error_message, "results_two": error_message}  # Message d'erreur retourné

        # Effectuer les calculs
        total_cotis_one = 12 * duree_1 * cotis_mens + coti_libre
        capi_acquis_one = table_taux_one * cotis_mens * (1 - fg) + coti_libre * (1 + t_it) ** duree_1 * (1 - fg)
        plus_value_one = capi_acquis_one - total_cotis_one

        total_cotis_two = 12 * duree_2 * cotis_mens + coti_libre
        capi_acquis_two = table_taux_two * cotis_mens * (1 - fg) + coti_libre * (1 + t_it) ** duree_2 * (1 - fg)
        plus_value_two = capi_acquis_two - total_cotis_two

        # Formatage des résultats
        results_one = (
            f"Après {duree_1} années de cotisation, le client aura :\n\n"
            f"Cotisé : {total_cotis_one:.2f} F CFA\n"
            f"Acquis au capital de : {capi_acquis_one:.2f} F CFA\n"
            f"Réalisé une plus-value de : {plus_value_one:.2f} F CFA\n"
        )

        results_two = (
            f"Après {duree_2} années de cotisation, le client aura :\n\n"
            f"Cotisé : {total_cotis_two:.2f} F CFA\n"
            f"Acquis au capital de : {capi_acquis_two:.2f} F CFA\n"
            f"Réalisé une plus-value de : {plus_value_two:.2f} F CFA\n"
        )

        return {
            "results_one": results_one,
            "results_two": results_two
        }

    except Exception as e:
        error_message = f"Erreur lors du calcul : {e}"
        print(error_message)
        return {"results_one": error_message, "results_two": error_message}

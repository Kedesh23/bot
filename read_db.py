import sqlite3

def get_data(taux_it, column_id):
    # Connexion à la base de données SQLite
    conn = sqlite3.connect('BOT.db')
    cursor = conn.cursor()

    # Exemple de requête SQL basée sur les entrées utilisateur
    query = f"SELECT {column_id} FROM value WHERE taux_it = ?"
    cursor.execute(query, (taux_it,))  # taux_it est passé comme paramètre ici

    # Récupérer les résultats
    result = cursor.fetchone()

    conn.close()

    # Assurez-vous que vous renvoyez une valeur par défaut si aucun résultat n'est trouvé
    return result[0] if result else None  # Renvoie None si aucun résultat trouvé






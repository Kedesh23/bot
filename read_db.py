import sqlite3

def get_data(taux_id, column_id):
    # Connexion à la base de données SQLite
    conn = sqlite3.connect('BOT.db')
    cursor = conn.cursor()

    # Exemple de requête SQL basée sur les entrées utilisateur
    query = f"SELECT {column_id} FROM value WHERE tauX_it = ?"
    cursor.execute(query, (taux_id,))

    # Récupérer les résultats
    result = cursor.fetchone()

    conn.close()
    return result

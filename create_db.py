import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError


# Fonction pour charger le fichier Excel dans la base de données SQLite
def insert_excel_to_sqlite(file_path, db_path, table_name):
    try:
        # Lire le fichier Excel
        df = pd.read_excel(file_path)
        print("Fichier Excel chargé avec succès.")

        # Créer ou se connecter à la base de données SQLite
        engine = create_engine(f'sqlite:///{db_path}')

        # Essayer d'insérer les données dans la base de données
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)
        print("Données insérées avec succès dans la base de données.")

    except FileNotFoundError:
        print(f"Erreur : Le fichier Excel '{file_path}' n'a pas été trouvé.")

    except SQLAlchemyError as e:
        print(f"Erreur de connexion à la base de données SQLite : {e}")

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")


# Chemin vers le fichier Excel et la base de données
file_path = './doc/BOT.xlsx'
db_path = './BOT.db'
table_name = 'value'

# Appel de la fonction pour insérer le fichier Excel dans la base de données SQLite
insert_excel_to_sqlite(file_path, db_path, table_name)

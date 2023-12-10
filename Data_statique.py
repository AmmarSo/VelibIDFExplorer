import pandas as pd
import json
import mysql.connector

# Charger les données JSON depuis le fichier
with open('velib-emplacement-des-stations.json', 'r') as file:
    data = json.load(file)

# Transformer les données en DataFrame
df = pd.DataFrame(data)

# Extraire les coordonnées géographiques en latitude et longitude
df['latitude'] = df['coordonnees_geo'].apply(lambda x: x['lat'])
df['longitude'] = df['coordonnees_geo'].apply(lambda x: x['lon'])

# Connexion à la base de données MySQL
conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='velibs'
)

# Créer la table station_information si elle n'existe pas déjà
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS station_information (
        stationcode VARCHAR(255),
        name VARCHAR(255),
        capacity INT,
        latitude FLOAT,
        longitude FLOAT
    )
''')

# Insérer les données dans la table station_information
for _, row in df.iterrows():
    query = '''
        INSERT INTO station_information (stationcode, name, capacity, latitude, longitude)
        VALUES (%s, %s, %s, %s, %s)
    '''
    values = (row['stationcode'], row['name'], row['capacity'], row['latitude'], row['longitude'])
    cursor.execute(query, values)

# Valider les changements et fermer la connexion à la base de données
conn.commit()


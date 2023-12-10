import mysql.connector as sql
import json
import requests
import time

def insérer_velib_data():
    url = "https://opendata.paris.fr/api/records/1.0/search/"

    payload = {
        'dataset' : 'velib-disponibilite-en-temps-reel',
        'rows': 10000,
        'sort': '-duedate',
        'facet': 'is_installed',
        'facet': 'is_renting',
        'facet': 'is_returning',
        'facet': 'nom_arrondissement_communes'
    }

    mydb = sql.connect(user="root", database='velibs')
    mycursor = mydb.cursor()

    while True:
        temps_reel = requests.get(url, params=payload)
        data = json.loads(temps_reel.text)

        for record in data['records']:
            fields = record['fields']
            stationcode = fields['stationcode']
            is_installed = 1 if fields['is_installed'] == 'OUI' else 0
            numdocksavailable = fields['numdocksavailable']
            numbikesavailable = fields['numbikesavailable']
            mechanical = fields['mechanical']
            ebike = fields['ebike']
            nom_arrondissement_communes = fields['nom_arrondissement_communes']

            insertion = "INSERT INTO station_status (stationcode, is_installed, numdocksavailable, numbikesavailable, mechanical, ebike, nom_arrondissement_communes, date) VALUES (%s, %s, %s, %s, %s, %s, %s, NOW()) ON DUPLICATE KEY UPDATE numdocksavailable=%s, numbikesavailable=%s"

            values = (stationcode, is_installed, numdocksavailable, numbikesavailable, mechanical, ebike, nom_arrondissement_communes, numdocksavailable, numbikesavailable)

            mycursor.execute(insertion, values)
            mydb.commit()

        # attendre 15 minutes pour réactualisation
        time.sleep(900)

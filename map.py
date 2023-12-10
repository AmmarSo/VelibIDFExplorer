import folium
from folium.plugins import MarkerCluster
import mysql.connector

def create_map():
    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='velibs'
    )

    # Retrieve station information from the database
    cursor = conn.cursor()
    query = '''
        SELECT name, latitude, longitude, numbikesavailable, numdocksavailable, ebike, mechanical
        FROM station_information
        INNER JOIN station_status ON station_information.stationcode = station_status.stationcode
    '''
    cursor.execute(query)
    stations = cursor.fetchall()

    # Create a folium map centered on Paris
    map_center = [48.8566, 2.3522]
    m = folium.Map(location=map_center, zoom_start=13)

    # Create a marker cluster
    marker_cluster = MarkerCluster().add_to(m)

    # Add markers for each station with pop-up information
    for station in stations:
        name, latitude, longitude, bikes_available, docks_available, ebikes, mechanicals = station

        # Format the content for the pop-up
        popup_content = f'''
            <b>{name}</b><br>
            Velo Electrique : {ebikes}<br>
            Velo Mecanique : {mechanicals}<br>
            Station : {docks_available}<br>
            Vélo disponible : {bikes_available}
        '''

        # Create a marker with the pop-up
        marker = folium.Marker(location=[latitude, longitude], popup=popup_content)

        # Add the marker to the cluster
        marker_cluster.add_child(marker)

    # Save the map as an HTML file
    m.save('static/bike_stations_map.html')

    # Close the database connection
    conn.close()

if __name__ == '__main__':
    create_map()

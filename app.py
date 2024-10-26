from flask import Flask, render_template, request
import folium
import json
from folium.plugins import Draw

# Import your algorithms
from Algorithms.Astar import astar
from Algorithms.BFS import bfs
from Algorithms.DFS import dfs
from Algorithms.GBFS import gbfs

app = Flask(__name__)

with open('/mnt/d/TUX/Math for AI/My_Flask_app/Data/cleaned3.json', 'r')as file:
    districts = json.load(file)

@app.route('/')
def index():
    m = folium.Map(location=[11.562675419726654, 104.8712042062723], zoom_start=7, control_scale=True)
    # folium.LayerControl().add_to(m)
    Draw().add_to(m)
    map_html = m._repr_html_()
    return render_template('index.html', map_html = map_html, content = districts, Distance = None, Duration = None)

@app.route('/search', methods=['POST'])
def search():
    origin = request.form['origin']
    destination = request.form['destination']
    algorithm = request.form['algorithm']
    formatted_distance = 0
    formatted_duration = [0, 0] 
    try:
        # Choose the algorithm based on user selection
        if algorithm == 'A*':
            path, distance, duration = astar(origin, destination, districts)
        elif algorithm == 'BFS':
            path, distance, duration = bfs(origin, destination,districts)
        elif algorithm == 'DFS':
            path, distance, duration = dfs(origin, destination,districts)
        elif algorithm == 'GBFS':
            path, distance, duration = gbfs(origin, destination,districts)
        else:
            path = []
    except ValueError as e:
        print(f'Unexpected problem occured: {e}')
        pass
        
# Create a map with the calculated path
        
    m = folium.Map(location=[11.562675419726654, 104.8712042062723], zoom_start=7, control_scale=True)
    # folium.LayerControl().add_to(m) 
    Draw().add_to(m)
    try:
        coordinations = []
        if path:
            print(path)
            for point in path: 
                for i in districts[point]:
                    if isinstance(i, dict): 
                        locations = list(i.values())[0]
                        coords = list(locations.values())[0]
                        lat = coords.get('lat')
                        lng = coords.get('lng')
                        coordinations.append([lat, lng])
                        folium.Marker(location=(lat, lng), tooltip=(point,lat,lng)).add_to(m)
                        break
        else:
            for i in districts[destination]:
                if isinstance(i, dict): 
                    locations = list(i.values())[0]
                    coords = list(locations.values())[0]
                    lat = coords.get('lat')
                    lng = coords.get('lng')
                    coordinations.append([lat, lng])
                    folium.Marker(location=(lat, lng), tooltip=(destination,lat,lng)).add_to(m)
                    break
        folium.PolyLine(
            locations=coordinations,
            color="blue",
            weight=2.5
        ).add_to(m)   
    except ValueError:
        pass
    map_html = m._repr_html_()

    formatted_distance = f"{float(distance):.2f}" if distance is not None else "0.00"
    formatted_duration = (
        (duration[0] if duration[0] is not None else 0),
        (duration[1] if duration[1] is not None else 0)
    ) if duration is not None else (0, 0)
    return render_template('index.html', map_html=map_html, content = districts, Distance = formatted_distance, Duration= formatted_duration, 
                        selected_algorithm= algorithm, selected_origin = origin, selected_destination=destination, Path = path)
if __name__ == '__main__':
    app.run(debug=True)

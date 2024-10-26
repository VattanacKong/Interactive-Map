import json
import re
from .Heuristic import get_lat_lng, straight_dis

def get_graph(districts, destination):
    temp = {}
    #get origin coord to calculate straight line
    destination_coords = get_lat_lng(destination, districts)
    #base district 
    for main_key, value in districts.items():
        neighbors = []
        dicts_only= [item for item in value if isinstance(item, dict)]
        #dictionary that store coords of the main key
        for key,value in dicts_only[0].items():
            coords = value['location']
        #neighbors dictionaries
        for i in dicts_only[1:]:
            #neighbor districts that were saved as dictionaries
            for key, value in i.items():
                #convert distance and duration from string to float
                dista = float(re.findall('\d*\.*\d+', value['distance'])[0])
                hour = re.findall(r'(\d+)\s*hour[s]?', value['duration'])
                mins = re.findall(r'(\d+)\s*min[s]?', value['duration'])
                hour = int(hour[0] if hour else 0)
                mins = int(mins[0] if mins else 0)
                dura = [hour , mins ]
                #get coords of the current neighbor
                current =[items for items in districts[key] if isinstance(items, dict)]
                for a, b in current[0].items():
                    nei_coords = b['location']
                distance = straight_dis(list(destination_coords.values()), list(nei_coords.values()))
                #add all data as content and add to temp
                content = [key, dista, dura, distance]
                neighbors.append(content)
        temp[main_key] = neighbors + list(coords.values())
    return temp

def gbfs(origin, destination, districts):
    if origin == destination:
        return None, None, None
    distances = 0
    duration =[0,0]
    open = [origin]
    close = []
    graph = get_graph(districts,destination)
    while open:
        node = open.pop(0)
        if node not in close:
            close.append(node)
            neighbors = graph[node][:-2]
            neighbors.sort(key = lambda x: x[-1])
            next_open, distance, dura, straight_Line = neighbors.pop(0)
            open.append(next_open)
            #calculate time and distance
            distances += distance
            duration[0] += dura[0]
            duration[1] += dura[1]
            if open[0] == destination:
                close.append(destination)
                if duration[1] >= 60:
                    duration[0] += int(duration[1]/60)
                    duration[1] = duration[1] % 60   
                return close ,distances, duration
            
# with open('/mnt/d/TUX/Math for AI/mapproject/Data/temp.json', 'w')as file:
#     json.dump(get_graph(districts, 'Mongkol Borei'), file, indent=4)      
        
        
# gbfs('Tuol Kouk', 'Mongkol Borei')

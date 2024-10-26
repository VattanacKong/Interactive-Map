import json
from .GBFS import get_graph
import copy

def get_path(destination, origin, store,path = None):   
    if path is None:
        path =[]
    if origin == destination:
        return None
    for i in store:
        if i[0] == destination:
            path.append(i)
            break
    if path[-1][1] == origin:
        return path
    else:
        new_destination = path[-1][1]
        return get_path(new_destination, origin, store, path)
            

def bfs(origin, destination, district):
    distance = 0
    duration = [0,0]           
    graph = get_graph(district, destination)
    real_path = [destination]
    close = []
    store =[]
    open = [origin]
    
    while open:
        node = open.pop(0)
        if node not in close:
            close.append(node)        
        for neighbor in graph[node][:-2]:
            if (neighbor[0] not in open) and (neighbor[0] not in close):
                open.append(neighbor[0])            
                store.append([neighbor[0], node])    
        if node == destination:
            path = get_path(destination, origin, store)
            if path:
                for i in path:
                    real_path.insert(0, i[1])
                    for neig in graph[i[1]]:
                        if neig[0] == i[0]:
                            distance += neig[1]
                            duration[0] += neig[2][0]
                            duration[1] += neig[2][1]
                            break
            else:
                return None, None, None
            for neig in graph[destination]:
                if isinstance(neig, list) and neig[0] == real_path[-2]:
                    distance += neig[1]
                    duration[0] += neig[2][0]
                    duration[1] += neig[2][1]
                    break
            duration[0] += int(duration[1]/ 60)
            duration[1] = duration[1] % 60
            return real_path , distance, duration
# with open('/mnt/d/TUX/Math for AI/My_Flask_app/Data/cleaned3.json', 'r')as file:
#     districts = json.load(file)

# print(bfs('Tuol Kouk', 'Mongkol Borei', districts))
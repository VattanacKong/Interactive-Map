import json
from .Heuristic import straight_dis
from .GBFS import get_graph
from queue import PriorityQueue


    
def astar(origin, destination, districts):
    if origin == destination:
        return None, None, None
    graph = get_graph(districts, destination)
    straightLine = {}
    for key in graph:
        straightLine[key] = straight_dis(graph[key][-2:],graph[destination][-2:])
    q = PriorityQueue()    
    q.put((straightLine[origin], 0, origin, [origin], [0,0]))  # Priority is the heuristic cost
    visited = {}  # Use a dictionary for visited nodes
    
    while not q.empty():
        (hCost, dCost, vertex, path, duration) = q.get()

        if vertex == destination: #break the loop when the condition is true
            return path, dCost, duration
        
        for next_node in graph[vertex][:-2]:
            total_dCost = dCost + next_node[1]
            total_cost = total_dCost + straightLine[next_node[0]]
            new_duration = [duration[0]+next_node[2][0], duration[1]+next_node[2][1]]
            new_duration[0] += int(new_duration[1]/60)
            new_duration[1] = new_duration[1]%60
            
            if next_node[0] not in visited or visited[next_node[0]] > total_cost:
                visited[next_node[0]] = total_cost
                q.put((total_cost,total_dCost, next_node[0], path + [next_node[0]],new_duration)) 
    print('No path found!')
    return None, None, None
#astar('Tuol Kouk', 'Mongkol Borei')
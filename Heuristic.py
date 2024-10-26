import json
import geopy.distance

#This file will create a new file and write straight line from one district to another
#For instance, if my destination was  Kork district

# destination ={
#         "lat": 11.561158,
#         "lng": 104.8980058
#         }

# with open('/mnt/d/TUX/Math for AI/mapproject/Data/cleaned3.json', 'r') as file:
#     districts = json.load(file)

# content = {}

#This function return straight line distance from one origin to one destination in km
def straight_dis(origin, destination):
    coords1 = (origin[0], origin[1])
    coords2 = (destination[0], destination[1])
    result = geopy.distance.geodesic(coords1, coords2).km
    return result
#This function retrieve lat and lng of the chosen district from the main data file
def get_lat_lng(district, districts):
    location_data = None
    for item in districts[district]:
        if isinstance(item, dict):
            for key, value in item.items():
                if isinstance(value, dict) and 'location' in value:
                    location_data = value['location']
                    return location_data
        if location_data:
            break 



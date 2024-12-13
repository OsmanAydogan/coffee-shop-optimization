import json
import requests
import folium
import pulp
from geopy.distance import great_circle

class XPoint(object):
    def __init__(self, x, y):
        self.x = x  # Longitude
        self.y = y  # Latitude
    def __str__(self):
        return f"P({self.x}_{self.y})"

class NamedPoint(XPoint):
    def __init__(self, name, x, y):
        super().__init__(x, y)
        self.name = name
    def __str__(self):
        return self.name

def get_distance(p1, p2):
    return great_circle((p1.y, p1.x), (p2.y, p2.x)).miles

def build_libraries_from_url(url, name_pos, lat_long_pos):
    r = requests.get(url)
    myjson = json.loads(r.text, parse_constant='utf-8')
    myjson = myjson['data']

    libraries = []
    k = 1
    for location in myjson:
        uname = location[name_pos]
        try:
            latitude = float(location[lat_long_pos][1])
            longitude = float(location[lat_long_pos][2])
        except (TypeError, IndexError):
            continue

        try:
            name = str(uname)
        except:
            name = "???"
        name = f"K_{name}_{k}"

        cp = NamedPoint(name, longitude, latitude)
        libraries.append(cp)
        k += 1
    return libraries

def optimize_coffee_shops(nb_shops=5):
    libraries_url = 'https://data.cityofchicago.org/api/views/x8fc-8rcq/rows.json?accessType=DOWNLOAD'
    libraries = build_libraries_from_url(libraries_url, name_pos=10, lat_long_pos=17)
    print(f"There are {len(libraries)} public libraries in Chicago")

    libraries = set(libraries)
    coffeeshop_locations = libraries

    mdl = pulp.LpProblem("coffee_shops", pulp.LpMinimize)

    BIGNUM = 999999999
    coffeeshop_vars = pulp.LpVariable.dicts("is_coffeeshop", coffeeshop_locations, cat="Binary")
    link_vars = {
        (c_loc, b): pulp.LpVariable(f"link_{c_loc}_{b}", cat="Binary")
        for c_loc in coffeeshop_locations
        for b in libraries
    }

    for c_loc in coffeeshop_locations:
        for b in libraries:
            if get_distance(c_loc, b) >= BIGNUM:
                mdl += link_vars[c_loc, b] == 0

    for b in libraries:
        mdl += pulp.lpSum(link_vars[c_loc, b] for c_loc in coffeeshop_locations) == 1

    for c_loc in coffeeshop_locations:
        for b in libraries:
            mdl += link_vars[c_loc, b] <= coffeeshop_vars[c_loc]

    mdl += pulp.lpSum(coffeeshop_vars[c_loc] for c_loc in coffeeshop_locations) == nb_shops

    mdl += pulp.lpSum(
        link_vars[c_loc, b] * get_distance(c_loc, b)
        for c_loc in coffeeshop_locations
        for b in libraries
    )

    mdl.solve()

    total_distance = pulp.value(mdl.objective)
    open_coffeeshops = [c_loc for c_loc in coffeeshop_locations if pulp.value(coffeeshop_vars[c_loc]) == 1]
    edges = [
        (c_loc, b)
        for c_loc in coffeeshop_locations
        for b in libraries
        if pulp.value(link_vars[c_loc, b]) == 1
    ]

    print("Total distance =", total_distance)
    print("# coffee shops =", len(open_coffeeshops))
    for c in open_coffeeshops:
        print("new coffee shop:", c)

    return open_coffeeshops, edges, libraries

open_coffeeshops, edges, libraries = optimize_coffee_shops()

map_osm = folium.Map(location=[41.878, -87.629], zoom_start=11)

for coffeeshop in open_coffeeshops:
    folium.Marker(
        [coffeeshop.y, coffeeshop.x], 
        icon=folium.Icon(color="red", icon="info-sign"),
        popup=folium.Popup(f"Kafe: {coffeeshop.name}", parse_html=True)
    ).add_to(map_osm)

for b in libraries:
    folium.Marker(
        [b.y, b.x], 
        icon=folium.Icon(color="blue", icon="book"),
        popup=folium.Popup(f"Kütüphane: {b.name}", parse_html=True)
    ).add_to(map_osm)

for (c, b) in edges:
    coordinates = [[c.y, c.x], [b.y, b.x]]
    map_osm.add_child(folium.PolyLine(coordinates, color="#FF0000", weight=5))

map_osm.save("coffee_shop_map.html")

def find_library_by_name(name, libraries):
    for lib in libraries:
        if lib.name.startswith(f"K_{name}"):
            return lib
    return None


addr1 = find_library_by_name("9525 S. Halsted St.", libraries) 
addr2 = find_library_by_name("731 E. 63rd St.", libraries)

if addr1 and addr2:
    distance = get_distance(addr1, addr2)
    print(f"{addr1} ile {addr2} arasındaki mesafe: {distance:.2f} mil")
else:
    print("Adreslerden biri bulunamadı.")

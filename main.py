import sys
from src.location_optimization import optimize_coffee_shops
import folium

def main():
    try:
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
        print("Map saved as coffee_shop_map.html")

    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

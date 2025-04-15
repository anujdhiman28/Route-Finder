import tkinter as tk
from tkinter import messagebox
import networkx as nx
import folium
import webbrowser
import random
import time
from geopy.geocoders import Nominatim

# Global Variables
city_locations = {
    "New York": (40.7128, -74.0060),
    "Los Angeles": (34.0522, -118.2437),
    "Chicago": (41.8781, -87.6298),
    "Houston": (29.7604, -95.3698),
    "Miami": (25.7617, -80.1918),
    "Dallas": (32.7767, -96.7970),
    "San Francisco": (37.7749, -122.4194),
    "Las Vegas": (36.1699, -115.1398),
    "Denver": (39.7392, -104.9903),
    "Seattle": (47.6062, -122.3321),
}

# Graph Representation
graph = nx.Graph()
for city in city_locations:
    graph.add_node(city, pos=city_locations[city])

# Adding random weighted edges to simulate real distances
edges = [
    ("New York", "Chicago"), ("New York", "Miami"),
    ("Los Angeles", "San Francisco"), ("Los Angeles", "Las Vegas"),
    ("Chicago", "Houston"), ("Chicago", "Dallas"),
    ("Houston", "Miami"), ("Houston", "Dallas"),
    ("San Francisco", "Seattle"), ("Las Vegas", "Denver"),
    ("Denver", "Seattle"), ("Dallas", "Las Vegas"),
]
for edge in edges:
    graph.add_edge(edge[0], edge[1], weight=random.randint(500, 2000))

# Tkinter UI
class RouteFinderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Interactive Route Finder")
        self.root.geometry("600x500")
        self.start_city = tk.StringVar()
        self.end_city = tk.StringVar()

        # UI Elements
        tk.Label(root, text="Start City:").pack()
        self.start_dropdown = tk.OptionMenu(root, self.start_city, *city_locations.keys())
        self.start_dropdown.pack()

        tk.Label(root, text="End City:").pack()
        self.end_dropdown = tk.OptionMenu(root, self.end_city, *city_locations.keys())
        self.end_dropdown.pack()

        # Buttons
        tk.Button(root, text="Find Route (BFS)", command=self.find_route_bfs).pack(pady=5)
        tk.Button(root, text="Find Route (DFS)", command=self.find_route_dfs).pack(pady=5)
        tk.Button(root, text="Find Best Route (A*)", command=self.find_route_astar).pack(pady=5)

    def find_route_bfs(self):
        self.find_route("BFS")

    def find_route_dfs(self):
        self.find_route("DFS")

    def find_route_astar(self):
        self.find_route("A*")

    def find_route(self, algorithm):
        start = self.start_city.get()
        end = self.end_city.get()
        if not start or not end:
            messagebox.showerror("Error", "Please select both start and end cities!")
            return

        if algorithm == "BFS":
            path = self.bfs(start, end)
        elif algorithm == "DFS":
            path = self.dfs(start, end)
        elif algorithm == "A*":
            path = self.astar(start, end)
        else:
            return

        if path:
            messagebox.showinfo("Success", f"Route found using {algorithm}: {' → '.join(path)}")
            self.show_route_on_map(path)
        else:
            messagebox.showerror("Error", "No route found!")

    def bfs(self, start, end):
        queue = [[start]]
        visited = set()

        while queue:
            path = queue.pop(0)
            node = path[-1]
            if node in visited:
                continue
            for neighbor in graph.neighbors(node):
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
                if neighbor == end:
                    return new_path
            visited.add(node)
        return None

    def dfs(self, start, end):
        stack = [[start]]
        visited = set()

        while stack:
            path = stack.pop()
            node = path[-1]
            if node in visited:
                continue
            for neighbor in graph.neighbors(node):
                new_path = list(path)
                new_path.append(neighbor)
                stack.append(new_path)
                if neighbor == end:
                    return new_path
            visited.add(node)
        return None

    def astar(self, start, end):
        def heuristic(city1, city2):
            lat1, lon1 = city_locations[city1]
            lat2, lon2 = city_locations[city2]
            return ((lat1 - lat2) ** 2 + (lon1 - lon2) ** 2) ** 0.5  # Euclidean Distance

        open_list = [(0, [start])]
        visited = set()

        while open_list:
            cost, path = min(open_list, key=lambda x: x[0])
            open_list.remove((cost, path))
            node = path[-1]
            if node in visited:
                continue
            if node == end:
                return path
            for neighbor in graph.neighbors(node):
                new_path = list(path)
                new_path.append(neighbor)
                new_cost = cost + graph[node][neighbor]['weight'] + heuristic(neighbor, end)
                open_list.append((new_cost, new_path))
            visited.add(node)
        return None

    def show_route_on_map(self, path):
        # Generate Map
        m = folium.Map(location=city_locations[path[0]], zoom_start=4)
        for city in path:
            folium.Marker(city_locations[city], popup=city).add_to(m)

        for i in range(len(path) - 1):
            folium.PolyLine([city_locations[path[i]], city_locations[path[i + 1]]], color="blue").add_to(m)

        map_path = "route_map.html"
        m.save(map_path)
        webbrowser.open(map_path)

# Start Tkinter App
if __name__ == "__main__":
    root = tk.Tk()
    app = RouteFinderApp(root)
    root.mainloop()





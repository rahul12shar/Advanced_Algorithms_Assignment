import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from collections import deque
import heapq
from typing import Dict, List, Tuple, Set, Optional
import math


class PolandCitiesGraph:
    """
    Graph representation of Poland cities network
    """
    
    def __init__(self):
        # Graph from diagram (a) - simplified network
        self.graph_a = {
            'Glogov': {'Leszno': 45, 'Poznan': 90},
            'Leszno': {'Glogov': 45, 'Poznan': 140, 'Kalisz': 100, 'Wroclaw': 125},
            'Poznan': {'Glogov': 90, 'Leszno': 140, 'Bydgoszcz': 140, 'Konin': 130},
            'Wroclaw': {'Leszno': 125, 'Opole': 100, 'Czestochowa': 128},
            'Bydgoszcz': {'Poznan': 140, 'Wloclawek': 120, 'Konin': 110},
            'Konin': {'Poznan': 130, 'Bydgoszcz': 110, 'Wloclawek': 55, 'Lodz': 120},
            'Wloclawek': {'Bydgoszcz': 120, 'Konin': 55, 'Plock': 130},
            'Plock': {'Wloclawek': 130, 'Warsaw': 105},
            'Kalisz': {'Leszno': 100, 'Lodz': 120},
            'Lodz': {'Kalisz': 120, 'Konin': 120, 'Czestochowa': 80, 'Warsaw': 150, 'Radom': 165},
            'Opole': {'Wroclaw': 100, 'Czestochowa': 118, 'Katowice': 85},
            'Czestochowa': {'Wroclaw': 128, 'Opole': 118, 'Lodz': 80, 'Katowice': 65, 'Kielce': 120},
            'Katowice': {'Opole': 85, 'Czestochowa': 65, 'Krakow': 82},
            'Warsaw': {'Plock': 105, 'Lodz': 150, 'Radom': 105},
            'Radom': {'Warsaw': 105, 'Lodz': 165, 'Kielce': 94},
            'Kielce': {'Czestochowa': 120, 'Radom': 94, 'Krakow': 120},
            'Krakow': {'Katowice': 82, 'Kielce': 120}
        }
        
        # Coordinates for heuristic calculation (approximate positions)
        # Based on rough geographical layout
        self.coordinates = {
            'Glogov': (0, 100),
            'Leszno': (50, 150),
            'Poznan': (50, 50),
            'Wroclaw': (100, 200),
            'Bydgoszcz': (150, 0),
            'Konin': (150, 100),
            'Wloclawek': (200, 50),
            'Plock': (300, 50),
            'Kalisz': (150, 180),
            'Lodz': (250, 150),
            'Opole': (150, 250),
            'Czestochowa': (200, 220),
            'Katowice': (200, 280),
            'Warsaw': (400, 100),
            'Radom': (380, 180),
            'Kielce': (320, 240),
            'Krakow': (300, 300)
        }
        
    def get_neighbors(self, node: str) -> Dict[str, int]:
        """Get neighbors of a node with distances"""
        return self.graph_a.get(node, {})
    
    def get_distance(self, node1: str, node2: str) -> Optional[int]:
        """Get distance between two connected nodes"""
        return self.graph_a.get(node1, {}).get(node2)
    
    def euclidean_distance(self, node1: str, node2: str) -> float:
        """Calculate Euclidean distance for heuristic"""
        x1, y1 = self.coordinates.get(node1, (0, 0))
        x2, y2 = self.coordinates.get(node2, (0, 0))
        return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


class PathfindingAlgorithms:
    """
    Implementation of DFS, BFS, and A* algorithms
    """
    
    def __init__(self, graph: PolandCitiesGraph):
        self.graph = graph
        self.execution_log = []
        
    def log(self, message: str):
        """Log execution step"""
        self.execution_log.append(message)
        
    def dfs(self, start: str, goal: str) -> Tuple[Optional[List[str]], int, List[str]]:
        """
        Depth-First Search Algorithm
        
        Returns: (path, total_distance, visited_order)
        """
        self.execution_log = []
        self.log("=" * 70)
        self.log("DEPTH-FIRST SEARCH (DFS) ALGORITHM")
        self.log("=" * 70)
        self.log(f"Start: {start}, Goal: {goal}")
        self.log("")
        
        # Open container (stack - LIFO)
        open_stack = [(start, [start], 0)]  # (node, path, distance)
        
        # Closed container (visited set)
        closed_set = set()
        
        visited_order = []
        iteration = 0
        
        self.log("Initial State:")
        self.log(f"  Open (Stack): [{start}]")
        self.log(f"  Closed (Visited): []")
        self.log("")
        
        while open_stack:
            iteration += 1
            
            # Pop from stack (LIFO - Last In First Out)
            current, path, distance = open_stack.pop()
            
            self.log(f"Iteration {iteration}:")
            self.log(f"  Current node: {current}")
            self.log(f"  Current path: {' -> '.join(path)}")
            self.log(f"  Distance so far: {distance}")
            
            # Check if already visited
            if current in closed_set:
                self.log(f"  ⚠ Already visited, skipping")
                self.log("")
                continue
            
            # Add to visited
            closed_set.add(current)
            visited_order.append(current)
            
            self.log(f"  ✓ Added to closed set")
            
            # Check if goal reached
            if current == goal:
                self.log(f"  🎯 GOAL REACHED!")
                self.log("")
                self.log("=" * 70)
                self.log("SEARCH COMPLETE - PATH FOUND")
                self.log("=" * 70)
                self.log(f"Final path: {' -> '.join(path)}")
                self.log(f"Total distance: {distance}")
                self.log(f"Nodes visited: {len(visited_order)}")
                return path, distance, visited_order
            
            # Get neighbors
            neighbors = self.graph.get_neighbors(current)
            unvisited_neighbors = [n for n in neighbors.keys() if n not in closed_set]
            
            self.log(f"  Neighbors: {list(neighbors.keys())}")
            self.log(f"  Unvisited neighbors: {unvisited_neighbors}")
            
            # Add unvisited neighbors to stack (in reverse order for consistent exploration)
            for neighbor in sorted(unvisited_neighbors, reverse=True):
                edge_dist = neighbors[neighbor]
                new_path = path + [neighbor]
                new_distance = distance + edge_dist
                open_stack.append((neighbor, new_path, new_distance))
                self.log(f"    → Adding {neighbor} to stack (distance: {edge_dist})")
            
            self.log(f"  Open (Stack): {[node for node, _, _ in open_stack]}")
            self.log(f"  Closed (Visited): {sorted(closed_set)}")
            self.log("")
        
        self.log("=" * 70)
        self.log("SEARCH COMPLETE - NO PATH FOUND")
        self.log("=" * 70)
        return None, 0, visited_order
    
    def bfs(self, start: str, goal: str) -> Tuple[Optional[List[str]], int, List[str]]:
        """
        Breadth-First Search Algorithm
        
        Returns: (path, total_distance, visited_order)
        """
        self.execution_log = []
        self.log("=" * 70)
        self.log("BREADTH-FIRST SEARCH (BFS) ALGORITHM")
        self.log("=" * 70)
        self.log(f"Start: {start}, Goal: {goal}")
        self.log("")
        
        # Open container (queue - FIFO)
        open_queue = deque([(start, [start], 0)])  # (node, path, distance)
        
        # Closed container (visited set)
        closed_set = set()
        
        visited_order = []
        iteration = 0
        
        self.log("Initial State:")
        self.log(f"  Open (Queue): [{start}]")
        self.log(f"  Closed (Visited): []")
        self.log("")
        
        while open_queue:
            iteration += 1
            
            # Dequeue from front (FIFO - First In First Out)
            current, path, distance = open_queue.popleft()
            
            self.log(f"Iteration {iteration}:")
            self.log(f"  Current node: {current}")
            self.log(f"  Current path: {' -> '.join(path)}")
            self.log(f"  Distance so far: {distance}")
            
            # Check if already visited
            if current in closed_set:
                self.log(f"  ⚠ Already visited, skipping")
                self.log("")
                continue
            
            # Add to visited
            closed_set.add(current)
            visited_order.append(current)
            
            self.log(f"  ✓ Added to closed set")
            
            # Check if goal reached
            if current == goal:
                self.log(f"  🎯 GOAL REACHED!")
                self.log("")
                self.log("=" * 70)
                self.log("SEARCH COMPLETE - PATH FOUND")
                self.log("=" * 70)
                self.log(f"Final path: {' -> '.join(path)}")
                self.log(f"Total distance: {distance}")
                self.log(f"Nodes visited: {len(visited_order)}")
                return path, distance, visited_order
            
            # Get neighbors
            neighbors = self.graph.get_neighbors(current)
            unvisited_neighbors = [n for n in neighbors.keys() if n not in closed_set]
            
            self.log(f"  Neighbors: {list(neighbors.keys())}")
            self.log(f"  Unvisited neighbors: {unvisited_neighbors}")
            
            # Add unvisited neighbors to queue
            for neighbor in sorted(unvisited_neighbors):
                edge_dist = neighbors[neighbor]
                new_path = path + [neighbor]
                new_distance = distance + edge_dist
                open_queue.append((neighbor, new_path, new_distance))
                self.log(f"    → Adding {neighbor} to queue (distance: {edge_dist})")
            
            self.log(f"  Open (Queue): {[node for node, _, _ in open_queue]}")
            self.log(f"  Closed (Visited): {sorted(closed_set)}")
            self.log("")
        
        self.log("=" * 70)
        self.log("SEARCH COMPLETE - NO PATH FOUND")
        self.log("=" * 70)
        return None, 0, visited_order
    
    def astar(self, start: str, goal: str) -> Tuple[Optional[List[str]], int, List[str]]:
        """
        A* Search Algorithm with Euclidean distance heuristic
        
        Returns: (path, total_distance, visited_order)
        """
        self.execution_log = []
        self.log("=" * 70)
        self.log("A* SEARCH ALGORITHM")
        self.log("=" * 70)
        self.log(f"Start: {start}, Goal: {goal}")
        self.log(f"Heuristic: Euclidean distance")
        self.log("")
        
        # Open container (priority queue)
        # (f_score, g_score, node, path)
        h_start = self.graph.euclidean_distance(start, goal)
        open_heap = [(h_start, 0, start, [start])]
        
        # Closed container (visited set)
        closed_set = set()
        
        # Track best g_score for each node
        g_scores = {start: 0}
        
        visited_order = []
        iteration = 0
        
        self.log("Initial State:")
        self.log(f"  h({start}) = {h_start:.2f}")
        self.log(f"  f({start}) = g({start}) + h({start}) = 0 + {h_start:.2f} = {h_start:.2f}")
        self.log(f"  Open (Priority Queue): [{start}]")
        self.log(f"  Closed (Visited): []")
        self.log("")
        
        while open_heap:
            iteration += 1
            
            # Pop node with lowest f_score
            f_score, g_score, current, path = heapq.heappop(open_heap)
            
            self.log(f"Iteration {iteration}:")
            self.log(f"  Current node: {current}")
            self.log(f"  g({current}) = {g_score}")
            h_current = self.graph.euclidean_distance(current, goal)
            self.log(f"  h({current}) = {h_current:.2f}")
            self.log(f"  f({current}) = {f_score:.2f}")
            self.log(f"  Current path: {' -> '.join(path)}")
            
            # Check if already visited
            if current in closed_set:
                self.log(f"  ⚠ Already visited, skipping")
                self.log("")
                continue
            
            # Add to visited
            closed_set.add(current)
            visited_order.append(current)
            
            self.log(f"  ✓ Added to closed set")
            
            # Check if goal reached
            if current == goal:
                self.log(f"  🎯 GOAL REACHED!")
                self.log("")
                self.log("=" * 70)
                self.log("SEARCH COMPLETE - PATH FOUND")
                self.log("=" * 70)
                self.log(f"Final path: {' -> '.join(path)}")
                self.log(f"Total distance (g): {g_score}")
                self.log(f"Nodes visited: {len(visited_order)}")
                return path, g_score, visited_order
            
            # Get neighbors
            neighbors = self.graph.get_neighbors(current)
            unvisited_neighbors = [n for n in neighbors.keys() if n not in closed_set]
            
            self.log(f"  Neighbors: {list(neighbors.keys())}")
            self.log(f"  Unvisited neighbors: {unvisited_neighbors}")
            
            # Evaluate neighbors
            for neighbor in sorted(unvisited_neighbors):
                edge_dist = neighbors[neighbor]
                new_g_score = g_score + edge_dist
                
                # Only consider if this path is better
                if neighbor not in g_scores or new_g_score < g_scores[neighbor]:
                    g_scores[neighbor] = new_g_score
                    h_score = self.graph.euclidean_distance(neighbor, goal)
                    f_score_new = new_g_score + h_score
                    new_path = path + [neighbor]
                    
                    heapq.heappush(open_heap, (f_score_new, new_g_score, neighbor, new_path))
                    
                    self.log(f"    → {neighbor}: g={new_g_score}, h={h_score:.2f}, f={f_score_new:.2f}")
            
            open_nodes = sorted(set(node for _, _, node, _ in open_heap))
            self.log(f"  Open (Priority Queue): {open_nodes}")
            self.log(f"  Closed (Visited): {sorted(closed_set)}")
            self.log("")
        
        self.log("=" * 70)
        self.log("SEARCH COMPLETE - NO PATH FOUND")
        self.log("=" * 70)
        return None, 0, visited_order


class PathfindingGUI:
    """
    Tkinter GUI for pathfinding visualization
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Poland Cities Pathfinding - DFS, BFS, A*")
        self.root.geometry("1200x900")
        
        self.graph = PolandCitiesGraph()
        self.pathfinding = PathfindingAlgorithms(self.graph)
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        self.create_widgets()
        
        # Set default values
        self.start_combo.set('Glogov')
        self.goal_combo.set('Plock')
        
    def create_widgets(self):
        """Create all GUI widgets"""
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Poland Cities Pathfinding - Robot Parcel Delivery",
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Description
        desc_label = ttk.Label(
            main_frame,
            text="Find optimal path using DFS, BFS, and A* algorithms",
            font=('Arial', 10)
        )
        desc_label.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Route Configuration", padding="10")
        input_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Start city
        ttk.Label(input_frame, text="Start City (Blue):").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        cities = sorted(self.graph.graph_a.keys())
        self.start_combo = ttk.Combobox(input_frame, values=cities, width=15, state='readonly')
        self.start_combo.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Goal city
        ttk.Label(input_frame, text="Goal City (Red):").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.goal_combo = ttk.Combobox(input_frame, values=cities, width=15, state='readonly')
        self.goal_combo.grid(row=0, column=3, padx=5, pady=5, sticky=tk.W)
        
        # Algorithm selection
        ttk.Label(input_frame, text="Algorithm:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.algo_var = tk.StringVar(value="dfs")
        
        algo_frame = ttk.Frame(input_frame)
        algo_frame.grid(row=1, column=1, columnspan=3, sticky=tk.W)
        
        ttk.Radiobutton(algo_frame, text="DFS (Depth-First)", variable=self.algo_var, value="dfs").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(algo_frame, text="BFS (Breadth-First)", variable=self.algo_var, value="bfs").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(algo_frame, text="A* (A-Star)", variable=self.algo_var, value="astar").pack(side=tk.LEFT, padx=5)
        
        # Control buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.grid(row=2, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame, text="🔍 Find Path", command=self.find_path, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🔄 Compare All", command=self.compare_all, width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="📊 Show State Space", command=self.show_state_space, width=18).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_results, width=10).pack(side=tk.LEFT, padx=5)
        
        # Results section
        results_frame = ttk.LabelFrame(main_frame, text="Path Results", padding="10")
        results_frame.grid(row=3, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        self.results_text = scrolledtext.ScrolledText(results_frame, width=55, height=35, wrap=tk.WORD, font=('Courier', 9))
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Execution log section
        log_frame = ttk.LabelFrame(main_frame, text="Execution Log (Open/Closed Containers)", padding="10")
        log_frame.grid(row=3, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        self.log_text = scrolledtext.ScrolledText(log_frame, width=55, height=35, wrap=tk.WORD, font=('Courier', 9))
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(3, weight=1)
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
    def find_path(self):
        """Find path using selected algorithm"""
        start = self.start_combo.get()
        goal = self.goal_combo.get()
        algorithm = self.algo_var.get()
        
        if not start or not goal:
            messagebox.showerror("Error", "Please select both start and goal cities!")
            return
        
        if start == goal:
            messagebox.showwarning("Warning", "Start and goal cities are the same!")
            return
        
        # Clear previous results
        self.results_text.delete(1.0, tk.END)
        self.log_text.delete(1.0, tk.END)
        
        # Run algorithm
        if algorithm == "dfs":
            path, distance, visited = self.pathfinding.dfs(start, goal)
            algo_name = "Depth-First Search (DFS)"
        elif algorithm == "bfs":
            path, distance, visited = self.pathfinding.bfs(start, goal)
            algo_name = "Breadth-First Search (BFS)"
        else:  # astar
            path, distance, visited = self.pathfinding.astar(start, goal)
            algo_name = "A* Search"
        
        # Display results
        self.results_text.insert(tk.END, "=" * 50 + "\n")
        self.results_text.insert(tk.END, f"{algo_name}\n")
        self.results_text.insert(tk.END, "=" * 50 + "\n\n")
        
        if path:
            self.results_text.insert(tk.END, f"✅ PATH FOUND!\n\n")
            self.results_text.insert(tk.END, f"Start: {start}\n")
            self.results_text.insert(tk.END, f"Goal: {goal}\n\n")
            self.results_text.insert(tk.END, f"Path:\n")
            for i, city in enumerate(path):
                if i < len(path) - 1:
                    dist = self.graph.get_distance(city, path[i+1])
                    self.results_text.insert(tk.END, f"  {i+1}. {city} → {path[i+1]} ({dist} km)\n")
            self.results_text.insert(tk.END, f"\nFinal destination: {path[-1]}\n\n")
            self.results_text.insert(tk.END, f"Total Distance: {distance} km\n")
            self.results_text.insert(tk.END, f"Nodes Visited: {len(visited)}\n")
            self.results_text.insert(tk.END, f"Path Length: {len(path)} cities\n\n")
            self.results_text.insert(tk.END, f"Visit Order: {' → '.join(visited)}\n")
        else:
            self.results_text.insert(tk.END, f"❌ NO PATH FOUND\n")
        
        # Display execution log
        for log_entry in self.pathfinding.execution_log:
            self.log_text.insert(tk.END, log_entry + "\n")
        
        self.log_text.see(tk.END)
    
    def compare_all(self):
        """Compare all three algorithms"""
        start = self.start_combo.get()
        goal = self.goal_combo.get()
        
        if not start or not goal:
            messagebox.showerror("Error", "Please select both start and goal cities!")
            return
        
        if start == goal:
            messagebox.showwarning("Warning", "Start and goal cities are the same!")
            return
        
        # Clear previous results
        self.results_text.delete(1.0, tk.END)
        self.log_text.delete(1.0, tk.END)
        
        # Run all algorithms
        dfs_path, dfs_dist, dfs_visited = self.pathfinding.dfs(start, goal)
        bfs_path, bfs_dist, bfs_visited = self.pathfinding.bfs(start, goal)
        astar_path, astar_dist, astar_visited = self.pathfinding.astar(start, goal)
        
        # Display comparison
        self.results_text.insert(tk.END, "=" * 50 + "\n")
        self.results_text.insert(tk.END, "ALGORITHM COMPARISON\n")
        self.results_text.insert(tk.END, "=" * 50 + "\n\n")
        self.results_text.insert(tk.END, f"Start: {start} → Goal: {goal}\n\n")
        
        # DFS Results
        self.results_text.insert(tk.END, "1. DEPTH-FIRST SEARCH (DFS)\n")
        self.results_text.insert(tk.END, "-" * 40 + "\n")
        if dfs_path:
            self.results_text.insert(tk.END, f"   Path: {' → '.join(dfs_path)}\n")
            self.results_text.insert(tk.END, f"   Distance: {dfs_dist} km\n")
            self.results_text.insert(tk.END, f"   Nodes visited: {len(dfs_visited)}\n")
        else:
            self.results_text.insert(tk.END, "   No path found\n")
        self.results_text.insert(tk.END, "\n")
        
        # BFS Results
        self.results_text.insert(tk.END, "2. BREADTH-FIRST SEARCH (BFS)\n")
        self.results_text.insert(tk.END, "-" * 40 + "\n")
        if bfs_path:
            self.results_text.insert(tk.END, f"   Path: {' → '.join(bfs_path)}\n")
            self.results_text.insert(tk.END, f"   Distance: {bfs_dist} km\n")
            self.results_text.insert(tk.END, f"   Nodes visited: {len(bfs_visited)}\n")
        else:
            self.results_text.insert(tk.END, "   No path found\n")
        self.results_text.insert(tk.END, "\n")
        
        # A* Results
        self.results_text.insert(tk.END, "3. A* SEARCH\n")
        self.results_text.insert(tk.END, "-" * 40 + "\n")
        if astar_path:
            self.results_text.insert(tk.END, f"   Path: {' → '.join(astar_path)}\n")
            self.results_text.insert(tk.END, f"   Distance: {astar_dist} km\n")
            self.results_text.insert(tk.END, f"   Nodes visited: {len(astar_visited)}\n")
        else:
            self.results_text.insert(tk.END, "   No path found\n")
        self.results_text.insert(tk.END, "\n")
        
        # Analysis
        self.results_text.insert(tk.END, "=" * 50 + "\n")
        self.results_text.insert(tk.END, "ANALYSIS\n")
        self.results_text.insert(tk.END, "=" * 50 + "\n\n")
        
        if dfs_path and bfs_path and astar_path:
            # Find best by distance
            distances = {'DFS': dfs_dist, 'BFS': bfs_dist, 'A*': astar_dist}
            best_dist = min(distances.values())
            best_algos_dist = [k for k, v in distances.items() if v == best_dist]
            
            # Find best by nodes visited
            nodes = {'DFS': len(dfs_visited), 'BFS': len(bfs_visited), 'A*': len(astar_visited)}
            best_nodes = min(nodes.values())
            best_algos_nodes = [k for k, v in nodes.items() if v == best_nodes]
            
            self.results_text.insert(tk.END, f"Shortest path: {', '.join(best_algos_dist)} ({best_dist} km)\n")
            self.results_text.insert(tk.END, f"Fewest nodes visited: {', '.join(best_algos_nodes)} ({best_nodes} nodes)\n\n")
            
            self.results_text.insert(tk.END, "Advantages & Disadvantages:\n\n")
            self.results_text.insert(tk.END, "DFS:\n")
            self.results_text.insert(tk.END, "  ✓ Memory efficient (stack)\n")
            self.results_text.insert(tk.END, "  ✓ Simple implementation\n")
            self.results_text.insert(tk.END, "  ✗ May not find shortest path\n")
            self.results_text.insert(tk.END, "  ✗ Can get stuck in deep branches\n\n")
            
            self.results_text.insert(tk.END, "BFS:\n")
            self.results_text.insert(tk.END, "  ✓ Guarantees shortest path (by hops)\n")
            self.results_text.insert(tk.END, "  ✓ Complete (finds solution if exists)\n")
            self.results_text.insert(tk.END, "  ✗ High memory usage (queue)\n")
            self.results_text.insert(tk.END, "  ✗ Explores many unnecessary nodes\n\n")
            
            self.results_text.insert(tk.END, "A*:\n")
            self.results_text.insert(tk.END, "  ✓ Optimal path (with admissible heuristic)\n")
            self.results_text.insert(tk.END, "  ✓ Efficient (fewer nodes explored)\n")
            self.results_text.insert(tk.END, "  ✓ Informed search strategy\n")
            self.results_text.insert(tk.END, "  ✗ Requires good heuristic function\n")
            self.results_text.insert(tk.END, "  ✗ More complex implementation\n")
        
        messagebox.showinfo("Complete", "Algorithm comparison completed!")
    
    def show_state_space(self):
        """Display the state space (graph structure)"""
        self.results_text.delete(1.0, tk.END)
        self.log_text.delete(1.0, tk.END)
        
        self.results_text.insert(tk.END, "=" * 50 + "\n")
        self.results_text.insert(tk.END, "STATE SPACE (GRAPH STRUCTURE)\n")
        self.results_text.insert(tk.END, "=" * 50 + "\n\n")
        self.results_text.insert(tk.END, "Cities Network from Diagram (a)\n\n")
        
        for city in sorted(self.graph.graph_a.keys()):
            neighbors = self.graph.get_neighbors(city)
            self.results_text.insert(tk.END, f"{city}:\n")
            for neighbor, distance in sorted(neighbors.items()):
                self.results_text.insert(tk.END, f"  → {neighbor} ({distance} km)\n")
            self.results_text.insert(tk.END, "\n")
        
        total_cities = len(self.graph.graph_a)
        total_connections = sum(len(neighbors) for neighbors in self.graph.graph_a.values()) // 2
        
        self.results_text.insert(tk.END, "=" * 50 + "\n")
        self.results_text.insert(tk.END, f"Total cities: {total_cities}\n")
        self.results_text.insert(tk.END, f"Total connections: {total_connections}\n")
        
        messagebox.showinfo("State Space", f"Graph has {total_cities} cities and {total_connections} bidirectional connections")
    
    def clear_results(self):
        """Clear all text areas"""
        self.results_text.delete(1.0, tk.END)
        self.log_text.delete(1.0, tk.END)


def main():
    """Main function to run the GUI"""
    root = tk.Tk()
    app = PathfindingGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
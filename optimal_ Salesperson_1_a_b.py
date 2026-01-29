import tkinter as tk
from tkinter import ttk, scrolledtext
import math
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class OptimizationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sensor Hub Optimization & TSP Solver")
        self.root.geometry("1200x800")
            
        # Create notebook for tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Create tabs
        self.sensor_tab = ttk.Frame(self.notebook)
        self.tsp_tab = ttk.Frame(self.notebook)
        
        self.notebook.add(self.sensor_tab, text="Part A: Sensor Hub Placement")
        self.notebook.add(self.tsp_tab, text="Part B: TSP Solver")
        
        self.setup_sensor_tab()
        self.setup_tsp_tab()
        
    def setup_sensor_tab(self):
        # Left panel for inputs
        left_frame = ttk.Frame(self.sensor_tab)
        left_frame.pack(side='left', fill='both', padx=10, pady=10)
        
        ttk.Label(left_frame, text="Sensor Hub Placement Optimizer", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        ttk.Label(left_frame, text="Enter sensor locations (format: [[x1,y1],[x2,y2],...]):").pack(anchor='w')
        
        self.sensor_input = scrolledtext.ScrolledText(left_frame, width=40, height=10)
        self.sensor_input.pack(pady=5)
        self.sensor_input.insert('1.0', "[[0,1],[1,0],[1,2],[2,1]]")
        
        ttk.Button(left_frame, text="Calculate Optimal Hub", 
                  command=self.calculate_optimal_hub).pack(pady=10)
        
        ttk.Label(left_frame, text="Results:", font=('Arial', 12, 'bold')).pack(pady=5)
        self.sensor_result = scrolledtext.ScrolledText(left_frame, width=40, height=15)
        self.sensor_result.pack(pady=5)
        
        # Right panel for visualization
        right_frame = ttk.Frame(self.sensor_tab)
        right_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)
        
        self.sensor_fig, self.sensor_ax = plt.subplots(figsize=(6, 6))
        self.sensor_canvas = FigureCanvasTkAgg(self.sensor_fig, right_frame)
        self.sensor_canvas.get_tk_widget().pack(fill='both', expand=True)
        
    def setup_tsp_tab(self):
        # Control panel
        control_frame = ttk.Frame(self.tsp_tab)
        control_frame.pack(side='left', fill='both', padx=10, pady=10)
        
        ttk.Label(control_frame, text="TSP Simulated Annealing", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        ttk.Label(control_frame, text="Number of Cities (N):").pack(anchor='w')
        self.n_cities = ttk.Entry(control_frame, width=20)
        self.n_cities.pack(pady=5)
        self.n_cities.insert(0, "20")
        
        ttk.Label(control_frame, text="Initial Temperature:").pack(anchor='w')
        self.init_temp = ttk.Entry(control_frame, width=20)
        self.init_temp.pack(pady=5)
        self.init_temp.insert(0, "1000")
        
        ttk.Label(control_frame, text="Cooling Schedule:").pack(anchor='w')
        self.cooling_var = tk.StringVar(value="exponential")
        ttk.Radiobutton(control_frame, text="Exponential (T * alpha^k)", 
                       variable=self.cooling_var, value="exponential").pack(anchor='w')
        ttk.Radiobutton(control_frame, text="Linear (T - beta * k)", 
                       variable=self.cooling_var, value="linear").pack(anchor='w')
        
        ttk.Label(control_frame, text="Alpha (for exponential):").pack(anchor='w')
        self.alpha = ttk.Entry(control_frame, width=20)
        self.alpha.pack(pady=5)
        self.alpha.insert(0, "0.995")
        
        ttk.Label(control_frame, text="Beta (for linear):").pack(anchor='w')
        self.beta = ttk.Entry(control_frame, width=20)
        self.beta.pack(pady=5)
        self.beta.insert(0, "0.5")
        
        ttk.Label(control_frame, text="Max Iterations:").pack(anchor='w')
        self.max_iter = ttk.Entry(control_frame, width=20)
        self.max_iter.pack(pady=5)
        self.max_iter.insert(0, "5000")
        
        ttk.Button(control_frame, text="Run Simulated Annealing", 
                  command=self.run_tsp).pack(pady=20)
        
        ttk.Label(control_frame, text="Results:", font=('Arial', 12, 'bold')).pack(pady=5)
        self.tsp_result = scrolledtext.ScrolledText(control_frame, width=40, height=10)
        self.tsp_result.pack(pady=5)
        
        # Visualization panel
        viz_frame = ttk.Frame(self.tsp_tab)
        viz_frame.pack(side='right', fill='both', expand=True, padx=10, pady=10)
        
        self.tsp_fig, (self.tsp_ax1, self.tsp_ax2) = plt.subplots(1, 2, figsize=(10, 5))
        self.tsp_canvas = FigureCanvasTkAgg(self.tsp_fig, viz_frame)
        self.tsp_canvas.get_tk_widget().pack(fill='both', expand=True)
        
    def calculate_optimal_hub(self):
        try:
            # Parse input
            sensor_locations = eval(self.sensor_input.get('1.0', 'end'))
            
            # Calculate optimal hub using geometric median (Weiszfeld's algorithm)
            hub_x, hub_y, min_distance = self.find_optimal_hub(sensor_locations)
            
            # Display results
            self.sensor_result.delete('1.0', 'end')
            self.sensor_result.insert('end', f"Optimal Hub Location: [{hub_x:.5f}, {hub_y:.5f}]\n\n")
            self.sensor_result.insert('end', f"Minimum Total Distance: {min_distance:.5f}\n\n")
            self.sensor_result.insert('end', "Individual Distances:\n")
            
            for i, (x, y) in enumerate(sensor_locations):
                dist = math.sqrt((x - hub_x)**2 + (y - hub_y)**2)
                self.sensor_result.insert('end', f"Sensor {i}: ({x}, {y}) -> {dist:.5f}\n")
            
            # Visualize
            self.visualize_sensors(sensor_locations, hub_x, hub_y)
            
        except Exception as e:
            self.sensor_result.delete('1.0', 'end')
            self.sensor_result.insert('end', f"Error: {str(e)}")
    
    def find_optimal_hub(self, sensors):
        """Find optimal hub location using Weiszfeld's algorithm"""
        n = len(sensors)
        
        # Start with centroid
        hub_x = sum(s[0] for s in sensors) / n
        hub_y = sum(s[1] for s in sensors) / n
        
        # Iterative refinement (Weiszfeld's algorithm)
        for _ in range(100):
            new_x, new_y = 0, 0
            total_weight = 0
            
            for sx, sy in sensors:
                dist = math.sqrt((sx - hub_x)**2 + (sy - hub_y)**2)
                if dist > 1e-10:  # Avoid division by zero
                    weight = 1 / dist
                    new_x += weight * sx
                    new_y += weight * sy
                    total_weight += weight
            
            if total_weight > 0:
                hub_x = new_x / total_weight
                hub_y = new_y / total_weight
        
        # Calculate minimum total distance
        min_distance = sum(math.sqrt((s[0] - hub_x)**2 + (s[1] - hub_y)**2) 
                          for s in sensors)
        
        return hub_x, hub_y, min_distance
    
    def visualize_sensors(self, sensors, hub_x, hub_y):
        self.sensor_ax.clear()
        
        # Plot sensors
        for i, (x, y) in enumerate(sensors):
            self.sensor_ax.plot(x, y, 'ko', markersize=10)
            self.sensor_ax.text(x+0.1, y+0.1, f'S{i}', fontsize=9)
            # Draw line to hub
            self.sensor_ax.plot([x, hub_x], [y, hub_y], 'b--', alpha=0.3)
        
        # Plot hub
        self.sensor_ax.plot(hub_x, hub_y, 'ro', markersize=12, label='Optimal Hub')
        self.sensor_ax.text(hub_x+0.1, hub_y+0.1, 'Hub', fontsize=10, color='red')
        
        self.sensor_ax.set_xlabel('X Coordinate')
        self.sensor_ax.set_ylabel('Y Coordinate')
        self.sensor_ax.set_title('Optimal Hub Placement')
        self.sensor_ax.legend()
        self.sensor_ax.grid(True, alpha=0.3)
        self.sensor_ax.set_aspect('equal')
        
        self.sensor_canvas.draw()
    
    def run_tsp(self):
        try:
            # Get parameters
            n = int(self.n_cities.get())
            t_init = float(self.init_temp.get())
            cooling = self.cooling_var.get()
            alpha = float(self.alpha.get())
            beta = float(self.beta.get())
            max_iterations = int(self.max_iter.get())
            
            # Generate random cities
            cities = [(random.uniform(0, 1000), random.uniform(0, 1000)) for _ in range(n)]
            
            # Run simulated annealing
            best_tour, best_distance, history = self.simulated_annealing(
                cities, t_init, cooling, alpha, beta, max_iterations)
            
            # Display results
            self.tsp_result.delete('1.0', 'end')
            self.tsp_result.insert('end', f"Number of Cities: {n}\n")
            self.tsp_result.insert('end', f"Initial Temperature: {t_init}\n")
            self.tsp_result.insert('end', f"Cooling Schedule: {cooling}\n")
            self.tsp_result.insert('end', f"Final Best Distance: {best_distance:.2f}\n\n")
            self.tsp_result.insert('end', f"Best Tour: {best_tour}\n")
            
            # Visualize
            self.visualize_tsp(cities, best_tour, history)
            
        except Exception as e:
            self.tsp_result.delete('1.0', 'end')
            self.tsp_result.insert('end', f"Error: {str(e)}")
    
    def simulated_annealing(self, cities, t_init, cooling, alpha, beta, max_iter):
        n = len(cities)
        
        # Initial solution: random tour
        current_tour = list(range(n))
        random.shuffle(current_tour)
        current_distance = self.calculate_tour_distance(cities, current_tour)
        
        best_tour = current_tour[:]
        best_distance = current_distance
        
        history = []
        temperature = t_init
        
        for iteration in range(max_iter):
            # Choose neighborhood operation randomly
            if random.random() < 0.5:
                # 2-opt
                new_tour = self.two_opt(current_tour)
            else:
                # Swap
                new_tour = self.swap(current_tour)
            
            new_distance = self.calculate_tour_distance(cities, new_tour)
            
            # Acceptance criterion
            delta = new_distance - current_distance
            
            if delta < 0 or random.random() < math.exp(-delta / temperature):
                current_tour = new_tour
                current_distance = new_distance
                
                if current_distance < best_distance:
                    best_tour = current_tour[:]
                    best_distance = current_distance
            
            # Update temperature
            if cooling == "exponential":
                temperature = t_init * (alpha ** iteration)
            else:  # linear
                temperature = max(0.01, t_init - beta * iteration)
            
            # Record history
            if iteration % 10 == 0:
                history.append((iteration, best_distance))
            
            # Stopping criterion
            if temperature < 0.01:
                break
        
        return best_tour, best_distance, history
    
    def calculate_tour_distance(self, cities, tour):
        distance = 0
        n = len(tour)
        for i in range(n):
            city1 = cities[tour[i]]
            city2 = cities[tour[(i + 1) % n]]
            distance += math.sqrt((city1[0] - city2[0])**2 + (city1[1] - city2[1])**2)
        return distance
    
    def two_opt(self, tour):
        new_tour = tour[:]
        i, j = sorted(random.sample(range(len(tour)), 2))
        new_tour[i:j+1] = reversed(new_tour[i:j+1])
        return new_tour
    
    def swap(self, tour):
        new_tour = tour[:]
        i, j = random.sample(range(len(tour)), 2)
        new_tour[i], new_tour[j] = new_tour[j], new_tour[i]
        return new_tour
    
    def visualize_tsp(self, cities, tour, history):
        # Clear previous plots
        self.tsp_ax1.clear()
        self.tsp_ax2.clear()
        
        # Plot tour
        n = len(tour)
        for i in range(n):
            city1 = cities[tour[i]]
            city2 = cities[tour[(i + 1) % n]]
            self.tsp_ax1.plot([city1[0], city2[0]], [city1[1], city2[1]], 'b-')
        
        # Plot cities
        for i, (x, y) in enumerate(cities):
            self.tsp_ax1.plot(x, y, 'ro', markersize=8)
            self.tsp_ax1.text(x+5, y+5, str(i), fontsize=8)
        
        # Mark start city
        start_city = cities[tour[0]]
        self.tsp_ax1.plot(start_city[0], start_city[1], 'go', markersize=12, label='Start')
        
        self.tsp_ax1.set_xlabel('X Coordinate')
        self.tsp_ax1.set_ylabel('Y Coordinate')
        self.tsp_ax1.set_title('Best TSP Tour')
        self.tsp_ax1.legend()
        self.tsp_ax1.grid(True, alpha=0.3)
        
        # Plot convergence
        if history:
            iterations, distances = zip(*history)
            self.tsp_ax2.plot(iterations, distances, 'b-')
            self.tsp_ax2.set_xlabel('Iteration')
            self.tsp_ax2.set_ylabel('Best Distance')
            self.tsp_ax2.set_title('Convergence History')
            self.tsp_ax2.grid(True, alpha=0.3)
        
        self.tsp_fig.tight_layout()
        self.tsp_canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = OptimizationApp(root)
    root.mainloop()
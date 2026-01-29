import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle
import numpy as np

class TileShatterGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Strategic Tile Shatter - Dynamic Programming Solution")
        self.root.geometry("1400x900")
        
        # Main container
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Strategic Tile Shatter Game", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Left panel - Input and Controls
        self.setup_input_panel(main_frame)
        
        # Right panel - Visualization
        self.setup_visualization_panel(main_frame)
        
        # Bottom panel - Solution details
        self.setup_solution_panel(main_frame)
        
        # Store solution data
        self.tiles = []
        self.dp = {}
        self.optimal_order = []
        
    def setup_input_panel(self, parent):
        input_frame = ttk.LabelFrame(parent, text="Input & Controls", padding="10")
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # Input section
        ttk.Label(input_frame, text="Tile Multipliers:", font=('Arial', 11, 'bold')).pack(anchor='w', pady=(0, 5))
        ttk.Label(input_frame, text="Enter as comma-separated values:").pack(anchor='w')
        
        self.tile_input = ttk.Entry(input_frame, width=40, font=('Arial', 10))
        self.tile_input.pack(pady=5, fill='x')
        self.tile_input.insert(0, "3, 1, 5, 8")
        
        # Buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(pady=10, fill='x')
        
        ttk.Button(button_frame, text="Solve with DP", 
                  command=self.solve_game, style='Accent.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="Clear", 
                  command=self.clear_all).pack(side='left', padx=5)
        
        # Examples section
        ttk.Label(input_frame, text="Quick Examples:", font=('Arial', 11, 'bold')).pack(anchor='w', pady=(15, 5))
        
        example_frame = ttk.Frame(input_frame)
        example_frame.pack(fill='x')
        
        ttk.Button(example_frame, text="Example 1: [3,1,5,8]", 
                  command=lambda: self.load_example("3, 1, 5, 8")).pack(fill='x', pady=2)
        ttk.Button(example_frame, text="Example 2: [1,5]", 
                  command=lambda: self.load_example("1, 5")).pack(fill='x', pady=2)
        ttk.Button(example_frame, text="Example 3: [2,3,1,4]", 
                  command=lambda: self.load_example("2, 3, 1, 4")).pack(fill='x', pady=2)
        
        # Algorithm explanation
        ttk.Label(input_frame, text="Algorithm Details:", font=('Arial', 11, 'bold')).pack(anchor='w', pady=(15, 5))
        
        algo_text = scrolledtext.ScrolledText(input_frame, width=45, height=15, wrap=tk.WORD, font=('Courier', 9))
        algo_text.pack(fill='both', expand=True, pady=5)
        
        explanation = """DP State Definition:
dp[i][j] = Maximum points obtainable by 
           shattering tiles from index i to j

Recurrence Relation:
For each tile k in range [i, j]:
  - Left neighbor: tile[k-1] if k > i, else 1
  - Right neighbor: tile[k+1] if k < j, else 1
  - Points = left * tile[k] * right
  - dp[i][j] = max(dp[i][k-1] + points + dp[k+1][j])

Base Cases:
- dp[i][i] = Single tile points
- Empty ranges = 0 points

Order of Computation:
- Bottom-up: Increasing subarray lengths
- Length 1 → Length 2 → ... → Length n

Time Complexity: O(n³)
Space Complexity: O(n²)"""
        
        algo_text.insert('1.0', explanation)
        algo_text.config(state='disabled')
        
    def setup_visualization_panel(self, parent):
        viz_frame = ttk.LabelFrame(parent, text="Visualization", padding="10")
        viz_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        # Create matplotlib figure
        self.fig, (self.ax1, self.ax2) = plt.subplots(2, 1, figsize=(8, 10))
        self.fig.tight_layout(pad=3.0)
        
        self.canvas = FigureCanvasTkAgg(self.fig, viz_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Initial empty plot
        self.ax1.text(0.5, 0.5, 'Enter tile multipliers and click "Solve with DP"', 
                     ha='center', va='center', transform=self.ax1.transAxes, fontsize=12)
        self.ax1.axis('off')
        self.ax2.axis('off')
        
    def setup_solution_panel(self, parent):
        solution_frame = ttk.LabelFrame(parent, text="Solution Details", padding="10")
        solution_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.solution_text = scrolledtext.ScrolledText(solution_frame, height=12, wrap=tk.WORD, font=('Courier', 9))
        self.solution_text.pack(fill='both', expand=True)
        
    def load_example(self, example):
        self.tile_input.delete(0, tk.END)
        self.tile_input.insert(0, example)
        
    def clear_all(self):
        self.tile_input.delete(0, tk.END)
        self.solution_text.delete('1.0', tk.END)
        self.ax1.clear()
        self.ax2.clear()
        self.ax1.axis('off')
        self.ax2.axis('off')
        self.canvas.draw()
        
    def solve_game(self):
        try:
            # Parse input
            input_text = self.tile_input.get().strip()
            self.tiles = [int(x.strip()) for x in input_text.split(',')]
            
            if len(self.tiles) == 0:
                messagebox.showerror("Error", "Please enter at least one tile multiplier")
                return
            
            # Solve using DP
            max_points, order = self.dynamic_programming_solution()
            
            # Display results
            self.display_solution(max_points, order)
            
            # Visualize
            self.visualize_solution()
            
        except ValueError:
            messagebox.showerror("Error", "Invalid input. Please enter comma-separated integers.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def dynamic_programming_solution(self):
        n = len(self.tiles)
        
        # DP table: dp[i][j] = max points for shattering tiles from i to j
        dp = [[0] * n for _ in range(n)]
        
        # parent table to track which tile was shattered
        parent = [[(-1, -1)] * n for _ in range(n)]
        
        # Base case: single tiles
        for i in range(n):
            left = self.tiles[i-1] if i > 0 else 1
            right = self.tiles[i+1] if i < n-1 else 1
            dp[i][i] = left * self.tiles[i] * right
            parent[i][i] = (i, dp[i][i])
        
        # Fill DP table for increasing lengths
        for length in range(2, n + 1):
            for i in range(n - length + 1):
                j = i + length - 1
                
                # Try shattering each tile k in range [i, j]
                for k in range(i, j + 1):
                    # Calculate neighbors for tile k
                    left = self.tiles[k-1] if k > i else 1
                    right = self.tiles[k+1] if k < j else 1
                    
                    # Points from shattering tile k
                    points = left * self.tiles[k] * right
                    
                    # Points from left and right subarrays
                    left_points = dp[i][k-1] if k > i else 0
                    right_points = dp[k+1][j] if k < j else 0
                    
                    total = left_points + points + right_points
                    
                    if total > dp[i][j]:
                        dp[i][j] = total
                        parent[i][j] = (k, points)
        
        # Reconstruct optimal order
        order = self.reconstruct_order(parent, 0, n-1, self.tiles[:])
        
        self.dp = dp
        self.parent = parent
        
        return dp[0][n-1], order
    
    def reconstruct_order(self, parent, i, j, remaining_tiles):
        if i > j:
            return []
        
        k, points = parent[i][j]
        
        if k == -1:
            return []
        
        tile_value = remaining_tiles[k]
        
        # Get the order: left subtree, current tile, right subtree
        result = []
        
        if i <= k - 1:
            result.extend(self.reconstruct_order(parent, i, k - 1, remaining_tiles))
        
        result.append((k, tile_value, points))
        
        if k + 1 <= j:
            result.extend(self.reconstruct_order(parent, k + 1, j, remaining_tiles))
        
        return result
    
    def display_solution(self, max_points, order):
        self.solution_text.delete('1.0', tk.END)
        
        # Header
        self.solution_text.insert('end', "="*80 + "\n")
        self.solution_text.insert('end', f"STRATEGIC TILE SHATTER - SOLUTION\n")
        self.solution_text.insert('end', "="*80 + "\n\n")
        
        self.solution_text.insert('end', f"Input Tiles: {self.tiles}\n")
        self.solution_text.insert('end', f"Maximum Points: {max_points}\n\n")
        
        self.solution_text.insert('end', "-"*80 + "\n")
        self.solution_text.insert('end', "OPTIMAL SHATTERING ORDER:\n")
        self.solution_text.insert('end', "-"*80 + "\n\n")
        
        remaining = self.tiles[:]
        total_points = 0
        
        for step, (idx, value, points) in enumerate(order, 1):
            # Calculate left and right multipliers
            left_idx = idx - 1
            right_idx = idx + 1
            
            left_mult = remaining[left_idx] if left_idx >= 0 and left_idx < len(remaining) else 1
            right_mult = remaining[right_idx] if right_idx >= 0 and right_idx < len(remaining) else 1
            
            self.solution_text.insert('end', f"Step {step}:\n")
            self.solution_text.insert('end', f"  Remaining Tiles: {remaining}\n")
            self.solution_text.insert('end', f"  Shatter Tile at Index {idx} (value={value})\n")
            self.solution_text.insert('end', f"  Calculation: {left_mult} × {value} × {right_mult} = {points} points\n")
            total_points += points
            self.solution_text.insert('end', f"  Running Total: {total_points} points\n\n")
            
            # Remove shattered tile
            remaining.pop(idx)
            
            # Adjust indices for remaining steps
            for i in range(len(order)):
                if i > step - 1:
                    old_idx, val, pts = order[i]
                    if old_idx > idx:
                        order[i] = (old_idx - 1, val, pts)
        
        self.solution_text.insert('end', "-"*80 + "\n")
        self.solution_text.insert('end', f"FINAL TOTAL POINTS: {max_points}\n")
        self.solution_text.insert('end', "="*80 + "\n")
    
    def visualize_solution(self):
        self.ax1.clear()
        self.ax2.clear()
        
        n = len(self.tiles)
        
        # Plot 1: Initial tiles and optimal order
        self.ax1.set_xlim(-0.5, n + 0.5)
        self.ax1.set_ylim(-1, 3)
        self.ax1.set_title('Tile Configuration and Shattering Order', fontsize=14, fontweight='bold')
        
        # Draw tiles
        for i, value in enumerate(self.tiles):
            rect = Rectangle((i, 0), 0.8, 1, 
                           facecolor='lightblue', 
                           edgecolor='black', 
                           linewidth=2)
            self.ax1.add_patch(rect)
            self.ax1.text(i + 0.4, 0.5, str(value), 
                         ha='center', va='center', 
                         fontsize=16, fontweight='bold')
            self.ax1.text(i + 0.4, -0.5, f'Index {i}', 
                         ha='center', va='center', 
                         fontsize=9, style='italic')
        
        # Show optimal order
        order_text = "Optimal Order: "
        for idx, (pos, val, pts) in enumerate(self.optimal_order):
            order_text += f"{pos}"
            if idx < len(self.optimal_order) - 1:
                order_text += " → "
        
        self.ax1.text(n/2, 2.5, order_text, 
                     ha='center', va='center', 
                     fontsize=11, fontweight='bold',
                     bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
        
        self.ax1.set_xticks([])
        self.ax1.set_yticks([])
        self.ax1.spines['top'].set_visible(False)
        self.ax1.spines['right'].set_visible(False)
        self.ax1.spines['bottom'].set_visible(False)
        self.ax1.spines['left'].set_visible(False)
        
        # Plot 2: DP table heatmap
        if n <= 10:  # Only show heatmap for small inputs
            dp_array = np.array(self.dp)
            im = self.ax2.imshow(dp_array, cmap='YlOrRd', aspect='auto')
            
            self.ax2.set_title('DP Table: dp[i][j] = Max Points for Range [i,j]', 
                             fontsize=12, fontweight='bold')
            self.ax2.set_xlabel('j (End Index)', fontsize=10)
            self.ax2.set_ylabel('i (Start Index)', fontsize=10)
            
            # Add text annotations
            for i in range(n):
                for j in range(n):
                    if dp_array[i][j] > 0:
                        self.ax2.text(j, i, str(int(dp_array[i][j])),
                                    ha='center', va='center',
                                    color='black', fontsize=8, fontweight='bold')
            
            self.ax2.set_xticks(range(n))
            self.ax2.set_yticks(range(n))
            plt.colorbar(im, ax=self.ax2, label='Points')
        else:
            self.ax2.text(0.5, 0.5, 'DP Table too large to display\n(Use smaller input)', 
                         ha='center', va='center', transform=self.ax2.transAxes, 
                         fontsize=12)
            self.ax2.axis('off')
        
        self.fig.tight_layout()
        self.canvas.draw()
        
        # Store order for display
        self.optimal_order = [(pos, val, pts) for pos, val, pts in self.reconstruct_order(self.parent, 0, n-1, self.tiles[:])]

if __name__ == "__main__":
    root = tk.Tk()
    app = TileShatterGame(root)
    root.mainloop()











































































































    
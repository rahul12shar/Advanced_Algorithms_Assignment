import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.patches as mpatches
from collections import deque

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class ServiceCenterPlacement:
    def __init__(self, root):
        self.root = root
        self.root.title("Binary Tree Service Center Placement Problem")
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
        title_label = ttk.Label(main_frame, text="Service Center Placement - Minimum Vertex Cover", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Setup panels
        self.setup_input_panel(main_frame)
        self.setup_visualization_panel(main_frame)
        self.setup_solution_panel(main_frame)
        
        # Store tree and solution
        self.tree_root = None
        self.service_centers = set()
        
    def setup_input_panel(self, parent):
        input_frame = ttk.LabelFrame(parent, text="Input & Controls", padding="10")
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        # Problem description
        desc_label = ttk.Label(input_frame, text="Problem: Minimum Service Centers", 
                              font=('Arial', 11, 'bold'))
        desc_label.pack(anchor='w', pady=(0, 5))
        
        desc_text = ("Find minimum number of service centers\n"
                    "such that every city (node) is either:\n"
                    "• A service center itself, OR\n"
                    "• Connected to a service center (parent/child)")
        desc = ttk.Label(input_frame, text=desc_text, justify='left', 
                        foreground='blue', font=('Arial', 9))
        desc.pack(anchor='w', pady=(0, 10))
        
        # Input section
        ttk.Label(input_frame, text="Tree Input (Level-order):", font=('Arial', 10, 'bold')).pack(anchor='w')
        ttk.Label(input_frame, text="Format: [val, left, right, ...]\nUse 'null' for empty nodes").pack(anchor='w')
        
        self.tree_input = scrolledtext.ScrolledText(input_frame, width=45, height=4, font=('Courier', 9))
        self.tree_input.pack(pady=5, fill='x')
        self.tree_input.insert('1.0', "[0, 0, null, 0, null, 0, null, 0]")
        
        # Buttons
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(pady=10, fill='x')
        
        ttk.Button(button_frame, text="Solve", 
                  command=self.solve_problem, style='Accent.TButton').pack(side='left', padx=5)
        ttk.Button(button_frame, text="Clear", 
                  command=self.clear_all).pack(side='left', padx=5)
        
        # Examples
        ttk.Label(input_frame, text="Quick Examples:", font=('Arial', 10, 'bold')).pack(anchor='w', pady=(15, 5))
        
        examples = [
            ("Example 1: Linear chain (5 nodes)", "[0, 0, null, 0, null, 0, null, 0]"),
            ("Example 2: Balanced tree", "[0, 0, 0, 0, 0, 0, 0]"),
            ("Example 3: Left skewed", "[1, 2, null, 3, null, 4]"),
            ("Example 4: Complete tree", "[0, 0, 0, 0, 0, null, null]"),
        ]
        
        for label, example in examples:
            ttk.Button(input_frame, text=label, 
                      command=lambda e=example: self.load_example(e)).pack(fill='x', pady=2)
        
        # Algorithm explanation
        ttk.Label(input_frame, text="Algorithm (Greedy DP):", font=('Arial', 10, 'bold')).pack(anchor='w', pady=(15, 5))
        
        algo_text = scrolledtext.ScrolledText(input_frame, width=45, height=15, 
                                             wrap=tk.WORD, font=('Courier', 8))
        algo_text.pack(fill='both', expand=True, pady=5)
        
        explanation = """State Definition:
For each node, compute 2 states:
  dp[node][0] = Min centers if node is NOT a center
  dp[node][1] = Min centers if node IS a center

Recurrence Relations:

1. If node IS a center (covered):
   dp[node][1] = 1 + dp[left][0] + dp[right][0]
   (Children can be anything; choose min)
   
2. If node is NOT a center:
   dp[node][0] = dp[left][1] + dp[right][1]
   (Both children MUST be centers to cover edges)

Base Cases:
- Leaf node: dp[leaf][0] = 0, dp[leaf][1] = 1
- Null node: dp[null][0] = 0, dp[null][1] = 0

Final Answer:
  min(dp[root][0], dp[root][1])

This is a Minimum Vertex Cover problem on a tree,
solved optimally using dynamic programming.

Time Complexity: O(n)
Space Complexity: O(h) where h is tree height"""
        
        algo_text.insert('1.0', explanation)
        algo_text.config(state='disabled')
        
    def setup_visualization_panel(self, parent):
        viz_frame = ttk.LabelFrame(parent, text="Tree Visualization", padding="10")
        viz_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, viz_frame)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        
        # Initial message
        self.ax.text(0.5, 0.5, 'Enter tree structure and click "Solve"', 
                    ha='center', va='center', transform=self.ax.transAxes, fontsize=12)
        self.ax.axis('off')
        
    def setup_solution_panel(self, parent):
        solution_frame = ttk.LabelFrame(parent, text="Solution Details", padding="10")
        solution_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        
        self.solution_text = scrolledtext.ScrolledText(solution_frame, height=10, 
                                                      wrap=tk.WORD, font=('Courier', 9))
        self.solution_text.pack(fill='both', expand=True)
        
    def load_example(self, example):
        self.tree_input.delete('1.0', tk.END)
        self.tree_input.insert('1.0', example)
        
    def clear_all(self):
        self.tree_input.delete('1.0', tk.END)
        self.solution_text.delete('1.0', tk.END)
        self.ax.clear()
        self.ax.axis('off')
        self.canvas.draw()
        
    def parse_tree(self, tree_list):
        """Build tree from level-order list"""
        if not tree_list or tree_list[0] is None:
            return None
        
        root = TreeNode(tree_list[0])
        queue = deque([root])
        i = 1
        
        while queue and i < len(tree_list):
            node = queue.popleft()
            
            # Left child
            if i < len(tree_list) and tree_list[i] is not None:
                node.left = TreeNode(tree_list[i])
                queue.append(node.left)
            i += 1
            
            # Right child
            if i < len(tree_list) and tree_list[i] is not None:
                node.right = TreeNode(tree_list[i])
                queue.append(node.right)
            i += 1
            
        return root
    
    def solve_problem(self):
        try:
            # Parse input
            input_text = self.tree_input.get('1.0', 'end').strip()
            input_text = input_text.replace('null', 'None')
            tree_list = eval(input_text)
            
            # Build tree
            self.tree_root = self.parse_tree(tree_list)
            
            if self.tree_root is None:
                messagebox.showerror("Error", "Invalid tree structure")
                return
            
            # Solve using DP
            min_centers, service_centers = self.minimum_vertex_cover(self.tree_root)
            self.service_centers = service_centers
            
            # Display solution
            self.display_solution(min_centers, service_centers)
            
            # Visualize
            self.visualize_tree()
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def minimum_vertex_cover(self, root):
        """
        Compute minimum vertex cover using DP
        Returns: (min_centers, set_of_center_nodes)
        """
        if not root:
            return 0, set()
        
        # DP with memoization
        dp = {}
        parent_map = {}
        
        def dfs(node, parent=None):
            if not node:
                return (0, 0)  # (not_covered, covered)
            
            parent_map[node] = parent
            
            left_not_covered, left_covered = dfs(node.left, node)
            right_not_covered, right_covered = dfs(node.right, node)
            
            # If current node is NOT a service center
            # Both children must be centers to cover the edges
            not_covered = left_covered + right_covered
            
            # If current node IS a service center
            # Children can be anything (choose minimum)
            covered = 1 + min(left_not_covered, left_covered) + min(right_not_covered, right_covered)
            
            dp[node] = (not_covered, covered)
            return (not_covered, covered)
        
        dfs(root)
        
        # Reconstruct solution
        min_cost = min(dp[root][0], dp[root][1])
        
        # Backtrack to find which nodes are service centers
        service_centers = set()
        
        def backtrack(node, parent_is_center):
            if not node:
                return
            
            not_covered_cost, covered_cost = dp[node]
            
            if parent_is_center:
                # Parent is center, node can be anything (choose cheaper)
                if covered_cost <= not_covered_cost:
                    service_centers.add(id(node))
                    backtrack(node.left, True)
                    backtrack(node.right, True)
                else:
                    backtrack(node.left, False)
                    backtrack(node.right, False)
            else:
                # Parent is not center, check optimal choice
                if node == root:
                    # Root: choose cheaper option
                    if covered_cost <= not_covered_cost:
                        service_centers.add(id(node))
                        backtrack(node.left, True)
                        backtrack(node.right, True)
                    else:
                        # Root not covered, children must be
                        backtrack(node.left, False)
                        backtrack(node.right, False)
                else:
                    # If not root and parent not center, node must be center
                    service_centers.add(id(node))
                    backtrack(node.left, True)
                    backtrack(node.right, True)
        
        # Start backtracking
        if dp[root][1] <= dp[root][0]:
            service_centers.add(id(root))
            backtrack(root.left, True)
            backtrack(root.right, True)
        else:
            backtrack(root.left, False)
            backtrack(root.right, False)
        
        return min_cost, service_centers
    
    def display_solution(self, min_centers, service_centers):
        self.solution_text.delete('1.0', 'end')
        
        self.solution_text.insert('end', "="*80 + "\n")
        self.solution_text.insert('end', "SERVICE CENTER PLACEMENT SOLUTION\n")
        self.solution_text.insert('end', "="*80 + "\n\n")
        
        self.solution_text.insert('end', f"Minimum Number of Service Centers: {min_centers}\n\n")
        
        self.solution_text.insert('end', "Strategy:\n")
        self.solution_text.insert('end', "• Every city (node) must be covered\n")
        self.solution_text.insert('end', "• A city is covered if:\n")
        self.solution_text.insert('end', "  - It has a service center, OR\n")
        self.solution_text.insert('end', "  - It's connected to a city with a service center\n\n")
        
        self.solution_text.insert('end', "-"*80 + "\n")
        self.solution_text.insert('end', "DP State Analysis:\n")
        self.solution_text.insert('end', "-"*80 + "\n\n")
        
        # Show DP values for each node
        self.show_dp_analysis(self.tree_root, "", True)
        
        self.solution_text.insert('end', "\n" + "="*80 + "\n")
        self.solution_text.insert('end', f"RESULT: {min_centers} service centers needed\n")
        self.solution_text.insert('end', "="*80 + "\n")
    
    def show_dp_analysis(self, node, prefix, is_tail):
        if not node:
            return
        
        connector = "└── " if is_tail else "├── "
        
        node_id = id(node)
        is_center = node_id in self.service_centers
        status = "SERVICE CENTER" if is_center else "Regular City"
        
        self.solution_text.insert('end', f"{prefix}{connector}Node(val={node.val}) - {status}\n")
        
        if node.left or node.right:
            extension = "    " if is_tail else "│   "
            
            if node.left:
                self.show_dp_analysis(node.left, prefix + extension, node.right is None)
            if node.right:
                self.show_dp_analysis(node.right, prefix + extension, True)
    
    def visualize_tree(self):
        self.ax.clear()
        
        if not self.tree_root:
            return
        
        # Calculate positions
        positions = {}
        self.calculate_positions(self.tree_root, 0, 0, 1.0, positions)
        
        # Draw edges first
        self.draw_edges(self.tree_root, positions)
        
        # Draw nodes
        for node, (x, y) in positions.items():
            node_id = id(node)
            is_center = node_id in self.service_centers
            
            if is_center:
                color = 'red'
                edgecolor = 'darkred'
                linewidth = 3
            else:
                color = 'lightblue'
                edgecolor = 'black'
                linewidth = 2
            
            circle = plt.Circle((x, y), 0.15, color=color, ec=edgecolor, linewidth=linewidth, zorder=10)
            self.ax.add_patch(circle)
            
            self.ax.text(x, y, str(node.val), ha='center', va='center', 
                        fontsize=12, fontweight='bold', zorder=11)
        
        # Add legend
        center_patch = mpatches.Patch(color='red', label='Service Center')
        city_patch = mpatches.Patch(color='lightblue', label='Regular City')
        self.ax.legend(handles=[center_patch, city_patch], loc='upper right')
        
        self.ax.set_title(f'Minimum Service Centers: {len(self.service_centers)}', 
                         fontsize=14, fontweight='bold')
        self.ax.set_aspect('equal')
        self.ax.axis('off')
        
        self.canvas.draw()
    
    def calculate_positions(self, node, x, y, width, positions):
        if not node:
            return
        
        positions[node] = (x, y)
        
        if node.left:
            self.calculate_positions(node.left, x - width, y - 1, width / 2, positions)
        if node.right:
            self.calculate_positions(node.right, x + width, y - 1, width / 2, positions)
    
    def draw_edges(self, node, positions):
        if not node:
            return
        
        x1, y1 = positions[node]
        
        if node.left:
            x2, y2 = positions[node.left]
            self.ax.plot([x1, x2], [y1, y2], 'k-', linewidth=1.5, zorder=1)
            self.draw_edges(node.left, positions)
        
        if node.right:
            x2, y2 = positions[node.right]
            self.ax.plot([x1, x2], [y1, y2], 'k-', linewidth=1.5, zorder=1)
            self.draw_edges(node.right, positions)

if __name__ == "__main__":
    root = tk.Tk()
    app = ServiceCenterPlacement(root)
    root.mainloop()
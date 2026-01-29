import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
from typing import Dict, List, Tuple
import copy

class EnergyGridOptimizer:
    def __init__(self):
        # Sample data for demonstration
        self.hourly_demand = {
            6: {'A': 20, 'B': 15, 'C': 25},
            7: {'A': 22, 'B': 16, 'C': 28},
            8: {'A': 25, 'B': 18, 'C': 30},
            9: {'A': 28, 'B': 20, 'C': 32},
            10: {'A': 30, 'B': 22, 'C': 35},
            11: {'A': 32, 'B': 24, 'C': 38},
            12: {'A': 35, 'B': 25, 'C': 40},
            13: {'A': 33, 'B': 24, 'C': 38},
            14: {'A': 31, 'B': 23, 'C': 36},
            15: {'A': 29, 'B': 21, 'C': 34},
            16: {'A': 27, 'B': 20, 'C': 32},
            17: {'A': 30, 'B': 22, 'C': 35},
            18: {'A': 32, 'B': 24, 'C': 38},
            19: {'A': 28, 'B': 21, 'C': 33},
            20: {'A': 25, 'B': 19, 'C': 30},
            21: {'A': 23, 'B': 18, 'C': 28},
            22: {'A': 21, 'B': 16, 'C': 26},
            23: {'A': 19, 'B': 14, 'C': 24}
        }
        
        self.energy_sources = {
            'S1': {
                'type': 'Solar',
                'max_capacity': 50,
                'available_hours': range(6, 19),
                'cost_per_kwh': 1.0
            },
            'S2': {
                'type': 'Hydro',
                'max_capacity': 40,
                'available_hours': range(0, 24),
                'cost_per_kwh': 1.5
            },
            'S3': {
                'type': 'Diesel',
                'max_capacity': 60,
                'available_hours': range(17, 24),
                'cost_per_kwh': 3.0
            }
        }
        
        self.tolerance = 0.10  # ±10% flexibility
        
    def is_source_available(self, source_id: str, hour: int) -> bool:
        """Check if an energy source is available at a given hour"""
        return hour in self.energy_sources[source_id]['available_hours']
    
    def greedy_allocation(self, hour: int, demands: Dict[str, float]) -> Tuple[Dict, float, bool]:
        """
        Greedy approach: Always choose cheapest available sources first
        Returns: (allocation_dict, total_cost, success)
        """
        allocation = {district: {} for district in demands.keys()}
        total_cost = 0
        remaining_demand = copy.deepcopy(demands)
        
        # Sort sources by cost (cheapest first)
        sorted_sources = sorted(
            self.energy_sources.items(),
            key=lambda x: x[1]['cost_per_kwh']
        )
        
        # Track remaining capacity for each source
        remaining_capacity = {
            sid: self.energy_sources[sid]['max_capacity'] 
            for sid in self.energy_sources.keys()
        }
        
        # Try to fulfill each district's demand
        for district, demand in demands.items():
            original_demand = demand
            min_acceptable = demand * (1 - self.tolerance)
            max_acceptable = demand * (1 + self.tolerance)
            
            for source_id, source_info in sorted_sources:
                if remaining_demand[district] <= 0:
                    break
                    
                if not self.is_source_available(source_id, hour):
                    continue
                
                if remaining_capacity[source_id] <= 0:
                    continue
                
                # Allocate as much as possible from this source
                allocation_amount = min(
                    remaining_demand[district],
                    remaining_capacity[source_id]
                )
                
                if allocation_amount > 0:
                    allocation[district][source_id] = allocation_amount
                    remaining_demand[district] -= allocation_amount
                    remaining_capacity[source_id] -= allocation_amount
                    total_cost += allocation_amount * source_info['cost_per_kwh']
            
            # Check if demand is satisfied within tolerance
            fulfilled = original_demand - remaining_demand[district]
            if fulfilled < min_acceptable:
                return allocation, total_cost, False
        
        return allocation, total_cost, True
    
    def dynamic_programming_allocation(self, hour: int, demands: Dict[str, float]) -> Tuple[Dict, float, bool]:
        """
        Dynamic Programming approach to find optimal allocation
        Explores different combinations while respecting constraints
        """
        districts = list(demands.keys())
        available_sources = [
            (sid, sinfo) for sid, sinfo in self.energy_sources.items()
            if self.is_source_available(sid, hour)
        ]
        
        if not available_sources:
            return {}, float('inf'), False
        
        # State: (district_idx, remaining_capacities_tuple)
        # Value: (min_cost, allocation_dict)
        memo = {}
        
        def dp(district_idx: int, remaining_caps: tuple) -> Tuple[float, Dict]:
            """Recursive DP function"""
            if district_idx >= len(districts):
                return 0, {}
            
            state = (district_idx, remaining_caps)
            if state in memo:
                return memo[state]
            
            district = districts[district_idx]
            demand = demands[district]
            min_acceptable = demand * (1 - self.tolerance)
            max_acceptable = demand * (1 + self.tolerance)
            
            best_cost = float('inf')
            best_allocation = None
            
            # Try different combinations of sources for this district
            # Generate possible allocations
            def generate_allocations(target: float, sources_left: List, caps_left: List, current: List):
                """Generate valid allocation combinations"""
                if not sources_left:
                    total = sum(current)
                    if min_acceptable <= total <= max_acceptable:
                        yield current[:]
                    return
                
                source_idx = len(current)
                source_id, source_info = sources_left[0]
                max_from_source = min(caps_left[source_idx], max_acceptable)
                
                # Try different amounts from this source (0 to max_from_source)
                # Use step size for efficiency
                step = max(1, int(max_from_source / 10))
                for amount in range(0, int(max_from_source) + 1, step):
                    current.append(amount)
                    yield from generate_allocations(
                        target, 
                        sources_left[1:], 
                        caps_left, 
                        current
                    )
                    current.pop()
                
                # Also try exact amounts needed
                exact_needed = max(0, min(target - sum(current), caps_left[source_idx]))
                if exact_needed not in range(0, int(max_from_source) + 1, step):
                    current.append(exact_needed)
                    yield from generate_allocations(
                        target,
                        sources_left[1:],
                        caps_left,
                        current
                    )
                    current.pop()
            
            # Try different valid allocations for current district
            caps_list = list(remaining_caps)
            
            for allocation_amounts in generate_allocations(demand, available_sources, caps_list, []):
                # Calculate cost for this allocation
                current_cost = sum(
                    allocation_amounts[i] * available_sources[i][1]['cost_per_kwh']
                    for i in range(len(allocation_amounts))
                )
                
                # Update remaining capacities
                new_caps = tuple(
                    caps_list[i] - allocation_amounts[i]
                    for i in range(len(caps_list))
                )
                
                # Recurse for next district
                future_cost, future_allocation = dp(district_idx + 1, new_caps)
                
                if future_cost != float('inf'):
                    total_cost = current_cost + future_cost
                    
                    if total_cost < best_cost:
                        best_cost = total_cost
                        # Build allocation dict
                        district_alloc = {
                            available_sources[i][0]: allocation_amounts[i]
                            for i in range(len(allocation_amounts))
                            if allocation_amounts[i] > 0
                        }
                        best_allocation = {district: district_alloc}
                        best_allocation.update(future_allocation)
            
            if best_allocation is None:
                result = (float('inf'), {})
            else:
                result = (best_cost, best_allocation)
            
            memo[state] = result
            return result
        
        # Initial capacities
        initial_caps = tuple(sinfo['max_capacity'] for _, sinfo in available_sources)
        
        try:
            min_cost, allocation = dp(0, initial_caps)
            
            if min_cost == float('inf'):
                return {}, float('inf'), False
            
            return allocation, min_cost, True
        except RecursionError:
            # Fallback to greedy if DP is too complex
            return self.greedy_allocation(hour, demands)
    
    def optimize_all_hours(self, method='greedy'):
        """Run optimization for all hours"""
        results = []
        total_cost = 0
        total_renewable = 0
        total_energy = 0
        diesel_usage = []
        
        for hour in sorted(self.hourly_demand.keys()):
            demands = self.hourly_demand[hour]
            
            if method == 'greedy':
                allocation, cost, success = self.greedy_allocation(hour, demands)
            else:  # dynamic programming
                allocation, cost, success = self.dynamic_programming_allocation(hour, demands)
            
            # Calculate statistics
            hour_energy = 0
            hour_renewable = 0
            hour_diesel = 0
            
            for district, sources in allocation.items():
                for source_id, amount in sources.items():
                    hour_energy += amount
                    if self.energy_sources[source_id]['type'] in ['Solar', 'Hydro']:
                        hour_renewable += amount
                    if self.energy_sources[source_id]['type'] == 'Diesel':
                        hour_diesel += amount
            
            if hour_diesel > 0:
                diesel_usage.append({
                    'hour': hour,
                    'amount': hour_diesel,
                    'reason': 'Peak demand or renewable sources insufficient'
                })
            
            total_cost += cost
            total_renewable += hour_renewable
            total_energy += hour_energy
            
            # Calculate fulfillment percentage for each district
            fulfillment = {}
            for district, demand in demands.items():
                allocated = sum(allocation.get(district, {}).values())
                fulfillment[district] = (allocated / demand * 100) if demand > 0 else 0
            
            results.append({
                'hour': hour,
                'allocation': allocation,
                'cost': cost,
                'success': success,
                'fulfillment': fulfillment,
                'demands': demands
            })
        
        renewable_percentage = (total_renewable / total_energy * 100) if total_energy > 0 else 0
        
        return {
            'results': results,
            'total_cost': total_cost,
            'renewable_percentage': renewable_percentage,
            'diesel_usage': diesel_usage,
            'total_energy': total_energy
        }


class EnergyGridGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Energy Grid Load Distribution Optimizer")
        self.root.geometry("1200x800")
        
        self.optimizer = EnergyGridOptimizer()
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Smart Energy Grid Load Distribution Optimization (Nepal)",
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=10)
        
        # Left panel - Input data
        left_frame = ttk.LabelFrame(main_frame, text="Input Data", padding="10")
        left_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        # Demand table
        ttk.Label(left_frame, text="Hourly Demand (kWh):", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=5)
        
        demand_frame = ttk.Frame(left_frame)
        demand_frame.grid(row=1, column=0, sticky=(tk.W, tk.E))
        
        self.demand_text = scrolledtext.ScrolledText(demand_frame, width=40, height=10, wrap=tk.WORD)
        self.demand_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.display_demand_data()
        
        # Energy sources table
        ttk.Label(left_frame, text="Energy Sources:", font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky=tk.W, pady=(10, 5))
        
        source_frame = ttk.Frame(left_frame)
        source_frame.grid(row=3, column=0, sticky=(tk.W, tk.E))
        
        self.source_text = scrolledtext.ScrolledText(source_frame, width=40, height=8, wrap=tk.WORD)
        self.source_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.display_source_data()
        
        # Constraints
        ttk.Label(left_frame, text="Constraints:", font=('Arial', 10, 'bold')).grid(row=4, column=0, sticky=tk.W, pady=(10, 5))
        constraint_label = ttk.Label(left_frame, text="• Each district's demand must be met within ±10%\n• Energy sources have limited capacity\n• Sources available only during specific hours\n• Objective: Minimize cost and reduce diesel usage")
        constraint_label.grid(row=5, column=0, sticky=tk.W)
        
        # Right panel - Controls and results
        right_frame = ttk.Frame(main_frame)
        right_frame.grid(row=1, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=5)
        
        # Control panel
        control_frame = ttk.LabelFrame(right_frame, text="Optimization Controls", padding="10")
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(control_frame, text="Select Method:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.method_var = tk.StringVar(value="greedy")
        
        ttk.Radiobutton(control_frame, text="Greedy Strategy (Fast)", variable=self.method_var, value="greedy").grid(row=1, column=0, sticky=tk.W)
        ttk.Radiobutton(control_frame, text="Dynamic Programming (Optimal)", variable=self.method_var, value="dp").grid(row=2, column=0, sticky=tk.W)
        
        # Optimize button
        optimize_btn = ttk.Button(control_frame, text="Run Optimization", command=self.run_optimization)
        optimize_btn.grid(row=3, column=0, pady=10, sticky=(tk.W, tk.E))
        
        # Results display
        results_frame = ttk.LabelFrame(right_frame, text="Results", padding="10")
        results_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        self.results_text = scrolledtext.ScrolledText(results_frame, width=70, height=35, wrap=tk.WORD)
        self.results_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=2)
        main_frame.rowconfigure(1, weight=1)
        right_frame.rowconfigure(1, weight=1)
        
    def display_demand_data(self):
        """Display demand data in text widget"""
        self.demand_text.delete(1.0, tk.END)
        self.demand_text.insert(tk.END, "Hour  District A  District B  District C\n")
        self.demand_text.insert(tk.END, "=" * 45 + "\n")
        for hour, demands in sorted(self.optimizer.hourly_demand.items()):
            line = f"{hour:02d}    {demands['A']:5.0f}      {demands['B']:5.0f}      {demands['C']:5.0f}\n"
            self.demand_text.insert(tk.END, line)
    
    def display_source_data(self):
        """Display energy source data"""
        self.source_text.delete(1.0, tk.END)
        self.source_text.insert(tk.END, "Source  Type    Max(kWh)  Hours      Cost(Rs.)\n")
        self.source_text.insert(tk.END, "=" * 50 + "\n")
        for source_id, info in self.optimizer.energy_sources.items():
            hours = f"{min(info['available_hours'])}-{max(info['available_hours'])}"
            line = f"{source_id}     {info['type']:8} {info['max_capacity']:4.0f}     {hours:10} {info['cost_per_kwh']:4.1f}\n"
            self.source_text.insert(tk.END, line)
    
    def run_optimization(self):
        """Run the optimization and display results"""
        method = self.method_var.get()
        
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, f"Running {method.upper()} optimization...\n\n")
        self.root.update()
        
        try:
            optimization_results = self.optimizer.optimize_all_hours(method)
            
            self.results_text.insert(tk.END, "=" * 80 + "\n")
            self.results_text.insert(tk.END, f"OPTIMIZATION RESULTS - {method.upper()} METHOD\n")
            self.results_text.insert(tk.END, "=" * 80 + "\n\n")
            
            # Display hourly results
            self.results_text.insert(tk.END, "HOURLY ALLOCATION DETAILS:\n")
            self.results_text.insert(tk.END, "-" * 80 + "\n\n")
            
            for result in optimization_results['results']:
                hour = result['hour']
                allocation = result['allocation']
                cost = result['cost']
                demands = result['demands']
                fulfillment = result['fulfillment']
                
                self.results_text.insert(tk.END, f"Hour {hour:02d}:00\n")
                self.results_text.insert(tk.END, f"  Demands: A={demands['A']}kWh, B={demands['B']}kWh, C={demands['C']}kWh\n")
                
                for district in ['A', 'B', 'C']:
                    if district in allocation and allocation[district]:
                        sources_used = ', '.join([
                            f"{sid}={amt:.1f}kWh" 
                            for sid, amt in allocation[district].items()
                        ])
                        self.results_text.insert(tk.END, f"  District {district}: {sources_used}")
                        self.results_text.insert(tk.END, f" (Fulfilled: {fulfillment[district]:.1f}%)\n")
                    else:
                        self.results_text.insert(tk.END, f"  District {district}: No allocation\n")
                
                self.results_text.insert(tk.END, f"  Cost: Rs. {cost:.2f}\n\n")
            
            # Summary statistics
            self.results_text.insert(tk.END, "\n" + "=" * 80 + "\n")
            self.results_text.insert(tk.END, "SUMMARY ANALYSIS\n")
            self.results_text.insert(tk.END, "=" * 80 + "\n\n")
            
            self.results_text.insert(tk.END, f"Total Cost: Rs. {optimization_results['total_cost']:.2f}\n\n")
            
            self.results_text.insert(tk.END, f"Renewable Energy Usage: {optimization_results['renewable_percentage']:.2f}%\n")
            self.results_text.insert(tk.END, f"Total Energy Distributed: {optimization_results['total_energy']:.2f} kWh\n\n")
            
            # Diesel usage analysis
            if optimization_results['diesel_usage']:
                self.results_text.insert(tk.END, "Diesel Usage Details:\n")
                for usage in optimization_results['diesel_usage']:
                    self.results_text.insert(tk.END, f"  Hour {usage['hour']:02d}: {usage['amount']:.2f} kWh - {usage['reason']}\n")
            else:
                self.results_text.insert(tk.END, "No diesel usage - 100% renewable energy!\n")
            
            self.results_text.insert(tk.END, "\n" + "-" * 80 + "\n")
            self.results_text.insert(tk.END, "ALGORITHM EFFICIENCY ANALYSIS:\n")
            self.results_text.insert(tk.END, "-" * 80 + "\n\n")
            
            if method == 'greedy':
                self.results_text.insert(tk.END, "Greedy Strategy:\n")
                self.results_text.insert(tk.END, "✓ Very fast execution\n")
                self.results_text.insert(tk.END, "✓ Always prioritizes cheapest sources\n")
                self.results_text.insert(tk.END, "✓ Good for real-time systems\n")
                self.results_text.insert(tk.END, "⚠ May not find global optimal solution\n")
                self.results_text.insert(tk.END, "⚠ Locally optimal decisions\n")
            else:
                self.results_text.insert(tk.END, "Dynamic Programming:\n")
                self.results_text.insert(tk.END, "✓ Explores multiple combinations\n")
                self.results_text.insert(tk.END, "✓ Finds optimal or near-optimal solution\n")
                self.results_text.insert(tk.END, "✓ Better cost efficiency\n")
                self.results_text.insert(tk.END, "⚠ Slower for large problems\n")
                self.results_text.insert(tk.END, "⚠ Higher computational complexity\n")
            
            self.results_text.insert(tk.END, "\n" + "=" * 80 + "\n")
            
            messagebox.showinfo("Success", "Optimization completed successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.results_text.insert(tk.END, f"\nERROR: {str(e)}\n")


def main():
    root = tk.Tk()
    app = EnergyGridGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
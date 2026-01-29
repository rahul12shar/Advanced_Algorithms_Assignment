import threading
import time
import random
from typing import List
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox


class MultithreadedSorter:
    """
    A class that implements multithreaded sorting with parallel execution
    """
    
    def __init__(self):
        self.original_list = []
        self.global_array = []
        self.sorted_array = []
        self.sublist1 = []
        self.sublist2 = []
        self.sorting_complete = threading.Event()
        self.thread1_complete = threading.Event()
        self.thread2_complete = threading.Event()
        self.log_messages = []
        
    def log(self, message: str):
        """Log a message with timestamp"""
        timestamp = time.strftime("%H:%M:%S.") + f"{int((time.time() % 1) * 1000):03d}"
        log_msg = f"[{timestamp}] {message}"
        self.log_messages.append(log_msg)
        print(log_msg)
    
    def merge_sort(self, arr: List[int]) -> List[int]:
        """
        Merge sort algorithm - divides and conquers
        """
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        left = self.merge_sort(arr[:mid])
        right = self.merge_sort(arr[mid:])
        
        return self.merge(left, right)
    
    def merge(self, left: List[int], right: List[int]) -> List[int]:
        """
        Merge two sorted lists into one sorted list
        """
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result
    
    def quick_sort(self, arr: List[int]) -> List[int]:
        """
        Quick sort algorithm - another efficient sorting method
        """
        if len(arr) <= 1:
            return arr
        
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        
        return self.quick_sort(left) + middle + self.quick_sort(right)
    
    def sorting_thread_0(self, data: List[int], start_index: int):
        """
        Sorting Thread 0 - sorts the first half
        """
        thread_name = threading.current_thread().name
        self.log(f"{thread_name}: Starting to sort from index {start_index}")
        self.log(f"{thread_name}: Data to sort: {data}")
        
        # Simulate some processing time
        time.sleep(0.5)
        
        # Sort using merge sort
        sorted_data = self.merge_sort(data.copy())
        
        self.log(f"{thread_name}: Sorting complete: {sorted_data}")
        
        # Store in global array
        for i, value in enumerate(sorted_data):
            self.global_array[start_index + i] = value
        
        self.sublist1 = sorted_data
        self.thread1_complete.set()
        self.log(f"{thread_name}: Exiting")
    
    def sorting_thread_1(self, data: List[int], start_index: int):
        """
        Sorting Thread 1 - sorts the second half
        """
        thread_name = threading.current_thread().name
        self.log(f"{thread_name}: Starting to sort from index {start_index}")
        self.log(f"{thread_name}: Data to sort: {data}")
        
        # Simulate some processing time
        time.sleep(0.5)
        
        # Sort using quick sort (to demonstrate different algorithms)
        sorted_data = self.quick_sort(data.copy())
        
        self.log(f"{thread_name}: Sorting complete: {sorted_data}")
        
        # Store in global array
        for i, value in enumerate(sorted_data):
            self.global_array[start_index + i] = value
        
        self.sublist2 = sorted_data
        self.thread2_complete.set()
        self.log(f"{thread_name}: Exiting")
    
    def merging_thread(self):
        """
        Merging Thread - waits for both sorting threads to complete, then merges
        """
        thread_name = threading.current_thread().name
        self.log(f"{thread_name}: Started, waiting for sorting threads to complete...")
        
        # Wait for both sorting threads to complete
        self.thread1_complete.wait()
        self.thread2_complete.wait()
        
        self.log(f"{thread_name}: Both sorting threads completed, beginning merge...")
        self.log(f"{thread_name}: Sublist 1: {self.sublist1}")
        self.log(f"{thread_name}: Sublist 2: {self.sublist2}")
        
        # Merge the two sorted sublists
        self.sorted_array = self.merge(self.sublist1, self.sublist2)
        
        self.log(f"{thread_name}: Merge complete!")
        self.log(f"{thread_name}: Final sorted array: {self.sorted_array}")
        
        self.sorting_complete.set()
        self.log(f"{thread_name}: Exiting")
    
    def sort_with_threads(self, input_list: List[int]) -> List[int]:
        """
        Main method to sort a list using multiple threads
        """
        self.log("=" * 70)
        self.log("MULTITHREADED SORTING STARTED")
        self.log("=" * 70)
        
        self.original_list = input_list.copy()
        n = len(input_list)
        
        # Initialize global array with same size
        self.global_array = [0] * n
        
        # Clear events
        self.thread1_complete.clear()
        self.thread2_complete.clear()
        self.sorting_complete.clear()
        
        self.log(f"Original list: {self.original_list}")
        self.log(f"List size: {n}")
        
        # Divide the list into two halves
        mid = n // 2
        first_half = input_list[:mid]
        second_half = input_list[mid:]
        
        self.log(f"Dividing into two sublists of size {mid} and {n - mid}")
        self.log(f"First half: {first_half}")
        self.log(f"Second half: {second_half}")
        self.log("")
        
        # Create and start sorting threads
        thread0 = threading.Thread(
            target=self.sorting_thread_0,
            args=(first_half, 0),
            name="SortingThread-0"
        )
        
        thread1 = threading.Thread(
            target=self.sorting_thread_1,
            args=(second_half, mid),
            name="SortingThread-1"
        )
        
        # Create merging thread
        merge_thread = threading.Thread(
            target=self.merging_thread,
            name="MergingThread"
        )
        
        # Start all threads
        self.log("Starting sorting threads...")
        thread0.start()
        thread1.start()
        merge_thread.start()
        
        # Wait for merging to complete
        self.sorting_complete.wait()
        
        # Wait for all threads to finish
        thread0.join()
        thread1.join()
        merge_thread.join()
        
        self.log("")
        self.log("=" * 70)
        self.log("MULTITHREADED SORTING COMPLETED")
        self.log("=" * 70)
        self.log(f"Original: {self.original_list}")
        self.log(f"Sorted:   {self.sorted_array}")
        
        return self.sorted_array


class MultithreadedSortingGUI:
    """
    GUI application for multithreaded sorting
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Multithreaded Sorting Application")
        self.root.geometry("1000x700")
        
        self.sorter = MultithreadedSorter()
        
        # Configure style
        style = ttk.Style()
        style.theme_use('clam')
        
        self.create_widgets()
        
        # Load example data
        self.load_example()
    
    def create_widgets(self):
        """Create all GUI widgets"""
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="Multithreaded Sorting Application",
            font=('Arial', 16, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=10)
        
        # Description
        desc_label = ttk.Label(
            main_frame,
            text="Divides list into two halves, sorts them in parallel threads, then merges",
            font=('Arial', 10)
        )
        desc_label.grid(row=1, column=0, columnspan=3, pady=5)
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Input Configuration", padding="10")
        input_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        ttk.Label(input_frame, text="Enter numbers (comma-separated):").grid(row=0, column=0, sticky=tk.W, pady=5)
        
        self.input_entry = ttk.Entry(input_frame, width=60)
        self.input_entry.grid(row=0, column=1, columnspan=2, padx=5, sticky=(tk.W, tk.E))
        
        ttk.Button(input_frame, text="Load Example", command=self.load_example).grid(row=1, column=0, pady=5, sticky=tk.W)
        ttk.Button(input_frame, text="Generate Random", command=self.generate_random).grid(row=1, column=1, pady=5)
        ttk.Button(input_frame, text="Clear", command=self.clear_input).grid(row=1, column=2, pady=5, sticky=tk.E)
        
        # Visualization section
        viz_frame = ttk.LabelFrame(main_frame, text="Visualization", padding="10")
        viz_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Original list display
        ttk.Label(viz_frame, text="Original List:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky=tk.W)
        self.original_text = tk.Text(viz_frame, height=2, width=70, wrap=tk.WORD)
        self.original_text.grid(row=1, column=0, columnspan=3, pady=5)
        
        # Sublists display
        sublist_frame = ttk.Frame(viz_frame)
        sublist_frame.grid(row=2, column=0, columnspan=3, pady=10)
        
        # Sublist 1
        sublist1_frame = ttk.Frame(sublist_frame)
        sublist1_frame.grid(row=0, column=0, padx=10)
        ttk.Label(sublist1_frame, text="Sublist 1 (Thread 0):", font=('Arial', 9, 'bold')).pack()
        self.sublist1_text = tk.Text(sublist1_frame, height=2, width=30, wrap=tk.WORD)
        self.sublist1_text.pack()
        
        # Sublist 2
        sublist2_frame = ttk.Frame(sublist_frame)
        sublist2_frame.grid(row=0, column=1, padx=10)
        ttk.Label(sublist2_frame, text="Sublist 2 (Thread 1):", font=('Arial', 9, 'bold')).pack()
        self.sublist2_text = tk.Text(sublist2_frame, height=2, width=30, wrap=tk.WORD)
        self.sublist2_text.pack()
        
        # Sorted list display
        ttk.Label(viz_frame, text="Final Sorted List:", font=('Arial', 10, 'bold')).grid(row=3, column=0, sticky=tk.W, pady=(10, 0))
        self.sorted_text = tk.Text(viz_frame, height=2, width=70, wrap=tk.WORD)
        self.sorted_text.grid(row=4, column=0, columnspan=3, pady=5)
        
        # Control buttons
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=4, column=0, columnspan=3, pady=10)
        
        ttk.Button(control_frame, text="▶ Start Sorting", command=self.start_sorting, width=20).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="🔄 Reset", command=self.reset, width=15).pack(side=tk.LEFT, padx=5)
        
        # Log section
        log_frame = ttk.LabelFrame(main_frame, text="Execution Log", padding="10")
        log_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, width=90, height=15, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(5, weight=1)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        viz_frame.columnconfigure(0, weight=1)
    
    def load_example(self):
        """Load the example from the problem"""
        example_list = [7, 12, 19, 3, 18, 4, 2, 6, 15, 8]
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, ", ".join(map(str, example_list)))
    
    def generate_random(self):
        """Generate random numbers"""
        size = random.randint(8, 20)
        random_list = [random.randint(1, 100) for _ in range(size)]
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, ", ".join(map(str, random_list)))
    
    def clear_input(self):
        """Clear input field"""
        self.input_entry.delete(0, tk.END)
    
    def reset(self):
        """Reset all displays"""
        self.original_text.delete(1.0, tk.END)
        self.sublist1_text.delete(1.0, tk.END)
        self.sublist2_text.delete(1.0, tk.END)
        self.sorted_text.delete(1.0, tk.END)
        self.log_text.delete(1.0, tk.END)
    
    def update_display(self):
        """Update the visualization displays"""
        # Original list
        self.original_text.delete(1.0, tk.END)
        self.original_text.insert(1.0, str(self.sorter.original_list))
        
        # Sublists (update periodically)
        def update_sublists():
            self.sublist1_text.delete(1.0, tk.END)
            self.sublist2_text.delete(1.0, tk.END)
            
            if self.sorter.sublist1:
                self.sublist1_text.insert(1.0, str(self.sorter.sublist1))
            if self.sorter.sublist2:
                self.sublist2_text.insert(1.0, str(self.sorter.sublist2))
            
            if not self.sorter.sorting_complete.is_set():
                self.root.after(100, update_sublists)
        
        update_sublists()
    
    def update_log(self):
        """Update the log display"""
        self.log_text.delete(1.0, tk.END)
        for message in self.sorter.log_messages:
            self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
    
    def start_sorting(self):
        """Start the sorting process"""
        # Get input
        input_text = self.input_entry.get().strip()
        
        if not input_text:
            messagebox.showerror("Error", "Please enter numbers to sort!")
            return
        
        try:
            # Parse input
            input_list = [int(x.strip()) for x in input_text.split(",")]
            
            if len(input_list) < 2:
                messagebox.showerror("Error", "Please enter at least 2 numbers!")
                return
            
            # Reset displays
            self.reset()
            
            # Create new sorter instance
            self.sorter = MultithreadedSorter()
            
            # Update display with original list
            self.sorter.original_list = input_list
            self.update_display()
            
            # Start sorting in a separate thread to keep GUI responsive
            def sort_and_update():
                result = self.sorter.sort_with_threads(input_list)
                
                # Update GUI in main thread
                self.root.after(0, lambda: self.finish_sorting(result))
            
            # Start monitoring thread for live updates
            def monitor_progress():
                self.update_log()
                if not self.sorter.sorting_complete.is_set():
                    self.root.after(100, monitor_progress)
            
            sort_thread = threading.Thread(target=sort_and_update)
            sort_thread.daemon = True
            sort_thread.start()
            
            # Start monitoring
            self.root.after(100, monitor_progress)
            
        except ValueError:
            messagebox.showerror("Error", "Invalid input! Please enter comma-separated integers.")
    
    def finish_sorting(self, result):
        """Finish the sorting and update displays"""
        # Update sorted list display
        self.sorted_text.delete(1.0, tk.END)
        self.sorted_text.insert(1.0, str(result))
        
        # Final log update
        self.update_log()
        
        # Show completion message
        messagebox.showinfo("Success", f"Sorting completed!\n\nOriginal: {self.sorter.original_list}\n\nSorted: {result}")


def main():
    """Main function to run the GUI application"""
    root = tk.Tk()
    app = MultithreadedSortingGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
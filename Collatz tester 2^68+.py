import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import random
import time
import queue

# Constants
TRIVIAL_THRESHOLD = 2**68  # Start automated search from 2^68
TRIVIAL_CYCLE = {1, 2, 4}

# Global state variables
running = False
paused = False
checked_numbers = set()  # Stores numbers already processed
lock = threading.Lock()

# Load checked numbers from file
try:
    with open('checked_numbers.txt', 'r') as f:
        for line in f:
            checked_numbers.add(int(line.strip()))
except FileNotFoundError:
    pass

# --- Optimized Collatz functions ---

def accelerated_collatz(n):
    """Optimized to remove factors of 2 using bitwise operations."""
    t = 3 * n + 1
    while t % 2 == 0:  # Remove all factors of 2
        t = t // 2
    return t

def full_collatz_tree(n, max_steps=10000):
    """Efficiently computes the sequence and detects cycles."""
    seen = {}
    sequence = []
    step = 0
    current = n
    while step < max_steps:
        sequence.append(current)
        if current in seen:
            return sequence, sequence[seen[current]:]
        seen[current] = step
        current = accelerated_collatz(current)
        if current == 1:  # Stop when reaching 1 (trivial cycle)
            sequence.append(1)
            return sequence, None
        step += 1
    return sequence, None

# --- Thread-safe UI updates ---

class CollatzTool(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Collatz Conjecture Explorer")
        self.geometry("800x600")
        self.queue = queue.Queue()
        self.search_thread = None  # Initialize the search thread attribute
        self.total_checked_overall = 0  # Track total numbers checked
        self.session_checked = 0  # Track numbers checked in this session
        self.create_widgets()
        self.after(100, self.process_queue)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_widgets(self):
        """Create and arrange UI elements."""
        control_frame = ttk.Frame(self)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # Start, Pause, Stop buttons
        self.start_btn = ttk.Button(control_frame, text="Start", command=self.start_search)
        self.start_btn.pack(side=tk.LEFT, padx=2)
        self.pause_btn = ttk.Button(control_frame, text="Pause", command=self.pause_search, state=tk.DISABLED)
        self.pause_btn.pack(side=tk.LEFT, padx=2)
        self.stop_btn = ttk.Button(control_frame, text="Stop", command=self.stop_search, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=2)

        # Automated search checkbox
        self.auto_var = tk.BooleanVar()
        self.auto_check = ttk.Checkbutton(control_frame, text="Automated Search", variable=self.auto_var)
        self.auto_check.pack(side=tk.LEFT, padx=2)

        # Sliders for resource usage
        ttk.Label(control_frame, text="Delay (ms):").pack(side=tk.LEFT, padx=2)
        self.delay_slider = ttk.Scale(control_frame, from_=0, to=1000, orient=tk.HORIZONTAL)
        self.delay_slider.set(100)  # Default 100ms
        self.delay_slider.pack(side=tk.LEFT, padx=2)

        ttk.Label(control_frame, text="Range Factor:").pack(side=tk.LEFT, padx=2)
        self.range_slider = ttk.Scale(control_frame, from_=1, to=10, orient=tk.HORIZONTAL)
        self.range_slider.set(1)  # Default factor 1
        self.range_slider.pack(side=tk.LEFT, padx=2)

        # Current number and telemetry
        self.current_label = ttk.Label(self, text="Current number: N/A", font=("Courier", 10))
        self.current_label.pack(side=tk.TOP, anchor=tk.W, padx=5)
        self.telemetry_label = ttk.Label(self, text="Overall checked: 0 | Session checked: 0")
        self.telemetry_label.pack(side=tk.TOP, anchor=tk.W, padx=5)

        # Log / Telemetry text box
        self.log_box = scrolledtext.ScrolledText(self, width=80, height=20)
        self.log_box.pack(side=tk.TOP, padx=5, pady=5, fill=tk.BOTH, expand=True)

        # Manual input field and button
        manual_frame = ttk.Frame(self)
        manual_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        ttk.Label(manual_frame, text="Manual check number:").pack(side=tk.LEFT, padx=2)
        self.manual_entry = ttk.Entry(manual_frame, width=20)
        self.manual_entry.pack(side=tk.LEFT, padx=2)

        # Power of 10 multiplier
        ttk.Label(manual_frame, text="×10^").pack(side=tk.LEFT, padx=2)
        self.power_slider = ttk.Scale(manual_frame, from_=0, to=100, orient=tk.HORIZONTAL)
        self.power_slider.set(0)  # Default power of 0
        self.power_slider.pack(side=tk.LEFT, padx=2)

        self.manual_btn = ttk.Button(manual_frame, text="Check", command=self.manual_check)
        self.manual_btn.pack(side=tk.LEFT, padx=2)

    def process_queue(self):
        """Process all pending UI updates from the queue."""
        try:
            while True:
                task = self.queue.get_nowait()
                task()
        except queue.Empty:
            pass
        self.after(100, self.process_queue)

    def thread_safe_log(self, message):
        """Thread-safe logging."""
        self.queue.put(lambda: self.log(message))

    def log(self, message):
        """Log a message to the text box."""
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.see(tk.END)

    def update_telemetry(self):
        """Update telemetry labels."""
        self.telemetry_label.config(text=f"Overall checked: {self.total_checked_overall} | Session checked: {self.session_checked}")

    def update_current(self, number):
        """Update the current number being checked."""
        if number > 1e20:  # Use scientific notation for very large numbers
            self.current_label.config(text=f"Current number: {number:.2e}")
        else:
            self.current_label.config(text=f"Current number: {number}")

    def start_search(self):
        """Start the search process."""
        global running, paused
        running = True
        paused = False
        self.session_checked = 0  # Reset session counter
        self.thread_safe_log("Starting search...")
        self.start_btn.config(state=tk.DISABLED)
        self.pause_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.NORMAL)
        if self.search_thread is None or not self.search_thread.is_alive():
            self.search_thread = threading.Thread(target=self.search_loop, daemon=True)
            self.search_thread.start()
            self.thread_safe_log("Search thread started.")

    def pause_search(self):
        """Pause or resume the search process."""
        global paused
        paused = not paused
        if paused:
            self.pause_btn.config(text="Resume")
            self.thread_safe_log("Paused.")
        else:
            self.pause_btn.config(text="Pause")
            self.thread_safe_log("Resumed.")

    def stop_search(self):
        """Stop the search process."""
        global running
        running = False
        self.thread_safe_log("Stopping search...")
        self.start_btn.config(state=tk.NORMAL)
        self.pause_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.DISABLED)

    def on_closing(self):
        """Handle window close event."""
        self.stop_search()
        self.destroy()

    def search_loop(self):
        """Main search loop."""
        global running, paused
        try:
            self.thread_safe_log("Entering search loop.")
            while running:
                if paused:
                    time.sleep(0.1)
                    continue

                # Generate candidate (odd numbers only)
                if self.auto_var.get():
                    # Automated mode: random odd numbers starting from 2^68
                    factor = self.range_slider.get()
                    high = int(TRIVIAL_THRESHOLD * (10 ** factor))
                    start = TRIVIAL_THRESHOLD if TRIVIAL_THRESHOLD % 2 else TRIVIAL_THRESHOLD + 1
                    if start > high:
                        self.thread_safe_log("No valid candidates in range.")
                        continue
                    candidate = random.randrange(start, high + 1, 2)
                else:
                    # Manual mode: sequential odd numbers
                    candidate = TRIVIAL_THRESHOLD + 1 + 2 * self.session_checked

                if candidate in checked_numbers:
                    self.thread_safe_log(f"Skipping already checked number: {candidate}")
                    continue

                # Full sequence check
                sequence, cycle = full_collatz_tree(candidate)
                trivial = False
                if cycle:
                    trivial = set(cycle) == TRIVIAL_CYCLE
                else:
                    trivial = sequence[-1] < TRIVIAL_THRESHOLD if sequence else True

                # Update telemetry
                with lock:
                    self.total_checked_overall += 1
                    self.session_checked += 1
                    checked_numbers.add(candidate)
                    with open('checked_numbers.txt', 'a') as f:
                        f.write(f"{candidate}\n")

                # UI updates via queue
                self.queue.put(lambda: self.update_telemetry())
                self.queue.put(lambda: self.update_current(candidate))
                if not trivial and cycle:
                    self.thread_safe_log(f"Non-trivial cycle found: {cycle}")
                    messagebox.showinfo("Cycle Found", f"Cycle detected at {candidate}!")
                else:
                    self.thread_safe_log(f"Checked {candidate}: Trivial={trivial}")

                # Delay between checks
                delay = self.delay_slider.get() / 1000.0
                time.sleep(delay)

        except Exception as e:
            self.thread_safe_log(f"Error in search loop: {str(e)}")
        finally:
            running = False
            self.thread_safe_log("Exiting search loop.")

    def manual_check(self):
        """Manually check a specific number."""
        try:
            num = int(self.manual_entry.get())
            power = int(self.power_slider.get())
            num *= 10**power  # Multiply by 10^power
            if num < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid positive integer.")
            return
        self.thread_safe_log(f"Manually checking {num}...")
        tree, cycle = full_collatz_tree(num)
        self.thread_safe_log("Full tree:")
        self.thread_safe_log(str(tree))
        if cycle:
            if set(cycle) != TRIVIAL_CYCLE:
                self.thread_safe_log("Non-trivial cycle found: " + str(cycle))
            else:
                self.thread_safe_log("Trivial cycle encountered.")
        else:
            self.thread_safe_log("Sequence reached trivial region without cycle detection.")

# Main execution
if __name__ == '__main__':
    app = CollatzTool()
    app.mainloop()
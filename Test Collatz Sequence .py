import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

# Constants
TRIVIAL_CYCLE = {1, 2, 4}

# Function to compute the next number in the Collatz sequence
def collatz_step(n):
    if n % 2 == 0:
        return n // 2
    else:
        return 3 * n + 1

# Function to compute the full Collatz sequence
def compute_collatz_sequence(n, max_steps=1000):
    sequence = []
    current = n
    step = 0
    while step < max_steps:
        sequence.append(current)
        if current in TRIVIAL_CYCLE:
            return sequence, "Trivial loop (4-2-1) detected."
        if current in sequence[:-1]:  # Check for non-trivial loops
            loop_start = sequence.index(current)
            return sequence, f"Non-trivial loop detected: {sequence[loop_start:]}"
        current = collatz_step(current)
        step += 1
    return sequence, "Reached max steps (1000). Possible divergence."

# GUI Application
class CollatzExplorer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Collatz Sequence Explorer")
        self.geometry("600x400")
        self.create_widgets()

    def create_widgets(self):
        # Input frame
        input_frame = ttk.Frame(self)
        input_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)

        # Number input
        ttk.Label(input_frame, text="Number:").pack(side=tk.LEFT, padx=5)
        self.number_entry = ttk.Entry(input_frame, width=20)
        self.number_entry.pack(side=tk.LEFT, padx=5)

        # Power of 10 multiplier
        ttk.Label(input_frame, text="×10^").pack(side=tk.LEFT, padx=5)
        self.power_entry = ttk.Entry(input_frame, width=5)
        self.power_entry.pack(side=tk.LEFT, padx=5)
        self.power_entry.insert(0, "0")  # Default power of 0

        # Start button
        self.start_btn = ttk.Button(input_frame, text="Start", command=self.start_computation)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        # Continue button (initially disabled)
        self.continue_btn = ttk.Button(input_frame, text="Continue", command=self.continue_computation, state=tk.DISABLED)
        self.continue_btn.pack(side=tk.LEFT, padx=5)

        # Output text box
        self.output_box = scrolledtext.ScrolledText(self, width=80, height=20)
        self.output_box.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

    def start_computation(self):
        """Start or restart the computation."""
        try:
            # Get the input number and power of 10
            num = int(self.number_entry.get())
            power = int(self.power_entry.get())
            num *= 10**power  # Multiply by 10^power

            if num < 1:
                raise ValueError("Number must be a positive integer.")

            # Reset the output box
            self.output_box.delete(1.0, tk.END)
            self.output_box.insert(tk.END, f"Starting computation for {num}...\n")

            # Start the computation
            self.current_number = num
            self.sequence = []
            self.compute_next_steps()

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def compute_next_steps(self, max_steps=1000):
        """Compute the next steps in the sequence."""
        for _ in range(max_steps):
            self.sequence.append(self.current_number)
            if self.current_number in TRIVIAL_CYCLE:
                self.output_box.insert(tk.END, f"Trivial loop (4-2-1) detected.\n")
                self.output_box.insert(tk.END, f"Full sequence: {self.sequence}\n")
                self.continue_btn.config(state=tk.DISABLED)
                return
            if self.current_number in self.sequence[:-1]:  # Check for non-trivial loops
                loop_start = self.sequence.index(self.current_number)
                self.output_box.insert(tk.END, f"Non-trivial loop detected: {self.sequence[loop_start:]}\n")
                self.output_box.insert(tk.END, f"Full sequence: {self.sequence}\n")
                self.continue_btn.config(state=tk.DISABLED)
                return
            self.current_number = collatz_step(self.current_number)

        # If max steps reached, pause and wait for user input
        self.output_box.insert(tk.END, f"Reached max steps ({max_steps}). Possible divergence.\n")
        self.output_box.insert(tk.END, f"Current sequence: {self.sequence}\n")
        self.continue_btn.config(state=tk.NORMAL)

    def continue_computation(self):
        """Continue the computation from where it left off."""
        self.continue_btn.config(state=tk.DISABLED)
        self.compute_next_steps()

# Run the application
if __name__ == "__main__":
    app = CollatzExplorer()
    app.mainloop()
# Collatz Conjecture Programs

This repository contains two Python programs that explore the Collatz Conjecture. The Collatz Conjecture is an unsolved mathematical problem that involves iterating a sequence of numbers based on specific rules. Both programs provide a graphical user interface (GUI) for users to interact with and explore the conjecture.

---

## **Program 1: Collatz Conjecture Explorer**

### **Overview**
The **Collatz Conjecture Explorer** is a program that automates the search for numbers that might violate the Collatz Conjecture. It checks large numbers for non-trivial cycles or divergence and logs the results. The program also allows users to manually check specific numbers and view their Collatz sequences.

### **Features**
1. **Automated Search**:
   - Searches for numbers starting from `2^68` (a large threshold).
   - Checks for non-trivial cycles or divergence.
   - Logs all checked numbers to a file (`checked_numbers.txt`).

2. **Manual Check**:
   - Allows users to input a specific number and view its Collatz sequence.
   - Supports multiplying the input number by a power of 10 for large inputs.

3. **Threaded Execution**:
   - Runs the search in a separate thread to keep the GUI responsive.
   - Includes start, pause, and stop controls.

4. **Real-Time Updates**:
   - Displays the current number being checked.
   - Logs results in a scrollable text box.

5. **Trivial and Non-Trivial Loops**:
   - Detects trivial loops (`4-2-1`) and non-trivial loops.
   - Alerts the user if a non-trivial loop is found.

### **Usage**
1. **Automated Search**:
   - Click "Start" to begin the automated search.
   - Use "Pause" to pause the search and "Resume" to continue.
   - Click "Stop" to end the search.

2. **Manual Check**:
   - Enter a number in the "Manual check number" field.
   - Optionally, adjust the "×10^" slider to multiply the number by a power of 10.
   - Click "Check" to compute and display the Collatz sequence.

3. **Output**:
   - The program logs all results in the text box.
   - If a non-trivial loop is found, a popup alert is displayed.

### **Example**
- Input: `22`
- Output:
- Manually checking 22...
Full tree:
[22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1]
Sequence reached trivial region without cycle detection.

---

## **Program 2: Collatz Sequence Explorer**

### **Overview**
The **Collatz Sequence Explorer** is a simpler program that computes the Collatz sequence for a given number. It continues the sequence until a trivial loop (`4-2-1`) or a non-trivial loop is found. If the program suspects divergence (after 1000 iterations), it pauses and waits for user input to continue.

### **Features**
1. **Input Fields**:
 - A field for the number.
 - A field for the power of 10 multiplier.

2. **Dynamic Computation**:
 - Computes the sequence until a loop is detected.
 - Pauses after 1000 iterations if no loop is found, allowing the user to continue.

3. **Full Sequence Display**:
 - Displays the full Collatz sequence when the computation ends.

4. **Trivial and Non-Trivial Loops**:
 - Detects and displays trivial loops (`4-2-1`) and non-trivial loops.

### **Usage**
1. **Input**:
 - Enter a number in the "Number" field.
 - Optionally, enter a power of 10 in the "×10^" field to multiply the number.

2. **Start Computation**:
 - Click "Start" to begin the computation.

3. **Continue Computation**:
 - If the program pauses (after 1000 iterations), click "Continue" to resume.

4. **Output**:
 - The program displays the sequence and any detected loops in the output box.

### **Example**
- Input: `27`
- Output:Starting computation for 27...
Reached max steps (1000). Possible divergence.
Current sequence: [27, 82, 41, 124, 62, 31, 94, 47, 142, 71, 214, 107, 322, 161, 484, 242, 121, 364, 182, 91, 274, 137, 412, 206, 103, 310, 155, 466, 233, 700, 350, 175, 526, 263, 790, 395, 1186, 593, 1780, 890, 445, 1336, 668, 334, 167, 502, 251, 754, 377, 1132, 566, 283, 850, 425, 1276, 638, 319, 958, 479, 1438, 719, 2158, 1079, 3238, 1619, 4858, 2429, 7288, 3644, 1822, 911, 2734, 1367, 4102, 2051, 6154, 3077, 9232, 4616, 2308, 1154, 577, 1732, 866, 433, 1300, 650, 325, 976, 488, 244, 122, 61, 184, 92, 46, 23, 70, 35, 106, 53, 160, 80, 40, 20, 10, 5, 16, 8, 4, 2, 1]

---

## **Requirements**
- Python 3.x
- `tkinter` (usually included with Python)

---

## **How to Run**
1. Clone the repository or download the Python files.
2. Run the desired program using Python:
 ```bash
 python collatz_conjecture_explorer.py  # For Program 1
 python collatz_sequence_explorer.py    # For Program 2

License
This project is open-source and available under the MIT License. Feel free to modify and distribute it as needed.

Contact
For questions or feedback, please open an issue on GitHub or contact the author rifatislamrupok02@gmail.com

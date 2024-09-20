import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime
import time

# Database setup
conn = sqlite3.connect("bmi_data.db")
c = conn.cursor()

# Create table for BMI records
c.execute("""
CREATE TABLE IF NOT EXISTS bmi_records (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user TEXT,
    date TEXT,
    weight REAL,
    height REAL,
    bmi REAL
)
""")
conn.commit()

# BMI calculation and category functions
def calculate_bmi(weight, height):
    return round(weight / (height ** 2), 2)

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal Weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

# Function to animate widget (enhanced styling)
def animate_widget(widget, animation, duration=0.1, repeat=2):
    style_name = widget.winfo_name() + "_TButton"
    widget_style = ttk.Style()

    for i in range(repeat):
        for prop, value in animation:
            style_variant = f"{style_name}.{prop}"
            widget_style.configure(style_variant, background=value)
            widget.configure(style=style_variant)
            root.update()
            time.sleep(duration)

# Function to calculate BMI and display results
def calculate():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())
        user = user_entry.get()

        if weight <= 0 or height <= 0 or user == "":
            raise ValueError("Invalid input")

        bmi = calculate_bmi(weight, height)
        category = get_bmi_category(bmi)

        result_label.config(text=f"BMI: {bmi} ({category})")
        save_bmi_record(user, weight, height, bmi)

        # Trigger widget animation for result_label
        animate_widget(result_label, [("background", "lightblue")])

    except ValueError:
        messagebox.showerror("Input Error", "Please provide valid inputs for weight, height, and user.")

# Function to save BMI record
def save_bmi_record(user, weight, height, bmi):
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute("INSERT INTO bmi_records (user, date, weight, height, bmi) VALUES (?, ?, ?, ?, ?)",
              (user, date, weight, height, bmi))
    conn.commit()
    messagebox.showinfo("Success", "BMI record saved successfully.")

# Function to view historical data and plot BMI trends
def view_history():
    user = user_entry.get()
    if user == "":
        messagebox.showerror("Input Error", "Please enter a user name.")
        return

    c.execute("SELECT date, bmi FROM bmi_records WHERE user = ? ORDER BY date", (user,))
    records = c.fetchall()

    if records:
        dates = [record[0] for record in records]
        bmis = [record[1] for record in records]
        plot_bmi_trend(dates, bmis)
    else:
        messagebox.showinfo("No Data", "No records found for this user.")

# Function to plot BMI trends
def plot_bmi_trend(dates, bmis):
    plt.figure(figsize=(10, 5))
    plt.plot(dates, bmis, marker="o", linestyle="-", color="b")
    plt.title("BMI Trend Over Time")
    plt.xlabel("Date")
    plt.ylabel("BMI")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()

# Tkinter GUI setup
root = tk.Tk()
root.title("BMI Calculator with History")
root.geometry("400x350")

# User input
tk.Label(root, text="User:").grid(row=0, column=0)
user_entry = tk.Entry(root)
user_entry.grid(row=0, column=1)

tk.Label(root, text="Weight (kg):").grid(row=1, column=0)
weight_entry = tk.Entry(root)
weight_entry.grid(row=1, column=1)

tk.Label(root, text="Height (m):").grid(row=2, column=0)
height_entry = tk.Entry(root)
height_entry.grid(row=2, column=1)

# Calculate BMI button
calculate_button = ttk.Button(root, text="Calculate BMI", command=calculate)
calculate_button.grid(row=3, column=0, columnspan=2)

# BMI result label
result_label = ttk.Label(root, text="BMI: ")
result_label.grid(row=4, column=0, columnspan=2)

# View History button
view_history_button = ttk.Button(root, text="View History", command=view_history)
view_history_button.grid(row=5, column=0, columnspan=2)

root.mainloop()

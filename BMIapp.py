import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time

def calculate_bmi(weight, height):
    bmi = weight / (height ** 2)
    return bmi

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal Weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:
        return "Obese"

def animate_widget(widget, animation, duration=0.1, repeat=2):
    for i in range(repeat):
        for style, value in animation:
            style_name = widget.winfo_name() + "_" + style
            widget_style.configure(style_name, background=value)
            widget.configure(style=style_name)
            root.update()
            time.sleep(duration)

def calculate():
    try:
        weight = float(weight_entry.get())
        height = float(height_entry.get())

        if weight <= 0 or height <= 0:
            raise ValueError("Weight and height must be greater than zero.")

        if weight_unit_var.get() == "lbs":
            weight = weight * 0.453592

        if height_unit_var.get() == "cm":
            height = height / 100
        elif height_unit_var.get() == "feet":
            height = height * 0.3048

        bmi = calculate_bmi(weight, height)
        bmi_category = get_bmi_category(bmi)

        bmi_label.config(text="BMI: {:.2f}".format(bmi))
        category_label.config(text="Category: {}".format(bmi_category))

        weight_range = get_weight_range(height)
        height_range = get_height_range(weight)

        weight_range_label.config(text="Suggested Weight Range: {:.2f} - {:.2f} kg".format(weight_range[0], weight_range[1]))
        height_range_label.config(text="Suggested Height Range: {:.2f} - {:.2f} meters".format(height_range[0], height_range[1]))

        animate_widget(bmi_label, [("background", "pink"), ("background", "SystemButtonFace")])
        animate_widget(category_label, [("background", "pink"), ("background", "SystemButtonFace")])
        animate_widget(weight_range_label, [("background", "pink"), ("background", "SystemButtonFace")])
        animate_widget(height_range_label, [("background", "pink"), ("background", "SystemButtonFace")])

        animate_widget(calculate_button, [("background", "yellow"), ("background", "#FFFFC5")])

    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

def get_weight_range(height):
    lower_limit = 18.5 * (height ** 2)
    upper_limit = 24.9 * (height ** 2)
    return lower_limit, upper_limit

def get_height_range(weight):
    lower_limit = (weight / 24.9) ** 0.5
    upper_limit = (weight / 18.5) ** 0.5
    return lower_limit, upper_limit

root = tk.Tk()
root.title("BMI Calculator")
root.geometry("900x500")
root.configure(bg="#171515")

# Create a ttk Style
widget_style = ttk.Style()
widget_style.configure('TButton', background='#4CAF50', foreground="#171515", font=("Comic Sans MS", 10, "bold"))
widget_style.map('TButton', background=[('active', '#43A047')])

main_frame = ttk.Frame(root, padding="20")
main_frame.pack(expand=True, fill="both")

header = ttk.Label(main_frame, text="BMI Calculator", font=("Comic Sans MS", 16, "bold"), background="#4CAF50", foreground="white")
header.grid(row=0, column=0, columnspan=3, pady=10, sticky="nsew")

weight_label = ttk.Label(main_frame, text="Weight:", font=("Comic Sans MS", 12))
weight_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

weight_entry = tk.Entry(main_frame, font=("Comic Sans MS", 12), relief="solid", borderwidth=1)
weight_entry.grid(row=1, column=1, padx=10, pady=5)

weight_unit_var = tk.StringVar(value="kgs")
weight_unit_combo = ttk.Combobox(main_frame, textvariable=weight_unit_var, values=("kgs", "lbs"), state="readonly", width=5, font=("Helvetica", 12))
weight_unit_combo.grid(row=1, column=2, padx=10, pady=5)

height_label = ttk.Label(main_frame, text="Height:", font=("Comic Sans MS", 12))
height_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

height_entry = tk.Entry(main_frame, font=("Comic Sans MS", 12), relief="solid", borderwidth=1)
height_entry.grid(row=2, column=1, padx=10, pady=5)

height_unit_var = tk.StringVar(value="meters")
height_unit_combo = ttk.Combobox(main_frame, textvariable=height_unit_var, values=("meters", "feet", "cm"), state="readonly", width=5, font=("Helvetica", 12))
height_unit_combo.grid(row=2, column=2, padx=10, pady=5)

calculate_button = ttk.Button(main_frame, text="Calculate", command=calculate, style='TButton')
calculate_button.grid(row=3, column=0, columnspan=3, pady=10, ipadx=5, ipady=5)

bmi_label = ttk.Label(main_frame, text="BMI: ", font=("Comic Sans MS", 12))
bmi_label.grid(row=4, column=0, sticky="w", padx=10, pady=5)

category_label = ttk.Label(main_frame, text="Category: ", font=("Comic Sans MS", 12))
category_label.grid(row=5, column=0, sticky="w", padx=10, pady=5)

weight_range_label = ttk.Label(main_frame, text="Suggested Weight Range: ", font=("Comic Sans MS", 12))
weight_range_label.grid(row=6, column=0, sticky="w", padx=10, pady=5)

height_range_label = ttk.Label(main_frame, text="Suggested Height Range: ", font=("Comic Sans MS", 12))
height_range_label.grid(row=7, column=0, sticky="w", padx=10, pady=5)

root.mainloop()

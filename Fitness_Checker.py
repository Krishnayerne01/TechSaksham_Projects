import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from PIL import Image, ImageTk  # Import the Python Imaging Library (PIL)

# Define Workout and User Classes (as before)

class Workout:
    def __init__(self, date, exercise_type, duration, calories_burned):
        self.date = date
        self.exercise_type = exercise_type
        self.duration = duration
        self.calories_burned = calories_burned

    def __str__(self):
        return f"{self.date}: {self.exercise_type} for {self.duration} minutes, {self.calories_burned} calories burned"


class User:
    def __init__(self, name, age, weight):
        self.name = name
        self.age = age
        self.weight = weight
        self.workouts = []

    def add_workout(self, workout):
        self.workouts.append(workout)

    def view_workouts(self):
        return "\n".join([str(workout) for workout in self.workouts])

    def save_data(self, filename):
        with open(filename, 'w') as file:
            for workout in self.workouts:
                file.write(f"{workout.date},{workout.exercise_type},{workout.duration},{workout.calories_burned}\n")

    def load_data(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                date, exercise_type, duration, calories_burned = line.strip().split(',')
                workout = Workout(date, exercise_type, int(duration), int(calories_burned))
                self.workouts.append(workout)


# GUI Functions

def add_workout(user):
    date = simpledialog.askstring("Input", "Enter the date (YYYY-MM-DD):")
    exercise_type = simpledialog.askstring("Input", "Enter the exercise type:")
    duration = simpledialog.askinteger("Input", "Enter the duration (minutes):")
    calories_burned = simpledialog.askinteger("Input", "Enter the calories burned:")

    if not date or not exercise_type or not duration or not calories_burned:
        messagebox.showerror("Input Error", "All fields must be filled out.")
        return

    workout = Workout(date, exercise_type, duration, calories_burned)
    user.add_workout(workout)
    messagebox.showinfo("Success", "Workout added successfully!")

def view_workouts(user):
    if user.workouts:
        workouts_str = user.view_workouts()
        messagebox.showinfo("Workouts", workouts_str)
    else:
        messagebox.showinfo("No Workouts", "No workouts to display.")

def save_data(user):
    filename = simpledialog.askstring("Save", "Enter the filename to save data:")
    if not filename:
        messagebox.showerror("Input Error", "Filename cannot be empty.")
        return
    try:
        user.save_data(filename)
        messagebox.showinfo("Success", "Data saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save data: {e}")

def load_data(user):
    filename = simpledialog.askstring("Load", "Enter the filename to load data:")
    if not filename:
        messagebox.showerror("Input Error", "Filename cannot be empty.")
        return
    try:
        user.load_data(filename)
        messagebox.showinfo("Success", "Data loaded successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load data: {e}")


# Main GUI Setup with Background Image

def main_gui():
    name = simpledialog.askstring("User Info", "Enter your name:")
    age = simpledialog.askinteger("User Info", "Enter your age:")
    weight = simpledialog.askfloat("User Info", "Enter your weight:")

    if not name or not age or not weight:
        messagebox.showerror("Input Error", "All fields must be filled out.")
        return

    user = User(name, age, weight)

    # Set up the main window
    root = tk.Tk()
    root.title("💪 Personal Fitness Checker 🏋️‍♂️")
    root.geometry("500x600")  # Set a size for the window

    # Set up the background image
    # bg_image = Image.open("Personal_Fitness_Checker/fitness_background.jpg")  # Replace with your image file
    # bg_image = bg_image.resize((500, 600), Image.ANTIALIAS)  # Resize the image to fit the window
    # bg_photo = ImageTk.PhotoImage(bg_image)
    # Set up the background image
    bg_image = Image.open("Personal_Fitness_Checker/fitness_background1.jpg")  # Replace with your image file

    # Resize the image to fit the window size (500x600)
    # bg_image = bg_image.resize((500, 600), Image.ANTIALIAS)

    bg_photo = ImageTk.PhotoImage(bg_image)

    # Create a canvas to display the background image
    canvas = tk.Canvas(root, width=500, height=600)
    canvas.pack(fill="both", expand=True)

    # Add the background image to the canvas
    canvas.create_image(0, 0, anchor="nw", image=bg_photo)

    # Create a canvas to display the background image
    canvas = tk.Canvas(root, width=500, height=600)
    canvas.pack(fill="both", expand=True)
    
    # Add the background image to the canvas
    canvas.create_image(0, 0, anchor="nw", image=bg_photo)

    # Display title with larger, bold font
    label = tk.Label(root, text="I am your personal fitness checker!", font=("Helvetica", 18, "bold"), bg="#D0E8A0")
    label.place(x=60, y=20)

    # Buttons to interact with the app with emojis and custom colors
    add_btn = tk.Button(root, text="🏋️‍♂️ Add Workout 🏃‍♀️", command=lambda: add_workout(user), width=20, font=("Arial", 14), bg="#FF6F61", fg="white", relief="raised", bd=4)
    add_btn.place(x=150, y=100)

    view_btn = tk.Button(root, text="👀 View Workouts 📊", command=lambda: view_workouts(user), width=20, font=("Arial", 14), bg="#4CAF50", fg="white", relief="raised", bd=4)
    view_btn.place(x=150, y=150)

    save_btn = tk.Button(root, text="💾 Save Data 💾", command=lambda: save_data(user), width=20, font=("Arial", 14), bg="#2196F3", fg="white", relief="raised", bd=4)
    save_btn.place(x=150, y=200)

    load_btn = tk.Button(root, text="📂 Load Data 📂", command=lambda: load_data(user), width=20, font=("Arial", 14), bg="#FF9800", fg="white", relief="raised", bd=4)
    load_btn.place(x=150, y=250)

    # Exit button with a different color
    exit_btn = tk.Button(root, text="❌ Exit ❌", command=root.quit, width=20, font=("Arial", 14), bg="#F44336", fg="white", relief="raised", bd=4)
    exit_btn.place(x=150, y=300)

    # Run the GUI
    root.mainloop()


if __name__ == "__main__":

    main_gui()

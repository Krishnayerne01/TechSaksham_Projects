import cv2
import face_recognition
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Sample Encoded Faces Database (For Demo)
known_faces = {
    "John Doe": face_recognition.face_encodings(face_recognition.load_image_file("john.jpg"))[0],
    "Alice Smith": face_recognition.face_encodings(face_recognition.load_image_file("alice.jpg"))[0]
}

attendance_log = {}

# Attendance Marking Function
def mark_attendance(name):
    if name not in attendance_log:
        attendance_log[name] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        messagebox.showinfo("✅ Attendance Marked", f"📝 {name}'s attendance recorded at {attendance_log[name]}")
    else:
        messagebox.showinfo("⚠️ Already Marked", f"⏳ {name} has already marked attendance!")

# Function to Start Face Recognition
def start_recognition():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(list(known_faces.values()), face_encoding)
            name = "Unknown"

            if True in matches:
                matched_index = matches.index(True)
                name = list(known_faces.keys())[matched_index]

            mark_attendance(name)

        cv2.imshow("📷 Face Recognition Attendance", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Tkinter UI
class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📸 Face Recognition Attendance")
        self.root.geometry("500x600")
        self.root.configure(bg="#1E1E2E")  # Dark Theme

        tk.Label(self.root, text="🎓 Smart Attendance System", font=("Helvetica", 20, "bold"), fg="#00FFD1", bg="#1E1E2E").pack(pady=20)
        tk.Label(self.root, text="🚀 Click below to start recognition!", font=("Arial", 14), fg="white", bg="#1E1E2E").pack(pady=5)

        self.create_button("📷 Start Attendance", start_recognition, "#00FFD1", "#00CCAA")
        self.create_button("📜 View Attendance Log", self.view_attendance, "#FFA500", "#CC8400")
        self.create_button("❌ Exit", root.quit, "#FF3B3B", "#CC2D2D")

    def create_button(self, text, command, color, hover_color):
        def on_enter(e):
            btn["background"] = hover_color

        def on_leave(e):
            btn["background"] = color

        btn = tk.Button(self.root, text=text, font=("Arial", 14, "bold"), bg=color, fg="white", activebackground=hover_color, padx=10, pady=5, relief="flat", command=command)
        btn.pack(pady=10, ipadx=5, ipady=3, fill="x")

        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    def view_attendance(self):
        log_text = "\n".join([f"{name}: {time}" for name, time in attendance_log.items()])
        messagebox.showinfo("📜 Attendance Log", log_text if log_text else "No attendance recorded yet!")

# Running the App
if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()

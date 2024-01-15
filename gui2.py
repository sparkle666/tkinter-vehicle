import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk


class WebcamApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.window.geometry("600x450")  # Set your preferred window size

        # Use default camera (change if you have multiple cameras)
        self.video_source = 0
        self.vid = cv2.VideoCapture(self.video_source)

        self.style = ttk.Style()
        # You can experiment with other available themes
        self.style.theme_use("clam")

        # Configure the style for dark mode
        self.style.configure("TButton", padding=6, relief="flat",
                             background="#2E2E2E", foreground="#FFFFFF")
        self.style.configure("TFrame", background="#2E2E2E")
        self.style.configure(
            "TLabel", background="#2E2E2E", foreground="#FFFFFF")
        self.style.configure("TCanvas", background="#2E2E2E")

        self.canvas = tk.Canvas(window, width=self.vid.get(
            cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT), bg="#2E2E2E")
        self.canvas.pack()

        self.btn_start = ttk.Button(
            window, text="Start", command=self.start_video)
        self.btn_start.pack(pady=10)

        self.btn_stop = ttk.Button(
            window, text="Stop", command=self.stop_video)
        self.btn_stop.pack(pady=10)
        self.btn_stop["state"] = "disabled"

        self.window.mainloop()

    def start_video(self):
        self.btn_start["state"] = "disabled"
        self.btn_stop["state"] = "normal"

        if not self.vid.isOpened():
            self.vid = cv2.VideoCapture(self.video_source)

        self.update()

    def stop_video(self):
        self.btn_start["state"] = "normal"
        self.btn_stop["state"] = "disabled"

        if self.vid.isOpened():
            self.vid.release()

    def update(self):
        ret, frame = self.vid.read()

        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(
                cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        if self.btn_start["state"] == "disabled":
            self.window.after(10, self.update)


if __name__ == "__main__":
    root = tk.Tk()
    app = WebcamApp(root, "Webcam App")

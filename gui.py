import tkinter as tk
from tkinter import ttk
import cv2
from PIL import Image, ImageTk
import torch


class WebcamApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.window.geometry("800x600")

        self.video_source = 0
        self.vid = cv2.VideoCapture(self.video_source)

        self.style = ttk.Style()
        self.style.theme_use("clam")

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
            window, text="Start", command=self.start_detection)
        self.btn_start.pack(pady=10)

        self.btn_stop = ttk.Button(
            window, text="Stop", command=self.stop_video)
        self.btn_stop.pack(pady=10)
        self.btn_stop["state"] = "disabled"

        self.detecting = False
        self.car_detected = False

        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu")
        self.model = torch.hub.load(
            'ultralytics/yolov5:v5.0', 'yolov5s', pretrained=True).to(self.device).eval()

        self.window.mainloop()

    def start_detection(self):
        self.btn_start["state"] = "disabled"
        self.btn_stop["state"] = "normal"

        if not self.vid.isOpened():
            self.vid = cv2.VideoCapture(self.video_source)

        self.detecting = True
        self.update()

    def stop_video(self):
        self.btn_start["state"] = "normal"
        self.btn_stop["state"] = "disabled"

        self.detecting = False
        if self.vid.isOpened():
            self.vid.release()

    def update(self):
        ret, frame = self.vid.read()

        if ret:
            if self.detecting:
                results = self.model(frame)
                cars = results.xyxy[results.names.index('car')]

                if len(cars) > 0 and not self.car_detected:
                    # Save the frame when the first car is detected
                    cv2.imwrite("car_detection.jpg", frame)
                    self.car_detected = True

                # Display the results on the canvas
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
                self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        if self.detecting:
            self.window.after(10, self.update)


if __name__ == "__main__":
    root = tk.Tk()
    app = WebcamApp(root, "Webcam App")

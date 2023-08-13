import sys
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QComboBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from PIL import Image


def detect_cameras(max_cameras=10):
    """Detect available camera indices."""
    available_cameras = []
    for i in range(max_cameras):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.read()[0]:
            available_cameras.append(i)
        cap.release()
    return available_cameras


class WebcamApp(QWidget):
    def __init__(self):
        super().__init__()

        # UI components
        self.camera_selector = QComboBox(self)
        self.camera_selector.addItems([str(cam) for cam in detect_cameras()])
        self.camera_selector.currentIndexChanged.connect(self.update_camera)

        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_stream)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop_stream)

        self.label = QLabel(self)

        layout = QVBoxLayout(self)
        layout.addWidget(self.camera_selector)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.label)

        self.setWindowTitle("Simple Webcam Streamer")
        self.resize(800, 600)  # width: 800, height: 600

        self.setLayout(layout)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.display_frame)
        self.video_source = 0
        self.cap = cv2.VideoCapture(self.video_source, cv2.CAP_DSHOW)

    def update_camera(self):
        self.video_source = int(self.camera_selector.currentText())
        self.cap.release()
        self.cap = cv2.VideoCapture(self.video_source, cv2.CAP_DSHOW)

    def start_stream(self):
        self.timer.start(30)

    def stop_stream(self):
        self.timer.stop()

    def display_frame(self):
        ret, frame = self.cap.read()
        if ret:
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            p = convert_to_Qt_format.scaled(640, 480, aspectRatioMode=1)
            self.label.setPixmap(QPixmap.fromImage(p))


app = QApplication(sys.argv)
window = WebcamApp()
window.show()
sys.exit(app.exec_())

from PyQt5.QtWidgets import QGraphicsLineItem, QInputDialog
from PyQt5.QtCore import QObject, Qt, QPointF
from PyQt5.QtGui import QPen

class ScaleCalibrator(QObject):
    def __init__(self, view, scene, callback):
        super().__init__()
        self.view = view
        self.scene = scene
        self.callback = callback
        self.active = False
        self.start_point = None
        self.temp_line = None
        self.view.viewport().installEventFilter(self)

    def start_calibration(self):
        print("[CALIBRATION] Scale calibration started.")
        self.active = True
        self.start_point = None
        if self.temp_line:
            self.scene.removeItem(self.temp_line)
            self.temp_line = None

    def eventFilter(self, obj, event):
        if not self.active:
            return False

        if event.type() == event.MouseButtonPress and event.button() == Qt.LeftButton:
            scene_pos = self.view.mapToScene(event.pos())
            if self.start_point is None:
                self.start_point = scene_pos
                print(f"[CALIBRATION] Start point: {scene_pos}")
            else:
                end_point = scene_pos
                print(f"[CALIBRATION] End point: {end_point}")
                self.draw_line(self.start_point, end_point)
                self.finish_calibration(self.start_point, end_point)
                self.active = False
            return True
        return False

    def draw_line(self, start, end):
        if self.temp_line:
            self.scene.removeItem(self.temp_line)
        pen = QPen(Qt.green, 2, Qt.DashLine)
        self.temp_line = QGraphicsLineItem(start.x(), start.y(), end.x(), end.y())
        self.temp_line.setPen(pen)
        self.scene.addItem(self.temp_line)

    def finish_calibration(self, start, end):
        pixel_distance = (end - start).manhattanLength()
        print(f"[CALIBRATION] Pixel distance: {pixel_distance:.2f}")
        feet, ok = QInputDialog.getDouble(self.view, "Enter Real Distance", "Enter real-world distance (in feet):", decimals=4)
        if ok and pixel_distance > 0:
            feet_per_pixel = feet / pixel_distance
            print(f"[CALIBRATION] {feet:.2f} feet over {pixel_distance:.2f} pixels = {feet_per_pixel:.4f} feet/pixel")
            self.callback(feet_per_pixel)
        else:
            print("[CALIBRATION] Calibration canceled or invalid distance.")

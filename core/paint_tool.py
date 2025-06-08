from PyQt5.QtWidgets import QGraphicsPathItem
from PyQt5.QtGui import QPainterPath, QPen
from PyQt5.QtCore import Qt

class PaintTool:
    def __init__(self, scene, scale_callback):
        self.scene = scene
        self.scale_callback = scale_callback
        self.active_label = None
        self.current_path = None
        self.points = []
        self.paths = []
        self.brush_width = 8  # Default width in feet

    def set_label(self, label):
        self.active_label = label
        print(f"[PAINT] Mode set to: {label}")

    def set_brush_width(self, width):
        self.brush_width = width
        print(f"[PAINT] Brush width set to: {width} ft")

    def add_point(self, point, scale):
        if not self.active_label:
            return

        if not self.current_path:
            print(f"[PAINT] Started new path: {self.active_label}")
            self.current_path = QPainterPath(point)
            self.points = [point]
        else:
            self.current_path.lineTo(point)
            self.points.append(point)

        pen = QPen(self.get_color(self.active_label))
        pen.setWidthF(self.brush_width / scale)

        path_item = QGraphicsPathItem(self.current_path)
        path_item.setPen(pen)

        if hasattr(self, "temp_path_item"):
            try:
                self.scene.removeItem(self.temp_path_item)
            except RuntimeError:
              print("[WARN] Attempted to remove already-deleted path item.")
            self.temp_path_item = None


        self.scene.addItem(path_item)
        self.temp_path_item = path_item
        print(f"[PAINT] Adding point: {point}")

    def finish(self):
        if len(self.points) < 2:
            print("[PAINT] Invalid or incomplete path, removing.")
            if hasattr(self, "temp_path_item"):
                self.scene.removeItem(self.temp_path_item)
            self.current_path = None
            self.points = []
            return None

        total_length = sum(
            (self.points[i] - self.points[i - 1]).manhattanLength()
            for i in range(1, len(self.points))
        )

        scale = self.scale_callback()
        label = self.active_label
        path_item = self.temp_path_item
        width = self.brush_width

        self.paths.append({
            "item": path_item,
            "label": label,
            "width": width,
            "length": total_length * scale
        })

        self.current_path = None
        self.points = []
        del self.temp_path_item

        return {
            "label": label,
            "length": total_length * scale
        }

    def get_color(self, label):
        colors = {
            "Gravel Driveway": Qt.gray,
            "Water Line": Qt.blue,
            "Power Line": Qt.yellow,
            "Fence": Qt.black,
            "Eraser": Qt.transparent,
            "Fluorescent Red": Qt.red,
            "Fluorescent Green": Qt.green,
            "Fluorescent Yellow": Qt.yellow,
            "Fluorescent Blue": Qt.cyan,
            "Fluorescent Orange": Qt.darkYellow,
            "Fluorescent Purple": Qt.magenta
        }
        return colors.get(label, Qt.darkGray)

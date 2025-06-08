import os
from PyQt5.QtWidgets import (
    QMainWindow, QAction, QFileDialog, QMessageBox,
    QGraphicsScene, QGraphicsView, QGraphicsPixmapItem,
    QLabel, QToolBar, QPushButton, QVBoxLayout, QWidget,
    QComboBox, QInputDialog
)
from PyQt5.QtGui import QPixmap, QPainter
from PyQt5.QtCore import Qt, QRectF

from core.prefab_item import PrefabItem
from core.paint_tool import PaintTool
from core.project_serializer import save_project, load_project
from core.scale_calibrator import ScaleCalibrator


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Property Planner")
        self.canvas_scene = QGraphicsScene(self)
        self.canvas_view = QGraphicsView(self.canvas_scene)
        self.canvas_view.setRenderHint(QPainter.Antialiasing)
        self.setCentralWidget(QWidget())
        self.image_path = None
        self.scale_feet_per_pixel = 1.0
        self.paint_tool = PaintTool(self.canvas_scene, self.get_current_scale)
        self.scale_calibrator = ScaleCalibrator(self.canvas_view, self.canvas_scene, self.set_scale)

        self.init_menu()
        self.init_toolbar()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()
        layout.addWidget(self.canvas_view)
        self.centralWidget().setLayout(layout)
        self.statusBar().showMessage("Welcome To Property Planner")

    def init_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("File")
        open_action = QAction("Open Image", self)
        save_action = QAction("Save Project", self)
        load_action = QAction("Load Project", self)
        exit_action = QAction("Exit", self)

        open_action.triggered.connect(self.load_image)
        save_action.triggered.connect(self.save_project)
        load_action.triggered.connect(self.load_project)
        exit_action.triggered.connect(self.close)

        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addAction(load_action)
        file_menu.addAction(exit_action)

    def init_toolbar(self):
        toolbar = QToolBar("Main Toolbar")
        self.addToolBar(toolbar)

        prefab_buttons = [
            ("Container 40'", 40, 8),
            ("Pickup Truck", 18, 6.5),
            ("Solar Panel", 4, 2),
            ("Planter Box", 6, 2)
        ]
        for label, width, height in prefab_buttons:
            btn = QPushButton(label)
            btn.clicked.connect(lambda _, w=width, h=height, l=label: self.place_prefab(w, h, l))
            toolbar.addWidget(btn)

        self.paint_dropdown = QComboBox()
        self.paint_dropdown.addItem("Select Paint Tool")
        self.paint_dropdown.addItems([
             "Gravel Driveway", "Water Line", "Power Line", "Fence",
             "Fluorescent Red", "Fluorescent Green", "Fluorescent Yellow",
             "Fluorescent Blue", "Fluorescent Orange", "Fluorescent Purple",
            "Eraser"
        ])
        self.paint_dropdown.currentTextChanged.connect(self.set_paint_mode)
        toolbar.addWidget(self.paint_dropdown)


        self.width_dropdown = QComboBox()
        for width in range(2, 22, 2):
            self.width_dropdown.addItem(f"{width}'", width)
        self.width_dropdown.currentIndexChanged.connect(self.set_brush_width)
        self.width_dropdown.setCurrentIndex(3)
        toolbar.addWidget(self.width_dropdown)

        calibrate_btn = QPushButton("Calibrate Scale")
        calibrate_btn.clicked.connect(self.start_calibration)
        toolbar.addWidget(calibrate_btn)

    def place_prefab(self, width_ft, height_ft, label):
        scale = self.get_current_scale()
        if scale <= 0:
            QMessageBox.warning(self, "Scale Error", "Please calibrate the scale before placing objects.")
            return

        width_px = width_ft / scale
        height_px = height_ft / scale

        item = PrefabItem(width_px, height_px, label)
        item.setPos(0, 0)
        self.canvas_scene.addItem(item)


    def set_paint_mode(self, text):
        label = text if text != "Select Paint Tool" else None
        self.paint_tool.set_label(label)

    def set_brush_width(self):
        value = self.width_dropdown.currentData()
        self.paint_tool.set_brush_width(value)

    def load_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Terrain Image", "", "Images (*.png *.jpg *.bmp)")
        if path:
            self.image_path = path
            pixmap = QPixmap(path)
            self.canvas_scene.clear()
            item = QGraphicsPixmapItem(pixmap)
            item.setZValue(-10)
            self.canvas_scene.addItem(item)
            self.canvas_scene.setSceneRect(QRectF(pixmap.rect()))
            self.scale_calibrator.start_calibration()

    def start_calibration(self):
        self.scale_calibrator.start_calibration()

    def set_scale(self, feet_per_pixel):
        self.scale_feet_per_pixel = feet_per_pixel
        print(f"[SCALE] 1 pixel = {feet_per_pixel:.4f} feet")

    def get_current_scale(self):
        return getattr(self, "scale_feet_per_pixel", 1.0)

    def save_project(self):
        path, _ = QFileDialog.getSaveFileName(self, "Save Project", "", "Property Project (*.pproj)")
        if path:
            try:
                save_project(self.canvas_scene, self.image_path, self.get_current_scale(), path)
                QMessageBox.information(self, "Saved", "Project saved successfully.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Failed to save project:\n{e}")

    def load_project(self):
        path, _ = QFileDialog.getOpenFileName(self, "Load Project", "", "Property Project (*.pproj)")
        if path:
            self.image_path, scale = load_project(self.canvas_scene, path)
            self.set_scale(scale)

    def mousePressEvent(self, event):
        if self.paint_tool.active_label:
            if event.button() == Qt.LeftButton:
                scene_pos = self.canvas_view.mapToScene(event.pos())
                self.paint_tool.add_point(scene_pos, self.get_current_scale())
            elif event.button() == Qt.RightButton:
                info = self.paint_tool.finish()
                if info:
                    self.statusBar().showMessage(f"{info['label']} added {info['length']:.1f}ft")
            return
        if event.button() == Qt.RightButton:
            item = self.canvas_view.itemAt(event.pos())
            if item and isinstance(item, PrefabItem) and item.isSelected():
                item.setRotation(item.rotation() + 15)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            for item in self.canvas_scene.selectedItems():
                self.canvas_scene.removeItem(item)
            print("[DELETE] Selected item(s) removed.")
        elif event.key() == Qt.Key_R:
              for item in self.canvas_scene.selectedItems():
                if isinstance(item, PrefabItem):
                    item.setRotation(item.rotation() + 15)
                    print(f"[ROTATE] Rotated item to {item.rotation()}°")

    def wheelEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            factor = 1.2 if event.angleDelta().y() > 0 else 0.8
            self.canvas_view.scale(factor, factor)

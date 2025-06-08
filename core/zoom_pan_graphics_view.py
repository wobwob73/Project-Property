from PyQt5.QtWidgets import QGraphicsView
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QWheelEvent, QMouseEvent


class ZoomPanGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragMode(QGraphicsView.NoDrag)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        self._panning = False
        self._pan_start = QPointF()

    def wheelEvent(self, event: QWheelEvent):
        if not (event.modifiers() & Qt.ControlModifier):
            return  # Only zoom if Ctrl is held
        zoom_in_factor = 1.15
        zoom_out_factor = 1 / zoom_in_factor
        zoom_factor = zoom_in_factor if event.angleDelta().y() > 0 else zoom_out_factor
        self.scale(zoom_factor, zoom_factor)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.RightButton:
            self._panning = True
            self.setCursor(Qt.ClosedHandCursor)
            self._pan_start = event.pos()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self._panning:
            delta = self.mapToScene(event.pos()) - self.mapToScene(self._pan_start)
            self._pan_start = event.pos()
            self.translate(-delta.x(), -delta.y())
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.RightButton:
            self._panning = False
            self.setCursor(Qt.ArrowCursor)
        else:
            super().mouseReleaseEvent(event)

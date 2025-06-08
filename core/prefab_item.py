from PyQt5.QtWidgets import QGraphicsRectItem
from PyQt5.QtGui import QBrush, QPen, QColor
from PyQt5.QtCore import Qt

class PrefabItem(QGraphicsRectItem):
    def __init__(self, width, height, label):
        super().__init__(0, 0, width, height)
        self.setBrush(QBrush(QColor(200, 200, 255, 120)))
        self.setPen(QPen(Qt.black, 1))
        self.setFlags(
            QGraphicsRectItem.ItemIsSelectable |
            QGraphicsRectItem.ItemIsMovable |
            QGraphicsRectItem.ItemSendsScenePositionChanges
        )
        self.setData(0, label)

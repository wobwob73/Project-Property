import json
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsPathItem
from PyQt5.QtGui import QPixmap, QPen, QPainterPath, QColor
from PyQt5.QtCore import QRectF, QPointF
from core.prefab_item import PrefabItem

def save_project(scene, image_path, scale, file_path):
    data = {
        "image_path": image_path,
        "scale": scale,
        "prefabs": [],
        "paths": []
    }

    for item in scene.items():
        if isinstance(item, PrefabItem):
            rect = item.rect()
            data["prefabs"].append({
                "label": item.data(0),
                "width": rect.width(),
                "height": rect.height(),
                "x": item.pos().x(),
                "y": item.pos().y(),
                "rotation": item.rotation()
            })
        elif isinstance(item, QGraphicsPathItem):
            path = item.path()
            points = []
            for i in range(1, path.elementCount()):
                pt = path.elementAt(i)
                points.append([pt.x, pt.y])
            data["paths"].append({
                "label": item.data(0) or "Unnamed",
                "color": item.pen().color().name(),
                "points": points
            })

    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def load_project(scene, file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)

    scene.clear()

    image_path = data.get("image_path")
    if image_path:
        pix = QPixmap(image_path)
        image_item = QGraphicsPixmapItem(pix)
        image_item.setZValue(-10)
        scene.addItem(image_item)
        scene.setSceneRect(QRectF(pix.rect()))

    for prefab in data.get("prefabs", []):
        item = PrefabItem(prefab["width"], prefab["height"], prefab["label"])
        item.setPos(prefab["x"], prefab["y"])
        item.setRotation(prefab.get("rotation", 0))
        scene.addItem(item)

    for path_data in data.get("paths", []):
        path = QPainterPath()
        pts = path_data["points"]
        if pts:
            path.moveTo(QPointF(*pts[0]))
            for pt in pts[1:]:
                path.lineTo(QPointF(*pt))
            path_item = QGraphicsPathItem(path)
            color = QColor(path_data.get("color", "#000000"))
            path_item.setPen(QPen(color, 3))
            path_item.setData(0, path_data.get("label"))
            scene.addItem(path_item)

    return image_path, data.get("scale", 1.0)

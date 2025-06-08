from PyQt5.QtWidgets import QApplication, QLabel
import sys

app = QApplication(sys.argv)
label = QLabel("If you can see this, PyQt is working")
label.resize(400, 100)
label.setStyleSheet("background-color: green; color: white; font-size: 18px;")
label.show()
sys.exit(app.exec_())

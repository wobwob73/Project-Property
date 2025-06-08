# 🏡 Property Planner

**Property Planner** is a lightweight, interactive tool for visualizing and planning infrastructure layouts over terrain or satellite imagery. It allows users to:

- 🏗️ Drag and place prefab objects (e.g., containers, trucks, solar panels)
- 🖌️ Paint lines for driveways, fences, water lines, electrical, and utility paths
- 📐 Calibrate image scale for real-world accuracy
- 💾 Save and load planning sessions
- 📸 Export the plan as an image

---

## 📦 Features

- Prefab item placement (40' container, truck, solar panel, planter box)
- Paint tool with adjustable width and customizable labels (e.g., driveway, water line)
- Eraser for selective segment deletion
- Scale calibration with real-world measurement entry
- Zooming and panning
- Save/load `.pproj` project files
- Export plan to image

---

## 🚀 Getting Started

### Requirements

- Python 3.8+
- PyQt5

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/property-planner.git
   cd property-planner

    Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Launch the application:

./launch.sh

If on Windows:

    python main.py

🛠 Usage Basics
🖼️ Load an Image

    Go to File > Open Image

    Load a terrain or satellite image to begin planning

📏 Calibrate Scale

    Click Calibrate Scale

    Left-click once to start a scale line, again to end

    Enter the real-world distance (in feet) when prompted

🧱 Add Prefab Items

    Use toolbar buttons to add 40' Containers, Trucks, etc.

    Click and drag to position them

    Press R to rotate

    Press Delete to remove

🎨 Use Paint Tool

    Choose a line type from the dropdown (e.g., Driveway, Water Line)

    Adjust line width using the width dropdown

    Left-click to add points

    Right-click to finish a path

🧽 Erase Lines

    Choose Eraser from paint tool

    Click a line segment to select it

    Press Delete to remove just that segment

💾 Save / Load

    Use File > Save Project to save your session as a .pproj

    Load later via File > Load Project

📷 Export Image

    Use File > Export as Image (coming soon)

⚙️ Extending the Tool

Adding new prefab items or paint types is simple:
➕ Add a New Prefab Button

In main_window.py, add to the prefab list:

("New Shed", 12, 10)

🎨 Add a New Paint Type

In main_window.py, extend the dropdown:

self.paint_dropdown.addItems(["Gravel Driveway", "Water Line", ..., "Fiber Optic Line"])

And in paint_tool.py, assign it a color in get_color():

"Fiber Optic Line": QColor("magenta"),

🧱 Directory Structure

PropertyPlanner/
├── core/
│   ├── paint_tool.py
│   ├── prefab_item.py
│   ├── project_serializer.py
│   └── scale_calibrator.py
├── ui/
│   └── main_window.py
├── zoom_pan_graphics_view.py
├── main.py
├── launch.sh
└── requirements.txt

🙌 Credits

Developed by [Your Name]. Contributions, suggestions, and pull requests are welcome!
📜 License

MIT License


---

Let me know if you'd like to include screenshots, GIFs, or badges — I can help generate those or format them for GitHub!

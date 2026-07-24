# AI3DScanner
AI3DScanner

AI3DScanner is a desktop application for reconstructing textured 3D models from multiple photographs.

## Goals

- Import photos
- Reconstruct a 3D model
- Preview the model
- Export OBJ, GLB, and STL

## Planned Tech Stack

- Python
- OpenCV
- Open3D
- PySide6
- COLMAP
- OpenMVS

## Project Structure

See the `/docs` directory for architecture documentation.

## Status

🚧 Early development (Day 1)

Day 2

We'll build a professional desktop application with this layout

+--------------------------------------------------------------+
| File  Edit  View  Help                                       |
+--------------------------------------------------------------+
| Toolbar                                                      |
+--------------------------------------------------------------+
| Projects |              3D Viewport              | Properties |
|          |                                       |            |
|----------|---------------------------------------|------------|
| Console / Logs                                               |
+--------------------------------------------------------------+
| Status Bar                                                   |
+--------------------------------------------------------------+

🎯 Day 2 Goals

By the end of today, we'll have:

✅ Professional PySide6 application
✅ Main Window
✅ Menu Bar
✅ Toolbar
✅ Status Bar
✅ Logging System
✅ Settings Manager
✅ Clean startup architecture

Step 1 — Update Folder Structure

Your project should now look like:

AI3DScanner/
│
├── app/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── application.py
│   │   ├── constants.py
│   │   ├── logger.py
│   │   ├── settings.py
│   │   └── theme.py
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   ├── menu_bar.py
│   │   ├── tool_bar.py
│   │   ├── status_bar.py
│   │   ├── dock_manager.py
│   │   ├── widgets/
│   │   ├── dialogs/
│   │   ├── icons/
│   │   └── styles/
│   │
│   ├── reconstruction/
│   ├── vision/
│   ├── exporters/
│   ├── models/
│   ├── services/
│   ├── utils/
│   └── resources/
│
├── run.py
└── ...

Step 2 — Add __init__.py

Inside:
app/
app/core/
app/ui/

Create:
\__init__.py

They can stay empty.

This tells Python these are packages.

Step 3 — We'll Build in This Order
run.py
      │
      ▼
application.py
      │
      ▼
MainWindow
      │
 ┌────┼─────┐
 │    │     │
 ▼    ▼     ▼
Menu Toolbar StatusBar
Everything starts from run.py

Step 4 — Before We Write Code
I want to slightly improve our architecture.

Instead of:
run.py
calling
app/main.py

I'd rather have:
run.py
      │
      ▼
Application
      │
      ▼
MainWindow
No unnecessary middle layer.

Much cleaner.

Final Architecture

run.py
    │
    ▼
Application
    │
    ▼
MainWindow
    │
    ▼
Menus
Toolbar
StatusBar

This is closer to how professional Qt applications are organized.
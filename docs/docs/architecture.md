# AI3DScanner Architecture

**Project:** AI3DScanner

**Version:** 0.1.0

**Author:** Mihir & ChatGPT

---

# Vision

AI3DScanner is a professional desktop application that reconstructs high-quality textured 3D models from multiple photographs.

The software is designed to be modular, scalable, and maintainable.

---

# Development Principles

- Clean Architecture
- Modular Design
- SOLID Principles
- Object-Oriented Programming
- Separation of Concerns
- Small reusable modules
- Git commit after every completed feature

---

# High Level Architecture

```
                  User
                    │
                    ▼
          Desktop UI (PySide6)
                    │
                    ▼
           Application Controller
                    │
      ┌─────────────┼─────────────┐
      │             │             │
      ▼             ▼             ▼
 Vision Engine  Reconstruction  Export Engine
   (OpenCV)      (COLMAP/MVS)   (OBJ/STL/GLB)
      │             │             │
      └─────────────┼─────────────┘
                    ▼
              Project Manager
                    ▼
               Project Files
```

---

# Repository Structure

```
AI3DScanner/

app/
assets/
config/
docs/
examples/
outputs/
projects/
tests/
tools/

README.md
LICENSE
requirements.txt
run.py
```

---

# app/

Contains the application source code.

---

# app/core/

Responsible for application startup and global services.

Files

application.py

Creates the QApplication and starts the program.

settings.py

Loads and saves application settings.

logger.py

Application logging.

constants.py

Global constants.

theme.py

Application theme.

future

dependency_container.py

---

# app/ui/

Everything related to the graphical interface.

main_window.py

Main application window.

menu_bar.py

Application menus.

tool_bar.py

Toolbar buttons.

status_bar.py

Bottom status bar.

dock_manager.py

Dockable panels.

widgets/

Custom widgets.

dialogs/

Popup windows.

styles/

QSS theme files.

icons/

Application icons.

---

# app/vision/

Computer vision algorithms.

Image loading

Image enhancement

Feature detection

Camera calibration

Background removal

Image validation

Libraries

OpenCV

NumPy

---

# app/reconstruction/

3D reconstruction pipeline.

Sparse Point Cloud

Dense Point Cloud

Mesh Generation

Texture Mapping

Future AI Reconstruction

Libraries

COLMAP

OpenMVS

Open3D

---

# app/exporters/

Export generated models.

OBJ

GLTF

GLB

STL

PLY

FBX (future)

---

# app/models/

Application data models.

Project

Camera

Image

Mesh

PointCloud

Settings

---

# app/services/

Business logic.

Project Manager

File Manager

Task Manager

Import Service

Export Service

---

# app/utils/

Helper functions.

Math

Files

Images

Validation

Common utilities

---

# app/resources/

Application resources.

Fonts

Icons

Stylesheets

Translations

---

# assets/

Demo assets used during development.

---

# config/

Application configuration.

---

# docs/

Documentation.

Architecture

Roadmap

API

Developer Notes

---

# examples/

Example image datasets.

---

# outputs/

Generated models.

Ignored by Git.

---

# projects/

Saved user projects.

Ignored by Git.

---

# tests/

Unit tests.

Integration tests.

Performance tests.

---

# tools/

Developer helper scripts.

---

# Development Roadmap

Phase 1

Project Foundation

GUI

Logging

Settings

Project System

Phase 2

Image Processing

OpenCV

Feature Detection

Calibration

Phase 3

Photogrammetry

COLMAP

OpenMVS

Open3D

Phase 4

3D Viewer

Mesh

Textures

Navigation

Phase 5

Export

OBJ

GLB

STL

Phase 6

AI

Object Detection

Background Removal

Single Image Reconstruction

NeRF

Gaussian Splatting

---

# Git Strategy

main

Stable production branch.

feature/*

Feature development.

Commit format

feat:

fix:

refactor:

docs:

test:

chore:

---

# Coding Style

Python 3.12

PEP8

Type Hints

Docstrings

Meaningful variable names

No duplicate code

Every module should have a single responsibility.

---

# End
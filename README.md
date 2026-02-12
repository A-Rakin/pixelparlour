#!/bin/bash

# PixelParlour - README.md Generator
# Run this script to create a professional README for your Flask Gallery App

cat > README.md << 'EOF'
# 📸 PixelParlour

<div align="center">
![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.8+-yellow)
![Flask](https://img.shields.io/badge/flask-2.0+-black)
</div>
<br>

<p align="center">
  <b>A beautiful, feature-rich photo gallery web application built with Flask</b><br>
  Upload, manage, and share your memories with titles, captions, and automatic thumbnail generation.
</p>

---

## ✨ Features

<div align="center">
  
  | 🖼️ | 📝 | 🗑️ | ⚡ |
  |---|---|---|---|
  | **Image Upload** | **Titles & Captions** | **Delete Photos** | **Thumbnails** |
  | Drag & drop support | Add descriptions | Secure deletion | Auto-generated |
  | Multiple formats | Rich text | With confirmation | Optimized sizes |

</div>

### ✅ Complete Feature List

- **📤 Image Upload** - Support for JPG, PNG, GIF formats (up to 16MB)
- **📝 Metadata** - Add custom titles and captions to every photo
- **🖼️ Grid Layout** - Responsive gallery with CSS Grid
- **🗑️ Delete Functionality** - Remove your photos with confirmation dialog
- **⚡ Thumbnail Generation** - Automatic image resizing using Pillow
- **🔍 Photo Details** - View individual photos with full metadata
- **👁️ View Counter** - Track how many times each photo is viewed
- **📱 Responsive Design** - Works perfectly on desktop, tablet, and mobile
- **🎨 Modern UI** - Clean, gradient-based design with smooth animations
- **📄 Pagination** - Browse large galleries efficiently
- **🔒 Security** - CSRF protection, secure filename handling, SQL injection prevention

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation in 30 Seconds

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/pixelparlour.git
cd pixelparlour

# 2. Create virtual environment
```bash
python -m venv venv
```
# 3. Activate virtual environment
# On Windows:
```bash
venv\Scripts\activate
```
# On macOS/Linux:
```bash
source venv/bin/activate
```
# 4. Install dependencies
``bash
pip install -r requirements.txt
```
# 5. Run the application
``bash
python run.py
```
<img width="1347" height="673" alt="image" src="https://github.com/user-attachments/assets/016eefcb-a7ab-4c54-a2fe-c464e7a2144c" />

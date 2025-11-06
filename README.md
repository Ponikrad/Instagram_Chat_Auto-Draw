# 🎨 InstaDraw

> Transform any image into an automated drawing with AI-powered path detection and mouse automation

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![OpenCV](https://img.shields.io/badge/opencv-4.0+-green.svg)](https://opencv.org/)

InstaDraw is a Python automation tool that converts images into vector paths and reproduces them using simulated mouse movements. Perfect for digital art, presentations, or just having fun with automated drawing!


## ✨ Features

- 🖼️ **Smart Edge Detection** - Automatically detects and extracts contours from any image
- 📐 **Path Simplification** - Uses Ramer-Douglas-Peucker algorithm to create smooth, efficient paths
- 🎯 **Precision Calibration** - Click-to-define canvas boundaries for pixel-perfect placement
- ⚡ **Adjustable Speed** - Control drawing speed and detail level
- 🛡️ **Failsafe Protection** - Emergency stop by moving mouse to screen corners

## 📋 Table of Contents

- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Configuration](#configuration)
- [How It Works](#how-it-works)
- [Examples](#examples)
- [Tips & Best Practices](#tips--best-practices)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Install Dependencies

```bash
# Install required packages
pip install opencv-python numpy pyautogui
```

## ⚡ Quick Start

1. **Prepare your canvas** - Open emulator with Instagram (BlueStacks etc.)

2. **Run with calibration**:
```bash
python insta_draw.py --image your_image.jpg --calibrate --speed your speed (default 0.0005) --simplify your precision (default 4.5)
```

3. **Define canvas area** - Click upper-left and lower-right corners when prompted

4. **Watch the magic happen!** ✨

## 📖 Usage

### Basic Command

```bash
python insta_draw.py --image <path_to_image>
```

### Full Command with Options

```bash
python insta_draw.py --image portrait.jpg --speed 0.005 --simplify 4.5 --calibrate
```

### Command-Line Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--image` | string | *required* | Path to the input image file |
| `--speed` | float | `0.005` | Duration (seconds) to move between points |
| `--simplify` | float | `4.5` | Path simplification epsilon (higher = simpler) |
| `--calibrate` | flag | `False` | Enable manual canvas calibration mode |

## ⚙️ Configuration

### Speed Settings

- **Fast Drawing** (`--speed 0.001`): Quick but may be jittery
- **Normal** (`--speed 0.003`): Balanced speed and smoothness (default)
- **Smooth** (`--speed 0.005`): Slower but very smooth lines
- **Precise** (`--speed 0.01`): Very slow, maximum precision

### Simplification Levels

- **High Detail** (`--simplify 1.0`): Maximum points, complex drawings
- **Balanced** (`--simplify 2.5`): Good detail with efficiency (default)
- **Simple** (`--simplify 5.0`): Fewer points, cleaner lines
- **Minimal** (`--simplify 10.0`): Very few points, abstract style

## 🔧 How It Works

```
Input Image → Edge Detection → Contour Extraction → Path Simplification
                                                            ↓
        Automated Drawing ← Coordinate Mapping ← Canvas Calibration
```

1. **Preprocessing**: Converts image to grayscale and applies Gaussian blur
2. **Edge Detection**: Uses Canny algorithm to identify edges
3. **Contour Extraction**: Finds external contours from edge map
4. **Simplification**: Applies RDP algorithm to reduce point count
5. **Scaling**: Maps paths to fit calibrated canvas area
6. **Drawing**: Automates mouse movements to reproduce the image

### Algorithm: Ramer-Douglas-Peucker (RDP)

The script uses RDP to simplify paths while preserving shape:
- Recursively finds points farthest from line segments
- Removes points that don't significantly affect the shape
- Configurable tolerance via `--simplify` parameter

## 🎯 Examples

### Example 1: Simple Line Art

```bash
python insta_draw.py --image line_art.png --speed 0.002 --simplify 2.0 --calibrate
```

**Best for**: Logos, icons, simple sketches

### Example 2: Detailed Portrait

```bash
python insta_draw.py --image portrait.jpg --speed 0.004 --simplify 1.5 --calibrate
```

**Best for**: Photographs, complex drawings

### Example 3: Fast Sketch

```bash
python insta_draw.py --image sketch.jpg --speed 0.001 --simplify 5.0 --calibrate
```

**Best for**: Quick demonstrations, abstract art

## 💡 Tips & Best Practices

### Image Preparation

✅ **Do:**
- If the drawing is too big, select the magic wand (highlighted lines) with the smallest brush size and go back to the pen, the lines will become smaller
- Use high-contrast images
- Remove backgrounds for cleaner results
- Use images with clear, defined edges

❌ **Avoid:**
- Low contrast or blurry images
- Very complex backgrounds


## 🐛 Troubleshooting

### Issue: "File not found or could not be opened"
**Solution**: Check image path and file format (jpg, png, bmp supported)

### Issue: Drawing is off-center or wrong size
**Solution**: Always use `--calibrate` mode for precise placement

### Issue: Drawing is too fast/slow
**Solution**: Adjust `--speed` parameter (increase to slow down)

### Issue: Too many/few details
**Solution**: Adjust `--simplify` parameter (increase to reduce detail)

### Issue: Script won't stop
**Solution**: Move mouse to any screen corner (failsafe feature)

### Issue: Lines are jagged
**Solution**: 
- Decrease `--speed` for smoother lines
- Ensure drawing app is responsive
- Check system performance

## 🛡️ Safety & Limitations

### Safety Features

- **FAILSAFE Mode**: PyAutoGUI's built-in protection - move mouse to corners to abort
- **Startup Delay**: 1-second pause before drawing begins
- **Manual Control**: Always requires user calibration

### Limitations

- ⚠️ **Takes full mouse control** - Cannot use computer during drawing
- ⚠️ **Canvas must remain visible** - Don't switch windows during execution
- ⚠️ **System-dependent speed** - Performance varies by hardware
- ⚠️ **No undo function** - Use applications with undo capabilities
- ⚠️ **Screen resolution dependent** - Calibrate for each display setup


## 🙏 Acknowledgments

- OpenCV team for computer vision algorithms
- PyAutoGUI for mouse automation
- NumPy for numerical computing

**⚠️ Disclaimer**: This tool controls your mouse automatically. Always test with simple images first and ensure you understand its behavior. The authors are not responsible for any unintended actions performed by the script.

**Made with ❤️ by Arek**

---

### Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/instadraw&type=Date)](https://star-history.com/#yourusername/instadraw&Date)

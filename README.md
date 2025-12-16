# 🚀 Smart Gesture-Controlled HCI System

> **Touchless Computer Control Through Advanced Computer Vision & Machine Learning**

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.9.0-green.svg)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.11-orange.svg)](https://mediapipe.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**👨‍💻 Developed by:** [SHREYAS M P.](https://www.linkedin.com/in/shreyas-m-p-2408a7260/)  
**📧 Contact:** [shreyas.cta61@gmail.com](mailto:shreyas.cta61@gmail.com)  
**💻 GitHub:** [github.com/Shreyu0301](https://github.com/Shreyu0301)

---

An enterprise-grade Human-Computer Interaction (HCI) system that enables **contactless computer control** through natural hand gestures. This production-ready application demonstrates expertise in real-time computer vision, gesture recognition algorithms, modern GUI development, and cloud-native architecture.

---

## 🌟 Why This Project Stands Out

**For Employers & Recruiters:**

| Aspect | Implementation | Skill Demonstration |
|--------|----------------|---------------------|
| **🎯 Real-World Problem** | Touchless computer control for accessibility & hygiene | Problem-solving, User-centric design |
| **⚡ Performance** | 30 FPS real-time processing, <100ms latency | Optimization, Performance engineering |
| **🧠 ML Integration** | Google MediaPipe with 21-point hand tracking | ML/AI integration, API utilization |
| **🎨 Professional UI** | Modern CustomTkinter GUI with live video feed | Frontend development, UX design |
| **☁️ Cloud Architecture** | MongoDB Atlas for distributed configuration | Cloud services, Database design |
| **🔧 Cross-Platform** | Windows & macOS with platform-specific optimizations | System programming, Portability |
| **📊 Documentation** | Complete UML diagrams, API docs, unit tests | Professional development practices |
| **🏗️ Architecture** | MVC pattern, modular design, clean code | Software architecture, Best practices |

---

## 📸 Project Snapshots & Demonstrations

<table>
  <tr>
    <td align="center">
      <img src="screenshots/main_interface.png" width="400" alt="Main Interface"/>
      <br /><em>Main Application Interface</em>
    </td>
    <td align="center">
      <img src="screenshots/customization_screen.png" width="400" alt="Customization Screen"/>
      <br /><em>Customization Screen</em>
    </td>
  </tr>
  <tr>
    <td align="center">
      <img src="screenshots/tutorial_screen.png" width="400" alt="Tutorial Mode"/>
      <br /><em>Tutorial Mode</em>
    </td>
    <td align="center">
      <img src="screenshots/virtual_keyboard.png" width="400" alt="Virtual Keyboard"/>
      <br /><em>Virtual Keyboard</em>
    </td>
  </tr>
</table>

---

### Animated Gesture Tutorials

The project includes pre-rendered GIF animations demonstrating each control mode:

| Mode | Left Hand (Mode Selection) | Right Hand (Action) | Description |
|------|---------------------------|---------------------|-------------|
| **Mouse Control** | ![Mode Select](animations/6.gif) | ![Action](animations/17.gif) | Select mode with index finger, then use index + middle to move cursor |
| **Media Control** | ![Mode Select](animations/1.gif) | ![Action](animations/8.gif) | Select mode with index + middle, pinch thumb-index to adjust volume |
| **Browser Control** | ![Mode Select](animations/5.gif) | ![Action](animations/11.gif) | Select mode with 3 fingers, use thumb/little for tab navigation |
| **Window Management** | ![Mode Select](animations/4.gif) | ![Action](animations/11.gif) | Select mode with thumb + index, open little finger to switch windows |
| **Brightness Control** | ![Mode Select](animations/2.gif) | ![Action](animations/8.gif) | Select mode with thumb only, pinch to adjust screen brightness |
| **Game Control** | ![Mode Select](animations/15.gif) | ![Action](animations/18.gif) | Select mode with index + little, use directional gestures (WASD) |
| **Virtual Keyboard** | ![Mode Select](animations/16.gif) | ![Action](animations/16.gif) | Select mode with 4 fingers (no thumb), point and pinch to type |
| **Custom App Launcher** | ![Mode Select](animations/7.gif) | ![Action](animations/18.gif) | User-defined apps with 5 programmable gesture slots |

*These tutorial assets are already included in the `animations/` folder and play automatically in the application's Tutorial mode.*

---

## 💡 Core Features & Capabilities

### 1. 🖱️ Precision Mouse Control
- Sub-pixel cursor positioning with smoothing
- Left/right/middle click detection
- Scroll gesture with speed control
- Platform-specific mouse APIs

### 2. 🔊 Media & Volume Management
- Pinch gesture for volume adjustment
- Windows: PyCaw (Core Audio API)
- macOS: AppleScript integration
- Visual feedback with current levels

### 3. 🌐 Browser Automation
- Tab switching (next/previous)
- Smooth scroll with acceleration
- Zoom in/out controls
- Auto-focus browser detection

### 4. 🪟 Window Management
- Application switcher (Alt+Tab equivalent)
- Show desktop gesture
- Window minimize/restore
- Multi-monitor support

### 5. 🎮 Gaming Controls
- Directional movement (WASD/Arrows)
- Jump/action commands
- Low-latency input (<50ms)
- Anti-repeat gesture detection

### 6. ⌨️ Virtual Keyboard
- Full QWERTY on-screen layout
- Caps lock & special characters
- Auto-focus target application
- Click-to-type with visual feedback

### 7. 🚀 Custom App Launcher
- 5 programmable gesture slots
- Launch any application/script
- Cloud-synced across devices
- Quick-access to favorites

### 8. 💡 Brightness Control
- Gesture-based screen brightness
- Windows: WMI integration
- macOS: brightness CLI
- Smooth transitions

---

### 🎯 Advanced Technical Features

✅ **Dual-Hand Recognition** - Independent left/right hand tracking with role separation  
✅ **Gesture Stability Algorithm** - 2-frame confirmation prevents false positives  
✅ **Smart Context Switching** - Seamless mode transitions based on hand positions  
✅ **Action Cooldown System** - Intelligent debouncing prevents command spam  
✅ **Real-Time Visual Feedback** - Live camera with gesture overlay & status  
✅ **Persistent State Management** - MongoDB-backed configuration system  
✅ **Error Recovery** - Graceful degradation & automatic reconnection  
✅ **Cross-Platform Support** - Windows 10/11 & macOS 11+ (Intel/Apple Silicon)

---

## 🛠️ Technology Stack

### Core Technologies

<table>
<tr>
<td width="50%" valign="top">

**Computer Vision & ML**
- **OpenCV 4.9.0** - Camera I/O & image processing
- **MediaPipe 0.10.11** - Google's ML hand tracking
  - BlazePalm hand detector
  - 21-point 3D landmark model
  - Real-time: <16ms per frame
- **NumPy 1.24.4** - Vectorized math operations

**GUI & Graphics**
- **CustomTkinter 5.2.2** - Modern themed interface
- **Pillow 12.0.0** - Image manipulation
- **Tkinter** - Native GUI framework

</td>
<td width="50%" valign="top">

**System Integration**
- **PyAutoGUI 0.9.54** - GUI automation
- **Pynput 1.7.7** - Low-level input control
- **PyWin32 311** - Windows API (window mgmt)
- **PyCaw 20251023** - Windows audio API
- **PyObjC** - macOS Cocoa frameworks

**Database & Cloud**
- **PyMongo 4.6.3** - MongoDB driver
- **Python-dotenv 1.0.1** - Config management
- **MongoDB Atlas** - Cloud database

</td>
</tr>
</table>

---

## 🎮 Complete Gesture Reference

### Left Hand (Mode Selection)

| Gesture | Visual | Finger Pattern | Mode Activated |
|---------|--------|---------------|----------------|
| Index only | ☝ | `[0, 1, 0, 0, 0]` | **Mouse Control** |
| Index + Middle | ✌️ | `[0, 1, 1, 0, 0]` | **Media/Volume Control** |
| Index + Middle + Ring | 🤟 | `[0, 1, 1, 1, 0]` | **Browser Control** |
| All except thumb | 🖐 | `[0, 1, 1, 1, 1]` | **Virtual Keyboard** |
| Thumb only | 👍 | `[1, 0, 0, 0, 0]` | **Brightness Control** |
| Thumb + Index | 🤏 | `[1, 1, 0, 0, 0]` | **Window Management** |
| Thumb + Index + Middle | 🖖 | `[1, 1, 1, 0, 0]` | **Game Control** |

### Right Hand (Context-Aware Actions)

#### 🖱️ Mouse Control Mode
| Gesture | Action | Details |
|---------|--------|---------|
| Index + Middle | Move cursor | Hand position → screen coordinates |
| Index + Middle + Ring | Left click | Single click at cursor position |
| Thumb + Index | Right click | Context menu |
| All fingers | Scroll mode | Vertical scrolling |

#### 🔊 Media Control Mode
| Gesture | Action | Algorithm |
|---------|--------|-----------|
| Pinch (Thumb + Index) | Volume adjust | Distance between thumb-index tips |
|  | Pinch closer = Lower | `volume = interp(distance, [min, max], [0, 100])` |
|  | Spread apart = Higher | Smooth interpolation |

#### 🌐 Browser Control Mode
| Gesture | Action | Keyboard Equivalent |
|---------|--------|---------------------|
| Little finger | Next tab | Ctrl+Tab |
| Thumb | Previous tab | Ctrl+Shift+Tab |
| Index | Scroll down | ↓ (smooth) |
| Index + Middle | Scroll up | ↑ (smooth) |
| All fingers | Zoom | Ctrl +/- |

#### 🪟 Window Control Mode
| Gesture | Action | Keyboard Equivalent |
|---------|--------|---------------------|
| Little finger | Next window | Alt+Tab |
| Thumb | Previous window | Alt+Shift+Tab |
| All fingers | Show desktop | Win+D / Cmd+M |

#### 🎮 Game Control Mode
| Gesture | Action | Key Sent |
|---------|--------|----------|
| Index | Jump/Forward | ↑ or W |
| Index + Middle | Backward/Slide | ↓ or S |
| Thumb | Move left | ← or A |
| Little finger | Move right | → or D |

#### 🚀 Custom App Launcher Mode
| Gesture | Slot | Customizable |
|---------|------|--------------|
| Index | App 1 | ✅ User-defined |
| Index + Middle | App 2 | ✅ User-defined |
| Index + Middle + Ring | App 3 | ✅ User-defined |
| All except thumb | App 4 | ✅ User-defined |
| Thumb | App 5 | ✅ User-defined |

---

## 🚀 Complete Setup Guide

### System Requirements

**Minimum:**
- OS: Windows 10 (64-bit) or macOS 11+
- Python: 3.11.0+
- RAM: 4 GB
- CPU: Dual-core 2.0 GHz
- Camera: 720p webcam
- Internet: For MongoDB setup

**Recommended:**
- RAM: 8 GB
- CPU: Quad-core
- Camera: 1080p
- SSD storage

---

### 📥 Step-by-Step Installation

#### Step 1: Install Prerequisites

**Install Python 3.11+**
- Windows: [python.org/downloads](https://www.python.org/downloads/)
- macOS: `brew install python@3.11`

**Install Git** (optional)
- Download from [git-scm.com](https://git-scm.com/downloads)

---

#### Step 2: Clone/Download Project

```bash
# Option A: Using Git
git clone <repository-url>
cd Smart-Gesture-Controlled-HCI-System

# Option B: Download ZIP and extract
# Navigate to extracted folder
cd Smart-Gesture-Controlled-HCI-System
```

---

#### Step 3: Create Virtual Environment

**🪟 Windows (PowerShell):**
```powershell
# Create virtual environment
python -m venv .venv

# Activate (if permission error, see solution below)
.venv\Scripts\Activate.ps1

# Verify activation (should see (.venv) in prompt)
python --version
```

**💡 Fix PowerShell Execution Policy Error:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**🍎 macOS/Linux:**
```bash
# Create virtual environment
python3 -m venv .venv

# Activate
source .venv/bin/activate

# Verify
python --version
```

---

#### Step 4: Install Dependencies

**🪟 Windows:**
```bash
# Upgrade pip (important!)
python -m pip install --upgrade pip

# Install all 48 packages (~2-3 minutes, ~500 MB)
pip install -r requirements_windows.txt

# Verify key packages
pip list | findstr "customtkinter mediapipe opencv-python"
```

**🍎 macOS (Apple Silicon):**
```bash
# Upgrade pip
pip install --upgrade pip

# Install all 57 packages (~3-4 minutes, ~550 MB)
pip install -r requirements_apple_silicon.txt

# Verify
pip list | grep -E "customtkinter|mediapipe|opencv-python"
```

---

#### Step 5: Setup MongoDB Cloud Database

**5.1: Create Free MongoDB Atlas Account**

1. Go to [mongodb.com/cloud/atlas/register](https://www.mongodb.com/cloud/atlas/register)
2. Sign up with email (FREE tier)
3. Create new project: `GestureControl`

**5.2: Create Cluster**

1. Click "Build a Cluster"
2. Choose **FREE M0** (512 MB)
3. Select cloud provider & region (closest to you)
4. Cluster name: `Cluster0`
5. Click "Create Cluster" (wait 3-5 min)

**5.3: Create Database & Collection**

1. Click "Browse Collections"
2. "Add My Own Data"
3. Database name: **`hci`**
4. Collection name: **`user-config`**
5. Create

**5.4: Setup Network Access**

1. Left sidebar: "Network Access"
2. "Add IP Address"
3. **"Allow Access from Anywhere"** (0.0.0.0/0)
   - Or add your specific IP
4. Confirm

**5.5: Get Connection String**

1. Left sidebar: "Database"
2. Click "Connect" on Cluster0
3. "Connect your application"
4. Driver: **Python**, Version: **3.6 or later**
5. Copy connection string (example format):
   ```
   mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority
   ```

**5.6: Create .env File**

In project root, create `.env`:

**Windows:**
```powershell
Copy-Item ".env.example" ".env"
notepad .env
```

**macOS:**
```bash
cp .env.example .env
nano .env
```

**Edit `.env` and paste YOUR actual connection string:**
```env
MONGODB.URI=mongodb+srv://<your-username>:<your-password>@<your-cluster>.mongodb.net/?retryWrites=true&w=majority
```

---

#### Step 6: Configure Camera Permissions

**🪟 Windows 10/11:**
1. Settings → Privacy → Camera
2. Enable "Allow apps to access your camera"
3. Scroll down, enable for "Python"

**🍎 macOS:**
1. System Preferences → Security & Privacy → Camera
2. Enable for "Terminal" or "Python"
3. Restart terminal if needed

---

#### Step 7: Run the Application

```bash
# Ensure virtual environment is activated
# You should see (.venv) in your prompt

python main.py
```

**✅ Expected Output:**

Console:
```
<unique-device-id-here>
✓ Gesture control program started
```

GUI Window:
- Title: "Smart Gesture-Controlled HCI System"
- Left panel: Menu with buttons
- Right panel: "Camera Feed (Activate to start)"
- Bottom: Status indicators

---

### 🎉 First-Time Usage

1. **Click "Activate"** button
2. **Allow camera access** if prompted
3. **Show your hands** to the camera (1-2 feet away)
4. **Try a gesture:** 
   - Left hand: Index finger only (Mouse mode)
   - Right hand: Index + Middle (move cursor)
5. **Watch status display** for feedback

**🎓 Tutorial Mode:**
- Click "Tutorial" to see animated gesture demonstrations
- Practice each gesture before using

---

### 🔄 Daily Usage

**Start application:**
```bash
cd VTU_Major_Project
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS
python main.py
```

**Stop application:**
- Click "Deactivate"
- Close GUI window
- Ctrl+C in terminal if needed

---

## 📖 User Guide

### Customizing Gesture Shortcuts

1. Click **"Customize Gestures"**
2. Select gesture slot (5 available)
3. Choose application from dropdown (199 apps)
4. Click **"Add"**
5. Click **"Save"** (syncs to MongoDB)
6. Test your custom gesture!

**Available in `appList.json`:**
- System apps (Calculator, Notepad, Settings)
- Browsers (Chrome, Firefox, Edge)
- Office (Word, Excel, PowerPoint)
- Media (VLC, Spotify, Photos)
- Utilities (Command Prompt, Task Manager)

---

## 🎯 Use Cases & Applications

### Real-World Applications

1. **🏥 Healthcare**
   - Touchless control for sterile environments
   - Operating room computer control
   - Patient interaction systems

2. **♿ Accessibility**
   - Control for users with mobility limitations
   - Alternative to traditional input devices
   - Ergonomic computer interaction

3. **🎮 Gaming**
   - Motion controls for compatible games
   - VR/AR integration potential
   - Interactive entertainment

4. **🏢 Professional**
   - Presentation control (touchless slides)
   - Digital signage interaction
   - Public kiosk interfaces

5. **🏠 Smart Home**
   - Touchless control panels
   - Home automation gestures
   - Voice-free interaction

---

## 🚀 Future Enhancements

**Potential Improvements:**
- [ ] Machine learning gesture customization
- [ ] Multi-user profile support
- [ ] Voice command integration
- [ ] Mobile app for configuration
- [ ] Gesture recording & playback
- [ ] Analytics dashboard
- [ ] Plugin system for custom controls
- [ ] Gesture templates marketplace

---

## 🔒 Privacy & Security

✅ **Local Processing** - All video processing happens on device  
✅ **No Data Transmission** - Camera feed never leaves your computer  
✅ **Minimal Cloud Data** - Only gesture configs stored in MongoDB  
✅ **Anonymized ID** - Device ID is hashed (MAC + hostname)  
✅ **Secure Connection** - MongoDB Atlas uses TLS encryption  
✅ **No Personal Info** - No name, email, or location collected  

---

## 📄 Technical Documentation

### API Reference

**GestureControl Class:**
```python
class GestureControl:
    def __init__(self, runFlag=True)
    def detect_gesture(self, raised_fingers) -> str
    def run(self) -> None
    # Main control loop with state machine
```

**HandTracker Class:**
```python
class HandTracker:
    def detect_raised_fingers(self, landmarks, hand_type) -> List[int]
    def find_position(self, frame) -> List[Tuple]
    # Returns 21 landmarks: [(id, x, y), ...]
```

### Configuration Files

**appList.json Structure:**
```json
{
  "displayName": "App Name",
  "shellName": ["command.exe", "args"]
}
```

**user_defined_data.json:**
```json
{
  "_id": "unique-device-id",
  "name": "hostname",
  "userDefinedControls": {
    "index": "app_shell_command",
    "index and middle": "app_shell_command",
    ...
  }
}
```

---

## 📦 Dependency Overview

**Total Packages:**
- Windows: 48 packages (~500 MB)
- macOS: 57 packages (~550 MB)

**Key Dependencies:**

| Package | Version | Purpose | Size |
|---------|---------|---------|------|
| customtkinter | 5.2.2 | Modern GUI | ~30 MB |
| mediapipe | 0.10.11 | Hand tracking ML | ~50 MB |
| opencv-python | 4.9.0.80 | Computer vision | ~38 MB |
| pymongo | 4.6.3 | Database driver | ~10 MB |
| pyautogui | 0.9.54 | System automation | ~5 MB |
| numpy | 1.24.4 | Math operations | ~15 MB |

---

## 💼 For Employers & Recruiters

### Skills Demonstrated

**Programming & Development:**
- ✅ Python 3.11+ (Advanced OOP, type hints)
- ✅ Multi-threading & concurrency
- ✅ State machine implementation
- ✅ Error handling & logging
- ✅ Clean code practices

**Computer Vision & AI/ML:**
- ✅ OpenCV for image processing
- ✅ MediaPipe ML model integration
- ✅ Real-time video processing
- ✅ Gesture recognition algorithms
- ✅ Performance optimization

**Software Engineering:**
- ✅ MVC architecture pattern
- ✅ Modular design & separation of concerns
- ✅ Unit testing (unittest framework)
- ✅ UML system design
- ✅ Version control (Git)

**Full-Stack Development:**
- ✅ GUI development (CustomTkinter)
- ✅ Database design (MongoDB)
- ✅ Cloud integration (MongoDB Atlas)
- ✅ API integration
- ✅ Cross-platform development

**System Programming:**
- ✅ Windows API (Win32, COM)
- ✅ macOS frameworks (PyObjC)
- ✅ System-level automation
- ✅ Platform-specific optimizations

### Project Metrics

- **📝 Lines of Code:** 2,500+ (clean, documented)
- **🏗️ Architecture:** Modular, 9 classes
- **⚡ Performance:** 30 FPS, <100ms latency
- **🧪 Test Coverage:** 80%+ with unit tests
- **📊 Documentation:** Complete UML + README
- **🌐 Deployment:** Production-ready

---

## 📞 Support & Contact

**Project Documentation:**
- Complete setup guide (above)
- Video tutorials (in-app)
- UML diagrams
- API documentation

**For Technical Issues:**
1. Check troubleshooting section
2. Review error messages carefully
3. Verify all prerequisites installed
4. Test camera permissions

---

## 🙏 Acknowledgments

**Technologies & Libraries:**
- [MediaPipe](https://mediapipe.dev/) - Google's ML framework
- [OpenCV](https://opencv.org/) - Computer vision library
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) - Modern GUI
- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas) - Cloud database
- Python community for excellent documentation

**Academic Support:**
- Visvesvaraya Technological University (VTU)
- Department of Computer Science & Engineering

---

## 👨‍💻 Author

**SHREYAS M P.**

- 🔗 LinkedIn: [linkedin.com/in/shreyas-m-p-2408a7260](((https://www.linkedin.com/in/shreyas-m-p-2408a7260/))
- 💻 GitHub: [github.com/Shreyu0301](https://github.com/Shreyu0301)
- 📧 Email: [shreyas.cta61@gmail.com](mailto:shreyas.cta61@gmail.com)

---

## 📜 License

This project is developed as an academic project for educational purposes.

**For Employers:** This project demonstrates technical skills and is available for discussion during interviews. Commercial use requires permission.

---

## 📈 Project Status

**Current Version:** 1.0.0  
**Last Updated:** November 2025  
**Status:** ✅ Production Ready  
**Python Version:** 3.11+  
**Tested On:** Windows 11, macOS (Apple Silicon)  

---

<div align="center">

### 🌟 Built with passion for Computer Vision & Human-Computer Interaction

**Developed by:** [Shreyas M P.](https://www.linkedin.com/in/shreyas-m-p-2408a7260)

**Showcasing expertise in:** Python • Computer Vision • ML Integration • GUI Development • Cloud Architecture • System Programming

---

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/shreyas-m-p-2408a7260)
[![GitHub](https://img.shields.io/badge/GitHub-Follow-black?style=for-the-badge&logo=github)](https://github.com/Shreyu0301)
[![Email](https://img.shields.io/badge/Email-Contact-red?style=for-the-badge&logo=gmail)](mailto:shreyas.cta61@gmail.com)

</div>

"""
Virtual Keyboard Module - On-screen QWERTY keyboard with gesture input

Author: Rohan S.
GitHub: https://github.com/Rohan9731
"""

import cv2
import numpy as np
from pynput.keyboard import Controller
import math
import time
import platform

# Import Windows-specific libraries for window focusing
if platform.system() == "Windows":
    try:
        import win32gui
        import win32con
        import win32process
    except ImportError:
        print("⚠ pywin32 not installed. Window focusing will not work.")
        win32gui = None

class Button:
    def __init__(self, pos, text, size=[70, 70], special=False):
        self.pos = pos
        self.size = size
        self.text = text
        self.special = special  # For special keys like CAPS, SPACE, etc.

class VirtualKeyboard:
    def __init__(self, hand_tracker, target_app_name=None):
        self.hand_tracker = hand_tracker
        self.keyboard = Controller()
        self.text = ""
        self.delay = 0
        self.target_app_name = target_app_name  # Store target application name
        self.target_hwnd = None  # Store target window handle
        self.last_focus_attempt = 0  # Track when we last tried to focus
        
        # Smoothing for better cursor control
        self.prev_kb_x = 0
        self.prev_kb_y = 0
        self.smoothing_factor = 0.3  # Higher = smoother but slower, Lower = more responsive (reduced for better sensitivity)
        
        # Caps lock state
        self.caps_lock = False
        
        # Create buttons with proper layout
        self.buttonList = self.create_keyboard_layout()
        
        # Window setup
        self.window_name = "Virtual Keyboard"
        self.window_created = False
    
    def create_keyboard_layout(self):
        """Create a properly styled keyboard layout"""
        buttons = []
        
        # Number row (1-0 with even spacing)
        number_keys = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
        start_x = 20
        for i, key in enumerate(number_keys):
            buttons.append(Button([start_x + i * 85, 15], key, [75, 70]))
        
        # Backspace (larger button at end of number row)
        buttons.append(Button([start_x + 10 * 85, 15], "DEL", [110, 70], special=True))
        
        # First letter row (Q-P)
        qwerty_keys = ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"]
        for i, key in enumerate(qwerty_keys):
            buttons.append(Button([start_x + i * 85, 100], key, [75, 70]))
        
        # Caps Lock (larger button at end)
        buttons.append(Button([start_x + 10 * 85, 100], "CAPS", [110, 70], special=True))
        
        # Second letter row (A-L) with slight offset
        asdf_keys = ["A", "S", "D", "F", "G", "H", "J", "K", "L"]
        offset_x = 40
        for i, key in enumerate(asdf_keys):
            buttons.append(Button([start_x + offset_x + i * 85, 185], key, [75, 70]))
        
        # Enter (larger button)
        buttons.append(Button([start_x + offset_x + 9 * 85, 185], "ENTER", [160, 70], special=True))
        
        # Third letter row (Z-M) with more offset
        zxcv_keys = ["Z", "X", "C", "V", "B", "N", "M"]
        offset_x2 = 60
        for i, key in enumerate(zxcv_keys):
            buttons.append(Button([start_x + offset_x2 + i * 85, 270], key, [75, 70]))
        
        # Space bar (large button at bottom, easy to reach)
        buttons.append(Button([start_x + 120, 365], "SPACE", [650, 65], special=True))
        
        return buttons
        
    def calculate_distance(self, x1, y1, x2, y2):
        """Calculate Euclidean distance between two points"""
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return distance
    
    def find_and_focus_target_app(self):
        """Find and focus the target application window"""
        if not self.target_app_name or not win32gui or platform.system() != "Windows":
            return False
        
        # Only try to focus every 0.5 seconds (reduced for better responsiveness)
        current_time = time.time()
        if current_time - self.last_focus_attempt < 0.5:
            return self.target_hwnd is not None
        
        self.last_focus_attempt = current_time
        
        try:
            import psutil
            import win32process
            
            # First, try to find process by name
            target_processes = []
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    proc_name = proc.info['name'].lower()
                    # Match process name with or without .exe
                    if (self.target_app_name.lower() in proc_name or 
                        f"{self.target_app_name.lower()}.exe" == proc_name):
                        target_processes.append(proc.info['pid'])
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            if not target_processes:
                if not hasattr(self, '_warned_process_not_found'):
                    print(f"⚠ Process '{self.target_app_name}' not running. Please open the application first.")
                    self._warned_process_not_found = True
                return False
            
            # Now find windows belonging to these processes
            def enum_callback(hwnd, results):
                if win32gui.IsWindowVisible(hwnd):
                    _, pid = win32process.GetWindowThreadProcessId(hwnd)
                    if pid in target_processes:
                        window_title = win32gui.GetWindowText(hwnd)
                        if window_title:  # Only consider windows with titles
                            results.append((hwnd, window_title, pid))
                return True
            
            matching_windows = []
            win32gui.EnumWindows(enum_callback, matching_windows)
            
            # Log found windows (only once)
            if not hasattr(self, '_logged_windows'):
                self._logged_windows = True
                if matching_windows:
                    print(f"\n✓ Found {len(matching_windows)} windows for '{self.target_app_name}':")
                    for hwnd, title, pid in matching_windows:
                        print(f"  - PID {pid}: {title}")
            
            if matching_windows:
                self.target_hwnd, window_title, pid = matching_windows[0]
                
                # Focus the window
                try:
                    # Get current foreground window
                    current_hwnd = win32gui.GetForegroundWindow()
                    current_title = win32gui.GetWindowText(current_hwnd)
                    
                    # Only focus if not already focused
                    if current_hwnd != self.target_hwnd:
                        print(f"🎯 Focusing '{window_title}' (PID: {pid})")
                        
                        # Get thread IDs
                        current_thread = win32process.GetCurrentThreadId()
                        target_thread, _ = win32process.GetWindowThreadProcessId(self.target_hwnd)
                        
                        # Attach to target thread
                        if current_thread != target_thread:
                            try:
                                win32process.AttachThreadInput(current_thread, target_thread, True)
                            except:
                                pass  # May fail if already attached
                        
                        # Restore and focus window
                        win32gui.ShowWindow(self.target_hwnd, win32con.SW_RESTORE)
                        win32gui.SetForegroundWindow(self.target_hwnd)
                        win32gui.BringWindowToTop(self.target_hwnd)
                        
                        # Detach
                        if current_thread != target_thread:
                            try:
                                win32process.AttachThreadInput(current_thread, target_thread, False)
                            except:
                                pass
                        
                        print(f"✓ Successfully focused: {window_title}")
                        time.sleep(0.2)  # Increased delay to ensure window is focused before typing
                    
                    return True
                except Exception as e:
                    print(f"⚠ Error focusing window: {e}")
                    return False
            else:
                if not hasattr(self, '_warned_no_windows'):
                    print(f"⚠ No visible windows found for '{self.target_app_name}'")
                    self._warned_no_windows = True
                return False
                
        except ImportError:
            print("⚠ psutil not installed. Install with: pip install psutil")
            return False
        except Exception as e:
            print(f"⚠ Error finding target app: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def drawAll(self, img):
        """Draw all keyboard buttons with proper styling"""
        for button in self.buttonList:
            x, y = button.pos
            w, h = button.size
            
            # Determine button color based on type
            if button.text == "CAPS":
                # Red when caps is ON, dark gray when OFF
                bg_color = (50, 50, 200) if self.caps_lock else (80, 80, 80)
                text_color = (255, 255, 255)
                font_size = 1.2
            elif button.special:
                # Special keys (SPACE, ENTER, DEL) - darker blue
                bg_color = (120, 100, 60)
                text_color = (255, 255, 255)
                font_size = 1.2 if button.text == "SPACE" else 1.4
            else:
                # Regular keys - light gray
                bg_color = (90, 90, 90)
                text_color = (255, 255, 255)
                font_size = 2.0
            
            # Draw button with rounded corners effect (3D look)
            cv2.rectangle(img, (x, y), (x + w, y + h), (60, 60, 60), cv2.FILLED)  # Shadow
            cv2.rectangle(img, (x-2, y-2), (x + w - 2, y + h - 2), bg_color, cv2.FILLED)  # Button
            cv2.rectangle(img, (x-2, y-2), (x + w - 2, y + h - 2), (120, 120, 120), 2)  # Border
            
            # Calculate text size for proper centering
            text = button.text
            (text_width, text_height), baseline = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, font_size, 2)
            
            # Center text properly
            text_x = x + (w - text_width) // 2
            text_y = y + (h + text_height) // 2
            
            # Apply caps lock styling to letters
            display_text = button.text
            if button.text.isalpha() and len(button.text) == 1:
                display_text = button.text.upper() if self.caps_lock else button.text
            
            cv2.putText(img, display_text, (text_x, text_y),
                       cv2.FONT_HERSHEY_SIMPLEX, font_size, text_color, 2)
        return img
    
    def create_keyboard_window(self):
        """Create the keyboard window"""
        if not self.window_created:
            cv2.namedWindow(self.window_name, cv2.WINDOW_NORMAL | cv2.WINDOW_GUI_NORMAL)
            cv2.resizeWindow(self.window_name, 1000, 480)  # Wider for all buttons
            cv2.setWindowProperty(self.window_name, cv2.WND_PROP_TOPMOST, 1)
            
            # On Windows, make the window a tool window that doesn't steal focus
            if platform.system() == "Windows" and win32gui:
                try:
                    import time
                    time.sleep(0.1)  # Small delay to ensure window is created
                    hwnd = win32gui.FindWindow(None, self.window_name)
                    if hwnd:
                        # Set extended window style to prevent focus stealing
                        exstyle = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
                        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, 
                                             exstyle | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST)
                except Exception as e:
                    print(f"⚠ Could not set window style: {e}")
            
            self.window_created = True
            print("✓ Virtual Keyboard window opened")
    
    def close_keyboard_window(self):
        """Close the keyboard window"""
        if self.window_created:
            try:
                cv2.destroyWindow(self.window_name)
                print("✓ Virtual Keyboard window closed - text cleared")
            except Exception as e:
                print(f"⚠ Window already closed: {e}")
            finally:
                self.window_created = False
                self.text = ""  # Clear text when closing
                self.caps_lock = False  # Reset caps lock
                self.prev_kb_x = 0  # Reset smoothing
                self.prev_kb_y = 0
    
    def process(self, frame, results=None):
        """Process hand gestures and update keyboard
        Args:
            frame: Camera frame
            results: MediaPipe results with multi_hand_landmarks and multi_handedness
        """
        # Create keyboard window if not exists
        if not self.window_created:
            self.create_keyboard_window()
        
        # Get frame dimensions
        h_frame, w_frame, _ = frame.shape
        
        # Create keyboard image with dark professional background
        keyboard_img = np.zeros((480, 1000, 3), dtype=np.uint8)
        keyboard_img[:] = (30, 30, 30)  # Professional dark background
        keyboard_img = self.drawAll(keyboard_img)
        
        # Draw text display area at bottom with better styling
        cv2.rectangle(keyboard_img, (15, 435), (985, 475), (200, 200, 200), 2)  # Border
        cv2.rectangle(keyboard_img, (17, 437), (983, 473), (50, 50, 50), cv2.FILLED)  # Background
        
        # Display text with scrolling if too long
        display_text = self.text[-55:] if len(self.text) > 55 else self.text
        cv2.putText(keyboard_img, display_text, (25, 462), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 2)
        
        # Show caps lock status with indicator
        if self.caps_lock:
            cv2.rectangle(keyboard_img, (920, 435), (985, 475), (50, 50, 200), cv2.FILLED)
            cv2.putText(keyboard_img, "CAPS", (925, 462), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Add status message on camera frame
        cv2.putText(frame, "KEYBOARD MODE ACTIVE", (10, h_frame - 50), 
                   cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 3)
        cv2.putText(frame, "Move RIGHT hand to control | Pinch thumb+index to type", (10, h_frame - 20), 
                   cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)
        
        # Process hand landmarks - ONLY RIGHT HAND
        right_hand_landmarks = None
        if results and results.multi_hand_landmarks:
            # Find the RIGHT hand
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                handedness = results.multi_handedness[idx].classification[0].label
                if handedness.lower() == "right":
                    right_hand_landmarks = hand_landmarks
                    break
        
        if right_hand_landmarks:
            landmarks = []
            
            # Get all landmarks from RIGHT hand
            for id, lm in enumerate(right_hand_landmarks.landmark):
                cx, cy = int(lm.x * w_frame), int(lm.y * h_frame)
                landmarks.append([id, cx, cy])
            
            if len(landmarks) > 17:
                try:
                    # Get fingertip positions - Using thumb and index for easier pinching
                    x_index, y_index = landmarks[8][1], landmarks[8][2]  # Index finger tip
                    x_thumb, y_thumb = landmarks[4][1], landmarks[4][2]  # Thumb tip
                    
                    # Draw finger positions on camera frame
                    cv2.circle(frame, (x_index, y_index), 15, (0, 255, 0), cv2.FILLED)
                    cv2.circle(frame, (x_thumb, y_thumb), 12, (255, 0, 255), cv2.FILLED)
                    
                    # Draw line between fingers to visualize pinch
                    cv2.line(frame, (x_index, y_index), (x_thumb, y_thumb), (255, 255, 0), 2)
                    
                    # Define detection zone - SMALLER zone (40% of screen) for easier control
                    # User only needs to move hand in a comfortable small area
                    zone_margin_x = int(w_frame * 0.3)  # 30% margin on each side = 40% center
                    zone_margin_y = int(h_frame * 0.3)  # 30% margin top/bottom = 40% center
                    
                    # Draw detection zone on camera frame
                    cv2.rectangle(frame, (zone_margin_x, zone_margin_y), 
                                (w_frame - zone_margin_x, h_frame - zone_margin_y), 
                                (0, 255, 255), 3)
                    cv2.putText(frame, "Move hand here (small area)", (zone_margin_x + 10, zone_margin_y - 10), 
                               cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 255), 2)
                    
                    # Map only the detection zone to keyboard coordinates
                    # Constrain finger position to detection zone
                    x_constrained = max(zone_margin_x, min(x_index, w_frame - zone_margin_x))
                    y_constrained = max(zone_margin_y, min(y_index, h_frame - zone_margin_y))
                    
                    # Map constrained coordinates to keyboard (center 40% of screen → full keyboard)
                    x_normalized = (x_constrained - zone_margin_x) / (w_frame - 2 * zone_margin_x)
                    y_normalized = (y_constrained - zone_margin_y) / (h_frame - 2 * zone_margin_y)
                    
                    kb_x_raw = int(x_normalized * 1000)
                    kb_y_raw = int(y_normalized * 440)  # Full keyboard height including space bar
                    
                    # Apply smoothing for stable cursor movement
                    if self.prev_kb_x == 0 and self.prev_kb_y == 0:
                        # First time, no smoothing
                        kb_x = kb_x_raw
                        kb_y = kb_y_raw
                    else:
                        # Smooth cursor movement: blend previous and current position
                        kb_x = int(self.prev_kb_x * self.smoothing_factor + kb_x_raw * (1 - self.smoothing_factor))
                        kb_y = int(self.prev_kb_y * self.smoothing_factor + kb_y_raw * (1 - self.smoothing_factor))
                    
                    # Keep coordinates within keyboard bounds
                    kb_x = max(0, min(kb_x, 999))  # 1000 width
                    kb_y = max(0, min(kb_y, 439))  # 440 height for space bar access
                    
                    # Store for next frame
                    self.prev_kb_x = kb_x
                    self.prev_kb_y = kb_y
                    
                    # Draw cursor on keyboard window
                    cv2.circle(keyboard_img, (kb_x, kb_y), 20, (0, 255, 0), 3)
                    cv2.circle(keyboard_img, (kb_x, kb_y), 5, (0, 255, 0), -1)
                    
                    # Show mapping info on camera frame
                    cv2.putText(frame, f"KB: ({kb_x},{kb_y})", (10, 30), 
                              cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 255), 2)
                    
                    # Calculate distance between index and thumb (pinch gesture)
                    dis = self.calculate_distance(x_index, y_index, x_thumb, y_thumb)
                    
                    # Show pinch distance
                    cv2.putText(frame, f"Pinch: {int(dis)}", (10, 60), 
                              cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 0), 2)
                    
                    # Check which button cursor is over
                    hovered_button = None
                    for button in self.buttonList:
                        xb, yb = button.pos
                        wb, hb = button.size
                        
                        if (xb < kb_x < xb + wb) and (yb < kb_y < yb + hb):
                            hovered_button = button
                            
                            # Highlight hovered button with bright cyan glow
                            cv2.rectangle(keyboard_img, (xb - 3, yb - 3), 
                                        (xb + wb + 3, yb + hb + 3),
                                        (0, 255, 255), 3)
                            
                            # Show which key is hovered on camera frame
                            display_name = button.text if len(button.text) > 1 else button.text
                            cv2.putText(frame, f"Key: {display_name}", (10, 90), 
                                      cv2.FONT_HERSHEY_PLAIN, 2.5, (0, 255, 0), 3)
                            
                            # IMPORTANT: Only type when pinched AND delay expired
                            # This prevents accidental typing from just hovering
                            if dis < 35 and self.delay == 0:
                                k = button.text
                                print(f"🔵 PINCH! Dist: {int(dis)} | Key: {k}")
                                
                                # Focus target app before typing (if configured)
                                if self.target_app_name:
                                    self.find_and_focus_target_app()
                                
                                # Handle special keys
                                if k == "CAPS":  # Caps Lock
                                    self.caps_lock = not self.caps_lock
                                    print(f"✓ Caps Lock: {'ON' if self.caps_lock else 'OFF'}")
                                elif k == "SPACE":
                                    self.text += ' '
                                    self.keyboard.press(' ')
                                    self.keyboard.release(' ')
                                    print("✓ Typed: SPACE")
                                elif k == "DEL":  # Backspace
                                    if len(self.text) > 0:
                                        self.text = self.text[:-1]
                                    from pynput.keyboard import Key
                                    self.keyboard.press(Key.backspace)
                                    self.keyboard.release(Key.backspace)
                                    print("✓ Typed: BACKSPACE")
                                elif k == "ENTER":  # Enter
                                    # Send enter key to focused application
                                    from pynput.keyboard import Key
                                    import time
                                    try:
                                        self.keyboard.press(Key.enter)
                                        time.sleep(0.05)  # Small delay for key registration
                                        self.keyboard.release(Key.enter)
                                        print("✓ Typed: ENTER key pressed")
                                    except Exception as e:
                                        print(f"⚠ Error typing ENTER: {e}")
                                else:
                                    # Regular character - apply caps lock
                                    if k.isalpha():
                                        char = k.upper() if self.caps_lock else k.lower()
                                    else:
                                        char = k  # Numbers and symbols unchanged
                                    
                                    self.text += char
                                    self.keyboard.press(char)
                                    self.keyboard.release(char)
                                    print(f"✓ Typed: {char}")
                                
                                self.delay = 1
                            
                            break  # Only process one button at a time
                    
                    # Show pinch status - visual feedback
                    if dis < 35:
                        cv2.putText(frame, "PINCHING!", (10, 120), 
                                  cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3)
                    elif dis < 50:
                        cv2.putText(frame, "Almost...", (10, 120), 
                                  cv2.FONT_HERSHEY_PLAIN, 2, (255, 165, 0), 2)
                
                except Exception as e:
                    print(f"⚠ Error processing gesture: {e}")
        else:
            # No RIGHT hand detected
            cv2.putText(frame, "Show RIGHT hand", (10, 30), 
                       cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        
        # Handle delay between keypresses - REDUCED for faster typing
        if self.delay != 0:
            self.delay += 1
            if self.delay > 8:  # Increased to prevent double typing
                self.delay = 0
        
        # Show keyboard window without stealing focus
        cv2.imshow(self.window_name, keyboard_img)
        
        # Ensure target app remains focused after displaying keyboard
        if self.target_app_name and self.target_hwnd and win32gui and platform.system() == "Windows":
            try:
                current_foreground = win32gui.GetForegroundWindow()
                keyboard_hwnd = win32gui.FindWindow(None, self.window_name)
                # If the keyboard window stole focus, give it back to the target
                if current_foreground == keyboard_hwnd and self.target_hwnd:
                    win32gui.SetForegroundWindow(self.target_hwnd)
            except:
                pass  # Silently fail if there's an issue
        
        return frame

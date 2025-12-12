import platform
import pyautogui
import time

# Use keyboard library for better Windows hotkey support
if platform.system() == "Windows":
    import keyboard
    import win32gui
    import win32con
    import win32process


class AppControl:
    def __init__(self, hand_tracker):
        self.hand_tracker = hand_tracker
        self.window_list = []
        self.current_window_index = 0

    def window_nav(self, raised_fingers):
        if raised_fingers is not None and raised_fingers != [0, 0, 0, 0, 0]:
            print(f"\n=== WINDOW CONTROL ===")
            print(f"Right hand fingers: {raised_fingers}")
            
            if raised_fingers == [0, 0, 0, 0, 1]:
                # switch window forward, gesture: little
                print("Action: Switching to next window")
                if platform.system() == "Darwin":
                    pyautogui.hotkey("command", "tab")
                elif platform.system() == "Windows":
                    self._switch_window_forward()
                time.sleep(0.1)
                print("✓ Window switched")
                
            elif raised_fingers == [1, 0, 0, 0, 0]:
                # switch window backward, gesture: thumb
                print("Action: Switching to previous window")
                if platform.system() == "Darwin":
                    pyautogui.hotkey("command", "shift", "tab")
                elif platform.system() == "Windows":
                    self._switch_window_backward()
                time.sleep(0.1)
                print("✓ Window switched")
                
            elif raised_fingers == [1, 1, 1, 1, 1]:
                # minimize window, gesture: all
                print("Action: Show desktop (Win+D)")
                if platform.system() == "Darwin":
                    pyautogui.hotkey("command", "m")
                elif platform.system() == "Windows":
                    keyboard.send("win+d")
                time.sleep(0.1)
                print("✓ Command sent")
                
            elif raised_fingers == [0, 0, 0, 1, 1]:
                # close window, gesture: ring and little
                print("Action: Closing window (Alt+F4)")
                if platform.system() == "Darwin":
                    pyautogui.hotkey("command", "w")
                elif platform.system() == "Windows":
                    keyboard.send("alt+f4")
                time.sleep(0.1)
                print("✓ Command sent")
                
            elif raised_fingers == [0, 1, 0, 0, 1]:
                # switch window(same application different windows) forward, gesture: index and little
                print("Action: Switching within same app (Ctrl+Tab)")
                if platform.system() == "Darwin":
                    pyautogui.hotkey("command", "`")
                elif platform.system() == "Windows":
                    keyboard.send("ctrl+tab")
                time.sleep(0.1)
                print("✓ Command sent")
                
            elif raised_fingers == [0, 1, 1, 1, 1]:
                # close a window of the application, gesture: index, middle, ring and little
                print("Action: Closing current window/tab (Ctrl+W)")
                if platform.system() == "Darwin":
                    pyautogui.hotkey("command", "w")
                elif platform.system() == "Windows":
                    keyboard.send("ctrl+w")
                time.sleep(0.1)
                print("✓ Command sent")
            else:
                print(f"⚠ Unknown finger pattern for window control")
    
    def _get_visible_windows(self):
        """Get list of visible windows (excluding hidden and minimized)"""
        def enum_callback(hwnd, results):
            try:
                if win32gui.IsWindowVisible(hwnd):
                    window_title = win32gui.GetWindowText(hwnd)
                    if not window_title:
                        return True
                    
                    class_name = win32gui.GetClassName(hwnd)
                    
                    # More comprehensive filtering
                    excluded_classes = [
                        'Shell_TrayWnd', 'DV2ControlHost', 'MsgrIMEWindowClass', 
                        'SysShadow', 'Button', 'Windows.UI.Core.CoreWindow',
                        'ApplicationFrameWindow'  # Some UWP app containers
                    ]
                    
                    excluded_titles = [
                        'Program Manager', 'Microsoft Text Input Application',
                        'MSCTFIME UI', 'Default IME'
                    ]
                    
                    # Filter out system windows
                    if class_name in excluded_classes:
                        return True
                    
                    # Filter out specific titles
                    if any(window_title.startswith(excluded) for excluded in excluded_titles):
                        return True
                    
                    # Check if window is actually visible (not minimized)
                    placement = win32gui.GetWindowPlacement(hwnd)
                    if placement[1] == win32con.SW_SHOWMINIMIZED:
                        return True
                    
                    results.append((hwnd, window_title))
            except Exception:
                pass  # Skip windows that cause errors
            return True
        
        windows = []
        win32gui.EnumWindows(enum_callback, windows)
        return windows
    
    def _switch_window_forward(self):
        """Switch to the next window in the list"""
        try:
            # Get current foreground window
            current_hwnd = win32gui.GetForegroundWindow()
            
            # Get all visible windows
            windows = self._get_visible_windows()
            
            if len(windows) <= 1:
                print("⚠ No other windows to switch to")
                return
            
            print(f"\nFound {len(windows)} windows:")
            for hwnd, title in windows:
                marker = " <- CURRENT" if hwnd == current_hwnd else ""
                print(f"  - {title}{marker}")
            
            # Find current window index
            current_index = -1
            for i, (hwnd, title) in enumerate(windows):
                if hwnd == current_hwnd:
                    current_index = i
                    break
            
            # Switch to next window
            next_index = (current_index + 1) % len(windows)
            next_hwnd, next_title = windows[next_index]
            
            print(f"\n✓ Switching to: {next_title}")
            
            # Force window to foreground with multiple attempts
            import win32process
            
            # Get the thread IDs
            current_thread = win32process.GetCurrentThreadId()
            target_thread, _ = win32process.GetWindowThreadProcessId(next_hwnd)
            
            # Attach to target thread to force focus
            if current_thread != target_thread:
                win32process.AttachThreadInput(current_thread, target_thread, True)
            
            # Show and focus the window
            win32gui.ShowWindow(next_hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(next_hwnd)
            win32gui.BringWindowToTop(next_hwnd)
            
            # Detach
            if current_thread != target_thread:
                win32process.AttachThreadInput(current_thread, target_thread, False)
            
        except Exception as e:
            print(f"⚠ Error switching window: {e}")
            import traceback
            traceback.print_exc()
            # Fallback to alt+tab
            keyboard.send("alt+tab")
    
    def _switch_window_backward(self):
        """Switch to the previous window in the list"""
        try:
            # Get current foreground window
            current_hwnd = win32gui.GetForegroundWindow()
            
            # Get all visible windows
            windows = self._get_visible_windows()
            
            if len(windows) <= 1:
                print("⚠ No other windows to switch to")
                return
            
            print(f"\nFound {len(windows)} windows:")
            for hwnd, title in windows:
                marker = " <- CURRENT" if hwnd == current_hwnd else ""
                print(f"  - {title}{marker}")
            
            # Find current window index
            current_index = -1
            for i, (hwnd, title) in enumerate(windows):
                if hwnd == current_hwnd:
                    current_index = i
                    break
            
            # Switch to previous window
            prev_index = (current_index - 1) % len(windows)
            prev_hwnd, prev_title = windows[prev_index]
            
            print(f"\n✓ Switching to: {prev_title}")
            
            # Force window to foreground with multiple attempts
            import win32process
            
            # Get the thread IDs
            current_thread = win32process.GetCurrentThreadId()
            target_thread, _ = win32process.GetWindowThreadProcessId(prev_hwnd)
            
            # Attach to target thread to force focus
            if current_thread != target_thread:
                win32process.AttachThreadInput(current_thread, target_thread, True)
            
            # Show and focus the window
            win32gui.ShowWindow(prev_hwnd, win32con.SW_RESTORE)
            win32gui.SetForegroundWindow(prev_hwnd)
            win32gui.BringWindowToTop(prev_hwnd)
            
            # Detach
            if current_thread != target_thread:
                win32process.AttachThreadInput(current_thread, target_thread, False)
            
        except Exception as e:
            print(f"⚠ Error switching window: {e}")
            import traceback
            traceback.print_exc()
            # Fallback to alt+shift+tab
            keyboard.send("alt+shift+tab")
            
            print("======================\n")

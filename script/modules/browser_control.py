import platform
import pyautogui
import time
import pygetwindow as gw

# Use keyboard library for better Windows hotkey support
if platform.system() == "Windows":
    import keyboard


class BrowserControl:
    def __init__(self, hand_tracker):
        self.hand_tracker = hand_tracker
        self.browser_names = ['Chrome', 'Firefox', 'Edge', 'Opera', 'Brave', 'Safari', 'Vivaldi']
        self.browser_focused = False  # Track if browser is already focused
    
    def focus_browser(self, force=False):
        """Find and focus a browser window only if not already focused"""
        # Skip if already focused (unless forced)
        if self.browser_focused and not force:
            return True
            
        try:
            all_windows = gw.getAllTitles()
            for window_title in all_windows:
                for browser in self.browser_names:
                    if browser.lower() in window_title.lower() and window_title:
                        try:
                            browser_window = gw.getWindowsWithTitle(window_title)[0]
                            if browser_window.isMinimized:
                                browser_window.restore()
                            browser_window.activate()
                            time.sleep(0.15)  # Increased wait for proper focus
                            self.browser_focused = True
                            print(f"  ✓ Focused browser: {window_title[:50]}")
                            return True
                        except Exception as e:
                            continue
            print("  ⚠ No browser window found - command may not work")
            self.browser_focused = False
            return False
        except Exception as e:
            print(f"  ⚠ Error focusing browser: {e}")
            self.browser_focused = False
            return False

    def tab_nav(self, raised_fingers):
        if raised_fingers is not None and raised_fingers != [0, 0, 0, 0, 0]:
            print(f"\n=== BROWSER CONTROL ===")
            print(f"Right hand fingers: {raised_fingers}")
            
            # Focus browser ONCE at the start of control session
            browser_ready = self.focus_browser()
            
            if not browser_ready:
                print("⚠ Cannot execute - no browser window found")
                print("======================\n")
                return
            
            if raised_fingers == [1, 0, 0, 0, 0]:
                # switch tab backward, gesture: thumb
                print("Action: Switching to previous tab (Ctrl+Shift+Tab)")
                if platform.system() == "Darwin":
                    pyautogui.hotkey("command", "shift", "[")
                elif platform.system() == "Windows":
                    keyboard.send("ctrl+shift+tab")
                time.sleep(0.05)
                print("✓ Command sent")
                
            elif raised_fingers == [0, 0, 0, 0, 1]:
                # switch tab forward, gesture: little
                print("Action: Switching to next tab (Ctrl+Tab)")
                if platform.system() == "Darwin":
                    pyautogui.hotkey("command", "shift", "]")
                elif platform.system() == "Windows":
                    keyboard.send("ctrl+tab")
                time.sleep(0.05)
                print("✓ Command sent")
                
            elif raised_fingers == [1, 1, 1, 1, 1]:
                # close tab, gesture: all
                print("Action: Closing tab (Ctrl+W)")
                if platform.system() == "Darwin":
                    pyautogui.hotkey("command", "w")
                elif platform.system() == "Windows":
                    keyboard.send("ctrl+w")
                time.sleep(0.05)
                print("✓ Command sent")
                
            elif raised_fingers == [0, 0, 0, 1, 1]:
                # new tab, gesture: ring and little
                print("Action: Opening new tab (Ctrl+T)")
                if platform.system() == "Darwin":
                    pyautogui.hotkey("command", "t")
                elif platform.system() == "Windows":
                    keyboard.send("ctrl+t")
                time.sleep(0.05)
                print("✓ Command sent")
                
            elif raised_fingers == [0, 1, 0, 0, 1]:
                # reopen closed tab, gesture: index and little
                print("Action: Reopening closed tab (Ctrl+Shift+T)")
                if platform.system() == "Darwin":
                    pyautogui.hotkey("command", "shift", "t")
                elif platform.system() == "Windows":
                    keyboard.send("ctrl+shift+t")
                time.sleep(0.05)
                print("✓ Command sent")
                
            elif raised_fingers == [0, 1, 1, 1, 1]:
                # new window, gesture: index, middle, ring and little
                print("Action: Opening new window (Ctrl+N)")
                # Only open new window if no browser was focused initially
                if not self.browser_focused:
                    print("⚠ No browser running - skipping new window command")
                else:
                    if platform.system() == "Darwin":
                        pyautogui.hotkey("command", "n")
                    elif platform.system() == "Windows":
                        keyboard.send("ctrl+n")
                    time.sleep(0.05)
                    print("✓ Command sent")
            else:
                print(f"⚠ Unknown finger pattern for browser control")
            
            print("======================\n")

"""
Gesture Control Engine - Core gesture recognition and mode switching

Author: Rohan S.
GitHub: https://github.com/Rohan9731
Email: rohanrony8431@gmail.com
"""

import cv2
import json
from script.modules.tracker import HandTracker
from script.modules.media_and_brightness_control import MediaControl
from script.modules.app_control import AppControl
from script.modules.browser_control import BrowserControl
from script.modules.user_def_controls import UserDefControls
from script.modules.mouse_control import MouseControl
from script.modules.game_control import GameControl
from script.modules.virtual_keyboard import VirtualKeyboard


class GestureControl:
    def __init__(self, runFlag=True):
        self.prev_gesture = None
        self.current_gesture = None
        self.mouse_control_active = False
        self.runFlag = runFlag
        self.last_action_key = None  # Track last action performed
        self.action_cooldown = 0  # Short cooldown between same actions
        self.gesture_stability_counter = 0  # Counter for gesture stability
        self.gesture_stability_threshold = 2  # Reduced to 2 frames for faster response
        self.last_right_hand_gesture = None  # Track right hand gesture for stability
        self.temp_gesture = None  # Track temporary detected gesture
        self.media_control_instance = None  # Persistent media control instance
        self.current_frame = None  # Store current frame for GUI display
        self.current_mode = "Standby"  # Current mode name
        self.current_action = "Waiting for gesture..."  # Current action description
        self.virtual_keyboard = None  # Virtual keyboard instance

    def detect_gesture(self, raised_fingers):
        gestures = {
            (0, 0, 0, 0, 1): "thumb",
            (1, 0, 0, 0, 0): "little",
            (0, 0, 0, 1, 1): "thumb and index",
            (0, 0, 1, 1, 1): "thumb, index and middle",
            (0, 1, 1, 1, 1): "thumb, index, middle and ring",
            (0, 0, 0, 1, 0): "index",
            (0, 0, 1, 1, 0): "index and middle",
            (0, 1, 1, 1, 0): "index, middle and ring",
            (1, 1, 1, 1, 0): "index, middle, ring and little",
            (1, 0, 0, 1, 0): "index and little",  # Fixed: [little, ring, middle, index, thumb]
            (1, 1, 1, 1, 1): "all",
        }
        return gestures.get(tuple(raised_fingers))
    
    def get_keyboard_target_app(self):
        """Load the target app name for keyboard gesture from user_defined_data.json"""
        try:
            with open("./script/modules/user_defined_data.json", "r") as file:
                data = json.load(file)
                # Get the app configured for "index, middle, ring and little" gesture (keyboard)
                keyboard_gesture_config = data.get("userDefinedControls", {}).get("index, middle, ring and little")
                
                if keyboard_gesture_config and keyboard_gesture_config != "null":
                    # keyboard_gesture_config is a shellName array like ["notepad.exe"]
                    # Extract display name from the first shell command
                    if isinstance(keyboard_gesture_config, list) and len(keyboard_gesture_config) > 0:
                        shell_name = keyboard_gesture_config[0]
                        # Extract app name from shell command (e.g., "notepad.exe" -> "notepad")
                        # or from path like "C:\\...\\app.exe" -> "app"
                        if "\\" in shell_name or "/" in shell_name:
                            app_name = shell_name.split("\\")[-1].split("/")[-1]
                        else:
                            app_name = shell_name
                        
                        # Remove .exe extension if present
                        if app_name.lower().endswith(".exe"):
                            app_name = app_name[:-4]
                        
                        print(f"✓ Keyboard will focus app: {app_name}")
                        return app_name
                    
                print("⚠ No app configured for keyboard gesture")
                return None
        except Exception as e:
            print(f"⚠ Error loading keyboard target app: {e}")
            return None
    

    def run(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # CAP_DSHOW for faster Windows camera init
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)  # Set FPS for better performance
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce buffer for lower latency
        self.hand_tracker = HandTracker()
        self.media_control_instance = MediaControl(self.hand_tracker)  # Create persistent instance
        
        # Get target app for keyboard and initialize virtual keyboard with it
        keyboard_target_app = self.get_keyboard_target_app()
        self.virtual_keyboard = VirtualKeyboard(self.hand_tracker, keyboard_target_app)  # Initialize virtual keyboard with target app
        print("✓ Camera initialized - Show your hands to the camera")
        hands_detected = False
        
        while True:
            success, frame = self.cap.read()
            if not success or not self.runFlag:
                exit(0)
            frame = cv2.flip(frame, 1)
            
            # Store frame for GUI display
            self.current_frame = frame.copy()
            
            results = self.hand_tracker.hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            if results.multi_hand_landmarks:
                if not hands_detected:
                    print("✓ Hands detected! Processing gestures...")
                    hands_detected = True
                    
                # Decrease action cooldown counter
                if self.action_cooldown > 0:
                    self.action_cooldown -= 1
                
                for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                    # Get correct handedness for each hand
                    handedness = results.multi_handedness[idx].classification[0].label
                    raised_fingers = self.hand_tracker.detect_raised_fingers(
                        hand_landmarks, handedness.lower(), self.mouse_control_active
                    )
                    
                    # LEFT HAND: Gesture detection (stable)
                    if handedness.lower() == "left" and raised_fingers is not None:
                        detected_gesture = self.detect_gesture(raised_fingers)
                        
                        # Debug: Show what's detected
                        if detected_gesture:
                            print(f"[DETECT] Left hand: {raised_fingers} → {detected_gesture}")
                        
                        # Check if gesture changed
                        if detected_gesture != self.temp_gesture:
                            self.temp_gesture = detected_gesture
                            self.gesture_stability_counter = 1  # Start counting for stability
                        else:
                            self.gesture_stability_counter += 1
                        
                        # Only update current gesture if stable for threshold frames
                        if self.gesture_stability_counter >= self.gesture_stability_threshold:
                            if detected_gesture and detected_gesture != self.current_gesture:
                                self.current_gesture = detected_gesture
                                print(f"✓ [STABLE] Left hand gesture confirmed: {self.current_gesture}")
                                self.last_action_key = None  # Reset when gesture changes
                                self.action_cooldown = 0
                                
                                # Update mode immediately when left hand gesture is confirmed
                                if self.current_gesture == "thumb":
                                    self.current_mode = "Volume Control"
                                    self.current_action = "Pinch: Decrease | Expand: Increase"
                                elif self.current_gesture == "thumb and index":
                                    self.current_mode = "Brightness Control"
                                    self.current_action = "Pinch: Decrease | Expand: Increase"
                                elif self.current_gesture == "thumb, index and middle":
                                    self.current_mode = "Media Control"
                                    self.current_action = "Thumb: Previous | Little: Next | All: Play/Pause"
                                elif self.current_gesture == "index":
                                    self.current_mode = "Window Control"
                                    self.current_action = "Little: Next | Thumb: Previous | All: Desktop"
                                elif self.current_gesture == "index and middle":
                                    self.current_mode = "Browser Control"
                                    self.current_action = "Thumb: Previous | Little: Next | All: Close"
                                elif self.current_gesture == "index, middle and ring":
                                    self.current_mode = "Mouse Control"
                                    self.current_action = "Index+Middle: Move | Index: Click"
                                elif self.current_gesture == "index and little":
                                    self.current_mode = "Game Control"
                                    self.current_action = "Index: Jump | Thumb: Left | Little: Right"
                                elif self.current_gesture == "index, middle, ring and little":
                                    self.current_mode = "Virtual Keyboard"
                                    self.current_action = "Point & Pinch to Type"
                                elif self.current_gesture == "all":
                                    self.current_mode = "Custom App Launch"
                                    self.current_action = "Index: App1 | Index+Middle: App2 | etc."

                    # RIGHT HAND: Execute controls based on left hand gesture
                    if handedness.lower() == "right" and raised_fingers is not None:
                        # Debug output
                        if self.current_gesture:
                            print(f"[RIGHT] Fingers: {raised_fingers} | Mode: {self.current_gesture}")
                        
                        # Also stabilize right hand gesture
                        right_hand_gesture = str(raised_fingers)
                        if right_hand_gesture != self.last_right_hand_gesture:
                            self.last_right_hand_gesture = right_hand_gesture
                        
                        action_key = f"{self.current_gesture}_{raised_fingers}"
                        
                        # Check if we should execute (different action OR cooldown expired)
                        can_execute = (action_key != self.last_action_key) or (self.action_cooldown == 0)
                        
                        # volume control, left gesture: thumb (continuous, no cooldown)
                        if self.current_gesture == "thumb":
                            self.current_mode = "Volume Control"
                            self.current_action = "Pinch: Decrease | Expand: Increase"
                            volume_control = MediaControl(self.hand_tracker)
                            volume_control.control_volume(frame)

                        # brightness control, left gesture: thumb and index (continuous, no cooldown)
                        elif self.current_gesture == "thumb and index":
                            self.current_mode = "Brightness Control"
                            self.current_action = "Pinch: Decrease | Expand: Increase"
                            brightness_control = MediaControl(self.hand_tracker)
                            brightness_control.control_brightness(frame)

                        # media control, left gesture: thumb, index and middle (no can_execute check - needs continuous calls for buffering)
                        elif self.current_gesture == "thumb, index and middle":
                            self.current_mode = "Media Control"
                            # Update action based on right hand gesture
                            if raised_fingers == [1, 0, 0, 0, 0]:
                                self.current_action = "Previous Track"
                            elif raised_fingers == [0, 0, 0, 0, 1]:
                                self.current_action = "Next Track"
                            elif raised_fingers == [1, 1, 1, 1, 1]:
                                self.current_action = "Play/Pause"
                            elif raised_fingers == [0, 1, 1, 1, 0]:
                                self.current_action = "Mute/Unmute"
                            else:
                                self.current_action = "Thumb: Previous | Little: Next | All: Play/Pause"
                            self.media_control_instance.control_media(raised_fingers)
                            # Note: media_control handles its own cooldown/repeat prevention internally
                        
                        # Virtual keyboard, left gesture: index, middle, ring and little
                        elif self.current_gesture == "index, middle, ring and little":
                            self.current_mode = "Virtual Keyboard"
                            self.current_action = "Point & Pinch to Type"
                            # Process keyboard with right hand - pass results for hand detection
                            frame = self.virtual_keyboard.process(frame, results)

                        # app control (window switching), left gesture: index
                        elif self.current_gesture == "index" and can_execute:
                            self.current_mode = "Window Control"
                            # Update action based on right hand gesture
                            if raised_fingers == [0, 0, 0, 0, 1]:
                                self.current_action = "Switch Window Forward"
                            elif raised_fingers == [1, 0, 0, 0, 0]:
                                self.current_action = "Switch Window Backward"
                            elif raised_fingers == [1, 1, 1, 1, 1]:
                                self.current_action = "Show Desktop"
                            elif raised_fingers == [0, 0, 0, 1, 1]:
                                self.current_action = "Close Window (Alt+F4)"
                            elif raised_fingers == [0, 1, 0, 0, 1]:
                                self.current_action = "Switch Within App"
                            elif raised_fingers == [0, 1, 1, 1, 1]:
                                self.current_action = "Close Current Tab (Ctrl+W)"
                            else:
                                self.current_action = "Little: Next | Thumb: Previous | All: Desktop"
                            app_control = AppControl(self.hand_tracker)
                            app_control.window_nav(raised_fingers)
                            self.last_action_key = action_key
                            self.action_cooldown = 20  # Short cooldown

                        # browser control, left gesture: index and middle
                        elif self.current_gesture == "index and middle" and can_execute:
                            self.current_mode = "Browser Control"
                            # Update action based on right hand gesture
                            if raised_fingers == [1, 0, 0, 0, 0]:
                                self.current_action = "Previous Tab"
                            elif raised_fingers == [0, 0, 0, 0, 1]:
                                self.current_action = "Next Tab"
                            elif raised_fingers == [1, 1, 1, 1, 1]:
                                self.current_action = "Close Tab"
                            elif raised_fingers == [0, 0, 0, 1, 1]:
                                self.current_action = "New Tab"
                            elif raised_fingers == [0, 1, 0, 0, 1]:
                                self.current_action = "Reopen Last Tab"
                            elif raised_fingers == [0, 1, 1, 1, 1]:
                                self.current_action = "New Window"
                            else:
                                self.current_action = "Thumb: Previous | Little: Next | All: Close"
                            browser_control = BrowserControl(self.hand_tracker)
                            browser_control.tab_nav(raised_fingers)
                            self.last_action_key = action_key
                            self.action_cooldown = 20  # Short cooldown to prevent accidental repeats

                        # mouse control, left gesture: index, middle and ring
                        elif self.current_gesture == "index, middle and ring":
                            self.current_mode = "Mouse Control"
                            # Update action based on right hand gesture
                            if raised_fingers == [0, 1, 1, 0, 0]:
                                self.current_action = "Moving Cursor"
                            elif raised_fingers == [0, 0, 0, 1, 0]:
                                self.current_action = "Left Click"
                            elif raised_fingers == [0, 1, 0, 0, 0]:
                                self.current_action = "Right Click"
                            elif raised_fingers == [1, 1, 1, 1, 1]:
                                self.current_action = "Scroll Down"
                            elif raised_fingers == [0, 1, 1, 1, 1]:
                                self.current_action = "Scroll Up"
                            else:
                                self.current_action = "Index+Middle: Move | Index: Click"
                            self.mouse_control_active = True
                            mouse_control = MouseControl(self.hand_tracker)
                            mouse_control.control_mouse(raised_fingers, frame)

                        # game control, left gesture: index and little (instant, no cooldown like game-simulator-lite)
                        elif self.current_gesture == "index and little":
                            self.current_mode = "Game Control"
                            # Update action based on right hand gesture
                            if raised_fingers == [0, 1, 0, 0, 0]:
                                self.current_action = "Jump/Forward (↑)"
                            elif raised_fingers == [0, 1, 1, 0, 0]:
                                self.current_action = "Slide/Down (↓)"
                            elif raised_fingers == [1, 0, 0, 0, 0]:
                                self.current_action = "Move Left (←)"
                            elif raised_fingers == [0, 0, 0, 0, 1]:
                                self.current_action = "Move Right (→)"
                            elif raised_fingers == [1, 1, 0, 0, 0]:
                                self.current_action = "Action (Space)"
                            else:
                                self.current_action = "Index: Jump | Thumb: Left | Little: Right"
                            game_control = GameControl(self.hand_tracker)
                            game_control.game_nav(raised_fingers)

                        # user defined controls, left gesture: all
                        elif self.current_gesture == "all" and can_execute:
                            self.current_mode = "Custom App Launch"
                            # Update action based on right hand gesture
                            if raised_fingers == [0, 1, 0, 0, 0]:
                                self.current_action = "Launch App 1"
                            elif raised_fingers == [0, 1, 1, 0, 0]:
                                self.current_action = "Launch App 2"
                            elif raised_fingers == [0, 1, 1, 1, 0]:
                                self.current_action = "Launch App 3"
                            elif raised_fingers == [0, 1, 1, 1, 1]:
                                self.current_action = "Launch App 4"
                            elif raised_fingers == [1, 0, 0, 0, 0]:
                                self.current_action = "Launch App 5"
                            else:
                                self.current_action = "Index: App1 | Index+Middle: App2 | etc."
                            user_def_controls = UserDefControls(self.hand_tracker)
                            user_def_controls.user_controls(raised_fingers)
                            self.last_action_key = action_key
                            self.action_cooldown = 20  # Short cooldown
                        
                        # Reset mouse control for other gestures
                        if self.current_gesture != "index, middle and ring":
                            self.mouse_control_active = False
                
                # Close keyboard when switching away from keyboard mode
                if self.current_gesture != "index, middle, ring and little" and self.virtual_keyboard.window_created:
                    self.virtual_keyboard.close_keyboard_window()
            else:
                # Reset when no hands detected
                if hands_detected:
                    hands_detected = False
                    print("⚠ No hands detected - show hands to camera")
                self.mouse_control_active = False
                # Don't reset mode - it should persist until user selects a different mode
                # Only show action hint when hands are not detected
                if self.current_mode != "Standby":
                    self.current_action = "Show hands to continue..."

            if not self.mouse_control_active:
                self.hand_tracker.frame_counter += 1

            # No longer display cv2 window - GUI will handle display
            # cv2.imshow("Frame", frame)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        self.cap.release()
        # cv2.destroyAllWindows()  # Not needed since we don't create windows
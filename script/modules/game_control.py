import platform
import pyautogui

try:
    import keyboard
    USE_KEYBOARD = True
except ImportError:
    USE_KEYBOARD = False
    print("⚠ keyboard library not installed - using pyautogui (may not work in all games)")


class GameControl:
    def __init__(self, hand_tracker):
        self.hand_tracker = hand_tracker
        self.last_finger_position = ""  # Track last gesture to prevent repeats

    def game_nav(self, raised_fingers):
        """
        Game controls mapped to gestures:
        - Index only (01000) → Jump/Forward (↑ / W)
        - Index + Middle (01100) → Slide/Backward (↓ / S)
        - Thumb only (10000) → Move Left (←)
        - Pinky only (00001) → Move Right (→)
        - Thumb + Index (11000) → Special action (Space)
        """
        if raised_fingers is not None and raised_fingers != [0, 0, 0, 0, 0]:
            current_position = str(raised_fingers)
            
            # Only execute if gesture changed (like game-simulator-lite)
            if current_position == self.last_finger_position:
                return
            
            self.last_finger_position = current_position
            print(f"\n=== GAME CONTROL ===")
            print(f"Right hand fingers: {raised_fingers}")

            if platform.system() == "Windows":
                # Index only - Jump/Forward (↑ or W)
                if raised_fingers == [0, 1, 0, 0, 0]:
                    print("Action: Jump/Forward (↑)")
                    pyautogui.press("up")
                    print("✓ Jump command sent")

                # Index + Middle - Slide/Backward (↓ or S)
                elif raised_fingers == [0, 1, 1, 0, 0]:
                    print("Action: Slide/Down (↓)")
                    pyautogui.press("down")
                    print("✓ Slide command sent")

                # Thumb only - Move Left (←)
                elif raised_fingers == [1, 0, 0, 0, 0]:
                    print("Action: Move Left (←)")
                    pyautogui.press("left")
                    print("✓ Left command sent")

                # Pinky only - Move Right (→)
                elif raised_fingers == [0, 0, 0, 0, 1]:
                    print("Action: Move Right (→)")
                    pyautogui.press("right")
                    print("✓ Right command sent")

                # Thumb + Index - Special action (Space)
                elif raised_fingers == [1, 1, 0, 0, 0]:
                    print("Action: Special (Space)")
                    if USE_KEYBOARD:
                        keyboard.press_and_release('space')
                    else:
                        pyautogui.press('space')
                    print("✓ Space command sent")

                # Index + Pinky - Alternative jump (for flexibility)
                elif raised_fingers == [0, 1, 0, 0, 1]:
                    print("Action: Alternative Jump (W)")
                    pyautogui.press("w")
                    print("✓ W command sent")

                # Middle + Ring - Alternative slide (for flexibility)
                elif raised_fingers == [0, 0, 1, 1, 0]:
                    print("Action: Alternative Slide (S)")
                    pyautogui.press("s")
                    print("✓ S command sent")

                else:
                    print(f"⚠ Unknown game gesture: {raised_fingers}")

            elif platform.system() == "Darwin":
                # macOS game controls (same keys work)
                if raised_fingers == [0, 1, 0, 0, 0]:
                    pyautogui.press("up")
                elif raised_fingers == [0, 1, 1, 0, 0]:
                    pyautogui.press("down")
                elif raised_fingers == [1, 0, 0, 0, 0]:
                    pyautogui.press("left")
                elif raised_fingers == [0, 0, 0, 0, 1]:
                    pyautogui.press("right")
                elif raised_fingers == [1, 1, 0, 0, 0]:
                    if USE_DIRECTINPUT:
                        pydirectinput.press('space')
                    else:
                        pyautogui.press('space')

            else:
                # Linux support
                if raised_fingers == [0, 1, 0, 0, 0]:
                    pyautogui.press("up")
                elif raised_fingers == [0, 1, 1, 0, 0]:
                    pyautogui.press("down")
                elif raised_fingers == [1, 0, 0, 0, 0]:
                    pyautogui.press("left")
                elif raised_fingers == [0, 0, 0, 0, 1]:
                    pyautogui.press("right")
                elif raised_fingers == [1, 1, 0, 0, 0]:
                    if USE_DIRECTINPUT:
                        pydirectinput.press('space')
                    else:
                        pyautogui.press('space')

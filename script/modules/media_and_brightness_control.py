import numpy as np
import pyautogui
import platform


class MediaControl:
    def __init__(self, hand_tracker):
        self.hand_tracker = hand_tracker

    def control_volume(self, frame):
        landmarks = self.hand_tracker.find_position(frame)
        if landmarks is not None and len(landmarks) != 0:
            x1, y1 = landmarks[4][1], landmarks[4][2]
            x2, y2 = landmarks[8][1], landmarks[8][2]

            mkx, mky = landmarks[9][1], landmarks[9][2]
            wx, wy = landmarks[0][1], landmarks[0][2]

            tipLength = (x2 - x1) ** 2 + (y2 - y1) ** 2
            palmLength = (wx - mkx) ** 2 + (wy - mky) ** 2
            ratio = tipLength / palmLength

            if platform.system() == "Windows":
                # Calculate target volume level (0-100) with same sensitivity as brightness
                target_volume = int(np.interp(ratio, [0.15, 1.5], [0, 100]))
                
                # Store last volume to prevent continuous adjustments
                if not hasattr(self, '_last_volume'):
                    self._last_volume = 50
                if not hasattr(self, '_volume_cooldown'):
                    self._volume_cooldown = 0
                
                # Reduce volume cooldown
                if self._volume_cooldown > 0:
                    self._volume_cooldown -= 1
                    return
                
                volume_diff = target_volume - self._last_volume
                
                # Only adjust if difference is significant (more than 10% like brightness)
                if abs(volume_diff) > 10:
                    import keyboard
                    import time
                    
                    # Press volume up/down keys based on difference
                    steps = abs(volume_diff) // 3  # Each key press is ~2% volume, so divide by 3
                    steps = min(steps, 5)  # Limit to 5 steps per update for smoothness
                    
                    for _ in range(steps):
                        if volume_diff > 0:
                            keyboard.press_and_release('volume up')
                        else:
                            keyboard.press_and_release('volume down')
                        time.sleep(0.02)  # Small delay between presses
                    
                    self._last_volume = target_volume
                    self._volume_cooldown = 3  # Add small cooldown like gesture detection

            elif platform.system() == "Darwin":
                import subprocess

                volume = np.interp(ratio, [0.15, 1.5], [0, 100])
                # print(f"volume: {volume}") TODO: make a better print statement for debug mode where values are 0-100
                subprocess.run(
                    ["osascript", "-e", f"set volume output volume {volume}"]
                )

            else:
                # could have done it for linux, but don't have a linux machine to test
                raise NotImplementedError("This OS is not supported")

    def control_media(self, raised_fingers):
        # not working on darwin
        if raised_fingers is not None and raised_fingers != [0, 0, 0, 0, 0]:
            # Initialize stability tracking
            if not hasattr(self, '_media_gesture_buffer'):
                self._media_gesture_buffer = {}
                self._media_last_executed = None
            
            gesture_key = str(raised_fingers)
            
            # Track gesture stability
            if gesture_key not in self._media_gesture_buffer:
                self._media_gesture_buffer = {gesture_key: 1}  # Reset buffer, start new count
            else:
                self._media_gesture_buffer[gesture_key] += 1
            
            # Only execute if gesture is stable for 3 frames (prevents thumb detection first)
            if self._media_gesture_buffer[gesture_key] < 3:
                print(f"[MEDIA] Buffering: {raised_fingers} ({self._media_gesture_buffer[gesture_key]}/3 frames)")
                return
            
            # Check if we already executed this gesture (prevent repeat execution)
            if self._media_last_executed == gesture_key:
                return
            
            print(f"\n=== MEDIA CONTROL ===")
            print(f"Media gesture stable: {raised_fingers}")
            
            if platform.system() == "Windows":
                # prev track, gesture: thumb
                if raised_fingers == [1, 0, 0, 0, 0]:
                    print("⏮ Previous track")
                    pyautogui.press("prevtrack")
                    self._media_last_executed = gesture_key
                # next track, gesture: little
                elif raised_fingers == [0, 0, 0, 0, 1]:
                    print("⏭ Next track")
                    pyautogui.press("nexttrack")
                    self._media_last_executed = gesture_key
                # play/pause, gesture: all
                elif raised_fingers == [1, 1, 1, 1, 1]:
                    print("⏯ Play/Pause")
                    pyautogui.press("playpause")
                    self._media_last_executed = gesture_key
                # volume mute, gesture: index, middle and ring
                elif raised_fingers == [0, 1, 1, 1, 0]:
                    print("🔇 Volume mute toggle")
                    pyautogui.press("volumemute")
                    self._media_last_executed = gesture_key
                print("✓ Command sent\n")
                
            elif platform.system() == "Darwin":
                # could do it if found the key code for media keys
                pass

            else:
                # could have done it for linux, but don't have a linux machine to test
                raise NotImplementedError("This OS is not supported")
        else:
            # Reset when no fingers raised
            if hasattr(self, '_media_last_executed'):
                self._media_last_executed = None

    def control_brightness(self, frame):
        landmarks = self.hand_tracker.find_position(frame)
        if landmarks is not None and len(landmarks) != 0:
            x1, y1 = landmarks[4][1], landmarks[4][2]
            x2, y2 = landmarks[8][1], landmarks[8][2]

            mkx, mky = landmarks[9][1], landmarks[9][2]
            wx, wy = landmarks[0][1], landmarks[0][2]

            tipLength = (x2 - x1) ** 2 + (y2 - y1) ** 2
            palmLength = (wx - mkx) ** 2 + (wy - mky) ** 2

            ratio = tipLength / palmLength

            if platform.system() == "Windows":
                import screen_brightness_control as sbc

                brightness = int(np.interp(ratio, [0.15, 1.5], [0, 100]))
                sbc.set_brightness(brightness)

            elif platform.system() == "Darwin":
                # this only works on apple silicon if you have the brightness cli tool, which should be built from source
                # link to repo: https://github.com/nriley/brightness
                import subprocess

                brightness = np.interp(ratio, [0.15, 1.5], [0, 1])
                # print(f"brightness: {brightness}") TODO: make a better print statement for debug mode where values are 0-100
                subprocess.run(["brightness", str(brightness)])

            else:
                # could have done it for linux, but don't have a linux machine to test
                raise NotImplementedError("This OS is not supported")

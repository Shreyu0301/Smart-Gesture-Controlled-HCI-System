import json
import subprocess
import os
import time
import sys


class UserDefControls:
    def __init__(self, hand_tracker):
        self.hand_tracker = hand_tracker
        self.last_launched_gesture = None  # Track last launched gesture
        self.launch_time = 0  # Track when last gesture was executed
        self.launch_cooldown = 1.0  # Minimum seconds between same gesture launches

        # Load the JSON file
        try:
            with open("./script/modules/user_defined_data.json", "r") as file:
                self.app_data = json.load(file)
                print("[DEBUG] Loaded user_defined_data.json successfully")
        except Exception as e:
            print(f"[ERROR] Failed to load user_defined_data.json: {e}")
            self.app_data = {"userDefinedControls": {}}

        self.gesture_map = {
            "[0, 1, 0, 0, 0]": "index",
            "[0, 1, 1, 0, 0]": "index and middle",
            "[0, 1, 1, 1, 0]": "index, middle and ring",
            "[0, 1, 1, 1, 1]": "index, middle, ring and little",
            "[1, 0, 0, 0, 0]": "thumb",
        }

    def launch_single_app(self, cmd):
        """Launch a single app with proper Windows handling"""
        try:
            cmd_str = str(cmd).strip()
            
            if not cmd_str or cmd_str == "null":
                print(f"  ⚠ Empty or null command - skipping")
                return False
            
            # Expand environment variables like %USERNAME%
            cmd_str = os.path.expandvars(cmd_str)
            
            # Check if it's a Windows Settings URI (ms-settings, etc.)
            if cmd_str.startswith("ms-") or cmd_str.startswith("microsoft.") or cmd_str.startswith("mailto:"):
                print(f"  → Launching Windows URI: {cmd_str}")
                # Use explorer to open Windows URIs reliably
                subprocess.Popen(['explorer', cmd_str], shell=False)
                time.sleep(0.3)
                return True
            
            # Check if it's a full path to an executable
            elif ("\\" in cmd_str or ":/" in cmd_str):
                if os.path.exists(cmd_str):
                    print(f"  → Launching from full path: {cmd_str}")
                    subprocess.Popen(cmd_str)
                    time.sleep(0.3)
                    return True
                else:
                    print(f"  ⚠ Path does not exist: {cmd_str}, trying next option...")
                    return False
            
            # For common Windows executables (calc.exe, notepad.exe, chrome.exe, etc.)
            else:
                print(f"  → Launching Windows app: {cmd_str}")
                # Use 'start' command which searches Windows PATH
                subprocess.Popen(f'start "" "{cmd_str}"', shell=True)
                time.sleep(0.3)
                return True
                
        except Exception as e:
            print(f"  ✗ Error launching {cmd}: {e}")
            return False
    
    def launch_app_from_array(self, app_array):
        """
        Launch the appropriate app from array.
        Priority: Windows URIs first (ms-, microsoft., mailto:), then executables
        Tries multiple paths until one succeeds
        """
        if not app_array:
            return False
        
        # Separate Windows URIs from executables
        windows_uris = [app for app in app_array if isinstance(app, str) and 
                       (app.startswith("ms-") or app.startswith("microsoft.") or app.startswith("mailto:"))]
        executables = [app for app in app_array if isinstance(app, str) and 
                       not (app.startswith("ms-") or app.startswith("microsoft.") or app.startswith("mailto:"))]
        
        # Try Windows URIs first (they're usually the "real" app)
        if windows_uris:
            app_to_launch = windows_uris[0].strip()
            print(f"  → Selected Windows URI from array: {app_to_launch}")
            if self.launch_single_app(app_to_launch):
                return True
        
        # Then try all executables in order until one succeeds
        if executables:
            for app_path in executables:
                app_to_launch = app_path.strip()
                print(f"  → Trying executable: {app_to_launch}")
                if self.launch_single_app(app_to_launch):
                    return True
        
        return False

    def user_controls(self, raised_fingers):
        if raised_fingers is None or raised_fingers == [0, 0, 0, 0, 0]:
            return
            
        gesture_str = str(raised_fingers)
        print(f"\n{'='*50}")
        print(f"USER DEFINED CONTROL - RIGHT HAND GESTURE")
        print(f"Fingers raised: {raised_fingers}")
        print(f"{'='*50}")
        
        if gesture_str not in self.gesture_map:
            print(f"✗ Unknown finger pattern: {gesture_str}")
            print(f"{'='*50}\n")
            return
        
        gesture_name = self.gesture_map[gesture_str]
        print(f"Gesture detected: '{gesture_name}'")
        
        # Check if this gesture has been executed recently (cooldown check)
        current_time = time.time()
        if (self.last_launched_gesture == gesture_name and 
            current_time - self.launch_time < self.launch_cooldown):
            remaining = self.launch_cooldown - (current_time - self.launch_time)
            print(f"⚠ Cooldown active ({remaining:.2f}s remaining)")
            print(f"{'='*50}\n")
            return
        
        # Get the app configuration for this gesture
        user_controls = self.app_data.get("userDefinedControls", {})
        apps_config = user_controls.get(gesture_name)
        
        print(f"[CONFIG] Raw config: {apps_config}")
        
        if not apps_config:
            print(f"✗ No app configured for gesture '{gesture_name}'")
            print(f"{'='*50}\n")
            return
        
        # Handle both list and string formats
        if isinstance(apps_config, str):
            # Single app stored as string
            app_list = [apps_config]
        elif isinstance(apps_config, list):
            # Multiple apps stored as array
            app_list = apps_config
        else:
            print(f"✗ Invalid app configuration format: {type(apps_config)}")
            print(f"{'='*50}\n")
            return
        
        # Filter out null/empty values
        app_list = [app for app in app_list if app and app != "null"]
        
        if not app_list:
            print(f"✗ No valid apps configured for gesture '{gesture_name}'")
            print(f"{'='*50}\n")
            return
        
        print(f"[CONFIG] Filtered apps: {app_list}")
        print(f"→ Attempting to launch from array with {len(app_list)} app(s)")
        
        # Use smart app selection (prioritizes Windows URIs)
        if self.launch_app_from_array(app_list):
            self.last_launched_gesture = gesture_name
            self.launch_time = current_time
            print(f"✓ Successfully executed gesture '{gesture_name}'")
        else:
            print(f"✗ Failed to execute gesture '{gesture_name}'")
        
        print(f"{'='*50}\n")

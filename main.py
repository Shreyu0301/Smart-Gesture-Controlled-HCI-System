"""
Smart Gesture-Controlled Human-Computer Interaction System

Author: Rohan S.
LinkedIn: https://www.linkedin.com/in/rohan-s-43201a2a3
GitHub: https://github.com/Rohan9731
Email: rohanrony8431@gmail.com

Description: Enterprise-grade HCI system for touchless computer control
through natural hand gestures using computer vision and machine learning.
"""

import customtkinter
import json
import uuid
import socket
import pymongo
from dotenv import load_dotenv
import os
from script.gesture_control import GestureControl
import threading
from script.modules.GestureAnimation import GestureAnimation
from PIL import Image, ImageTk
import cv2

load_dotenv()

def get_unique_id():
    mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
    hostname = socket.gethostname()
    return f"{mac}-{hostname}"

unique_id = get_unique_id()
print(unique_id)

client = pymongo.MongoClient(os.getenv("MONGODB.URI"))

db = client["hci"]

collection = db["user-config"]

customGestureJson = collection.find_one({"_id": unique_id})

f = open("resources\\appList.json", "r")
data = json.load(f)

f = open("resources\\anim_data.json", "r")
anim_data = json.load(f)

if customGestureJson == None:
    collection.insert_one(
        {
            "_id": unique_id,
            "name": socket.gethostname(),
            "userDefinedControls": {
                "index": "null",
                "index and middle": "null",
                "index, middle and ring": "null",
                "index, middle, ring and little": "null",
                "thumb": "null",
            },
        }
    )

    customGestureJson = collection.find_one({"_id": unique_id})

    with open("./script/modules/user_defined_data.json", "w") as f:
        json.dump(customGestureJson, f)

app = customtkinter.CTk()
app.title("Smart Gesture-Controlled HCI System")
app.geometry("1100x600")
app.iconbitmap("resources\\dark.ico")

# system mode
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

# Create main container frame
main_container = customtkinter.CTkFrame(app, fg_color="transparent")
main_container.pack(fill="both", expand=True)

# Create left side frame (for all screens)
left_side_frame = customtkinter.CTkFrame(
    main_container, 
    fg_color="transparent",
    corner_radius=25,
    border_width=2,
    border_color="#000000"
)
left_side_frame.pack(side="left", fill="both", expand=True, padx=(20, 10), pady=20)

# Create right side frame (for video - always visible)
right_side_frame = customtkinter.CTkFrame(
    main_container,
    fg_color="transparent",
    corner_radius=25,
    border_width=2,
    border_color="#000000"
)
right_side_frame.pack(side="right", fill="both", padx=(10, 20), pady=20)

# Create frames for different screens (all go in left_side_frame)
menuFrame = customtkinter.CTkFrame(left_side_frame, fg_color="transparent")
customiseFrame = customtkinter.CTkFrame(left_side_frame, fg_color="transparent")
tutorialFrame = customtkinter.CTkFrame(left_side_frame, fg_color="transparent")


def getAppNames():
    # read a file appList.json and fetch names
    # return the list of app names
    ls = ["Select"]
    for i in data:
        ls.append(i["displayName"])
    return ls


# Function to switch to the second screen
def goToCustomise():
    menuFrame.pack_forget()
    tutorialFrame.pack_forget()
    customiseFrame.pack(fill="both", expand=True, padx=10, pady=10)


# Function to switch to the third screen
def goToTutorial():
    menuFrame.pack_forget()
    customiseFrame.pack_forget()
    tutorialFrame.pack(fill="both", expand=True, padx=10, pady=10)


# Global variable to track gesture control thread
ges_con = None
ges_con_thread = None
is_running = False
video_update_id = None
show_video_feed = False  # Track if video feed should be displayed


# Function to update video frame in GUI
def update_video_frame():
    global ges_con, is_running, video_update_id, show_video_feed
    
    if is_running and ges_con and hasattr(ges_con, 'current_frame') and ges_con.current_frame is not None:
        try:
            # Only update video display if show_video_feed is True
            if show_video_feed:
                # Get the processed frame from gesture control
                frame = ges_con.current_frame.copy()
                
                # Resize for display
                frame = cv2.resize(frame, (480, 320))
                
                # Convert to RGB for tkinter
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                imgtk = ImageTk.PhotoImage(image=img)
                
                # Update label
                video_label.configure(image=imgtk, text="")
                video_label.image = imgtk
            else:
                # Show message when video feed is off
                video_label.configure(image="", text="Camera Feed OFF\n(Running in background)")
                video_label.image = None
            
            # Always update mode and action labels
            if hasattr(ges_con, 'current_mode'):
                mode_label.configure(text=ges_con.current_mode)
            if hasattr(ges_con, 'current_action'):
                action_label.configure(text=ges_con.current_action)
        except Exception as e:
            print(f"Error updating video frame: {e}")
        
        # Schedule next update (33ms for ~30 FPS)
        video_update_id = app.after(33, update_video_frame)
    elif is_running:
        # Still starting up, keep trying
        video_update_id = app.after(100, update_video_frame)
    else:
        # Reset video label when stopped
        video_label.configure(image="", text="Camera Feed\\n(Activate to start)")
        video_label.image = None
        # Reset mode and action
        mode_label.configure(text="Standby")
        action_label.configure(text="Waiting for gesture...")


# Function to run python script
def launchGestureControl():
    global ges_con, ges_con_thread
    
    # If thread is already running, don't start another
    if ges_con_thread and ges_con_thread.is_alive():
        print("The gesture control program is already running. Please wait.")
        return
    
    # Create new GestureControl instance and thread
    ges_con = GestureControl(True)
    ges_con_thread = threading.Thread(target=ges_con.run)
    ges_con_thread.daemon = True  # Allow program to exit even if thread is running
    ges_con_thread.start()
    print("✓ Gesture control program started")


# Function to toggle gesture control
def toggleGestureControl():
    global is_running, ges_con, ges_con_thread, video_update_id
    
    if not is_running:
        # Start gesture control
        if not ges_con_thread or not ges_con_thread.is_alive():
            ges_con = GestureControl(True)
            ges_con_thread = threading.Thread(target=ges_con.run)
            ges_con_thread.daemon = True
            ges_con_thread.start()
            is_running = True
            toggle_switch.configure(text="ON", fg_color="#28a745", progress_color="#28a745")
            status_label.configure(text="● SYSTEM ACTIVE", text_color="#28a745")
            print("✓ Gesture control ACTIVATED")
            
            # Start video frame updates
            update_video_frame()
    else:
        # Stop gesture control
        if ges_con:
            ges_con.runFlag = False
            is_running = False
            
            # Stop video frame updates first
            if video_update_id:
                app.after_cancel(video_update_id)
                video_update_id = None
            
            # Reset video display immediately
            video_label.configure(image="", text="Camera Feed\n(Activate to start)")
            video_label.image = None
            
            # Release camera
            if hasattr(ges_con, 'cap') and ges_con.cap is not None:
                ges_con.cap.release()
                print("✓ Camera released")
            
            # Update UI
            toggle_switch.configure(text="OFF", fg_color="#dc3545", progress_color="#dc3545")
            status_label.configure(text="● SYSTEM INACTIVE", text_color="#dc3545")
            print("✗ Gesture control DEACTIVATED")
            
            # Clear the frame reference
            ges_con.current_frame = None

# Function to switch back to the first screen
def backToMenuFrame():
    customiseFrame.pack_forget()
    tutorialFrame.pack_forget()
    menuFrame.pack(fill="both", expand=True, padx=10, pady=10)


# Function to print "Hello, World!"
def print_hello_world(varName):
    print("Hello, World!", varName)


def saveGestures(data):
    """Save user-selected gestures to database and JSON file"""
    userDefinedControls = {}
    
    # Map each gesture to the app's shellName (which is an array)
    gesture_selections = {
        "index": gesture1_dropdown.get(),
        "index and middle": gesture2_dropdown.get(),
        "index, middle and ring": gesture3_dropdown.get(),
        "index, middle, ring and little": gesture4_dropdown.get(),
        "thumb": gesture5_dropdown.get(),
    }
    
    # Convert display names to shellName arrays
    for gesture_name, selected_app in gesture_selections.items():
        if selected_app == "Select" or not selected_app:
            userDefinedControls[gesture_name] = "null"
        else:
            # Find the shellName array for this app
            found = False
            for app_entry in data:
                if app_entry["displayName"] == selected_app:
                    userDefinedControls[gesture_name] = app_entry["shellName"]
                    found = True
                    break
            if not found:
                userDefinedControls[gesture_name] = "null"
    
    # Update database and JSON file
    if customGestureJson is not None:
        customGestureJson["userDefinedControls"] = userDefinedControls
        collection.update_one({"_id": unique_id}, {"$set": customGestureJson})
        
        # Save to local JSON file
        with open("./script/modules/user_defined_data.json", "w") as f:
            json.dump(customGestureJson, f, indent=2)
        
        print(f"[DEBUG] Gestures saved successfully")
        print(f"[DEBUG] Saved config: {userDefinedControls}")


############################################################################################################
# First screen
menuFrame.pack(fill="both", expand=True, padx=10, pady=10)

# Main title label with gradient effect
title_label = customtkinter.CTkLabel(
    menuFrame, 
    text="SMART GESTURE-CONTROLLED", 
    font=("Segoe UI", 22, "bold"),
    text_color="#728FCE"
)
title_label.pack(pady=(15, 0))

# Subtitle
subtitle_label = customtkinter.CTkLabel(
    menuFrame, 
    text="HUMAN-COMPUTER INTERACTION SYSTEM", 
    font=("Segoe UI", 22, "bold"),
    text_color="#728FCE"
)
subtitle_label.pack(pady=(0, 10))

# Divider line
divider_frame = customtkinter.CTkFrame(menuFrame, height=2, fg_color="#728FCE")
divider_frame.pack(fill="x", padx=60, pady=(8, 20))

# Status label with enhanced styling
status_label = customtkinter.CTkLabel(
    menuFrame,
    text="● SYSTEM INACTIVE",
    font=("Segoe UI", 16, "bold"),
    text_color="#dc3545"
)
status_label.pack(pady=(10, 30))

# Toggle switch frame with enhanced design
toggle_frame = customtkinter.CTkFrame(
    menuFrame, 
    fg_color="#2C3E50",
    corner_radius=20,
    border_width=2,
    border_color="#000000"
)
toggle_frame.pack(pady=25, padx=40, fill="x")

toggle_label = customtkinter.CTkLabel(
    toggle_frame,
    text="⚡ Launch Program:",
    font=("Segoe UI", 18, "bold"),
    text_color="#728FCE"
)
toggle_label.pack(side="left", pady=25, padx=30)

toggle_switch = customtkinter.CTkSwitch(
    toggle_frame,
    text="OFF",
    command=lambda: toggleGestureControl(),
    font=("Segoe UI", 18, "bold"),
    fg_color="#dc3545",
    progress_color="#dc3545",
    button_color="#ffffff",
    button_hover_color="#f0f0f0",
    width=120,
    height=45
)
toggle_switch.pack(side="left", padx=35, pady=25)

customiseButton = customtkinter.CTkButton(
    menuFrame, 
    text="⚙ CUSTOMISE GESTURES", 
    command=lambda: threading.Thread(target=goToCustomise).start(),
    font=("Segoe UI", 16, "bold"),
    fg_color="#728FCE",
    hover_color="#3A7BC8",
    height=55,
    corner_radius=15,
    border_width=0
)
customiseButton.pack(pady=20, padx=40, fill="x")

tutorialButton = customtkinter.CTkButton(
    menuFrame, 
    text="📚 TUTORIAL & GUIDE", 
    command=lambda: goToTutorial(),
    font=("Segoe UI", 17, "bold"),
    fg_color="#728FCE",
    hover_color="#3A7BC8",
    height=55,
    corner_radius=15,
    border_width=0
)
tutorialButton.pack(pady=20, padx=40, fill="x")

############################################################################################################
# Right side - Video frame (always visible)
# Camera Feed Toggle above video
camera_toggle_frame = customtkinter.CTkFrame(
    right_side_frame,
    fg_color="#2C3E50",
    corner_radius=15,
    border_width=2,
    border_color="#000000"
)
camera_toggle_frame.pack(fill="x", pady=(10, 5), padx=10)

camera_toggle_label = customtkinter.CTkLabel(
    camera_toggle_frame,
    text="📹 Show Camera Feed:",
    font=("Segoe UI", 16, "bold"),
    text_color="#728FCE"
)
camera_toggle_label.pack(side="left", pady=15, padx=20)

def toggleCameraFeed():
    global show_video_feed
    show_video_feed = not show_video_feed
    if show_video_feed:
        camera_toggle_switch.configure(text="ON", fg_color="#28a745", progress_color="#28a745")
        print("✓ Camera feed display ENABLED")
    else:
        camera_toggle_switch.configure(text="OFF", fg_color="#dc3545", progress_color="#dc3545")
        print("✗ Camera feed display DISABLED (running in background)")

camera_toggle_switch = customtkinter.CTkSwitch(
    camera_toggle_frame,
    text="OFF",
    command=lambda: toggleCameraFeed(),
    font=("Segoe UI", 16, "bold"),
    fg_color="#dc3545",
    progress_color="#dc3545",
    button_color="#ffffff",
    button_hover_color="#f0f0f0",
    width=100,
    height=40
)
camera_toggle_switch.pack(side="left", padx=20, pady=15)

video_frame_container = customtkinter.CTkFrame(
    right_side_frame,
    fg_color="#2C3E50",
    corner_radius=15,
    border_width=2,
    border_color="#000000",
    width=480,
    height=320
)
video_frame_container.pack(fill="x", pady=(5, 5), padx=10)
video_frame_container.pack_propagate(False)

# Video label for camera feed
video_label = customtkinter.CTkLabel(
    video_frame_container,
    text="Camera Feed\n(Activate to start)",
    font=("Segoe UI", 16, "bold"),
    text_color="#95A5A6"
)
video_label.pack(expand=True)

# Mode and Action display below camera feed
mode_action_container = customtkinter.CTkFrame(
    right_side_frame,
    fg_color="#2C3E50",
    corner_radius=15,
    border_width=2,
    border_color="#000000"
)
mode_action_container.pack(fill="both", expand=True, pady=(5, 20), padx=10)

# Create inner container for perfect centering
mode_action_inner = customtkinter.CTkFrame(
    mode_action_container,
    fg_color="transparent"
)
mode_action_inner.place(relx=0.5, rely=0.5, anchor="center")

# Mode display
mode_title_label = customtkinter.CTkLabel(
    mode_action_inner,
    text="MODE",
    font=("Segoe UI", 20, "bold"),
    text_color="#95A5A6"
)
mode_title_label.pack(pady=(0, 3))

mode_label = customtkinter.CTkLabel(
    mode_action_inner,
    text="Standby",
    font=("Segoe UI", 20, "bold"),
    text_color="#728FCE"
)
mode_label.pack(pady=(0, 8))

# Divider
mode_divider = customtkinter.CTkFrame(mode_action_inner, height=2, width=350, fg_color="#728FCE")
mode_divider.pack(pady=5)

# Action display
action_title_label = customtkinter.CTkLabel(
    mode_action_inner,
    text="ACTION",
    font=("Segoe UI", 20, "bold"),
    text_color="#95A5A6"
)
action_title_label.pack(pady=(8, 3))

action_label = customtkinter.CTkLabel(
    mode_action_inner,
    text="Waiting for gesture...",
    font=("Segoe UI", 20, "bold"),
    text_color="#728FCE",
    wraplength=420
)
action_label.pack(pady=(0, 0))

############################################################################################################
# Second screen
customiseTitle = customtkinter.CTkLabel(
    customiseFrame, 
    text="⚙ GESTURE CUSTOMISATION",
    font=("Segoe UI", 20, "bold"),
    text_color="#728FCE"
)
customiseTitle.pack(pady=(15, 5))

customiseDesc = customtkinter.CTkLabel(
    customiseFrame, 
    text="Configure your custom gesture controls",
    font=("Segoe UI", 12),
    text_color="#999999"
)
customiseDesc.pack(pady=3)
customiseDesc2 = customtkinter.CTkLabel(
    customiseFrame,
    text="Select applications to launch with five available gestures",
    font=("Segoe UI", 11),
    text_color="#777777"
)
customiseDesc2.pack(pady=(0, 15))

# Five drop down lists should be there

# Gesture 1
gesture1_frame = customtkinter.CTkFrame(customiseFrame)
gesture1_frame.pack(fill="both", pady=5, ipadx=80, padx=50, ipady=10)

gesture1_label = customtkinter.CTkLabel(gesture1_frame, text="Gesture 1")
gesture1_label.pack(side="left", pady=5, padx=80)

gesture1_dropdown = customtkinter.CTkComboBox(gesture1_frame, values=getAppNames())
gesture1_dropdown.pack(side="left", pady=5, padx=30)
if customGestureJson is not None:
    for i in data:
        if i["shellName"] == customGestureJson["userDefinedControls"]["index"]:
            gesture1_dropdown.set(i["displayName"])
gesture1_frame.pack_configure(anchor="center")

# Gesture 2
gesture2_frame = customtkinter.CTkFrame(customiseFrame)
gesture2_frame.pack(fill="both", pady=5, ipadx=80, padx=50, ipady=10)

gesture2_label = customtkinter.CTkLabel(gesture2_frame, text="Gesture 2")
gesture2_label.pack(side="left", pady=5, padx=80)

gesture2_dropdown = customtkinter.CTkComboBox(gesture2_frame, values=getAppNames())
gesture2_dropdown.pack(side="left", pady=5, padx=30)
if customGestureJson is not None:
    for i in data:
        if (
            i["shellName"]
            == customGestureJson["userDefinedControls"]["index and middle"]
        ):
            gesture2_dropdown.set(i["displayName"])
gesture2_frame.pack_configure(anchor="center")

# Gesture 3
gesture3_frame = customtkinter.CTkFrame(customiseFrame)
gesture3_frame.pack(fill="both", pady=5, ipadx=80, padx=50, ipady=10)

gesture3_label = customtkinter.CTkLabel(gesture3_frame, text="Gesture 3")
gesture3_label.pack(side="left", pady=5, padx=80)

gesture3_dropdown = customtkinter.CTkComboBox(gesture3_frame, values=getAppNames())
gesture3_dropdown.pack(side="left", pady=5, padx=30)
if customGestureJson is not None:
    for i in data:
        if (
            i["shellName"]
            == customGestureJson["userDefinedControls"]["index, middle and ring"]
        ):
            gesture3_dropdown.set(i["displayName"])
gesture3_frame.pack_configure(anchor="center")

# Gesture 4
gesture4_frame = customtkinter.CTkFrame(customiseFrame)
gesture4_frame.pack(fill="both", pady=5, ipadx=80, padx=50, ipady=10)

gesture4_label = customtkinter.CTkLabel(gesture4_frame, text="Gesture 4")
gesture4_label.pack(side="left", pady=5, padx=80)

gesture4_dropdown = customtkinter.CTkComboBox(gesture4_frame, values=getAppNames())
gesture4_dropdown.pack(side="left", pady=5, padx=30)
if customGestureJson is not None:
    for i in data:
        if (
            i["shellName"]
            == customGestureJson["userDefinedControls"][
                "index, middle, ring and little"
            ]
        ):
            gesture4_dropdown.set(i["displayName"])
gesture4_frame.pack_configure(anchor="center")

# Gesture 5
gesture5_frame = customtkinter.CTkFrame(customiseFrame)
gesture5_frame.pack(fill="both", pady=5, ipadx=80, padx=50, ipady=10)

gesture5_label = customtkinter.CTkLabel(gesture5_frame, text="Gesture 5")
gesture5_label.pack(side="left", pady=5, padx=80)

gesture5_dropdown = customtkinter.CTkComboBox(gesture5_frame, values=getAppNames())
gesture5_dropdown.pack(side="left", pady=5, padx=30)
if customGestureJson is not None:
    for i in data:
        if i["shellName"] == customGestureJson["userDefinedControls"]["thumb"]:
            gesture5_dropdown.set(i["displayName"])
gesture5_frame.pack_configure(anchor="center")


# button to save gestures
saveButton = customtkinter.CTkButton(
    customiseFrame, 
    text="💾 SAVE GESTURES", 
    command=lambda: saveGestures(data),
    font=("Segoe UI", 14, "bold"),
    fg_color="#728FCE",
    hover_color="#3A7BC8",
    height=50,
    corner_radius=12,
    border_width=0
)
saveButton.pack_configure(anchor="center", pady=25)
backToMainMenu = customtkinter.CTkButton(
    customiseFrame, 
    text="← BACK", 
    command=lambda: backToMenuFrame(),
    font=("Segoe UI", 13, "bold"),
    fg_color="#7F8C8D",
    hover_color="#6C7A7B",
    height=45,
    corner_radius=10,
    border_width=0
)
backToMainMenu.pack_configure(anchor="center", pady=10)

############################################################################################################
# Third Screen
# Third screen is for the user to view tutorial

# Create a dropdown list
options = list(anim_data.keys())
selected_option = customtkinter.StringVar()
dropdown = customtkinter.CTkComboBox(
    tutorialFrame, values=options, variable=selected_option
)
dropdown.set(options[0])
dropdown.pack(pady=20)

# Create a frame for the GIFs
gif_frame = customtkinter.CTkFrame(tutorialFrame)
gif_frame.pack(ipady=20, ipadx=20)

# Specify the hands for the GIFs, these should be displayed side by side above the GIFs
left_hand = customtkinter.CTkLabel(gif_frame, text="Left Hand")
left_hand.grid(row=0, column=0, padx=30, pady=10)

right_hand = customtkinter.CTkLabel(gif_frame, text="Right Hand")
right_hand.grid(row=0, column=1, pady=10)

# Create labels for the GIFs
left_gif_label = GestureAnimation(gif_frame, "left", "animations\\1.gif")
right_gif_label = GestureAnimation(gif_frame, "right", "animations\\2.gif")

# Create a frame for the heading and description
description_frame = customtkinter.CTkFrame(
    tutorialFrame, width=400, height=200, corner_radius=25, border_width=5
)
description_frame.pack(ipady=5, pady=10)

# Create the heading
heading = customtkinter.CTkLabel(
    description_frame, text="Description", font=("Arial", 16, "bold")
)
heading.pack(pady=10)

# Create the description text
description_label = customtkinter.CTkLabel(
    description_frame, text=anim_data[options[0]]["description"], wraplength=500
)
description_label.pack(pady=5, padx=20)


# Function to update the GIFs based on the selected option
def update_gifs(*_):
    try:
        option = selected_option.get()
        description_label.configure(text=anim_data[option]["description"])
        left_gif_label.update_gif(anim_data[option]["left"])
        right_gif_label.update_gif(anim_data[option]["right"])
    except Exception as e:
        pass

# Bind the update_gifs function to the dropdown selection
selected_option.trace_add("write", update_gifs)

# Create a button to go back to the main menu
back_button = customtkinter.CTkButton(
    tutorialFrame, 
    text="← BACK", 
    command=backToMenuFrame,
    font=("Segoe UI", 13, "bold"),
    fg_color="#7F8C8D",
    hover_color="#6C7A7B",
    height=45,
    corner_radius=10,
    border_width=0
)
back_button.pack(pady=15)

# Add author footer to the app window
footer_frame = customtkinter.CTkFrame(app, fg_color="#1a1a1a", height=70)
footer_frame.pack(side="bottom", fill="x", pady=(0, 5), padx=10)

# Footer content frame
footer_content = customtkinter.CTkFrame(footer_frame, fg_color="transparent")
footer_content.pack(expand=True, pady=10)

# Developer name
dev_label = customtkinter.CTkLabel(
    footer_content,
    text="👨‍💻 Developed by: Rohan S.",
    font=("Segoe UI", 16, "bold"),
    text_color="#FFFFFF"
)
dev_label.pack(pady=(5, 5))

# Links frame
links_frame = customtkinter.CTkFrame(footer_content, fg_color="transparent")
links_frame.pack()

# Email link
email_button = customtkinter.CTkButton(
    links_frame,
    text="📧 Email",
    font=("Segoe UI", 12, "bold"),
    fg_color="transparent",
    text_color="#3498DB",
    hover_color="#2C3E50",
    width=100,
    height=25,
    command=lambda: __import__('webbrowser').open('mailto:rohanrony8431@gmail.com')
)
email_button.pack(side="left", padx=10)

# LinkedIn link
linkedin_button = customtkinter.CTkButton(
    links_frame,
    text="🔗 LinkedIn",
    font=("Segoe UI", 12, "bold"),
    fg_color="transparent",
    text_color="#0077B5",
    hover_color="#2C3E50",
    width=100,
    height=25,
    command=lambda: __import__('webbrowser').open('https://www.linkedin.com/in/rohan-s-43201a2a3')
)
linkedin_button.pack(side="left", padx=10)

# GitHub link
github_button = customtkinter.CTkButton(
    links_frame,
    text="💻 GitHub",
    font=("Segoe UI", 12, "bold"),
    fg_color="transparent",
    text_color="#FFFFFF",
    hover_color="#2C3E50",
    width=100,
    height=25,
    command=lambda: __import__('webbrowser').open('https://github.com/Rohan9731')
)
github_button.pack(side="left", padx=10)

app.mainloop()

# To be executed when the app is closed
if ges_con and hasattr(ges_con, 'runFlag'):
    ges_con.runFlag = False
if ges_con_thread and ges_con_thread.is_alive():
    ges_con_thread.join()

client.close()

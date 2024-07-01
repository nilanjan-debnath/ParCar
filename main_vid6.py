import json
import pickle
import datetime
import threading
import cv2
import cvzone
import numpy as np
from PIL import Image, ImageTk
import customtkinter as ctk
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db

# 230801
# Initialize Firebase
# cred = credentials.Certificate("Private_Key.json")
# firebase_admin.initialize_app(cred, {
#     'databaseURL': 'https://parcar-dd9d9-default-rtdb.asia-southeast1.firebasedatabase.app/'
# })

file_path = "sample6.json"

with open(file_path, "r") as file:
    data = json.load(file)


frames = []
slots = []
statuses = []
park_states = []
park_buttons = []
namelbs = []
carnolbs = []
bookingtimelbs = []
edit_buttons = []
spaces = []

states = {
    0: ("Empty", "Green"),
    1: ("Booked", "Blue"),
    2: ("Parked", "Red"),
}

def change_state(n, i):
    text, color = states[i]
    park_buttons[n].configure(text=text, fg_color=color)


posList = []
for i in data["Parking_Spots"]:
    loc = i["Position"]
    posList.append(loc)

def cloudUpdate():
    # db.reference('/demo_test/slot_details').update(data)
    pass

def localUpdate(slotNo, i):
    data["Parking_Spots"][slotNo]["State"] = i
    threading.Thread(target=change_state(slotNo, i)).start()
    if i == 2:
        data["Parking_Spots"][slotNo]["Booking_Time"] = str(datetime.datetime.now())
    else:
        data["Parking_Spots"][slotNo]["Leaving_Time"] = str(datetime.datetime.now())
    saveUpdate()
    # print(slotNo)

def saveUpdate():
    threading.Thread(target=cloudUpdate).start()
    with open(file_path, 'w', ) as file:
        json.dump(data, file)

def updateSpaces(occupied, total):
    spaces[0].configure(text=f"Free Spaces: {total-occupied}")
    spaces[1].configure(text=f"Occupid Spaces: {occupied}")
    spaces[2].configure(text=f"Total Spces: {total}")



class parkDetails(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        font0 = ctk.CTkFont(family='Times New Roman', size=24, weight='bold')
        font1 = ctk.CTkFont(family='Helvetica', size=18, weight='bold')
        font2 = ctk.CTkFont(family='Helvetica', size=14)
        
        prev_SpaceCounter = None

        # Create lists to store UI elements
        global frames
        global slots
        global statuses
        global park_states
        global park_buttons
        global namelbs
        global carnolbs
        global bookingtimelbs
        global edit_buttons

        # Loop through parking spots
        for i in data["Parking_Spots"]:
            # Create frame
            frame = ctk.CTkFrame(
                master=self,
                width=500,
                height=50,
                fg_color="gray",
            ).grid(row=i["Slot_No"] -1, column=0, padx=5, pady=5, columnspan=6, sticky="EW")
            frames.append(frame)

            # Create slot label
            slot = ctk.CTkLabel(
                master=self,
                text=f'Slot: {i["Slot_No"]}',
                bg_color="grey",
                text_color="White",
                font=font1,
            ).grid(row=i["Slot_No"] -1, column=0, padx=20, sticky="W")
            slots.append(slot)

            # Create status label
            status = ctk.CTkLabel(
                master=self,
                text="Status",
                bg_color="grey",
                text_color="White",
                font=font1,
            ).grid(row=i["Slot_No"] -1, column=1, padx=5, sticky="W")
            statuses.append(status)


            park_state = i["State"]
            park_button = ctk.CTkButton(
                master=self,
                text=states[park_state][0],
                font=font1,
                fg_color=states[park_state][1],
                bg_color="grey",
                hover=None,
                command=lambda n=i["Slot_No"] - 1: change_state(n),
            )
            park_button.grid(row=i["Slot_No"] -1, column=2, padx=20, sticky="W")
            park_buttons.append(park_button)
            park_states.append(park_state)

            self.name = i["Name"]
            namelb = ctk.CTkLabel(
                master=self, 
                text=f"Name: {self.name}", 
                bg_color="grey", 
                text_color="White", 
                font=font2,
                ).grid(row=i["Slot_No"] -1, column=3, padx=20, sticky="W")
            
            namelbs.append(namelb)

            self.carno = i["Car_No"]
            carnolb = ctk.CTkLabel(
                master=self, 
                text=f"Car No: {self.carno}", 
                bg_color="grey", 
                text_color="White", 
                font=font2,
                ).grid(row=i["Slot_No"] -1, column=4, padx=20, sticky="W")
            
            carnolbs.append(carnolb)

            bookingtimestr = i["Booking_Time"]
            try:
                bokingtime_obj = datetime.datetime.strptime(bookingtimestr, "%Y-%m-%d %H:%M:%S.%f")
                self.bookingtime = bokingtime_obj.strftime('%a %d %b %Y, %I:%M%p')
            except ValueError:
                self.bookingtime = ""

            bookingtimelb = ctk.CTkLabel(
                master=self, 
                text=f"Booking Time: {self.bookingtime}", 
                bg_color="grey", 
                text_color="White", 
                font=font2,
                ).grid(row=i["Slot_No"] -1, column=5, padx=20, sticky="W")

            bookingtimelbs.append(bookingtimelb)
            

            editbt = ctk.CTkButton(
                master=self,
                text="Edit",
                font=font2,
                fg_color="brown",
                bg_color="transparent",
                hover=None,
            )
            editbt.grid(row=i["Slot_No"] -1, column=6, padx=10, sticky="W")
            edit_buttons.append(editbt)
 
prev_SpaceCounter = None

class MyTabView(ctk.CTkTabview):
    def __init__(self, master, **kwargs):
        super().__init__(master, height=700, width=1260, **kwargs)

        self.dashboard_tab = self.add("Dashboard")
        self.cctv_tab = self.add("CCTV")
        
        font0 = ctk.CTkFont(family='Times New Roman', size=30, weight='bold')
        font1 = ctk.CTkFont(family='Helvetica', size=18, weight='bold')
        font2 = ctk.CTkFont(family='Helvetica', size=14)

        placeName = ctk.CTkLabel(
            master=self.tab("Dashboard"), 
            text="Demo Parking Area",
            font=font0
        ).grid(row=0, column=0, padx=20, pady=10)

        global spaces
        for n in range(3):
            slotsDetails = ctk.CTkLabel(
                master=self.tab("Dashboard"), 
                text="",
                font=font1
            )
            slotsDetails.grid(row=1, column=n, padx=20, pady=10)
            spaces.append(slotsDetails)

        self.my_frame = parkDetails(master=self.tab("Dashboard"), width=1220, height=500)
        self.my_frame.grid(row=2, column=0, columnspan=20)
        
               

        # Camera setup
        self.cap = cv2.VideoCapture("NewVidFeed.mp4")  

        # self.cap = cv2.VideoCapture(1)
        ret, frame = self.cap.read()  # Check for initial frame capture

        if not ret:
            print("Error: Unable to capture initial frame from the camera.")
            self.cap.release()
            return

        # Video display canvas
        self.canvas_cctv = ctk.CTkCanvas(master=self.tab("CCTV"), width=1530, height=790)
        self.canvas_cctv.grid(row=0, column=0, padx=10, pady=10)

        # Capture and display loop
        self.update()

    

    def checking_parking_space(self, imgPro):
        width = 200
        height = 50
        global prev_SpaceCounter
        SpaceCounter = 0
        slot_status_mapping = {}  # Dictionary to store slot occupancy status

        for i, pos in enumerate(posList):
            x, y = pos
            slot_number = i + 1
            imgcrop = imgPro[y:y+height, x:x+width]
            count = cv2.countNonZero(imgcrop)
            cvzone.putTextRect(self.frame, str(count), (x,y+height-3), scale=1.1, thickness=2, offset=0)
            cvzone.putTextRect(self.frame, str(slot_number), (x,y+height-30), scale=1, thickness=2, offset=0, colorR=(255, 0, 0))  # Draw slot number
            
            def check():
                pass

            if count > 900:
                colour = (255, 0, 0)
                thickness = 3
                SpaceCounter += 1
                if data["Parking_Spots"][slot_number-1]["State"] != 2:
                    threading.Thread(target=localUpdate(slot_number-1, 2)).start()
            else:
                colour = (0, 255, 0)
                thickness = 1
                if data["Parking_Spots"][slot_number-1]["State"] != 0:
                    threading.Thread(target=localUpdate(slot_number-1, 0)).start()
            
            if prev_SpaceCounter != SpaceCounter:
                threading.Thread(target=updateSpaces(SpaceCounter, len(posList))).start()

            prev_SpaceCounter = SpaceCounter
                
            cv2.rectangle(self.frame, pos, (pos[0] + width, pos[1] + height), colour, thickness)
            
        cvzone.putTextRect(self.frame, f'Free: {SpaceCounter}/{len(posList)}', (100, 50), scale=2, thickness=5, offset=20)

        
        # Push data to Firebase
        # db.reference('/parking_status_vid').update({
        #     'slot_status_mapping': slot_status_mapping,
        #     'Empty_Spaces': SpaceCounter,
        #     'total_slots': len(posList)
        # })
        return slot_status_mapping

    def update(self):
        if self.cap.get(cv2.CAP_PROP_POS_FRAMES) == self.cap.get(cv2.CAP_PROP_FRAME_COUNT):
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = self.cap.read()
        if not ret:
            return
        self.frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        original_height, original_width, _ = frame.shape
        ratio = (original_width / original_height)
        # new_height = int(ratio * 790)
        # new_width = int(790)
        new_height = 1280
        new_width = 720
        self.frame = cv2.resize(self.frame, (new_height, new_width))

        imgGray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (3,3), 1)
        imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
        imgMedian = cv2.medianBlur(imgThreshold, 5)
        kernel = np.ones((3, 3), np.uint8)
        imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)
        slot_status_mapping = self.checking_parking_space(imgDilate)

        # print(frame.shape)
        img = Image.fromarray(self.frame)
        self.photo = ImageTk.PhotoImage(image=img)
        self.canvas_cctv.create_image(5, 5, image=self.photo, anchor="nw")
        self.canvas_cctv.update_idletasks()
        self.canvas_cctv.after(10, self.update)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1280x720")
        self.title('ParCar')
        self.iconbitmap('parcar.ico')
        self.tab_view = MyTabView(master=self)
        self.tab_view.grid(row=0, column=0, padx=10, pady=10)

app = App()
app.mainloop()

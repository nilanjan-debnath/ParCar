import pickle
import json

try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
        print(posList)
except:
    posList = []

data = {"Parking_Spots": []}
details = {
    "Slot_No": "",
    "Position": "",
    "State": "",
    "Name": "",
    "Booking_Time": "",
    "Leaving_Time": "",
    "Car_No": ""
}



with open("sample.json", "w") as outfile:
    json.dump(posList, outfile)
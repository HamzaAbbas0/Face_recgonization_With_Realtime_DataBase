import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': 'https://faceattendancerealtime-19687-default-rtdb.firebaseio.com/',
})
ref = db.reference('students')

data = {
    "321654":
        {
            "name" : "Murtaza Retotics",
            "major" : 'Rebotics',
            "starting_year" : 2017,
            "total_attendence" : 8,
            "standing" : "G",
            "year" : 4,
            "Last_attendance_time" : "2022-1-18 00:54:45"
        },

    "462534":
        {
            "name": "Hamza Abbas",
            "major": 'AI',
            "starting_year": 2018,
            "total_attendence": 9,
            "standing": "G",
            "year": 4,
            "Last_attendance_time": "2023-2-5 00:54:45"
        },

    "852741":
        {
            "name": "Emmile Blunt",
            "major": 'Marketing',
            "starting_year": 2020,
            "total_attendence": 3,
            "standing": "p",
            "year": 2,
            "Last_attendance_time": "2023-1-2 00:54:45"
        },

    "963852":
        {
            "name": "Elun Musk",
            "major": 'space_Science',
            "starting_year": 2013,
            "total_attendence": 7,
            "standing": "G",
            "year": 6,
            "Last_attendance_time": "2022-12-11 00:54:45"
        }

}

for key, value in data.items():
    ref.child(key).set(value),
import os



def execute():
    print("HERE")
    os.system("bench pip install cmake")
    os.system("bench pip install opencv-contrib-python")
    os.system("bench pip install face_recognition")
    os.system("bench pip install qrcode")

    # os.system("ls")
    # os.system("source env/bin/activate")

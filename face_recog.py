import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image,ImageTk
import sqlite3
import os
import face_recognition as facerecg

def convert_binary(file):
        with open(file,"rb") as img_read:
            img = img_read.read()
            return img
            
def data_base_init_entry(save_path):
    
    conn = sqlite3.connect("Images.db")
    cur = conn.cursor()
    # cur.execute("""CREATE TABLE ImageDB
    # (Person TEXT, Person_Img BLOB, Face_Encoding TEXT)""")

    path = r"face_recog_gui\\newcreatedfaces\\" +f"{save_path}.jpg"
    print(path)

    name = save_path
    print(name)

    img_binary = convert_binary(path)
    face = facerecg.load_image_file(path)
    face_encoding = facerecg.face_encodings(face)[0]
    print(face_encoding)

    # cur.execute("""INSERT INTO ImageDB (Person, Person_Img, Face_Encoding)
    #             VALUES (?, ?, ?)""", (name, img_binary, face_encoding) )

    conn.commit()
    cur.close()
    FR_mainwindow.destroy()


def create_entry():
    global DB_names
    global id
    global status

    if id.get() not in DB_names:
        cam = cv2.VideoCapture(0)
        cam.set(3, 720)  
        cam.set(4, 540)  
        path_harcascade = r'F:\GEN2programming\PYTHONPROG\face_recog_gui\haarcascade_frontalface_default.xml'
        face_detector = cv2.CascadeClassifier(path_harcascade)
        print("\n [INFO] Initializing face capture. Look the camera and wait ...")

        count = 0
        while (True):
            ret, img = cam.read()
            RGB_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            faces = face_detector.detectMultiScale(RGB_img, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 3)
                count += 1
            
                t_path = r"F:\\GEN2programming\\PYTHONPROG\\face_recog_gui\\newcreatedfaces\\"
                cv2.imwrite(t_path  + f"{id.get()}.jpg" ,RGB_img[y:y + h, x:x + w])

                cv2.imshow('image', img)

            k = cv2.waitKey(100) & 0xff  

            if k == 27:
                break

            elif count >= 1:  
                break

        print("\n [INFO] Your Facial Data has been Successfully been taken saving to database...")

        cam.release()
        cv2.destroyAllWindows()
        # data_base_init_entry(id.get())
    else:
        status.set("User With Same ID exist in DB use Different ID")
        return

def send_to_DB():
    data_base_init_entry(id.get())


FR_mainwindow = tk.Tk()
FR_mainwindow.geometry("1000x598")
FR_mainwindow.resizable(False,False)
FR_mainwindow.title("ADD USERS TO DATABASE") 
FR_mainwindow.configure(background = 'black') 

bg1 = Image.open(r'F:\GEN2programming\PYTHONPROG\face_recog_gui\GUI_Images\background.jpg')
bg1_p = ImageTk.PhotoImage(bg1)
bg_label = tk.Label(FR_mainwindow ,image = bg1_p) 
bg_label.place(x=0,y=0)

FR_mainwindow.grid_rowconfigure(0, weight = 1) 
FR_mainwindow.grid_columnconfigure(0, weight = 1) 

heading = Image.open(r'F:\GEN2programming\PYTHONPROG\face_recog_gui\GUI_Images\bg2.png')
heading_p = ImageTk.PhotoImage(heading)
heading_label = tk.Label(FR_mainwindow,image = heading_p,bd=0,bg='#fefefe',activebackground='#fefefe') 
heading_label.place(x=230,y=119)

side_image = Image.open(r'F:\GEN2programming\PYTHONPROG\face_recog_gui\GUI_Images\ub.png')
side_image_p = ImageTk.PhotoImage(side_image)
side_image_label = tk.Label(FR_mainwindow,image = side_image_p,bd=0,bg='#fefefe',activebackground='#fefefe') 
side_image_label.place(x=760,y=17)

conn = sqlite3.connect("Images.db")
cur = conn.cursor()
DB_names = []

cur.execute("SELECT Person FROM ImageDB")
name_vals = cur.fetchall()

for name in name_vals:
        name = ''.join(name)
        DB_names.append(name)


id = tk.StringVar()
status = tk.StringVar(value = "Please Enter the profile id for New user")

id_image = Image.open(r'F:\GEN2programming\PYTHONPROG\face_recog_gui\GUI_Images\enter.png')
id_image_p = ImageTk.PhotoImage(id_image)
id_label = tk.Label(FR_mainwindow,image = id_image_p ,bd=0,bg='#fefefe',activebackground='#fefefe') 
id_label.place(x=295, y=345)

entry_id = tk.Entry(FR_mainwindow,width=25,bg="#fefefe" ,fg="black",font=('Ar cena', 15),textvariable=id)
entry_id.place(x=400, y=350)

status_label = tk.Label(FR_mainwindow,textvariable=status,fg="red",bg="#fefefe",font=('Ar cena', 9))
status_label.place(x=396, y=380)


capture_button_image = Image.open(r'F:\GEN2programming\PYTHONPROG\face_recog_gui\GUI_Images\capture.png')
cap_but_img_p = ImageTk.PhotoImage(capture_button_image)


cam_button = tk.Button(FR_mainwindow,command = create_entry, image = cap_but_img_p , bd=0 , bg='#fefefe',
                                                                     activebackground='#fefefe')
cam_button.place(x = 379, y = 435)
caminfo_label = tk.Label(FR_mainwindow,text = "Capture Face",fg="black",bg="#fefefe",font=('Ar cena', 11))
caminfo_label.place(x=369, y=505)


DB_button_image = Image.open(r'F:\GEN2programming\PYTHONPROG\face_recog_gui\GUI_Images\save.png')
DB_but_img_p = ImageTk.PhotoImage(DB_button_image)
sendDB_button = tk.Button(FR_mainwindow,command = send_to_DB, image = DB_but_img_p , bd=0 , bg='#fefefe',
                                                                     activebackground='#fefefe')
sendDB_button.place(x = 521, y = 435)
sendDbinfo = tk.Label(FR_mainwindow,text = "Save to DB",fg="black",bg="#fefefe",font=('Ar cena', 11))
sendDbinfo.place(x=513, y=505)


FR_mainwindow.mainloop()
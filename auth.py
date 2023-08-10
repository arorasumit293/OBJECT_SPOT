import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk
from PIL import Image,ImageTk
import sqlite3
import os
import face_recognition

unique_list = []

def start_process():
    running_state.set(value=True)
    label2.destroy()
    authenticate(AU_mainwindow, label1)

def stop_process():
    running_state.set(False)
    global unique_list
    unique_list = []
    text_area.delete("1.0","end")
    str_counter = f"{counter.get()}" + ".0"
    text_area.insert(str_counter, "Persons Detected\n")

def quit_process():
    if running_state.get():
        stop_process()
    AU_mainwindow.destroy()

def insert_into_text(Unique_obj):
    global unique_list
    if Unique_obj not in unique_list:
        unique_list.append(Unique_obj)
        global t_count
        t_count+= 1
        str_counter = f"{t_count}" + ".0"
        text_area.insert(str_counter, Unique_obj+"\n")

def authenticate(AU_mainwindow, label1):
   
    DB_face_encodings = []
    DB_names = []

    conn = sqlite3.connect("Images.db")
    cur = conn.cursor()

    cur.execute("SELECT Person FROM ImageDB")
    name_vals = cur.fetchall()
    
    cur.execute("SELECT Face_Encoding FROM ImageDB")
    face_encodings_vals = cur.fetchall()

    for name,face_encoding in zip(name_vals,face_encodings_vals):
        
        name = ''.join(name)
        face_encoding = b''.join(face_encoding)

        arrayed_face_encoding = np.frombuffer(face_encoding)
        DB_face_encodings.append(arrayed_face_encoding)
        DB_names.append(name)
    
    process_this_frame = True
    
    while running_state.get(): 
        
        video_capture = cv2.VideoCapture(0)
        face_locations = []
        face_encodings = []

        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25) 
        rgb_small_frame = small_frame[:, :, ::-1]
        
        if process_this_frame:

            face_locations = face_recognition.face_locations(rgb_small_frame)
            print(face_locations)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
            print(face_encodings)

            face_names = []
            
            for face_encoding in face_encodings:

                name = "Unknown"
        
                matches = face_recognition.compare_faces(DB_face_encodings, face_encoding)

                face_distances = face_recognition.face_distance(DB_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                
                if matches[best_match_index]:
                    name = DB_names[best_match_index]

                face_names.append(name)


        for (top, right, bottom, left), name in zip(face_locations, face_names):

            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        insert_into_text(name)
        img= cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo = ImageTk.PhotoImage(Image.fromarray(img))
        label1['image'] = photo
        AU_mainwindow.update()


AU_mainwindow = tk.Tk()
AU_mainwindow.geometry("800x500")
AU_mainwindow.resizable(False,False)
AU_mainwindow.title("FACE RECOGNIZER")

style = ttk.Style(AU_mainwindow)

cam_frame = tk.Frame(AU_mainwindow)
cam_frame.pack(side = 'left',fill = 'both',expand=True)
cam_frame['borderwidth'] = 1
cam_frame['relief'] = 'solid'

ttk.Separator(AU_mainwindow,orient='vertical').pack(side = 'left' , fill='y',padx =(0,5))

button_frame = ttk.Frame(AU_mainwindow)
button_frame.pack(side = 'left',fill = 'both')
button_frame['borderwidth'] = 1
button_frame['relief'] = 'solid'
button_frame.grid_columnconfigure(0,weight=1)
button_frame.grid_rowconfigure(0,weight=1)

running_state = tk.BooleanVar()

init_msg = tk.StringVar(value = "Camera Will Open In Here")
label1 = ttk.Label(cam_frame)
label1.pack(fill='both',expand=True)

label1_img= ImageTk.PhotoImage(file = r'F:\GEN2programming\PYTHONPROG\face_recog_gui\GUI_Images\bg11.jpg')
label1['style'] = 'CustomLabelStyle.TLabel'
style.configure('CustomLabelStyle.TLabel',image = label1_img)

label2_img= ImageTk.PhotoImage(file = r'F:\GEN2programming\PYTHONPROG\face_recog_gui\GUI_Images\text2.png')
label2 = tk.Label(cam_frame,image = label2_img,bd = 0,bg = '#fefefe',activebackground = '#fefefe')
label2.place(x = 212,y = 230)


b_img= ImageTk.PhotoImage(file = r'F:\GEN2programming\PYTHONPROG\face_recog_gui\object_detector\images\background.jpg')
label = tk.Label(button_frame,image=b_img)
label.place(x=0,y=0)

name_label = tk.Label(button_frame)
name_label.grid(row=0,column=0,padx=(50,85),pady=(5,5))

action_img= ImageTk.PhotoImage(file = r'F:\GEN2programming\PYTHONPROG\face_recog_gui\object_detector\images\actions.png')
action_label = tk.Label(button_frame,image = action_img,bd = 0,bg = '#fefefe',activebackground = '#fefefe')
action_label.place(x = 34, y= 50)


b1_img= ImageTk.PhotoImage(file = r'F:\GEN2programming\PYTHONPROG\face_recog_gui\object_detector\images\button_detect.ico')
b2_img= ImageTk.PhotoImage(file = r'F:\GEN2programming\PYTHONPROG\face_recog_gui\object_detector\images\button_stop.ico')
b3_img= ImageTk.PhotoImage(file = r'F:\GEN2programming\PYTHONPROG\face_recog_gui\object_detector\images\button_quit.png')

start_button = tk.Button(button_frame, image = b1_img , bd=0 , bg='#fefefe',
                         activebackground='#fefefe',
                         command = start_process)
start_button.place(x = 21, y = 98)

stop_button = tk.Button(button_frame, image = b2_img, bd=0 , bg='#fefefe',
                        activebackground='#fefefe',
                        command = stop_process)
stop_button.place(x = 21, y = 177)

quit_button = tk.Button(button_frame, image = b3_img, bd=0 , bg='#fefefe',
                        activebackground='#fefefe',
                        command = quit_process,padx=10)
quit_button.place(x = 21, y = 255)

text_area = tk.Text(button_frame,height = 10,width = 15,font = ("Arial",9))
text_area.place(x = 12, y = 328)

counter = tk.IntVar(value=1)
t_count = counter.get()

str_counter = f"{counter.get()}" + ".0"
text_area.insert(str_counter, "Person Detected\n")

AU_mainwindow.mainloop()


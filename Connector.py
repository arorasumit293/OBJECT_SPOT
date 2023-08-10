import tkinter as tk 
from PIL import Image,ImageTk
import subprocess

def add_face_pressed():
    subprocess.call(['python', r'F:\GEN2programming\PYTHONPROG\face_recog_gui\face_recog.py'])

def recognize_pressed():
    subprocess.call(['python', r'F:\GEN2programming\PYTHONPROG\face_recog_gui\auth.py'])


Connector_frame = tk.Tk()
Connector_frame.geometry("552x410")
Connector_frame.title("FACE RCG DASHBOARD")
Connector_frame.configure(background = '#16232B') 

Connector_frame.grid_rowconfigure(0, weight = 1) 
Connector_frame.grid_columnconfigure(0, weight = 1) 

Bg_image = Image.open(r'F:\GEN2programming\PYTHONPROG\face_recog_gui\GUI_Images\connect_bg.jpg')
Bg_image_p = ImageTk.PhotoImage(Bg_image)
Bg_label = tk.Label(Connector_frame,image = Bg_image_p) 
Bg_label.place(x=0,y=0)

text_image = Image.open(r'F:\GEN2programming\PYTHONPROG\face_recog_gui\GUI_Images\text3.png')
text_image_p = ImageTk.PhotoImage(text_image)
text_label = tk.Label(Connector_frame,image = text_image_p,bd=0,bg='#16232B',activebackground='#16232B') 
text_label.place(x=70,y=8)

sub1img = Image.open(r'F:\GEN2programming\PYTHONPROG\face_recog_gui\GUI_Images\sub1.png')
sub1img_p = ImageTk.PhotoImage(sub1img)

sub1button = tk.Button(Connector_frame,command = add_face_pressed,image = sub1img_p , bd=0 , bg='#16232B',
                                                                     activebackground='#16232B')
sub1button.place(x = 214, y = 60)
sub1button_label = tk.Label(Connector_frame,text = "Add Face",fg="white",bg="#16232B",font=('Ar cena', 11))
sub1button_label.place(x=244, y=190)


sub2img = Image.open(r'F:\GEN2programming\PYTHONPROG\face_recog_gui\GUI_Images\sub2.2.png')
sub2img_p = ImageTk.PhotoImage(sub2img)

sub2button = tk.Button(Connector_frame,command = recognize_pressed, image = sub2img_p , bd=0 , bg='#16232B',
                                                                     activebackground='#16232B')
sub2button.place(x = 214, y = 244)
sub2button_label = tk.Label(Connector_frame,text = "Recognize",fg="white",bg="#16232B",font=('Ar cena', 11))
sub2button_label.place(x=244, y=375)

Connector_frame.mainloop()
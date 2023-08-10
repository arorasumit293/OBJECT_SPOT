import tkinter as tk 
from PIL import Image,ImageTk
import subprocess

def objdetc_pressed():
    subprocess.call(['python', r'F:\GEN2programming\PYTHONPROG\face_recog_gui\object_detector\guiobj.py'])

def connection_pressed():
    subprocess.call(['python', r'F:\GEN2programming\PYTHONPROG\face_recog_gui\Connector.py'])


Main_frame = tk.Tk()
Main_frame.geometry("800x585")
Main_frame.resizable(False,False)
Main_frame.title("SMART SECURITY SYSTEM")
Main_frame.configure(background = 'black') 

Main_frame.grid_rowconfigure(0, weight = 1) 
Main_frame.grid_columnconfigure(0, weight = 1) 

Bg_image = Image.open(r'F:\GEN2programming\PYTHONPROG\face_recog_gui\GUI_Images\photo.jpg')
Bg_image_p = ImageTk.PhotoImage(Bg_image)
Bg_label = tk.Label(Main_frame,image = Bg_image_p) 
Bg_label.place(x=0,y=0)


sub1img = Image.open(r'F:\GEN2programming\PYTHONPROG\face_recog_gui\GUI_Images\obj12.png')
sub1img_p = ImageTk.PhotoImage(sub1img)

sub1button = tk.Button(Main_frame,command = objdetc_pressed,image = sub1img_p , bd=0 , bg='white',
                                                                     activebackground='white')
sub1button.place(x = 568, y = 210)
sub1button_label = tk.Label(Main_frame,text = "Object Detector",fg="white",bg="#5B49CF",font=('Ar cena', 9))
sub1button_label.place(x=598, y=364)


sub2img = Image.open(r'F:\GEN2programming\PYTHONPROG\face_recog_gui\GUI_Images\facedet23.png')
sub2img_p = ImageTk.PhotoImage(sub2img)

sub2button = tk.Button(Main_frame,command = connection_pressed, image = sub2img_p , bd=0 , bg='white',
                                                                     activebackground='white')
sub2button.place(x = 568, y = 406)
sub2button_label = tk.Label(Main_frame,text = "Face Recognizer",fg="white",bg="#4F22B3",font=('Ar cena', 9))
sub2button_label.place(x=593, y=559)

Main_frame.mainloop()
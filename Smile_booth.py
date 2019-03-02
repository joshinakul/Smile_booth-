from scipy.spatial import distance as dist
from imutils import face_utils
import imutils
import numpy as np
import dlib
import cv2
from tkinter import *
from PIL import Image,ImageTk
import time
import re
from tkinter import messagebox
import os
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from threading import Thread
import subprocess

def mail(name,email):
    t = name+'.jpg'
    img_data = open(t, 'rb').read()
    msg = MIMEMultipart()
    msg['Subject'] = 'Smiling Rajasthan'
    msg['From'] = 'nakulswims@gmail.com'
    msg['To'] = email


    image = MIMEImage(img_data, name=os.path.basename(t))
    msg.attach(image)

    s = smtplib.SMTP('smtp.gmail.com',587)
    s.starttls()
    s.ehlo()
    s.login('nakulswims@gmail.com', 'jaijaijaihanumanji')
    s.sendmail('nakulswims@gmail.com', email,msg.as_string())
    s.close()

def preview(name,email,root1,temp):
    x = cv2.imread(name+'.jpg')
    cv2.namedWindow("preview", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("preview", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    im = cv2.imread(name+'.jpg')
    row,col = im.shape[:2]
    bottom  = im[row-2:row,0:col]

    bordersize = 10
    border = cv2.copyMakeBorder(im,top=bordersize,bottom=bordersize,left=0,right=0,borderType=cv2.BORDER_CONSTANT,value=[32,173,243])

    
    now = time.time() + 7
    while time.time()<now:
        cv2.imshow('preview',border)
        cv2.waitKey(1)
    cv2.destroyAllWindows()
    thankyou(name,email,root1,temp)

def thankyou(name,email,root1,temp):
    root1.destroy()    
    root = Tk()
    root.title('Smile_detector')
    p1 = Image.open(temp)
    p1 = ImageTk.PhotoImage(p1)
    yscrollbar = Scrollbar(root,orient = VERTICAL)
    canvas = Canvas(root,width = 1080,height = 1920,yscrollcommand = yscrollbar.set,scrollregion=(0,0,1080,1920))
    l = Label(canvas,image = p1)
    l.pack(fill = BOTH,expand = YES)
    yscrollbar.config(command=canvas.yview)
    yscrollbar.pack(side = RIGHT,fill = BOTH)
    canvas.bind_all('<MouseWheel>',lambda event : canvas.yview_scroll(int(-1*(event.delta/120)), "units"))
    canvas.pack(fill = BOTH,expand = True)
    root.after(2000,lambda:root.destroy())
    root.mainloop()

    t2 = Thread(target = mail,args = (name,email)).start()
    
    
def smile(mouth):
    MAR = dist.euclidean(mouth[0], mouth[6])
    return MAR

def isValidEmail(email):
            if len(email) > 7:
                if re.search("[@.]",email) != None:
                    return True
            return False

def main(root1,name, email,temp):
    flag = True
    name=name.get()
    email=email.get()

    if(name=='' and email==''):
        messagebox.showinfo("Alert", "Please enter your Name and Email. ")
    elif(email==''):
        messagebox.showinfo("Alert", "Please enter your Email. ")
    elif(name==''):
        messagebox.showinfo("Alert", "Please enter your Name. ")

    else:
        t = isValidEmail(email)
        if t == False:
            messagebox.showinfo("Alert", "Please enter your Correct Email. ")
    
        else:
                
            shape_predictor= "shape_predictor_68_face_landmarks.dat"
            detector = dlib.get_frontal_face_detector()
            predictor = dlib.shape_predictor(shape_predictor)
            
            
            (mStart, mEnd) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]
            
            print("Lets go..!!")
            cap = cv2.VideoCapture(0)
            cv2.namedWindow("Smile-Detector", cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty("Smile-Detector", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

            q = cv2.imread('12.png')
            w = cv2.imread('13.png')
            e = cv2.imread('14.png')
            r = cv2.imread('15.png')
            t = cv2.imread('16.png')
            
                
            while flag:
                _,frame = cap.read()
                frame = imutils.resize(frame,width = 1080)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                rects = detector(gray, 0)
                for rect in rects:
                    shape = predictor(gray, rect)
                    shape = face_utils.shape_to_np(shape)
                    mouth = shape[mStart:mEnd]
                    MAR = smile(mouth)
                
                
                
                    if MAR >50 and MAR < 55:
                        #cv2.putText(frame, '60%', (200,420), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)
                        frame[:e.shape[0],:e.shape[1]] = e
                    elif MAR >= 55 and MAR < 59:
                        #cv2.putText(frame, '80%', (200,420), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)
                        frame[:r.shape[0],:r.shape[1]] = r
                    elif MAR >= 59:
                        #cv2.putText(frame, '100%', (200,420), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)
                        frame[:t.shape[0],:t.shape[1]] = t
                        cv2.imwrite(name+'.jpg',frame)
                        flag = False
                        del cap
                        preview(name,email,root1,temp)
                    elif MAR <=46:
                        #cv2.putText(frame, 'Not Smiling', (190,420), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 1)
                        frame[:q.shape[0],:q.shape[1]] = q
                    elif MAR >46 and MAR <= 50:
                        #cv2.putText(frame, '40%', (200,420), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2)
                        frame[:w.shape[0],:w.shape[1]] = w
                        
                  
                cv2.imshow("Smile-Detector", frame)
            
                key2 = cv2.waitKey(1) & 0xFF
                if key2 == ord('q'):
                    break
            
            
            cv2.destroyAllWindows()
    
def k():
    subprocess.Popen(["C:\\WINDOWS\\system32\\osk.exe"], shell=True)
    
def female(root):
    root.destroy()
    root1 = Tk()
    root1.title('Login Page')
    root1.overrideredirect(1)
    p2 = Image.open('Pictures/2.png')
    p2 = ImageTk.PhotoImage(p2)
    temp = 'Pictures/3.png'
    btnimg1 = Image.open('Pictures/7.jpg')
    btnimg1 = ImageTk.PhotoImage(btnimg1)
    yscrollbar = Scrollbar(root1,orient = VERTICAL)
    canvas = Canvas(root1,width = 1080,height = 1920,yscrollcommand = yscrollbar.set,scrollregion=(0,0,1080,1920))
    canvas.create_image(542,970,image=p2)
    name = Entry(canvas, width=20, font=('Times', 18))
    #name.bind('<FocusIn>',lambda event: k())
    canvas.create_window(655,745, window=name)
    email = Entry(canvas, width=20, font=('Times', 18))
    canvas.create_window(655,895, window=email)
    btn2 = Button(canvas,image = btnimg1,bg = 'white',padx=0,pady=0,command = lambda:main(root1,name,email,temp))
    #btn2.bind('<Button-1>',lambda event : k())
    canvas.create_window(553,1057,window = btn2)
    yscrollbar.config(command=canvas.yview)
    yscrollbar.pack(side = RIGHT,fill = BOTH)
    canvas.bind_all('<MouseWheel>',lambda event : canvas.yview_scroll(int(-1*(event.delta/120)), "units"))
    btn2.bind('<Return>',lambda event:main(root1,name,email,temp))
    canvas.pack()
    root1.mainloop()


def male(root):
    root.destroy()
    root1 = Tk()
    root1.title('Login Page')
    root1.overrideredirect(1)
    p2 = Image.open("Pictures/7.png")
    p2 = ImageTk.PhotoImage(p2)
    temp = 'Pictures/8.png'
    btnimg1 = Image.open('Pictures/7.jpg')
    btnimg1 = ImageTk.PhotoImage(btnimg1)
    yscrollbar = Scrollbar(root1,orient = VERTICAL)
    canvas = Canvas(root1,width = 1080,height = 1920,yscrollcommand = yscrollbar.set,scrollregion=(0,0,1080,1920))
    canvas.create_image(542,970,image=p2)
    name = Entry(canvas, width=20, font=('Times', 18))
    canvas.create_window(655,760, window=name)
    email = Entry(canvas, width=20, font=('Times', 18))
    canvas.create_window(655,910, window=email)
    btn2 = Button(canvas,image = btnimg1,bg = 'white',padx=0,pady=0,command = lambda:main(root1,name,email,temp))
    canvas.create_window(553,1057,window = btn2)
    yscrollbar.config(command=canvas.yview)
    yscrollbar.pack(side = RIGHT,fill = BOTH)
    canvas.bind_all('<MouseWheel>',lambda event : canvas.yview_scroll(int(-1*(event.delta/120)), "units"))
    btn2.bind('<Return>',lambda event:main(root1,name,email,temp))
    canvas.pack()
    root1.mainloop()



def gender():
    root = Tk()
    root.title('Smile_detector')
    root.overrideredirect(1)
    p1 = Image.open('Pictures/9.png')
    p1 = ImageTk.PhotoImage(p1)
    btnimg1 = Image.open('Pictures/11.png') 
    btnimg1 = ImageTk.PhotoImage(btnimg1)
    btnimg2 = Image.open('Pictures/10.png') 
    btnimg2 = ImageTk.PhotoImage(btnimg2)
    yscrollbar = Scrollbar(root,orient = VERTICAL)
    canvas = Canvas(root,width = 1080,height = 1920,yscrollcommand = yscrollbar.set,scrollregion=(0,0,1080,1920))
    canvas.create_image(542,950,image=p1)
    btn1 = Button(canvas,image = btnimg1,bg = 'white',padx=0,pady=0,bd = 0,command = lambda: male(root))
    canvas.create_window(218,1536,window = btn1)
    btn2 = Button(canvas,image = btnimg2,bg = 'white',padx=0,pady=0,bd = 0,command = lambda:female(root))
    canvas.create_window(869,1536,window = btn2)
    yscrollbar.config(command=canvas.yview)
    yscrollbar.pack(side = RIGHT,fill = BOTH)
    canvas.bind_all('<MouseWheel>',lambda event : canvas.yview_scroll(int(-1*(event.delta/120)), "units"))
    canvas.pack()
    root.mainloop()

while 1:
    gender()

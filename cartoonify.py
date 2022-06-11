# -*- coding: utf-8 -*-
"""
Created on Fri Jun 10 21:35:17 2022

@author: gokul
"""

import cv2
import numpy as np
import imageio
import sys
import matplotlib.pyplot as plt
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile
from PIL import ImageTk, Image
import time

ws = Tk()
ws.title('Upload an image')
ws.geometry('400x200')

# Building a Filebox that helps the user to choose a file from their system and reads the file
def upload():
    # imgpath = easygui.fileopenbox()
    global imgpath 
    imgpath = askopenfile(mode='r', filetypes=[('Image Files', '*jpg')])
    print(imgpath.name)
    imgpath = imgpath.name
    pb1 = Progressbar(
        ws, 
        orient=HORIZONTAL, 
        length=300, 
        mode='determinate'
        )
    pb1.grid(row=4, columnspan=3, pady=20)
    for i in range(5):
        ws.update_idletasks()
        pb1['value'] += 20
        time.sleep(1)
    pb1.destroy()
    Label(ws, text='File Uploaded Successfully!', foreground='green').grid(row=4, columnspan=3, pady=10)
    cartoonify(imgpath)
    
def cartoonify(imgpath):
    img = cv2.imread(imgpath) #image is read from the given path
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Displaying an error msg if img file is not found
    if img is None:
        print("Can't find any image at the given location!\n")
        sys.exit()
        
    resizedimg = cv2.resize(img, (960, 540))
    
    # Gets the resized image in black and white
    grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    resized2 = cv2.resize(grayimg, (960, 540))
    
    # Gets the resized grayscale image with smoothening filter applied
    smoothgrayimg = cv2.medianBlur(grayimg, 5)
    
    resized3 = cv2.resize(smoothgrayimg, (960, 540))
    
    # Retrieving the edges from the smoothened grayscale img
    edgeimg = cv2.adaptiveThreshold(smoothgrayimg, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 9, 9)
    
    resized4 = cv2.resize(edgeimg, (960, 540))
    
    # Gets the resized version of a slightly colored version of the original image
    colorimg = cv2.bilateralFilter(img, 9, 300, 300)
    
    resized5 = cv2.resize(colorimg, (960, 540))
    
    # applies the edge img as mask to the above generated img
    global cartoonimg 
    cartoonimg = cv2.bitwise_and(colorimg, colorimg, mask=edgeimg)
    
    global resized6 
    resized6 = cv2.resize(cartoonimg, (960, 540))
    
    images=[resizedimg, resized2, resized3, resized4, resized5, resized6]
    fig, axes = plt.subplots(3,2, figsize=(8,8), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):
        ax.imshow(images[i], cmap='gray')
    # save button code
    plt.show()
    
    # cv2.imshow(resized6)
    
def save(resized6, imgpath):
    newName="cartoonified_image"
    path1 = os.path.dirname(str(imgpath))
    extension=os.path.splitext(str(imgpath))[1]
    path = os.path.join(path1 + '/' + newName + extension)
    # finalimg = cv2.cvtColor(resized6, cv2.COLOR_RGB2BGR)
    cv2.imwrite(path, cv2.cvtColor(cartoonimg, cv2.COLOR_RGB2BGR))
    # print(os.listdir(path1))
    I = "Image saved by name " + newName +" at "+ path
    tk.messagebox.showinfo(title=None, message=I)
    
top=tk.Tk()
top.geometry('400x400')
top.title('Cartoonify Your Image !')
top.configure(background='white')
label=Label(top,background='#CDCDCD', font=('calibri',20,'bold'))
label.pack()

upload=Button(top,text="Cartoonify an Image",command=upload())
# upload.grid(row=1, column=1, padx=10, pady=5)
# upload.configure(background='#364156', foreground='white',font=('calibri',10,'bold'))
upload.pack(side=TOP,pady=50)

save1=Button(top,text="Save cartoon image",command=lambda: save(cartoonimg, imgpath))
# save1.grid(row=1, column=1, padx=30, pady=5)
# save1.configure(background='#364156', foreground='white',font=('calibri',10,'bold'))
save1.pack(side=TOP,pady=50)

label.mainloop()
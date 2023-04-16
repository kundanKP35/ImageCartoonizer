import cv2              # For image processing
import easygui          # To create the filebox
import numpy as np      # For storing image

import sys
import matplotlib.pyplot as plt
import os                       # For reading path and storing image to that path
import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import customtkinter as ctk    


# root-window
top=ctk.CTk()
top.geometry('900x600')
top.title('Cartoonify Your Image!')
top.configure(background='white')
label=ctk.CTkLabel(top, font=('Century Gothic',20,'bold'))


# Fileopenbox to create a window for selecting image and store image path as string 
def upload():
    global ImagePath
    ImagePath=easygui.fileopenbox()

    image=cv2.imread(ImagePath)
    
    image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    image = cv2.resize(image,(600,400))
    
    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(image)

    canvas.image = image
    canvas.create_image(0,0,anchor="nw",image=image)

    
def dummy():
    cartoonify(ImagePath)
  

def cartoonify(ImagePath):
    # Read the image
    originalmage = cv2.imread(ImagePath)
    originalmage = cv2.cvtColor(originalmage, cv2.COLOR_BGR2RGB)

    # Confirm that the image is chosen
    if originalmage is None:
        print("Image not found. Please Choose appropriate file")
        sys.exit()

    ReSizedImg = cv2.resize(originalmage, (960, 540))


    # Transforming the image to grayscale
    grayScaleImage= cv2.cvtColor(originalmage, cv2.COLOR_BGR2GRAY)
    grayImg = cv2.resize(grayScaleImage, (960, 540))


    # Applying median blur to smoothen the image
    smoothGrayScale = cv2.medianBlur(grayScaleImage, 7)
    blurImg = cv2.resize(smoothGrayScale, (960, 540))


    # Retrieving the edges for cartoon effect by using thresholding technique
    getEdge = cv2.adaptiveThreshold(smoothGrayScale, 255, 
        cv2.ADAPTIVE_THRESH_MEAN_C, 
        cv2.THRESH_BINARY, 19, 7) #line_size,blur_value

    edgeImg = cv2.resize(getEdge, (960, 540))

    # Applying bilateral filter to remove noise and keep edge sharp as required
    colorImage = cv2.bilateralFilter(originalmage, 9, 200, 200)
    filterImg = cv2.resize(colorImage, (960, 540))


    # Masking edged image with our  image
    cartoonImage = cv2.bitwise_and(colorImage, colorImage, mask=getEdge)

    cartoonImg = cv2.resize(cartoonImage, (960, 540))

    # Plotting the whole transition
    images=[ReSizedImg, grayImg, blurImg, edgeImg, filterImg, cartoonImg]

    fig, axes = plt.subplots(3,2, figsize=(8,8), subplot_kw={'xticks':[], 'yticks':[]}, gridspec_kw=dict(hspace=0.1, wspace=0.1))
    for i, ax in enumerate(axes.flat):        
        ax.imshow(images[i], cmap='gray')


    
    plt.show()

    image = cartoonImg.copy()
    
    image = cv2.resize(image,(600,400))
    
    image = Image.fromarray(image)
    image = ImageTk.PhotoImage(image)

    canvas.image = image
    canvas.create_image(0,0,anchor="nw",image=image)

    
    save1=ctk.CTkButton(top,text="Save Cartoon Image",fg_color="blue",command=lambda: save(cartoonImg, ImagePath))
    save1.place(x=665,y=230)
    
    
def save(cartoonImg, ImagePath):

    # Saving the image using imwrite()
    newName="cartoonified_Image"
    path1 = os.path.dirname(ImagePath)
    extension=os.path.splitext(ImagePath)[1]
    path = os.path.join(path1, newName+extension)
    cv2.imwrite(path, cv2.cvtColor(cartoonImg, cv2.COLOR_RGB2BGR))
    I= "Image saved by name " + newName +" at "+ path
    tk.messagebox.showinfo(title=None, message=I)


# Custom frame inside root
frame=ctk.CTkFrame(master=top,width=740,height=500,corner_radius=15)
frame.place(relx=0.5,rely=0.5,anchor=tk.CENTER)


text_var = tk.StringVar(value="Image Cartoonizer")

label = ctk.CTkLabel(master=frame,
                               textvariable=text_var,
                               width=120,
                               height=25,
                               fg_color="transparent",
                               font=('Century Gothic',40),
                               corner_radius=8)
label.place(x=180,y=10)

# Canvas to insert uploaded image
canvas = Canvas(frame,width=600,height=400,highlightthickness=0)
myColor = '#2b2b2b'
image=cv2.imread("upload.png")
    
image = cv2.resize(image,(600,400))
    
image = Image.fromarray(image)
image = ImageTk.PhotoImage(image)

canvas.image = image
canvas.create_image(0,0,anchor="nw",image=image)
canvas.configure(bg=myColor)
canvas.place(x=250,y=110)


upload=ctk.CTkButton(frame,text="Select image",fg_color="red",command=upload)
upload.place(x=300,y=400)

upload=ctk.CTkButton(frame,text="Cartoonify",fg_color="green",command=dummy)
upload.place(x=300,y=440)

top.mainloop()




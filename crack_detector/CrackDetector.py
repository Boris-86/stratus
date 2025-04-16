#===============================================================================
# 
# Created on june 10th, 2015
# 
# @author: Boris Rozenman
# @id: 310179635
#
#===============================================================================

#===============================================================================
#                                 Libraries
#===============================================================================
import matplotlib.pyplot as plt
import numpy as np
import tkFileDialog
from numpy import *
import cv2
import copy
import ImageTk
import Image
import tkMessageBox
import ImageOps
import Image
from scipy import signal
from pylab import *
import Tkinter
import tkMessageBox
import Image
import tkFileDialog
import os
import glob
import ImageTk
from ImageOps import fit
from Tkconstants import HORIZONTAL
from Tkinter import tkinter
#===============================================================================
#                                   Constants
#===============================================================================
n = 0
pad_x = 10
pad_y = 5
canvas_n = 450
x = range(0,256)
#===============================================================================
#                                  GUI Methods
#===============================================================================
class WindowsForm(Tkinter.Tk):
    
    def __init__(self,parent):
        # Constructor
        Tkinter.Tk.__init__(self,parent) 
        self.parent = parent
        self.Build_Form() 
    
    def nothing(self, x):
        pass
    
    def Build_GUI(self):
        #Labels: 
        enter_lbl = Tkinter.Label(self,anchor="w",text="Hey There! ")
        brt_lbl = Tkinter.Label(self,anchor="w",text="Brightness : ")      
        cont_lbl = Tkinter.Label(self,anchor="w",text="Contrast : ")             
        gama_lbl = Tkinter.Label(self,anchor="w",text="Gamma Correction : ")
        canny_lbl = Tkinter.Label(self,anchor="w",text="Canny Param's (0-1500) : ")
         
        self.pic1_lbl =  Tkinter.Label(self,anchor="w",text="Source Picture:")
        self.pic2_lbl =  Tkinter.Label(self,anchor="w",text="Transformed Picture:")
        self.pic3_lbl =  Tkinter.Label(self,anchor="w",text="Canny Picture:")
        self.pic4_lbl =  Tkinter.Label(self,anchor="w",text="Auxiliary Laplace Picture:")

        #Labels Placing:
        enter_lbl.grid(columnspan=3,row=0,sticky='EW',padx=pad_x) 
        brt_lbl.grid(column=1,row=0,sticky='EW',padx=pad_x)       
        cont_lbl.grid(column=2,row=0,sticky='EW',padx=pad_x)       
        gama_lbl.grid(column=3,row=0,sticky='EW',padx=pad_x)
        canny_lbl.grid(column=4,row=0,sticky='EW',padx=pad_x)
        
        #Entries: 
        self.brt_bar = Tkinter.Scale(from_=-200,to_=200, resolution=10, orient=HORIZONTAL,command = self.BrightnessTransform, sliderlength = 22)
        self.cont_bar = Tkinter.Scale(from_=0.05,to_=3, resolution=0.05, orient=HORIZONTAL,command = self.ContrastTransform, sliderlength = 22)
        self.gama_bar = Tkinter.Scale(from_=-2,to_=7, resolution=0.05, orient=HORIZONTAL,command = self.GammaCorrection, sliderlength = 22)
        self.cannyMin_bar = Tkinter.Scale(from_=0,to_=1400, resolution=5, orient=HORIZONTAL, sliderlength = 22)
        self.cannyMax_bar = Tkinter.Scale(from_=50,to_=1500, resolution=5, orient=HORIZONTAL, sliderlength = 22)
        self.brt_bar.set(0)
        self.cont_bar.set(1)
        self.gama_bar.set(1)
        self.cannyMin_bar.set(100)
        self.cannyMax_bar.set(400)
        
        #Entries Placing:
        self.brt_bar.grid(column=1,row=1,sticky='EW', padx=pad_x)
        self.cont_bar.grid(column=2,row=1,sticky='EW', padx=pad_x)
        self.gama_bar.grid(column=3,row=1,sticky='EW', padx=pad_x)
        self.cannyMin_bar.grid(column=4,row=1,sticky='EW', padx=pad_x)
        self.cannyMax_bar.grid(column=5,row=1,sticky='EW', padx=pad_x)       

    def Build_Buttons(self):
        #Buttons: 
        self.hist_btn = Tkinter.Button(self,text="*Hist Equalization*", font = "verdana 10 bold ", fg = "orange", command = self.HistEqualization, state="disabled")
        self.load_btn = Tkinter.Button(self,text="<Load Image>",font = "verdana 10 bold ", fg = "blue",command = self.LoadImage)
        self.resetP_btn = Tkinter.Button(self,text="<Reset Image>",font = "verdana 10 bold ", fg = "green", command = self.ResetPic, state="disabled")
        self.reset_btn = Tkinter.Button(self,text="@Reset App@",font = "verdana 10 bold ", fg = "red", command = self.ResetApp, state="disabled")
        self.detect_btn = Tkinter.Button(self,text="$> Detect Cracks! <$",font = "verdana 10 bold ", fg = "blue", command = self.DetectCracks, state="disabled")
        
        #Buttons Placing:
        self.load_btn.grid(column=0,row=1,rowspan=1,pady=pad_y,sticky='ew',padx=pad_x)
        self.detect_btn.grid(column=6,row=1,columnspan=2,sticky='ew',padx=pad_x)
        self.hist_btn.grid(column=5,row=0,columnspan=1,sticky='ew',padx=pad_x,pady=pad_y)
        
        self.reset_btn.grid(column=7,row=0,sticky='ew',padx=pad_x, pady=pad_y)
        self.resetP_btn.grid(column=6,row=0,sticky='ew',padx=pad_x)
             
    def Build_Form(self):
        #Building form parts:
        self.grid()
        self.Build_GUI()
        self.Build_Buttons()
        self.img_flag = 0
        self.brit = 0
        self.cont = 1
        self.gama = 1

#===============================================================================
#                                - Methods - 
#===============================================================================   

    def RGB2gray(self, rgb):
        r, g, b = rgb[:,:,0], rgb[:,:,1], rgb[:,:,2]
        gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
        return gray
    
    def ImageResize(self, temp_image):
        '''Gets gray array picture, resizing picture & saving the ratio
           returns resized photo'''
        size_m, size_n = temp_image.shape
        ratio = float(size_m)/float(size_n)
        self.canvas_m = (int(canvas_n * ratio) + 1)  
        self.dataImage = Image.fromarray(temp_image)
        self.scaledDataImage = self.dataImage.resize((canvas_n,self.canvas_m), Image.ANTIALIAS)
        self.scaledPhoto = ImageTk.PhotoImage(self.scaledDataImage)
        return self.scaledPhoto
       
    def LoadImage (self):
        #Loading image:
        if (self.img_flag == 0):
            try:           
                fileName = tkFileDialog.askopenfilename() 
                self.arrayImage = np.array(Image.open(fileName))   
            except:
                tkMessageBox.showinfo("Note","Image not loaded.")
                return
        else: 
            try:
                self.ResetApp()           
                fileName = tkFileDialog.askopenfilename() 
                self.arrayImage = np.array(Image.open(fileName))   
            except:
                tkMessageBox.showinfo("Note","Image not loaded.")
                return 
        self.MainGrayImage = self.RGB2gray(self.arrayImage)
        #Main Photo Display:
        self.mainFixPhoto = self.ImageResize(self.MainGrayImage)
        #self.temp_canvas.delete("all")
        self.mainImage_canvas = Tkinter.Canvas(self, height= self.canvas_m, width= canvas_n)
        self.mainImage_canvas.grid(row=7,column=0,rowspan=6,columnspan=3,padx=pad_x,pady=pad_y)
        self.mainImage_canvas.create_image(0, 0, image=self.mainFixPhoto, state="normal",anchor="nw" )
        self.pic1_lbl.grid(column=0, row=6,sticky='EW', padx = 3*pad_x)
        self.transImage = self.MainGrayImage
        self.DisplayTransformed()
        
        #Enabling Buttons:  
        self.hist_btn.config(state='normal')
        self.reset_btn.config(state='normal')
        self.resetP_btn.config(state='normal')
        self.detect_btn.config(state='normal')
        self.img_flag = self.img_flag + 1
           
    def DisplayTransformed (self):
        #Transformed Photo Display: 
        self.transFixPhoto = self.ImageResize(self.transImage)
        self.transImage_canvas = Tkinter.Canvas(self, height= self.canvas_m, width= canvas_n) 
        self.transImage_canvas.grid(row=15,column=0,rowspan=6,columnspan=3,padx=pad_x,pady=pad_y)
        self.transImage_canvas.create_image(0, 0, image=self.transFixPhoto, state="normal",anchor="nw" )
        self.pic2_lbl.grid(column=0, row=14,sticky='EW', padx = 3*pad_x)
        return
    
    def BrightnessTransform(self,x):
        brightness = np.double(x) 
        #Transformations:
        try:
            self.transImage = self.transImage + (brightness - self.brit) # self.brit = previous value
        except: 
            return
        self.DisplayTransformed()
        self.brit = brightness
   
    def ContrastTransform(self,x):
        contrast = np.double(x) 
        #Transformations:
        try:
            self.transImage = (self.transImage / self.cont) #previous value
            self.transImage = (self.transImage * contrast)
        except: 
            return
        self.DisplayTransformed()
        self.cont = contrast 
        
    def GammaCorrection(self,x):
        gamma = np.double(x)
        if (gamma < 0.01 and gamma > -0.01 ):
                gamma = 0.01    
        #Transformations:
        try:
                self.transImage = (255) * ((self.transImage /255)**(self.gama)) #previous value
                self.transImage = 255 * ((self.transImage /255)**(1.0/gamma))
        except: 
            return
        self.DisplayTransformed()
        self.gama = gamma
    
    def CreateLUT (self):
        #Aux Function for Histogram Equalization:
        plt.clf()
        data = self.transImage.flatten() 
        self.n, _, _ = plt.hist(data, bins = 256, range = [0,256], color = "white") 
        temp_lut = [0.0]*256
        nD = max(self.MainGrayImage.flatten())
        nD = np.around(nD)
        pixelsSum = 0
        pixelsNum = self.MainGrayImage.size
        for i in range(0,256): 
            pixelsSum += self.n[i]
            cdf = float(pixelsSum)/float(pixelsNum)
            temp_lut[i] = nD*cdf
        temp_lut = [int(round(element)) for element in temp_lut]     
        return temp_lut 
     
    def HistEqualization (self):
        lut = self.CreateLUT()
        m,n = self.MainGrayImage.shape
        equalHistImage = self.MainGrayImage
        #Equalization Process: 
        for i in range(0,m):
            for j in range(0,n):
                equalHistImage[i,j] = lut[int(np.around(self.MainGrayImage[i,j]))]
        #Equalized Photo Display:
        self.equalPhoto = self.ImageResize(equalHistImage) 
        self.equalPhoto_canvas = Tkinter.Canvas(self, height= self.canvas_m, width= canvas_n)
        self.equalPhoto_canvas.grid(row=15,column=0,rowspan=6,columnspan=3,padx=pad_x,pady=pad_y)
        self.equalPhoto_canvas.create_image(0, 0, image=self.equalPhoto, state="normal",anchor="nw" )
        self.pic2_lbl.grid(column=0, row=14,sticky='EW', padx = 3*pad_x)
    
    def ResetApp (self):
        #Resets the entire app:
        self.hist_btn.config(state='disabled')
        self.reset_btn.config(state='disabled')
        self.resetP_btn.config(state='disabled')
        self.load_btn.config(state='normal')
        self.detect_btn.config(state='disabled')
        
        self.brt_bar.set(0)
        self.cont_bar.set(1)
        self.gama_bar.set(1)
        self.cannyMin_bar.set(100)
        self.cannyMax_bar.set(400)
        
        self.mainImage_canvas.delete("all")
        self.mainImage_canvas.grid_remove()
        self.transImage_canvas.delete("all")
        self.transImage_canvas.grid_remove()
        
        self.pic1_lbl.grid_remove()
        self.pic2_lbl.grid_remove()
        self.pic3_lbl.grid_remove()
        self.pic4_lbl.grid_remove()
        
        try:
            self.cannyImg_canvas.delete("all")
            self.cannyImg_canvas.grid_remove()
            self.LplsImg_canvas.delete("all")
            self.LplsImg_canvas.grid_remove()
        except:
            return

        return
    
    def ResetPic (self):
        #Resets Picture parameters:
        self.brt_bar.set(0)
        self.cont_bar.set(1)
        self.gama_bar.set(1)
        self.cannyMin_bar.set(100)
        self.cannyMax_bar.set(400)
        
        self.MainGrayImage = self.RGB2gray(self.arrayImage)
        self.transImage = self.MainGrayImage
        #Main Photo Display:
        self.mainFixPhoto = self.ImageResize(self.MainGrayImage)
        self.mainImage_canvas = Tkinter.Canvas(self, height= self.canvas_m, width= canvas_n)
        self.mainImage_canvas.grid(row=7,column=0,rowspan=6,columnspan=3,padx=pad_x,pady=pad_y)
        self.mainImage_canvas.create_image(0, 0, image=self.mainFixPhoto, state="normal",anchor="nw" ) 
        self.transImage_canvas = Tkinter.Canvas(self, height= self.canvas_m, width= canvas_n)
        self.transImage_canvas.grid(row=15,column=0,rowspan=6,columnspan=3,padx=pad_x,pady=pad_y)
        self.transImage_canvas.create_image(0, 0, image=self.mainFixPhoto, state="normal",anchor="nw" ) 
        return        
    
    def DetectCracks (self):
        # Canny and Laplace operator edge detection:
        matplotlib.image.imsave('tmp.png', self.transImage)
        matplotlib.image.imsave('tmp2.png', self.transImage)
        cvImg = cv2.imread('tmp.png')
        cvImg2 = cv2.imread('tmp2.png',0)
        
        self.cannyMin = np.double(self.cannyMin_bar.get())
        self.cannyMax = np.double(self.cannyMax_bar.get()) 
        #kernel = np.ones((15,15),np.uint8)
             
        cvImgBlr = cv2.GaussianBlur(cvImg,(5,5),0)
        cvImgBlr = cv2.GaussianBlur(cvImgBlr,(5,5),0)
        cvImgBlr = cv2.GaussianBlur(cvImgBlr,(5,5),0)
        
        self.canny = cv2.Canny(cvImgBlr, self.cannyMin, self.cannyMax)
        self.canny = cv2.GaussianBlur(self.canny,(5,5),0)
        self.canny = cv2.Canny(self.canny, self.cannyMin, self.cannyMax)
        self.canny = 3*self.canny
        
        #=======================================================================
      
        self.laplace = cv2.Laplacian(cvImg2,cv2.CV_32F)
        self.laplace = 255 * ((self.laplace /255)**(2))
        self.laplace = 1.5*self.laplace+25
       
        #Displaying Canny result:
        self.cannyImg = self.ImageResize(self.canny) 
        self.cannyImg_canvas = Tkinter.Canvas(self, height= self.canvas_m, width= canvas_n)
        self.cannyImg_canvas.grid(row=7,column=3,rowspan=6,columnspan=3,padx=pad_x,pady=pad_y)
        self.cannyImg_canvas.create_image(0, 0, image=self.cannyImg, state="normal",anchor="nw" )
        self.pic3_lbl.grid(column=3, row=6,sticky='EW', padx = 3*pad_x)
        
        #Displaying Laplace result:
        self.LplsImg = self.ImageResize(self.laplace) 
        self.LplsImg_canvas = Tkinter.Canvas(self, height= self.canvas_m, width= canvas_n)
        self.LplsImg_canvas.grid(row=16,column=3,rowspan=6,columnspan=3,padx=pad_x,pady=pad_y)
        self.LplsImg_canvas.create_image(0, 0, image=self.LplsImg , state="normal",anchor="nw" )
        self.pic4_lbl.grid(column=3, row=14,sticky='EW', padx = 3*pad_x)

plt.show()
        
#===============================================================================
#                                  - MAIN - 
#===============================================================================   
if __name__ == '__main__':
    
    form1=WindowsForm(None)
    form1.title("Crack Detector By Boris Rozenman. (c). ")
    form1.mainloop()
    
#===============================================================================
#                                  - END OF FILE - 
#===============================================================================
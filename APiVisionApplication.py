import os
import io

import gspread
import tkinter as tk
from tkinter import ttk, messagebox 
from PIL import Image, ImageTk

from google.cloud import vision
from google.cloud.vision_v1 import types

import logging

'''__Summary___

This project will gather data from the batch, return results

Constants:
__ Gspread __
'''

CREDENTIAL="C:\\Users\\admin\\Downloads\\Python_Project\\Machine learning\\AbccProductionCredentials.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS']=CREDENTIAL

sa=gspread.service_account(filename=CREDENTIAL)

def Object_Recognizer(Image_url=str)->list:
    client=vision.ImageAnnotatorClient()
    image=types.Image()
    image.source.image_uri=Image_url

    response= client.object_localization(image=image)
    txt=''
    num=0
    var=""
    
    for obj in response.localized_object_annotations:
        if obj.name in ["Dog","Cat",'Person','People']:
            num+=1
            txt+=f"{obj.name} : {obj.score}\n"
    Output_Localized=[num,txt]
    num=0
    txt=''
    response_image=client.face_detection(image=image)
    for face in response_image.face_annotations:
        num+=1
        txt+=f"Confidence:{face.detection_confidence}\n"
    
    Output_Localized.append(num)
    Output_Localized.append(txt)
    
    return Output_Localized
    '''__ Expected Result__
    
    [Number of people, Confidence detection in number]
    '''



'''__ Images ___'''
CloudImage="C:\\Users\\admin\\Downloads\\Python_Project\\Machine learning\\CloudIPVision.jpg"
ApiImg=Image.open(CloudImage)
resize_img=ApiImg.resize((400,180),Image.Resampling.LANCZOS)

'''__ LOGO __'''

Logo_img="C:\\Users\\admin\\Downloads\\LOGO.ico"

'''__ Fonts __'''
font_tuple=('Calibri 14')
sheet_list=list()

def next_available_row(worksheet,i=int):
    str_list = list(filter(None, worksheet.col_values(i)))
    return int(len(str_list)+1)


class API_Vision_App(tk.Tk):
    global sheet_list
    def Batch_Checker(self):
        try:
            sa.open(self.Batch_Entry.get())
            messagebox.showinfo("Update", f"(UPDATE) - {self.Batch_Entry.get()} is added!")
            sheet_list.append(self.Batch_Entry.get())
            
        except:
            messagebox.showerror("Error",f"(ERROR) - Spreadsheet Not Found")
        

    def API_Vision_Generator(self):
        global sheet_list
        output=[]
        for sheet in sheet_list:
            Batch=sa.open(sheet)
            Datium=Batch.worksheet("Data")
            Batch_Tracker_Sheet=Batch.worksheet("Batch tracker")
            next_row=next_available_row(Batch_Tracker_Sheet,1)
            Image_List= Batch_Tracker_Sheet.get(f"E2:E{next_row+2}")
            
            for url in Image_List:
                if url!=[]:
                    if url[0][:17]=="https://orderdesk":
                        output.append(Object_Recognizer(url[0]))    
                    else:
                        output.append(['','','',''])
                else:
                    output.append(['','','',''])
            
            output.insert(0,["Number of person,","Accuracy","Confidence","Accuracy"])
            Datium.update(f"AD1:AG{next_row + 1}",output, raw=False)
        messagebox.showinfo("Update","All batches have been updated")
        sheet_list.clear()
            

    
    def __init__(self) -> None:
        super().__init__()
        '''__ Title & Logo '''
        self.title("API Vision")
        self.iconbitmap(Logo_img)        
        '''__ Style text __'''
        style1=ttk.Style()
        style1.configure('my.TButton',font=font_tuple,foreground='blue4')
        style1.configure('Big.TButton',font=('Calibri 16'),foreground='blue4')        
        '''__Image Label__'''
        self.Ip_Img=ImageTk.PhotoImage(resize_img)
        self.Ip_Img_label=ttk.Label(self,image=self.Ip_Img)
        self.Ip_Img_label.pack()
        '''__ Batch Entry & Submit button __'''
        self.Frame_Work=ttk.Frame(self,)
        self.Frame_Work.pack()
        
        self.Batch_Entry=ttk.Entry(self.Frame_Work,width=25, font=font_tuple,)
        self.Batch_Entry.grid(row=0,column=0)

        self.Submit_Batch=ttk.Button(self.Frame_Work,text="Submit Batch", style='my.TButton', command=self.Batch_Checker)
        self.Submit_Batch.grid(row=0,column=1,padx=10)

        '''__ Submit Data to batches __'''
        
        self.Create_Data=ttk.Button(self,text="Generate Data", width=15, style='Big.TButton',command=self.API_Vision_Generator)
        self.Create_Data.pack()

if __name__=="__main__":
    
    API_APP=API_Vision_App()
    API_APP.mainloop()

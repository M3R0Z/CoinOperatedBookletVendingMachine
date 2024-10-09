import customtkinter, os, time, psutil, shutil, convertapi, PyPDF2, win32print, subprocess, serial
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter import Frame, Label
from PIL import Image, ImageTk
from threading import Thread
from datetime import datetime
from CTkTable import *
from twilio.rest import Client
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId

BackgroundColor = "Dimgray"
WidgetColor = "Skyblue"
Available_Booklets = 17
Available_Papers = 50
Available_Coins = 30
Number_Of_Booklet = 0
Number_Of_Paper = 0
Max_Booklet = 17
Max_Paper = 50
Max_Coin = 30
Booklet_Cost = 10
Paper_Cost = 5
Total_Cost = 0
Total_Paper_Cost = 0
Inserted = 0
One = 0
Five = 0
Ten = 0
USB = 1
Current = "Main"
Service_Current = "Booklet"
Unique_Filename = ""
ID = 1
Print_ID = 0
Select = 0
Current_Row = 0
Previous_Row = 0
Preview_ID = 0
Check = 0
Entered_Passcode = ""
Current_UserCode = ""
Admin_Attempt = 0
User_Attempt = 0
Booklet_State = 1
Paper_State = 1
Max_Coin_Storage = 150
Papers_Check = 3
Booklets_Check = 3
Coins_Check = 3
Vend_Money = 0
Main_Image = "images/SkyBlue_Main.png"
USB_Image = "images/SkyBlue_USB.png"
Encountered_B = ""
Encountered_B1 = 0
Encountered_B2 = 0
Encountered_B3 = 0
Encountered_P = ""
Encountered_P1 = 0
Encountered_P2 = 0
Encountered_P3 = 0
Encountered_P4 = 0
Encountered_C = ""
Encountered_C1 = 0
Encountered_C2 = 0
class Vending_Machine:
    def __init__(self):
        self.UI_Properties()

    def UI_Properties(self):
        global BackgroundColor, WidgetColor
        self.UI = customtkinter.CTk()
        self.UI.overrideredirect(True)
        Screen_Width = self.UI.winfo_screenwidth()
        Screen_Height = self.UI.winfo_screenheight()
        self.UI.geometry(f"{Screen_Width}x{Screen_Height}+0+0")
        customtkinter.set_appearance_mode("Dark")
        customtkinter.set_default_color_theme("green")
        #self.MongoDB() uncomment line 81, 88, 119+, 223
        self.Unique_File_Names = []
        self.User_ID = []
        self.Vend_Database = []
        Twilio_Account_SID = 'AC12b5ba58f15f903cd066727b825bd96d'
        Twilio_Auth_Token = '7cd13f1604573306218ceb30f2c673e3'
        self.Twilio_Client = Client(Twilio_Account_SID, Twilio_Auth_Token)
        #self.Database_Users() uncomment
        self.Start_UI()

    def MongoDB(self):
        MongoDB_URI = "mongodb+srv://markwilsonyb:markwilsonyb@coinvend.6ckzs.mongodb.net/?retryWrites=true&w=majority"
        UserVend = MongoClient(MongoDB_URI, server_api=ServerApi('1'))
        UserData = UserVend["CoinVend"]
        VendStock = UserVend["CoinVend"]
        self.Collection_UserData = UserData["CoinVend"]
        self.Collection_VendStock = VendStock["VendStock"]

    def Start_UI(self):
        global BackgroundColor, WidgetColor, Current, USB, Main_Image, Available_Papers, Available_Booklets, Available_Coins, ID
        USB = 0
        for widget in self.UI.winfo_children():
            widget.destroy()
        Current = "Main"
        self.Background = self.Frame(1920,1080,0,0)
        self.Background.configure(fg_color=WidgetColor)
        self.LeftMain = self.Frame(300, 817, 25, 25, master=self.Background)
        self.RightMain = self.Frame(1160, 697, 350, 145, master=self.Background)
        self.RightMainM = self.Frame(1160, 817, 350, 25, master=self.Background)
        self.Image("images/CDM.png", 175, 175, 45, 45, master=self.LeftMain)
        self.Image(Main_Image, 1300, 350, -60, 350, master=self.RightMainM).configure(
            height=400, border_color=WidgetColor, border_width=10)
        self.Label("Coin-Operated Booklet Vending Machine", 30, 45, master=self.RightMainM)
        self.Label("       With Printing Services        ", 155, 145, master=self.RightMainM)
        self.Label("     For CDM Students And Faculty    ", 75, 245, master=self.RightMainM)
        self.Main_Widgets()
        self.Service_State()
        Current_Date = datetime.now().strftime("%Y-%m-%d")
        #Database = self.Collection_UserData.find({"Date": Current_Date})  uncomment from here to below
        IDs = []
        id_num = 1
        #for document in Database:
        #    User_ID = document.get('User_ID')
        #    if User_ID is not None:
        #        STR_User_ID = str(User_ID)
        #        INT_User_ID = int((STR_User_ID)[-2])
        #        IDs.append(INT_User_ID)
        #    self.User_ID.append(STR_User_ID)
        #    id_num += 1
        #ID = (len(IDs)) + 1
        #Database_Stock = self.Collection_VendStock.find_one({"User_ID": "ADMIN01"})
        #if Database_Stock:
        #    Database_Booklet_Stock = Database_Stock.get('Booklet')
        #    Database_Booklet_Stock_Value = Database_Booklet_Stock.split('/')[0].strip()
        #    Available_Booklets = int(Database_Booklet_Stock_Value)
        #    Database_Paper_Stock = Database_Stock.get('Paper')
        #    Database_Paper_Stock_Value = Database_Paper_Stock.split('/')[0].strip()
        #    Available_Papers = int(Database_Paper_Stock_Value)
        #    Database_Change_Stock = Database_Stock.get('Change')
        #    Database_Change_Stock_Value = Database_Change_Stock.split('/')[0].strip()
        #    Available_Coins = int(Database_Change_Stock_Value)
        self.Service_State()


    def Main_Widgets(self):
        global BackgroundColor
        self.Main = self.Button("Main", 25, 300, "images/Main.png", self.Main_UI, master=self.LeftMain)
        self.Buy = self.Button("Booklet", 25, 380, "images/Booklet.png", self.Booklet_UI, master=self.LeftMain)
        self.Print = self.Button("Print", 25, 460, "images/Printer.png", self.Print_UI, master=self.LeftMain)
        self.Setting = self.Button("Setting", 25, 540, "images/Setting.png", self.Admin_UI, master=self.LeftMain)
        self.Request = self.Button("Request", 25, 620, "images/Request.png", self.Request_UI, master=self.LeftMain)
        self.Main2 = self.Button("Main", 25, 300, "images/Main.png", command=None, master=self.LeftMain)
        self.Buy.configure(fg_color=BackgroundColor)
        self.Print.configure(fg_color=BackgroundColor)
        self.Setting.configure(fg_color=BackgroundColor)
        self.Request.configure(fg_color=BackgroundColor)

    def Main_UI(self):
        self.Main.configure(fg_color=WidgetColor)
        self.Buy.configure(fg_color=BackgroundColor)
        self.Print.configure(fg_color=BackgroundColor)
        self.Setting.configure(fg_color=BackgroundColor)
        self.Request.configure(fg_color=BackgroundColor)
        self.Start_UI()

    def Database_Users(self):
        Current_Date = datetime.now().strftime("%Y-%m-%d")
        Database = self.Collection_UserData.find({"Date": Current_Date})
        IDs = []
        id_num = 1
        for document in Database:
            User_ID = document.get('User_ID')
            User_Time = document.get('Time')
            User_Service = document.get('Service')
            User_Quantity = document.get('Quantity')
            User_Cost = document.get('Cost')
            User_Total = document.get('Total')
            User_Coins = document.get('Coins')
            User_Change = document.get('Change')
            self.Vend_Database.append(id_num)
            self.Vend_Database.append(User_ID)
            self.Vend_Database.append(Current_Date)
            self.Vend_Database.append(User_Time)
            self.Vend_Database.append(User_Service)
            self.Vend_Database.append(User_Quantity)
            self.Vend_Database.append(User_Cost)
            self.Vend_Database.append(User_Total)
            self.Vend_Database.append(User_Coins)
            self.Vend_Database.append(User_Change)
            id_num += 1
    def Booklet_UI(self):
        global BackgroundColor, WidgetColor, Available_Booklets, Booklet_Cost, Current, Service_Current, USB
        USB = 0
        self.RightMainM.destroy()
        self.RightMain.configure(fg_color="black")
        self.Buy.configure(fg_color=WidgetColor)
        self.Main.configure(fg_color=BackgroundColor)
        self.Print.configure(fg_color=BackgroundColor)
        self.Setting.configure(fg_color=BackgroundColor)
        self.Request.configure(fg_color=BackgroundColor)
        self.Delete()
        self.Service_State()
        self.Buy2 = self.Button("Booklet", 25, 380, "images/Booklet.png", command=None, master=self.LeftMain)
        self.Title = self.Frame(1180, 130, 340, 15, master=self.Background)
        self.Title.configure(border_width=10, border_color=WidgetColor, corner_radius=20, fg_color="black")
        self.Label(" B O O K L E T ", 380, 33, master=self.Title).configure(font=("Arial", 60, "bold"), fg_color="black")
        if Current == "Main":
            self.Main2.destroy()
        elif Current == "Print":
            self.Delete_Print_Frames()
            self.Print2.destroy()
        elif Current == "File Choose":
            self.Delete_File_Choose_frames()
            self.Print2.destroy()
        elif Current == "Admin":
            self.Delete_Admin_Frames()
            self.Setting2.destroy()
        elif Current == "Help":
            self.Delete_User_Frames()
            self.Request2.destroy()
        Current = "Booklet"
        Service_Current = "Booklet"
        #Database_Booklet_Stock = self.Collection_VendStock.find_one({"User_ID": "ADMIN01"}) uncomment
        self.Available = self.Frame(1110, 130, 375, 170, master=self.Background)
        self.Available.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Label(f"Available: {Available_Booklets} pcs.", 45, 35, master=self.Available)
        Booklet_Stock = customtkinter.CTkProgressBar(master=self.Available, width=450, height=40, progress_color="green",
                                                     border_color=WidgetColor, border_width=5)
        Booklet_Stock.set(Available_Booklets / Max_Booklet)
        Booklet_Stock.place(x=600, y=45)
        if Available_Booklets <= 5:
            Booklet_Stock.configure(progress_color="red")
        elif Available_Booklets <= 10:
            Booklet_Stock.configure(progress_color="yellow")

        self.Quantity = self.Frame(1110, 130, 375, 290, master=self.Background)
        self.Quantity.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        Quantity = self.Label("Quantity:  0 pcs.", 65, 35, master=self.Quantity)
        Quantity2 = self.Label(" ", 665, 28, master=self.Quantity)
        self.Cost = self.Frame(1110, 130, 375, 410, master=self.Background)
        self.Cost.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        Total = self.Label("Total:  0 ₱", 157, 35, master=self.Cost)
        Total2 = self.Label(f"0 📕 x {Booklet_Cost} 🪙", 675, 28, master=self.Cost)

        def Update_Text(event):
            global Total_Cost, Number_Of_Booklet
            Quantity.configure(text=f"Quantity:  {int(Slider_Booklet.get())} pcs.")
            if int(Slider_Booklet.get()) != 0:
                if int(Slider_Booklet.get()) == 5:
                    Quantity2.configure(text="📕 📕 📕 📕 📕")
                elif int(Slider_Booklet.get()) == 4:
                    Quantity2.configure(text="📕 📕 📕 📕")
                elif int(Slider_Booklet.get()) == 3:
                    Quantity2.configure(text="📕 📕 📕")
                elif int(Slider_Booklet.get()) == 2:
                    Quantity2.configure(text="📕 📕")
                elif int(Slider_Booklet.get()) == 1:
                    Quantity2.configure(text="📕")
                Proceed.configure(state="normal")
            else:
                Quantity2.configure(text="")
                Proceed.configure(state="disabled")
            Total.configure(text=f"Total:  {int(Slider_Booklet.get())*Booklet_Cost} ₱")
            Total2.configure(text=f"{int(Slider_Booklet.get())} 📕 x {Booklet_Cost} 🪙")
            Number_Of_Booklet = int(Slider_Booklet.get())
            Total_Cost = int(Slider_Booklet.get())*Booklet_Cost

        self.Slider_Frame = self.Frame(560, 250, 925, 565, master=self.Background)
        self.Slider_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        #self.Image("images/SkyBlueBooklet.png",300,300,20,23,master=self.Booklet_Image)
        Available = 5
        if Available_Booklets < 5:
            Available = Available_Booklets
        self.Extra_Frame = self.Frame(560, 250, 375, 565, master=self.Background)
        self.Extra_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Label("Select The Number\n Of Booklet", 18, 50, master=self.Extra_Frame)
        self.Label("-", 37, 10, master=self.Slider_Frame).configure(font=("Arial", 80))
        self.Label("+", 487, 10, master=self.Slider_Frame).configure(font=("Arial", 80))
        Slider_Booklet = self.Slider(0, Available, Available, 500, 40, 30, 85, master=self.Slider_Frame)
        Slider_Booklet.bind("<ButtonRelease-1>", Update_Text)
        Slider_Booklet.set(0)
        Proceed = self.Button2("Proceed", 150, 155, self.Clean, master=self.Slider_Frame, state="disabled")
        Proceed.configure(anchor="center")

    def Clean(self):
        global Current
        if Current == "Booklet":
            self.Delete_Booklet_Frames()
        self.Transaction()

    def Transaction(self):
        global Total_Cost, Current, Service_Current
        self.RightMain.configure(fg_color="Black")

        self.Buy.configure(state="disabled")
        self.Print.configure(state="disabled")
        self.Main.configure(state="disabled")
        self.Setting.configure(state="disabled")
        self.Request.configure(state="disabled")
        self.RightMain3 = self.Frame(1160, 697, 350, 145, master=self.Background)
        self.RightMain3.configure(fg_color="black")
        self.Title3 = self.Frame(1180, 130, 340, 15, master=self.Background)
        self.Title3.configure(border_width=10, border_color=WidgetColor, corner_radius=20, fg_color="black")
        if Service_Current == "Print":
            self.Label(" P R I N T ", 460, 33, master=self.Title3).configure(font=("Arial", 60, "bold"), fg_color="black")
        elif Service_Current == "Booklet":
            self.Label(" B O O K L E T ", 380, 33, master=self.Title3).configure(font=("Arial", 60, "bold"),fg_color="black")

        Current = "Transaction"

        self.Amount_Frame = self.Frame(560, 130, 375, 170, master=self.Background)
        self.Amount_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Label(f"Amount: {Total_Cost} ₱", 85, 30,master=self.Amount_Frame)

        self.Coin_Frame = self.Frame(560, 130, 375, 290, master=self.Background)
        self.Coin_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Coin = self.Label("Coin:  0 ₱", 170, 30, master=self.Coin_Frame)

        self.Change_Frame = self.Frame(560, 130, 375, 410, master=self.Background)
        self.Change_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Change = self.Label("Change:  0 ₱", 85, 30, master=self.Change_Frame)

        self.Accepted_Frame = self.Frame(560, 130, 925, 170, master=self.Background)
        self.Accepted_Frame.configure(border_width=10, border_color=WidgetColor, fg_color="gray", corner_radius=20)
        self.Label("Accepted Coins", 63, 30, master=self.Accepted_Frame).configure(fg_color="gray")

        self.New_Frame = self.Frame(560, 130, 925, 290, master=self.Background)
        self.New_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Label("New:", 20, 30, master=self.New_Frame)
        self.Image("images/New_Piso.png", 100, 100, 150, 10, master=self.New_Frame)
        self.Image("images/New_Lima.png", 100, 100, 270, 10, master=self.New_Frame)
        self.Image("images/New_Sampu.png", 100, 100, 390, 10, master=self.New_Frame)

        self.Old_Frame = self.Frame(560, 130, 925, 410, master=self.Background)
        self.Old_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Label("Old:", 45, 30, master=self.Old_Frame)
        self.Image("images/Old_Piso.png", 100, 100, 150, 10, master=self.Old_Frame)
        self.Image("images/Old_Lima.png", 100, 100, 270, 10, master=self.Old_Frame)
        self.Image("images/Old_Sampu.png", 100, 100, 390, 10, master=self.Old_Frame)

        self.Back_Frame = self.Frame(560, 250, 375, 565, master=self.Background)
        self.Back_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Label("Insert Coins", 110, 50, master=self.Back_Frame)
        if Service_Current == "Booklet":
            self.Back_Buy = self.Button2("Change", 150, 155, command=self.Back_To_Booklet_UI, master=self.Back_Frame)
        elif Service_Current == "Print":
            self.Back_Buy = self.Button2("Change", 150, 155, command=self.Back_To_File_Choose_UI, master=self.Back_Frame)
        self.Back_Buy.configure(anchor="center")

        self.Extra2_Frame = self.Frame(560, 250, 925, 565, master=self.Background)
        self.Extra2_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        #self.Image("images/Skyblue_Coin_Acceptor.png", 250, 250, 45, 18, master=self.Transaction_Image_Frame)
        #self.UI.after(3000, self.Final)
        #self.UI.after(1000, self.Print_File)
        self.Serial_Thread = Thread(target=self.Coin_Sensor)
        self.Serial_Thread.start()


    def Back_To_Booklet_UI(self):
        self.RightMain.configure(fg_color="Dimgray")
        self.Delete_Transaction_frames()
        self.Buy2.destroy()
        self.Service_State()
        self.Main.configure(state="normal")
        self.Setting.configure(state="normal")
        self.Request.configure(state="normal")
        self.ser.close()
        self.Booklet_UI()

    def Back_To_File_Choose_UI(self):
        global Current
        Current = "File Choose"
        self.ser.close()
        self.Delete_Transaction_frames()

    def Delete_Booklet_Frames(self):
        self.Title.destroy()
        self.Available.destroy()
        self.Quantity.destroy()
        self.Cost.destroy()
        self.Slider_Frame.destroy()
        self.Extra_Frame.destroy()

    def Delete_Transaction_frames(self):
        self.RightMain3.destroy()
        self.Title3.destroy()
        self.Amount_Frame.destroy()
        self.Coin_Frame.destroy()
        self.Change_Frame.destroy()
        self.Accepted_Frame.destroy()
        self.New_Frame.destroy()
        self.Old_Frame.destroy()
        self.Back_Frame.destroy()
        self.Extra2_Frame.destroy()

    def Delete_Admin_Frames(self):
        self.Admin_Keypad_Frame.destroy()
        self.Admin_State_Frame.destroy()
        self.Admin_Timer_Frame.destroy()
        self.Admin_Code_Frame.destroy()
        self.Admin_Frame.destroy()
        self.Admin_Attempt1.destroy()
        self.Admin_Attempt2.destroy()
        self.Admin_Attempt3.destroy()
        self.Admin_Attempt1_border.destroy()
        self.Admin_Attempt2_border.destroy()
        self.Admin_Attempt3_border.destroy()

    def Delete_User_Frames(self):
        self.User_Keypad_Frame.destroy()
        self.User_State_Frame.destroy()
        self.User_Timer_Frame.destroy()
        self.User_Code_Frame.destroy()
        self.User_Frame.destroy()
        self.User_Attempt1.destroy()
        self.User_Attempt2.destroy()
        self.User_Attempt3.destroy()
        self.User_Attempt1_border.destroy()
        self.User_Attempt2_border.destroy()
        self.User_Attempt3_border.destroy()

    def Print_UI(self):
        global BackgroundColor, WidgetColor, Current, USB, Service_Current, USB_Image
        USB = 1
        self.Print.configure(fg_color=WidgetColor)
        self.Main.configure(fg_color=BackgroundColor)
        self.Buy.configure(fg_color=BackgroundColor)
        self.Setting.configure(fg_color=BackgroundColor)
        self.Request.configure(fg_color=BackgroundColor)
        self.RightMainM.destroy()
        self.Delete()
        if Current == "Main":
            self.Main2.destroy()
        elif Current == "Booklet":
            self.Delete_Booklet_Frames()
            self.Buy2.destroy()
        elif Current == "Transaction":
            self.Delete_Transaction_frames()
            self.Buy2.destroy()
            self.ser.close()
        elif Current == "Admin":
            self.Delete_Admin_Frames()
            self.Setting2.destroy()
        elif Current == "Help":
            self.Delete_User_Frames()
            self.Request2.destroy()
        self.RightMain.configure(fg_color=BackgroundColor)
        self.Print2 = self.Button("Print", 25, 460, "images/Printer.png", command=None, master=self.LeftMain)
        self.RightMain.configure(fg_color="black")
        self.Title = self.Frame(1180, 130, 340, 15, master=self.Background)
        self.Title.configure(border_width=10, border_color=WidgetColor, corner_radius=20, fg_color="black")
        self.Label(" P R I N T ", 460, 33, master=self.Title).configure(font=("Arial", 60, "bold"), fg_color="black")
        Current = "Print"
        Service_Current = "Print"
        self.Insert_USB_Frame = self.Frame(1110, 165, 375, 170, master=self.Background)
        self.Insert_USB_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Label("Please Insert Your Flash Drive", 145, 45, master=self.Insert_USB_Frame)

        self.File_Types_Title = self.Frame(600, 115, 375, 360, master=self.Background)
        self.File_Types_Title.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Label("Auto Conversion", 75, 25, master=self.File_Types_Title)

        self.File_Types = self.Frame(600, 350, 375, 465, master=self.Background)
        self.File_Types.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Image("images/File_Types.png", 500, 300, 30, 25, master=self.File_Types)

        self.USB_Name_Title = self.Frame(490, 115, 995, 360, master=self.Background)
        self.USB_Name_Title.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.USB_Name = self.Label("Name: ", 25, 25, master=self.USB_Name_Title)

        self.USB_Frame = self.Frame(490, 350, 995, 465, master=self.Background)
        self.USB_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Image(USB_Image, 300, 291, 75, 25, master=self.USB_Frame)
        self.USB()

    def USB(self):
        def DetectUSB():
            usb_devices = []
            for partition in psutil.disk_partitions():
                if 'removable' in partition.opts or 'usb' in partition.opts:
                    usb_devices.append(partition.device)
            return usb_devices

        usb_devices = DetectUSB()
        if usb_devices:
            self.USB_Name.configure(text=f"Name: {usb_devices}")
            print(usb_devices)
            self.UI.after(5000, self.Check1_USB)
        else:
            self.UI.after(5000, self.Check2_USB)
        self.Service_State()

    def Check1_USB(self):
        global USB
        if USB == 1:
            self.File_Choose()

    def Check2_USB(self):
        global USB
        if USB == 1:
            self.USB()

    def File_Choose(self):
        global Available_Papers, Current
        self.Delete_Print_Frames()
        Current = "File Choose"
        self.Paper_Frame = self.Frame(1110, 130, 375, 170, master=self.Background)
        self.Paper_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Available_Paper = self.Label(f"Available: {Available_Papers} pgs.", 25, 35, master=self.Paper_Frame)
        self.Files_Paper_Frame = self.Frame(550, 115, 375, 325, master=self.Background)
        self.Files_Paper_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Quantity_Paper = self.Label("Quantity:  0 pgs.", 45, 20, master=self.Files_Paper_Frame)
        self.Total_Paper_Frame = self.Frame(550, 110, 375, 430, master=self.Background)
        self.Total_Paper_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Total_Paper = self.Label("Total:  0 ₱", 135, 25, master=self.Total_Paper_Frame)

        Paper_Stock = customtkinter.CTkProgressBar(master=self.Paper_Frame, width=450, height=40, progress_color="green",
                                                   border_color=WidgetColor, border_width=5)
        Paper_Stock.set(Available_Papers / Max_Paper)
        Paper_Stock.place(x=590, y=45)
        if Available_Papers <= 15:
            Paper_Stock.configure(progress_color="red")
        elif Available_Papers <= 30:
            Paper_Stock.configure(progress_color="yellow")

        self.Print_Buttons = self.Frame(550, 285, 375, 530, master=self.Background)
        self.Print_Buttons.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Add_Button = self.Button2("Add", 26, 45, self.Add_File, master=self.Print_Buttons)
        self.Add_Button.configure(anchor="c", width=240)
        self.Delete_Button = self.Button2("Delete", 282, 45, self.Delete_File, master=self.Print_Buttons, state="disabled")
        self.Delete_Button.configure(anchor="c", width=240)
        self.View_Button = self.Button2("View", 26, 120, self.View_File, master=self.Print_Buttons, state="disabled")
        self.View_Button.configure(anchor="c", width=160)
        self.Clear_Button = self.Button2("Clear", 362, 120, self.Clear_File, master=self.Print_Buttons, state="disabled")
        self.Clear_Button.configure(anchor="c", width=160)
        self.Update_Button = self.Button2("Update", 26, 195, self.Update_File, master=self.Print_Buttons, state="disabled")
        self.Update_Button.configure(anchor="c", width=240)
        self.Print_Button = self.Button2("Proceed", 282, 195, self.Transaction, master=self.Print_Buttons, state="disabled")
        self.Print_Button.configure(anchor="c", width=240)

        def Update_Requirement(event=None):
            if self.Copy_Box.get() != "Copy":
                self.Update_Button.configure(state="normal")

        self.Copy_Box = self.Combobox(list(map(str, range(1, 11))), 205, 120, master=self.Print_Buttons, command=Update_Requirement)
        self.Copy_Box.set(value="Copy")
        self.Copy_Box.configure(state="disabled")


        def Table_File(cell):
            global Select, Number_Of_Paper, Available_Papers, Previous_Row, Print_ID, Current_Row
            if cell["row"] != 0 and Select != 1:
                Current_Row = cell["row"]
                Current_Column = cell["column"]
                self.Table.select_row(Current_Row)
                Previous_Row = Current_Row
                if Previous_Row <= Print_ID:
                    self.Delete_Button.configure(state="normal")
                    self.View_Button.configure(state="normal")
                    self.Copy_Box.configure(state="readonly")
                Select = 1
            elif Select == 1:
                self.Table.deselect_row(Previous_Row)
                self.Delete_Button.configure(state="disabled")
                self.View_Button.configure(state="disabled")
                self.Copy_Box.set(value="Copy")
                self.Copy_Box.configure(state="disabled")
                Select = 0
            if Number_Of_Paper <= Available_Papers and Number_Of_Paper != 0:
                self.Print_Button.configure(state="normal")


        self.Table_Frame = customtkinter.CTkScrollableFrame(master=self.Background, fg_color=BackgroundColor,
                                                            border_color=WidgetColor, border_width=10, width=524,
                                                            height=429.5, orientation="vertical",
                                                            scrollbar_button_color=WidgetColor, corner_radius=20,
                                                            scrollbar_button_hover_color="white")
        self.Table_Frame.place(x=915, y=325)

        Table_Title = [["ID", "File Name", "Copy", "Pages", "Total"]]
        self.Table = CTkTable(master=self.Table_Frame, row=14, column=5, font=("Arial", 15), values=Table_Title,
                              colors=["gray", "gray"], border_color=WidgetColor, border_width=7, text_color="black",
                              header_color="light gray", hover_color="White", command=Table_File)

        self.Table.pack(expand=True, fill="both", padx=15, pady=5)

    def Delete_File_Choose_frames(self):
        self.Paper_Frame.destroy()
        self.Files_Paper_Frame.destroy()
        self.Total_Paper_Frame.destroy()
        self.Print_Buttons.destroy()
        self.Table.pack_forget()
        self.Table_Frame.place_forget()
    def CountTotalPages(self, PDF_File):
        with open(PDF_File, 'rb') as PDF_File:
            PDF_Reader = PyPDF2.PdfReader(PDF_File)
            return len(PDF_Reader.pages)

    def Add_File(self):
        global Print_ID, Paper_Cost, Total_Paper_Cost, Number_Of_Paper, Previous_Row, Select

        file_types = [('PDF Files', '*.pdf'),
                      ('Word Files', '*.docx'),
                      ('Excel Files', '*.xlsx'),
                      ('PowerPoint Files', '*.pptx')]
        File = askopenfilename(filetypes=file_types)
        if File:
            Timestamp = int(time.time())
            Unique_File = f"file_{Timestamp}"
            self.Unique_File_Names.append(Unique_File)

            output_path = os.path.join('print_path', Unique_File)
            pdf_path = self.Convert_To_Pdf(File, output_path)

            if Select == 1:
                self.Table.deselect_row(Previous_Row)
                Select = 0

            Print_ID += 1
            FileName = os.path.basename(File)[:8]
            TotalPages = self.CountTotalPages(pdf_path)
            FileTotal = TotalPages * Paper_Cost
            if TotalPages > Available_Papers:
                self.Print_Button.configure(state="disabled")
            else:
                self.Print_Button.configure(state="normal")
            self.Table.add_row(values=[Print_ID, FileName, "1", TotalPages, FileTotal], index=Print_ID)
            self.Update_Print_Frame_Value()
            self.Clear_Button.configure(state="normal")

        if Print_ID >= 1:
            self.Main.configure(state="disabled")
            self.Buy.configure(state="disabled")
            self.Setting.configure(state="disabled")
            self.Request.configure(state="disabled")

    def Delete_File(self):
        global Current_Row, Print_ID, Select
        self.Table.delete_row(Current_Row)
        File_ID = Current_Row - 1
        if File_ID < len(self.Unique_File_Names):
            File_Delete = os.path.join('print_path', self.Unique_File_Names[File_ID])
            File_Delete += '.pdf'
            if os.path.exists(File_Delete):
                os.remove(File_Delete)
        del self.Unique_File_Names[File_ID]
        Print_ID -= 1
        Select = 0
        for i in range(1, Print_ID+1):
            self.Table.insert(i, 0, i)
        self.Update_Print_Frame_Value()
        self.Delete_Button.configure(state="disabled")
        self.View_Button.configure(state="disabled")
        self.Copy_Box.set(value="Copy")
        self.Copy_Box.configure(state="disabled")
        if Print_ID == 0:
            self.Print_Button.configure(state="disabled")
            self.Clear_Button.configure(state="disabled")
            self.Main.configure(state="normal")
            self.Buy.configure(state="normal")
            self.Setting.configure(state="normal")
            self.Request.configure(state="normal")
            self.Service_State()

    def Clear_File(self):
        global Select, Print_ID, Number_Of_Paper, Total_Paper_Cost
        self.Table.delete_rows(list(range(1, Print_ID+1)))

        self.Clear_Button.configure(state="disabled")
        self.Print_Button.configure(state="disabled")
        self.Delete_Button.configure(state="disabled")
        self.View_Button.configure(state="disabled")
        self.Update_Button.configure(state="disabled")
        self.Copy_Box.set(value="Copy")
        self.Copy_Box.configure(state="disabled")
        self.Main.configure(state="normal")
        self.Buy.configure(state="normal")
        self.Setting.configure(state="normal")
        self.Request.configure(state="normal")
        self.Service_State()

        for filename in self.Unique_File_Names:
            File_Delete = os.path.join('print_path', filename)
            File_Delete += '.pdf'
            if os.path.exists(File_Delete):
                os.remove(File_Delete)
        if Select == 1:
            self.Table.deselect_row(Previous_Row)
            Select = 0

        Print_ID = 0
        Number_Of_Paper = 0
        Total_Paper_Cost = 0
        self.Update_Print_Frame_Value()
        self.Unique_File_Names.clear()

    def Update_File(self):
        global Select, Print_ID, Current_Row, Previous_Row, Paper_Cost
        Copy = self.Copy_Box.get()
        self.Table.insert(Current_Row, 2, Copy)
        Select = 0
        self.Table.insert(Current_Row, 4, int(Copy) * int(self.Table.get(Current_Row, 3)) * Paper_Cost)
        self.Table.deselect_row(Previous_Row)
        self.Delete_Button.configure(state="disabled")
        self.View_Button.configure(state="disabled")
        self.Copy_Box.set(value="Copy")
        self.Copy_Box.configure(state="disabled")
        self.Update_Button.configure(state="disabled")
        self.Update_Print_Frame_Value()

    def View_File(self):
        global Current_Row, Print_ID, Preview_ID
        self.RightMain2 = self.Frame(1160, 697, 350, 145, master=self.Background)
        self.RightMain2.configure(fg_color="black")
        self.Title2 = self.Frame(1180, 130, 340, 15, master=self.Background)
        self.Title2.configure(border_width=10, border_color=WidgetColor, corner_radius=20, fg_color="black")
        File_Title = self.Table.get(Current_Row, 1)
        File_Copy = self.Table.get(Current_Row, 2)
        self.Label("P D F  R E V I E W", 330, 33, master=self.Title2).configure(font=("Arial", 60, "bold"),fg_color="black")
        self.Title_Frame = self.Frame(435, 130, 375, 170, master=self.Background)
        self.Title_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.PDF_Title = self.Label(f"{File_Title}", 35, 33, master=self.Title_Frame)
        self.Copy_Frame = self.Frame(435, 130, 375, 325, master=self.Background)
        self.Copy_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.PDF_Copy = self.Label(f"{File_Copy} Copy", 35, 33, master=self.Copy_Frame)
        if int(File_Copy) > 1:
            self.PDF_Copy.configure(text=f"{File_Copy} Copies")

        def Next_Preview():
            global Print_ID, Preview_ID, Current_Row
            if Current_Row + Preview_ID <= Print_ID:
                if Current_Row + Preview_ID == Print_ID-1:
                    self.Next_Button.configure(state="disabled")
                Preview_ID += 1
                self.Previous_Button.configure(state="normal")
                File_Title = self.Table.get(Current_Row + Preview_ID, 1)
                File_Copy = self.Table.get(Current_Row + Preview_ID, 2)
                self.PDF_Title.configure(text=f"{File_Title}")
                if int(File_Copy) > 1:
                    self.PDF_Copy.configure(text=f"{File_Copy} Copies")
                else:
                    self.PDF_Copy.configure(text=f"{File_Copy} Copy")
                self.scrollbar_y.destroy()
                Preview_File()

        def Previous_Preview():
            global Preview_ID, Current_Row, Print_ID
            if Current_Row + Preview_ID >= 1:
                if Current_Row + Preview_ID == 2:
                    self.Previous_Button.configure(state="disabled")
                Preview_ID -= 1
                self.Next_Button.configure(state="normal")
                File_Title = self.Table.get(Current_Row + Preview_ID, 1)
                File_Copy = self.Table.get(Current_Row + Preview_ID, 2)
                self.PDF_Title.configure(text=f"{File_Title}")
                if int(File_Copy) > 1:
                    self.PDF_Copy.configure(text=f"{File_Copy} Copies")
                else:
                    self.PDF_Copy.configure(text=f"{File_Copy} Copy")
                self.scrollbar_y.destroy()
                Preview_File()

        self.Review_Buttons = self.Frame(435, 336, 375, 480, master=self.Background)
        self.Review_Buttons.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Previous_Button = self.Button2("Prev", 90, 45, Previous_Preview, master=self.Review_Buttons)
        self.Previous_Button.configure(anchor="c", width=240)
        self.Next_Button = self.Button2("Next", 90, 140, Next_Preview, master=self.Review_Buttons)
        self.Next_Button.configure(anchor="c", width=240)
        if Current_Row + Preview_ID == Print_ID:
            self.Next_Button.configure(state="disabled")
            if Print_ID == 1:
                self.Previous_Button.configure(state="disabled")
        elif Current_Row + Preview_ID == 1:
            self.Previous_Button.configure(state="disabled")

        def Return_To_File_Choose_UI():
            global Preview_ID
            self.RightMain2.destroy()
            self.Title2.destroy()
            self.Title_Frame.destroy()
            self.Copy_Frame.destroy()
            self.Review_Buttons.destroy()
            self.View_Frame.destroy()
            self.scrollbar_y.destroy()
            Preview_ID = 0

        self.Return_Button = self.Button2("Return", 90, 240, Return_To_File_Choose_UI, master=self.Review_Buttons)
        self.Return_Button.configure(anchor="c", width=240)
        self.View_Frame = self.Frame(650, 645, 835, 170, master=self.Background)
        self.View_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)

        def Preview_File():
            global Current_Row, Preview_ID
            Item_ID = self.Table.get(Current_Row + Preview_ID, 0)
            File_Name = Item_ID - 1
            PDF_Path = os.path.join('print_path', self.Unique_File_Names[File_Name])
            PDF_Path += '.pdf'
            PDF_Document = fitz.open(PDF_Path)
            canvas = tk.Canvas(self.View_Frame, width=735, height=730)
            canvas.place(x=35, y=35)
            thumbnails_frame = Frame(canvas)
            canvas.create_window((50, 0), window=thumbnails_frame, anchor="nw")
            for page_num in range(len(PDF_Document)):
                page = PDF_Document.load_page(page_num)
                image = page.get_pixmap()
                img = Image.frombytes("RGB", (image.width, image.height), image.samples)
                img_tk = ImageTk.PhotoImage(img)
                label = Label(thumbnails_frame, image=img_tk)
                label.image = img_tk
                label.grid(row=page_num, column=0, padx=10, pady=10)
            PDF_Document.close()
            thumbnails_frame.update_idletasks()
            self.scrollbar_y = tk.Scrollbar(self.UI, command=canvas.yview)
            self.scrollbar_y.place(x=1797, y=270, height=700)
            canvas.configure(yscrollcommand=self.scrollbar_y.set)
            canvas.configure(scrollregion=canvas.bbox("all"))
        Preview_File()

    def Print_File(self):
        global Print_ID
        SumatraPath = r"C:\Users\CodeMunVen\AppData\Local\SumatraPDF\SumatraPDF.exe"
        CurrentPrinter = win32print.GetDefaultPrinter()
        Path = 'print_path'
        Copy_Matrix = []
        id = 0
        for i in range(1, Print_ID+1):
            Copy = int(self.Table.get(i, 2))
            Copy_Matrix.append(Copy)
        for filename in os.listdir(Path):
            if filename.endswith('.pdf'):
                file_path = os.path.join(Path, filename)
                Copy_Value = Copy_Matrix[id]
                num = 1
                while num <= Copy_Value:
                    subprocess.Popen([SumatraPath, '-print-to', CurrentPrinter, file_path], shell=True).wait()
                    num += 1
                id += 1

        for filename in self.Unique_File_Names:
            File_Delete = os.path.join('print_path', filename)
            File_Delete += '.pdf'
            if os.path.exists(File_Delete):
                os.remove(File_Delete)

        self.Final()

    def Update_Print_Frame_Value(self):
        global Print_ID, Number_Of_Paper, Total_Paper_Cost, Paper_Cost, Current_Row, Total_Cost
        Total_Pages = 0
        Total_Paper_Cost = 0
        for i in range(1, Print_ID+1):
            Copy = self.Table.get(i, 2)
            Page = self.Table.get(i, 3)
            Cost = self.Table.get(i, 4)
            Total_Pages += int(Page) * int(Copy)
            Number_Of_Paper = Total_Pages
            Total_Paper_Cost += Cost
            Total_Cost = Total_Paper_Cost

        self.Quantity_Paper.configure(text=f"Quantity: {Total_Pages} pgs.")
        self.Total_Paper.configure(text=f"Total: {Total_Paper_Cost} ₱")


    def Convert_To_Pdf(self, file_path, output_path):
        file_name, file_extension = os.path.splitext(file_path)
        file_extension = file_extension.lower()
        output_path += '.pdf'
        convertapi.api_secret = 'L8k2k8J6L0x2aLMg'

        if file_extension == '.pdf':
            shutil.copyfile(file_path, output_path)

        elif file_extension == '.docx':
            convertapi.convert('pdf', {'File': file_path}, from_format='docx').save_files(output_path)

        elif file_extension == '.xlsx':
            convertapi.convert('pdf', {'File': file_path}, from_format='xlsx').save_files(output_path)

        elif file_extension == '.pptx':
            convertapi.convert('pdf', {'File': file_path}, from_format='pptx').save_files(output_path)

        return output_path

    def Delete_Print_Frames(self):
        self.Insert_USB_Frame.destroy()
        self.File_Types_Title.destroy()
        self.File_Types.destroy()
        self.USB_Name_Title.destroy()
        self.USB_Frame.destroy()
        self.Delete()

    def Coin_Sensor(self):
        global Service_Current, Total_Cost, One, Five, Ten, Inserted
        global Available_Coins, Number_Of_Booklet, Max_Booklet, Available_Booklets
        self.ser = serial.Serial('COM3', 9600, timeout=1)
        time.sleep(2)
        Past_Totat = 0
        data_to_send = f"{Total_Cost},{Number_Of_Booklet}\n"
        print(Service_Current)
        self.ser.write(data_to_send.encode())
        while True:
            if self.ser.in_waiting > 0:
                data = self.ser.readline()
                try:
                    Total = int(data.decode().strip())
                    self.Coin.configure(text=f"Coin: {Total} ₱")
                    if Total - 1 == Past_Totat:
                        One += 1
                    elif Total - 5 == Past_Totat:
                        Five += 1
                    elif Total - 10 == Past_Totat:
                        Ten += 1
                    Past_Totat = Total
                    if Total > 0:
                        self.Back_Buy.configure(state="disabled")
                        self.Main.configure(state="disabled")
                        self.Buy.configure(state="disabled")
                        self.Print.configure(state="disabled")
                        self.Setting.configure(state="disabled")
                        self.Request.configure(state="disabled")
                        if Total >= Total_Cost:
                            self.Change.configure(text=f"Change: {Total - Total_Cost}₱")
                            Inserted = Total
                            if Service_Current == "Booklet":
                                booklet = f"{-1},{Available_Booklets}\n"
                                self.ser.write(booklet.encode())
                                self.UI.after(3000, self.Final)
                            else:
                                self.ser.close()
                                self.UI.after(3000, self.Print_File)


                except UnicodeDecodeError:
                    print("Error decoding data from Arduino.")
                except ValueError:
                    print("Error converting data to integer from Arduino.")

    def Final(self):
        global Service_Current, One, Five, Ten, Number_Of_Booklet, Booklet_Cost, Total_Cost, Inserted, ID, \
               Available_Booklets, Select, Available_Papers, Number_Of_Paper, Paper_Cost, Print_ID, Preview_ID, \
               Available_Coins, Vend_Money, Max_Coin, Max_Paper, Max_Booklet

        self.RightMain.configure(fg_color="Black")
        self.Main.configure(state="disabled")
        self.Buy.configure(state="disabled")
        self.Print.configure(state="disabled")
        self.Setting.configure(state="disabled")
        self.Request.configure(state="disabled")
        self.Delete_Transaction_frames()
        self.RightMain4 = self.Frame(1160, 817, 350, 25, master=self.Background)
        self.RightMain4.configure(fg_color="black")
        self.Title4 = self.Frame(1180, 130, 340, 15, master=self.Background)
        self.Title4.configure(border_width=10, border_color=WidgetColor, corner_radius=20, fg_color="black")
        self.Label("T H A N K  Y O U", 340, 33, master=self.Title4).configure(font=("Arial", 60, "bold"), fg_color="black")
        if Service_Current == "Print":
            Service_ID = 9
        else:
            Service_ID = 7
        self.Upper_Final_Frame = self.Frame(1110, 165, 375, 170, master=self.Background)
        self.Upper_Final_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Lower_Final_Frame = self.Frame(450, 110, 375, 360, master=self.Background)
        self.Lower_Final_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Lower2_Final_Frame = self.Frame(450, 355, 375, 460, master=self.Background)
        self.Lower2_Final_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Lower3_Final_Frame = self.Frame(670, 110, 815, 360, master=self.Background)
        self.Lower3_Final_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Lower4_Final_Frame = self.Frame(670, 355, 815, 460, master=self.Background)
        self.Lower4_Final_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Label("Details", 250, 25, master=self.Lower3_Final_Frame)
        Current_ID = datetime.now().strftime("%d%y%H")
        self.Label(f"ID : {Current_ID}{ID}{Service_ID}", 297, 20, master=self.Lower4_Final_Frame).configure(font=("Arial", 30))
        self.Label(f"Total : {Total_Cost} ₱", 258, 160, master=self.Lower4_Final_Frame).configure(font=("Arial", 30))
        self.Label(f"Coin : {Inserted} ₱", 264, 195, master=self.Lower4_Final_Frame).configure(font=("Arial", 30))
        Available_Coins -= (Inserted-Total_Cost)
        self.Label(f"Change : {Inserted-Total_Cost} ₱", 222, 230, master=self.Lower4_Final_Frame).configure(font=("Arial", 30))
        Current_Date = datetime.now().strftime("%Y-%m-%d")
        Current_Time = datetime.now().strftime("%I:%M:%S %p")
        self.Label(f"Date : {Current_Date}", 264, 265, master=self.Lower4_Final_Frame).configure(font=("Arial", 30))
        self.Label(f"Time : {Current_Time}", 259, 300, master=self.Lower4_Final_Frame).configure(font=("Arial", 30))

        if Service_Current == "Booklet":
            self.Label("Kindly Await Booklet Dispensing", 145, 45, master=self.Upper_Final_Frame)
            self.Label(f"Output : Booklet", 234, 55, master=self.Lower4_Final_Frame).configure(font=("Arial", 30))
            self.Label(f"Quantity : {Number_Of_Booklet}", 212, 90, master=self.Lower4_Final_Frame).configure(font=("Arial", 30))
            self.Label(f"Cost : {Booklet_Cost} ₱", 264, 125, master=self.Lower4_Final_Frame).configure(font=("Arial", 30))
            Available_Booklets -= Number_Of_Booklet

        elif Service_Current == "Print":
            self.Label("Kindly Await Printing Process", 145, 45, master=self.Upper_Final_Frame)
            self.Label(f"Output : Printed", 234, 55, master=self.Lower4_Final_Frame).configure(font=("Arial", 30))
            self.Label(f"Quantity : {Number_Of_Paper}", 212, 90, master=self.Lower4_Final_Frame).configure(font=("Arial", 30))
            self.Label(f"Cost : {Paper_Cost} ₱", 264, 125, master=self.Lower4_Final_Frame).configure(font=("Arial", 30))
            Available_Papers -= Number_Of_Paper
        if Service_Current == "Print":
            Service_ID = 9
        else:
            Service_ID = 7
            #self.ser.close()
            print("Ava:")
            print(Available_Booklets)
        self.Label("Inserted", 110, 25, master=self.Lower_Final_Frame)
        self.Label(f"Ⓘ x {One} = {One * 1} ₱", 60, 45, master=self.Lower2_Final_Frame)
        self.Label(f"Ⓥ x {Five} = {Five * 5} ₱", 60, 145, master=self.Lower2_Final_Frame)
        self.Label(f"Ⓧ x {Ten} = {Ten * 10} ₱", 60, 245, master=self.Lower2_Final_Frame)
        self.Vend_Database.append([ID])
        self.Vend_Database.append([f"{Current_ID}{ID}{Service_ID}"])
        self.Vend_Database.append([Current_Date])
        self.Vend_Database.append([datetime.now().strftime("%I:%M:%S")])
        self.Vend_Database.append([Service_Current])
        if Service_Current == "Booklet":
            self.Vend_Database.append([Number_Of_Booklet])
            self.Vend_Database.append([Booklet_Cost])
            MongoDB_UserData = {"User_ID": f"{Current_ID}{ID}{Service_ID}",
                            "Date": Current_Date,
                            "Time": Current_Time,
                            "Service": Service_Current,
                            "Quantity": Number_Of_Booklet,
                            "Cost": Booklet_Cost,
                            "Total": Total_Cost,
                            "Coins": Inserted,
                            "Change": Inserted - Total_Cost}
        else:
            self.Vend_Database.append([Number_Of_Paper])
            self.Vend_Database.append([Paper_Cost])
            MongoDB_UserData = {"User_ID": f"{Current_ID}{ID}{Service_ID}",
                            "Date": Current_Date,
                            "Time": Current_Time,
                            "Service": Service_Current,
                            "Quantity": Number_Of_Paper,
                            "Cost": Paper_Cost,
                            "Total": Total_Cost,
                            "Coins": Inserted,
                            "Change": Inserted - Total_Cost}
        self.Vend_Database.append([Total_Cost])
        self.Vend_Database.append([Inserted])
        self.Vend_Database.append([Inserted-Total_Cost])
        self.User_ID.append(([f"{Current_ID}{ID}{Service_ID}"]))
        self.Collection_UserData.insert_one(MongoDB_UserData)
        self.Collection_VendStock.delete_many({})
        Vend_Money += Total_Cost
        MongoDB_VendStock = {"User_ID": f"ADMIN01",
                             "Booklet": f"{Available_Booklets} / {Max_Booklet}",
                             "Paper": f"{Available_Papers} / {Max_Paper}",
                             "Change": f"{Available_Coins} / {Max_Coin}",
                             "Inserted": f"{One+Five+Ten} / {Max_Coin_Storage}",
                             "Piso": f"{One} = {One*1} ₱",
                             "Five": f"{Five} = {Five*5} ₱",
                             "Ten": f"{Ten} = {Ten*10} ₱",
                             "Total": Vend_Money}
        self.Collection_VendStock.insert_one(MongoDB_VendStock)
        ID += 1
        Select = 0
        Print_ID = 0
        Preview_ID = 0
        self.Unique_File_Names.clear()
        self.Stock_Notification_Alert()
        if Service_Current == "Booklet":
            self.UI.after((2000*Number_Of_Booklet) + 5000, self.Back_To_Main)
        else:
            self.UI.after((3000*Number_Of_Paper) + 7000, self.Back_To_Main)

    def Stock_Notification_Alert(self):
        global Available_Coins, Available_Papers, Available_Booklets, Max_Coin, Max_Paper, Max_Booklet, \
               Coins_Check, Papers_Check, Booklets_Check
        Sinch_URL = "https://sms.api.sinch.com/xms/v1/444efabf10fb44078cbc91df1c62d7d3/batches"
        Sinch_Headers = {
            "Authorization": "Bearer 50412fddccab40afac91410667d24c21",
            "Content-Type": "application/json",
        }

        def Notification_Data():
            Sinch_Data = {
                "from": "447520651788",
                "to": ["639397178930"],
                "body": f"REMINDER!!!"
                        f"\nCurrent Vending Machine Stocks: "
                        f"\nPapers = {Available_Papers} / {Max_Paper} "
                        f"\nBooklets = {Available_Booklets} / {Max_Booklet}"
                        f"\nChange = {Available_Coins} / {Max_Coin}",
            }
            # requests.post(url, headers=Sinch_Headers, json=Sinch_Data)
            self.Twilio_Client.messages.create(
                from_='whatsapp:+14155238886',
                body=f"REMINDER!!!"
                     f"\nCurrent Vending Machine Stocks: "
                     f"\nPapers = {Available_Papers} / {Max_Paper} "
                     f"\nBooklets = {Available_Booklets} / {Max_Booklet}"
                     f"\nChange = {Available_Coins} / {Max_Coin}",
                to='whatsapp:+639397178930'
            )
        if ((Available_Coins <= 10 and Coins_Check == 2) or
            (Available_Papers <= 15 and Papers_Check == 2) or
            (Available_Booklets <= 5 and Booklets_Check == 2)):
            Notification_Data()
            if Available_Coins <= 10 and Coins_Check == 2:
                Coins_Check = 1
            if Available_Papers <= 15 and Papers_Check == 2:
                Papers_Check = 1
            if Available_Booklets <= 5 and Booklets_Check == 2:
                Booklets_Check = 1

        elif ((Available_Coins <= 20 and Coins_Check == 3) or
             (Available_Papers <= 30 and Papers_Check == 3) or
             (Available_Booklets <= 10 and Booklets_Check == 3)):
            Notification_Data()
            if Available_Coins <= 20 and Coins_Check == 3:
                Coins_Check = 2
            if Available_Papers <= 30 and Papers_Check == 3:
                Papers_Check = 2
            if Available_Booklets <= 10 and Booklets_Check == 3:
                Booklets_Check = 2

        if Available_Coins == 0 and Coins_Check == 1:
            Sinch_Data = {
                "from": "447520651788",
                "to": ["639397178930"],
                "body": f"REMINDER!!!"
                        f"\nNo More Coins!!!  "
                        f"\nChange = {Available_Coins} / {Max_Coin}"
                        f"\nPlease Restock ASAP!!!",
            }
            # requests.post(url, headers=Sinch_Headers, json=Sinch_Data)
            self.Twilio_Client.messages.create(
                from_='whatsapp:+14155238886',
                body=f"REMINDER!!!"
                     f"\nNo More Coins!!!  "
                        f"\nChange = {Available_Coins} / {Max_Coin}"
                        f"\nPlease Restock ASAP!!!",
                to='whatsapp:+639397178930'
            )
            Coins_Check = 0
        if Available_Papers == 0 and Papers_Check == 1:
            Sinch_Data = {
                "from": "447520651788",
                "to": ["639397178930"],
                "body": f"REMINDER!!!"
                        f"\nNo More Papers!!!  "
                        f"\nPaper = {Available_Papers} / {Max_Paper}"
                        f"\nPlease Restock ASAP!!!",
            }
            # requests.post(url, headers=Sinch_Headers, json=Sinch_Data)
            self.Twilio_Client.messages.create(
                from_='whatsapp:+14155238886',
                body=f"REMINDER!!!"
                     f"\nNo More Papers!!!  "
                     f"\nPaper = {Available_Papers} / {Max_Paper}"
                     f"\nPlease Restock ASAP!!!",
                to='whatsapp:+639397178930'
            )
            Papers_Check = 0
        if Available_Booklets == 0 and Booklets_Check == 1:
            Sinch_Data = {
                "from": "447520651788",
                "to": ["639397178930"],
                "body": f"REMINDER!!!"
                        f"\nNo More Booklets!!!  "
                        f"\nBooklet = {Available_Booklets} / {Max_Booklet}"
                        f"\nPlease Restock ASAP!!!",
            }
            # requests.post(url, headers=Sinch_Headers, json=Sinch_Data)
            self.Twilio_Client.messages.create(
                from_='whatsapp:+14155238886',
                body=f"REMINDER!!!"
                     f"\nNo More Booklets!!!  "
                     f"\nBooklet = {Available_Booklets} / {Max_Booklet}"
                     f"\nPlease Restock ASAP!!!",
                to='whatsapp:+639397178930'
            )
            Booklets_Check = 0


    def Back_To_Main(self):
        global One, Five, Ten
        One = 0
        Five = 0
        Ten = 0
        self.Main.configure(state="normal")
        self.Setting.configure(state="normal")
        self.Service_State()
        self.Start_UI()



    def Admin_UI(self):
        global BackgroundColor, WidgetColor, Current, Admin_Attempt, Entered_Passcode, USB, Service_Current
        USB = 0
        Entered_Passcode = ""
        self.RightMainM.destroy()
        if Current == "Main":
            self.Main2.destroy()
        elif Current == "Booklet":
            self.Delete_Booklet_Frames()
            self.Buy2.destroy()
        elif Current == "Transaction":
            self.Delete_Transaction_frames()
            if Service_Current == "Booklet":
                self.Buy2.destroy()
            else:
                self.Print2.destroy()
        elif Current == "Print":
            self.Delete_Print_Frames()
            self.Print2.destroy()
        elif Current == "File Choose":
            self.Delete_File_Choose_frames()
            self.Print2.destroy()
        elif Current == "Help":
            self.Delete_User_Frames()
            self.Request2.destroy()
        self.Delete()
        self.RightMain.configure(fg_color="black")
        self.Buy.configure(fg_color=BackgroundColor)
        self.Main.configure(fg_color=BackgroundColor)
        self.Print.configure(fg_color=BackgroundColor)
        self.Setting.configure(fg_color=WidgetColor)
        self.Request.configure(fg_color=BackgroundColor)
        Current = "Admin"
        self.Setting2 = self.Button("Setting", 25, 540, "images/Setting.png", command=None, master=self.LeftMain)
        self.Title = self.Frame(1180, 130, 340, 15, master=self.Background)
        self.Title.configure(border_width=10, border_color=WidgetColor, corner_radius=20, fg_color="black")
        self.Label(" A D M I N ", 440, 33, master=self.Title).configure(font=("Arial", 60, "bold"), fg_color="black")
        self.Admin_State_Frame = self.Frame(1110, 130, 375, 170, master=self.Background)
        self.Admin_State_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        if Admin_Attempt != 3:
            self.Login_State = self.Label("ACTIVE", 440, 30, master=self.Admin_State_Frame)
            self.Login_State.configure(font=("Arial", 60, "bold"))
        else:
            self.Login_State = self.Label("LOCKED", 430, 30, master=self.Admin_State_Frame)
            self.Login_State.configure(font=("Arial", 60, "bold"))
        self.Admin_Attempt1_border = self.Frame(190, 150, 375, 325, master=self.Background)
        self.Admin_Attempt1_border.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Admin_Attempt1 = self.Frame(170, 130, 385, 334, master=self.Background)
        self.Admin_Attempt1.configure(border_width=15, border_color="gray", corner_radius=20)
        self.Admin_Attempt2_border = self.Frame(190, 150, 555, 325, master=self.Background)
        self.Admin_Attempt2_border.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Admin_Attempt2 = self.Frame(170, 130, 565, 334, master=self.Background)
        self.Admin_Attempt2.configure(border_width=15, border_color="gray", corner_radius=20)
        self.Admin_Attempt3_border = self.Frame(190, 150, 735, 325, master=self.Background)
        self.Admin_Attempt3_border.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Admin_Attempt3 = self.Frame(170, 130, 745, 334, master=self.Background)
        self.Admin_Attempt3.configure(border_width=15, border_color="gray", corner_radius=20)
        if Admin_Attempt >= 1:
            self.Admin_Attempt1.configure(fg_color="red")
            if Admin_Attempt >= 2:
                self.Admin_Attempt2.configure(fg_color="red")
                if Admin_Attempt == 3:
                    self.Admin_Attempt3.configure(fg_color="red")
        self.Admin_Code_Frame = self.Frame(550, 200, 375, 465, master=self.Background)
        self.Admin_Code_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Passcode = self.Button2(" ", 55, 52, command=None, master=self.Admin_Code_Frame, state="normal")
        self.Passcode.configure(width=435, height=100, anchor="c", font=("Arial", 40, "bold"), hover="False")
        self.Admin_Frame = self.Frame(550, 160, 375, 655, master=self.Background)
        self.Admin_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        
        self.Admin_Timer_Frame = self.Frame(535, 150, 950, 325, master=self.Background)
        self.Admin_Timer_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        if Admin_Attempt != 3:
            self.Admin_Login_Message = self.Label("Enter Passcode", 50, 40, master=self.Admin_Timer_Frame)
        else:
            self.Admin_Login_Message = self.Label("", 50, 40, master=self.Admin_Timer_Frame)
        def Countdown():
            global Admin_Attempt
            delay = 0
            for Hundreds in range(0, -1, -1):
                for Tens in range(5, -1, -1):
                    for Ones in range(9, -1, -1):
                        self.UI.after(delay, lambda h=Hundreds, t=Tens, o=Ones:
                        self.Admin_Login_Message.configure(text=f"   Timer - {h}:{t}{o}"))
                        delay += 1000
            self.UI.after(delay, After_Countdown)

        def After_Countdown():
            global Admin_Attempt
            Admin_Attempt = 0
            self.Main_UI()

        def Key_1_Press():
            global Entered_Passcode
            if len(Entered_Passcode) <= 9:
                Entered_Passcode += self.Key_1.cget("text")
                Key_Press()
        def Key_2_Press():
            global Entered_Passcode
            if len(Entered_Passcode) <= 9:
                Entered_Passcode += self.Key_2.cget("text")
                Key_Press()
        def Key_3_Press():
            global Entered_Passcode
            if len(Entered_Passcode) <= 9:
                Entered_Passcode += self.Key_3.cget("text")
                Key_Press()
        def Key_4_Press():
            global Entered_Passcode
            if len(Entered_Passcode) <= 9:
                Entered_Passcode += self.Key_4.cget("text")
                Key_Press()
        def Key_5_Press():
            global Entered_Passcode
            if len(Entered_Passcode) <= 9:
                Entered_Passcode += self.Key_4.cget("text")
                Key_Press()
        def Key_6_Press():
            global Entered_Passcode
            if len(Entered_Passcode) <= 9:
                Entered_Passcode += self.Key_6.cget("text")
                Key_Press()
        def Key_7_Press():
            global Entered_Passcode
            if len(Entered_Passcode) <= 9:
                Entered_Passcode += self.Key_7.cget("text")
                Key_Press()
        def Key_8_Press():
            global Entered_Passcode
            if len(Entered_Passcode) <= 9:
                Entered_Passcode += self.Key_8.cget("text")
                Key_Press()
        def Key_9_Press():
            global Entered_Passcode
            if len(Entered_Passcode) <= 9:
                Entered_Passcode += self.Key_9.cget("text")
                Key_Press()
        def Key_0_Press():
            global Entered_Passcode
            if len(Entered_Passcode) <= 9:
                Entered_Passcode += self.Key_0.cget("text")
                Key_Press()
        def Key_d_Press():
            global Entered_Passcode
            Entered_Passcode = Entered_Passcode[:-1]
            Key_Press()
        def Key_c_Press():
            global Entered_Passcode
            Entered_Passcode = ""
            Key_Press()
        def Key_E_Press():
            global Entered_Passcode, Admin_Attempt, BackgroundColor, Current_UserCode
            def Entered_Correct():
                global Entered_Passcode, Admin_Attempt, BackgroundColor
                Admin_Attempt = 0
                Entered_Passcode = ""
                Key_Press()
                self.Disable_Keys()
                self.Main.configure(state="disabled")
                self.Buy.configure(state="disabled")
                self.Print.configure(state="disabled")
                self.Request.configure(state="disabled")
                self.Login_State.configure(font=("Arial", 60, "bold"), text_color=BackgroundColor)
                self.UI.after(1000, lambda: self.Admin_Attempt1.configure(fg_color="green"))
                self.UI.after(2000, lambda: self.Admin_Attempt2.configure(fg_color="green"))
                self.UI.after(3000, lambda: self.Admin_Attempt3.configure(fg_color="green"))
                self.UI.after(4000, lambda: self.Admin_Login_Message.configure(text="     Welcome"))
                self.UI.after(4000, lambda: self.Login_State.configure(text_color=WidgetColor))

            def Entered_Incorrect():
                global Entered_Passcode, Admin_Attempt, BackgroundColor
                Admin_Attempt += 1
                if Admin_Attempt >= 1:
                    self.Admin_Attempt1.configure(fg_color="red")
                    if Admin_Attempt >= 2:
                        self.Admin_Attempt2.configure(fg_color="red")
                        if Admin_Attempt == 3:
                            self.Admin_Attempt3.configure(fg_color="red")
                            self.Login_State.destroy()
                            self.Disable_Keys()
                            self.Login_State = self.Label("LOCKED", 430, 30, master=self.Admin_State_Frame)
                            self.Login_State.configure(font=("Arial", 60, "bold"))
                            Countdown()
                Entered_Passcode = ""
                Key_Press()

            if len(Entered_Passcode) != 0:
                if Entered_Passcode == "123":
                    self.Login_State.destroy()
                    self.Login_State = self.Label("UNLOCKED", 380, 30, master=self.Admin_State_Frame)
                    Entered_Correct()
                    self.UI.after(5500, self.Admin_Setting)
                else:
                    Entered_Incorrect()

        def Key_Press():
            global Entered_Passcode
            Entered_Pass_Length = len(Entered_Passcode)
            Hide_Entered_Pass = ""
            for i in range(0, Entered_Pass_Length):
                Hide_Entered_Pass += '*'
            self.Passcode.configure(text=Hide_Entered_Pass)

        self.Admin_Keypad_Frame = self.Frame(535, 350, 950, 465, master=self.Background)
        self.Admin_Keypad_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Key_1 = self.Button2("1", 35, 37, Key_1_Press, master=self.Admin_Keypad_Frame)
        self.Key_1.configure(width=75, height=75, anchor="c", font=("Arial", 40, "bold"))
        self.Key_4 = self.Button2("4", 35, 137, Key_4_Press, master=self.Admin_Keypad_Frame)
        self.Key_4.configure(width=75, height=75, anchor="c", font=("Arial", 40, "bold"))
        self.Key_7 = self.Button2("7", 35, 237, Key_7_Press, master=self.Admin_Keypad_Frame)
        self.Key_7.configure(width=75, height=75, anchor="c", font=("Arial", 40, "bold"))
        self.Key_2 = self.Button2("2", 135, 37, Key_2_Press, master=self.Admin_Keypad_Frame)
        self.Key_2.configure(width=75, height=75, anchor="c", font=("Arial", 40, "bold"))
        self.Key_5 = self.Button2("5", 135, 137, Key_5_Press, master=self.Admin_Keypad_Frame)
        self.Key_5.configure(width=75, height=75, anchor="c", font=("Arial", 40, "bold"))
        self.Key_8 = self.Button2("8", 135, 237, Key_8_Press, master=self.Admin_Keypad_Frame)
        self.Key_8.configure(width=75, height=75, anchor="c", font=("Arial", 40, "bold"))
        self.Key_3 = self.Button2("3", 235, 37, Key_3_Press, master=self.Admin_Keypad_Frame)
        self.Key_3.configure(width=75, height=75, anchor="c", font=("Arial", 40, "bold"))
        self.Key_6 = self.Button2("6", 235, 137, Key_6_Press, master=self.Admin_Keypad_Frame)
        self.Key_6.configure(width=75, height=75, anchor="c", font=("Arial", 40, "bold"))
        self.Key_9 = self.Button2("9", 235, 237, Key_9_Press, master=self.Admin_Keypad_Frame)
        self.Key_9.configure(width=75, height=75, anchor="c", font=("Arial", 40, "bold"))
        self.Key_Delete = self.Button2("←", 335, 37, Key_d_Press, master=self.Admin_Keypad_Frame)
        self.Key_Delete.configure(width=75, height=75, anchor="c", font=("Arial", 40, "bold"))
        self.Key_Clear = self.Button2("c", 335, 137, Key_c_Press, master=self.Admin_Keypad_Frame)
        self.Key_Clear.configure(width=75, height=75, anchor="c", font=("Arial", 40, "bold"))
        self.Key_0 = self.Button2("0", 335, 237, Key_0_Press, master=self.Admin_Keypad_Frame)
        self.Key_0.configure(width=75, height=75, anchor="c", font=("Arial", 40, "bold"))
        self.Key_Enter = self.Button2("E", 435, 37, Key_E_Press, master=self.Admin_Keypad_Frame)
        self.Key_Enter.configure(width=65, height=275, anchor="c", font=("Arial", 40, "bold"))
        if Admin_Attempt == 3:
            self.Disable_Keys()

    def User_Request_Help(self):
        global Current_UserCode
        self.Delete_User_Frames()
        self.RightMain.configure(fg_color="black")
        self.Buy.configure(state="disabled")
        self.Print.configure(state="disabled")
        self.Setting.configure(state="disabled")
        self.Label(" R E Q U E S T ", 370, 33, master=self.Title).configure(font=("Arial", 60, "bold"), fg_color="black")
        self.User_Request_Frame = self.Frame(1110, 130, 375, 170, master=self.Background)
        self.User_Request_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Label("SELECT ENCOUNTERED", 180, 30, master=self.User_Request_Frame).configure(font=("Arial", 60, "bold"))
        def EBI_1():
            global Encountered_B, Encountered_B1
            Encountered_B = "B1"
            Encountered_B1 += 1
            Select_Encountered_Booklet()
        def EBI_2():
            global Encountered_B, Encountered_B2
            Encountered_B = "B2"
            Encountered_B2 += 1
            Select_Encountered_Booklet()
        def EBI_3():
            global Encountered_B, Encountered_B3
            if Encountered_B != "B2":
                Encountered_B = ""
            Encountered_B3 += 1
            Damaged_Booklet()
        def Damaged_Booklet():
            global Encountered_B1, Encountered_B3
            self.EBI_3.configure(border_width=5, border_color="black")
            self.EBI_1.configure(border_width=0)
            Encountered_B1 = 0
            if Encountered_B3 == 2:
                self.EBI_3.configure(border_width=0)
                Encountered_B3 = 0
            All_Encountered()
        def Select_Encountered_Booklet():
            global Encountered_B, Encountered_B1,  Encountered_B2, Encountered_B3
            if Encountered_B == "B1":
                self.EBI_1.configure(border_width=5, border_color="black")
                self.EBI_2.configure(border_width=0)
                self.EBI_3.configure(border_width=0)
                Encountered_B2 = 0
                Encountered_B3 = 0
                if Encountered_B1 == 2:
                    self.EBI_1.configure(border_width=0)
                    Encountered_B = ""
                    Encountered_B1 = 0
            elif Encountered_B == "B2":
                self.EBI_2.configure(border_width=5, border_color="black")
                self.EBI_1.configure(border_width=0)
                Encountered_B1 = 0
                if Encountered_B2 == 2:
                    self.EBI_2.configure(border_width=0)
                    Encountered_B = ""
                    Encountered_B2 = 0
            All_Encountered()

        self.Encountered_Booklet = self.Frame(300, 100, 375, 325, master=self.Background)
        self.Encountered_Booklet.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Label("📕", 115, 10, master=self.Encountered_Booklet).configure(font=("Arial", 60, "bold"))
        self.Encountered_Booklet_Issues = self.Frame(300, 400, 375, 415, master=self.Background)
        self.Encountered_Booklet_Issues.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.EBI_1 = self.Button2("No Booklet", 35, 35, command=EBI_1,
                                  master=self.Encountered_Booklet_Issues)
        self.EBI_1.configure(width=50, anchor="w", font=("Arial", 30), hover="false")
        self.EBI_2 = self.Button2("Less Booklet", 35, 100, command=EBI_2,
                                  master=self.Encountered_Booklet_Issues)
        self.EBI_2.configure(width=50, anchor="w", font=("Arial", 30), hover="false")
        self.EBI_3 = self.Button2("Damaged \nBooklet", 35, 165, command=EBI_3,
                                  master=self.Encountered_Booklet_Issues)
        self.EBI_3.configure(width=50, anchor="w", font=("Arial", 30), hover="false")

        def EPI_1():
            global Encountered_P, Encountered_P1
            Encountered_P = "P1"
            Encountered_P1 += 1
            Select_Encountered_Print()
        def EPI_2():
            global Encountered_P, Encountered_P2
            Encountered_P = "P2"
            Encountered_P2 += 1
            Select_Encountered_Print()
        def EPI_3():
            global Encountered_P, Encountered_P3
            Encountered_P = "P3"
            Encountered_P3 += 1
            Select_Encountered_Print()
        def EPI_4():
            global Encountered_P, Encountered_P4
            if Encountered_P == "P1":
                Encountered_P = ""
            Encountered_P4 += 1
            Damaged_Print()
        def Damaged_Print():
            global Encountered_P, Encountered_P1, Encountered_P4
            self.EPI_4.configure(border_width=5, border_color="black")
            self.EPI_1.configure(border_width=0)
            Encountered_P1 = 0
            if Encountered_P4 == 2:
                self.EPI_4.configure(border_width=0)
                Encountered_P4 = 0
            All_Encountered()

        def Select_Encountered_Print():
            global Encountered_P, Encountered_P1,  Encountered_P2,  Encountered_P3, Encountered_P4
            if Encountered_P == "P1":
                self.EPI_1.configure(border_width=5, border_color="black")
                self.EPI_2.configure(border_width=0)
                self.EPI_3.configure(border_width=0)
                self.EPI_4.configure(border_width=0)
                Encountered_P2 = 0
                Encountered_P3 = 0
                Encountered_P4 = 0
                if Encountered_P1 == 2:
                    self.EPI_1.configure(border_width=0)
                    Encountered_P = ""
                    Encountered_P1 = 0
            elif Encountered_P == "P2":
                self.EPI_2.configure(border_width=5, border_color="black")
                self.EPI_1.configure(border_width=0)
                self.EPI_3.configure(border_width=0)
                Encountered_P1 = 0
                Encountered_P3 = 0
                if Encountered_P2 == 2:
                    self.EPI_2.configure(border_width=0)
                    Encountered_P = ""
                    Encountered_P2 = 0
            elif Encountered_P == "P3":
                self.EPI_3.configure(border_width=5, border_color="black")
                self.EPI_1.configure(border_width=0)
                self.EPI_2.configure(border_width=0)
                Encountered_P1 = 0
                Encountered_P2 = 0
                if Encountered_P3 == 2:
                    self.EPI_3.configure(border_width=0)
                    Encountered_P = ""
                    Encountered_P3 = 0
            All_Encountered()

        self.Encountered_Print = self.Frame(300, 100, 665, 325, master=self.Background)
        self.Encountered_Print.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Label("🖶", 125, 10, master=self.Encountered_Print).configure(font=("Arial", 60, "bold"))
        self.Encountered_Print_Issues = self.Frame(300, 400, 665, 415, master=self.Background)
        self.Encountered_Print_Issues.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.EPI_1 = self.Button2("No Printout", 35, 35, command=EPI_1, master=self.Encountered_Print_Issues)
        self.EPI_1.configure(width=50, anchor="w", font=("Arial", 30), hover="false")
        self.EPI_2 = self.Button2("Less Printout", 35, 100, command=EPI_2, master=self.Encountered_Print_Issues)
        self.EPI_2.configure(width=50, anchor="w", font=("Arial", 30), hover="false")
        self.EPI_3 = self.Button2("Wrong Printout", 35, 165, command=EPI_3, master=self.Encountered_Print_Issues)
        self.EPI_3.configure(width=50, anchor="w", font=("Arial", 30), hover="false")
        self.EPI_4 = self.Button2("Damaged \nPrintout", 35, 230, command=EPI_4, master=self.Encountered_Print_Issues)
        self.EPI_4.configure(width=50, anchor="w", font=("Arial", 30), hover="false")

        def ECI_1():
            global Encountered_C, Encountered_C1
            Encountered_C = "C1"
            Encountered_C1 += 1
            Select_Encountered_Change()
        def ECI_2():
            global Encountered_C, Encountered_C2
            Encountered_C = "C2"
            Encountered_C2 += 1
            Select_Encountered_Change()
        def Select_Encountered_Change():
            global Encountered_C, Encountered_C1, Encountered_C2
            if Encountered_C == "C1":
                self.ECI_1.configure(border_width=5, border_color="black")
                self.ECI_2.configure(border_width=0)
                Encountered_C2 = 0
                if Encountered_C1 == 2:
                    self.ECI_1.configure(border_width=0)
                    Encountered_C = ""
                    Encountered_C1 = 0
            elif Encountered_C == "C2":
                self.ECI_2.configure(border_width=5, border_color="black")
                self.ECI_1.configure(border_width=0)
                Encountered_C1 = 0
                if Encountered_C2 == 2:
                    self.ECI_2.configure(border_width=0)
                    Encountered_C = ""
                    Encountered_C2 = 0
            All_Encountered()
        self.Encountered_Change = self.Frame(300, 100, 955, 325, master=self.Background)
        self.Encountered_Change.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Label("🪙", 115, 10, master=self.Encountered_Change).configure(font=("Arial", 60, "bold"))
        self.Encountered_Change_Issues = self.Frame(300, 400, 955, 415, master=self.Background)
        self.Encountered_Change_Issues.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.ECI_1 = self.Button2("No Change", 35, 35, command=ECI_1, master=self.Encountered_Change_Issues)
        self.ECI_1.configure(width=50, anchor="w", font=("Arial", 30), hover="false")
        self.ECI_2 = self.Button2("Less Change", 35, 100, command=ECI_2, master=self.Encountered_Change_Issues)
        self.ECI_2.configure(width=50, anchor="w", font=("Arial", 30), hover="false")

        def All_Encountered():
            global Encountered_B, Encountered_P, Encountered_C, Encountered_B3, Encountered_P4
            New_Text = ""
            self.Encountered_Text.configure(text=New_Text)
            Existing_Text = self.Encountered_Text.cget("text")
            if Encountered_B == "B1":
                New_Text = Existing_Text + "• No Booklet\n"
            elif Encountered_B == "B2":
                New_Text = Existing_Text + "• Less Booklet\n"
            self.Encountered_Text.configure(text=New_Text)
            Existing_Text = self.Encountered_Text.cget("text")
            if Encountered_P == "P1":
                New_Text = Existing_Text + "• No Printout\n"
            elif Encountered_P == "P2":
                New_Text = Existing_Text + "• Less Printout\n"
            elif Encountered_P == "P3":
                New_Text = Existing_Text + "• Wrong Printout\n"
            self.Encountered_Text.configure(text=New_Text)
            Existing_Text = self.Encountered_Text.cget("text")
            if Encountered_C == "C1":
                New_Text = Existing_Text + "• No Change\n"
            elif Encountered_C == "C2":
                New_Text = Existing_Text + "• Less Change\n"
            self.Encountered_Text.configure(text=New_Text)
            Existing_Text = self.Encountered_Text.cget("text")
            if Encountered_B3 == 1:
                New_Text = Existing_Text + "• Damaged Booklet\n"
            self.Encountered_Text.configure(text=New_Text)
            Existing_Text = self.Encountered_Text.cget("text")
            if Encountered_P4 == 1:
                New_Text = Existing_Text + "• Damaged Printout\n"
            self.Encountered_Text.configure(text=New_Text)
        def Help_To_Main():
            global Encountered_B, Encountered_B1, Encountered_B2, Encountered_B3, Encountered_P, Encountered_P1, \
                   Encountered_P2, Encountered_P3, Encountered_P4, Encountered_C, Encountered_C1, Encountered_C2
            Encountered_B = ""
            Encountered_B1 = 0
            Encountered_B2 = 0
            Encountered_B3 = 0
            Encountered_P = ""
            Encountered_P1 = 0
            Encountered_P2 = 0
            Encountered_P3 = 0
            Encountered_P4 = 0
            Encountered_C = ""
            Encountered_C1 = 0
            Encountered_C2 = 0
            self.Start_UI()
        def Send_To_Admin():
            New_Text = self.Encountered_Text.cget("text")
            self.Twilio_Client.messages.create(
                from_='whatsapp:+14155238886',
                body=f"REQUEST HELP!!!"
                     f"\n{New_Text}",
                to='whatsapp:+639397178930'
            )
            Help_To_Main()

        self.Send_Encountered = self.Frame(240, 100, 1245, 325, master=self.Background)
        self.Send_Encountered.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Send_Encountered_Issues = self.Frame(240, 400,  1245, 415, master=self.Background)
        self.Send_Encountered_Issues.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Encountered_Text = self.Label("", 15, 25, master=self.Send_Encountered_Issues)
        self.Encountered_Text.configure(font=("Arial", 25))
        if Current_UserCode[-1] == "7":
            self.EPI_1.configure(state="disabled")
            self.EPI_2.configure(state="disabled")
            self.EPI_3.configure(state="disabled")
            self.EPI_4.configure(state="disabled")
        elif Current_UserCode[-1] == "9":
            self.EBI_1.configure(state="disabled")
            self.EBI_2.configure(state="disabled")
            self.EBI_3.configure(state="disabled")
        self.WhatsApp_Send_Encountered = self.Button2("Send", 35, 235, command=Send_To_Admin, master=self.Send_Encountered_Issues)
        self.WhatsApp_Send_Encountered.configure(width=50, anchor="w", font=("Arial", 30))

    def Admin_Setting(self):
        global BackgroundColor, Booklet_Cost, Paper_Cost, Available_Booklets, Available_Papers, Max_Booklet, Max_Paper, \
               Available_Coins, Max_Coin, One, Five, Ten, Max_Coin_Storage, Booklet_State
        self.Delete_Admin_Frames()
        self.RightMain.configure(fg_color="black")
        self.Main.configure(state="disabled")
        self.Buy.configure(state="disabled")
        self.Print.configure(state="disabled")
        self.Request.configure(state="disabled")
        self.State_Price_Frame = self.Frame(445, 100, 375, 170, master=self.Background)
        self.State_Price_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Label("State Price", 75, 15, master=self.State_Price_Frame)
        self.State_Price_Widgets_Frame = self.Frame(445, 315, 375, 260, master=self.Background)
        self.State_Price_Widgets_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        def Set_Booklet_Price(events):
            global Booklet_Cost
            Booklet_Cost = int(self.Booklet_Price_Slider.get())
            if Booklet_Cost < 10:
                self.Booklet_Price.configure(text=f" {Booklet_Cost}")
            else:
                self.Booklet_Price.configure(text=Booklet_Cost)
        def Set_Booklet_State():
            global Booklet_State, Available_Booklets
            if self.Booklet_Switch.get() == "On" and Available_Booklets != 0:
                self.Booklet_State.configure(text="ON", text_color="green")
                Booklet_State = 1
            else:
                self.Booklet_State.configure(text="OFF", text_color="red")
                Booklet_State = 0
                if Available_Booklets == 0:
                    self.Booklet_Switch.configure(state="disabled")
        self.Booklet_Price_Name= self.Button2(f"       Booklet", 35, 35, command=None, master=self.State_Price_Widgets_Frame)
        self.Booklet_Price_Name.configure(width=100, height=50, anchor="c", font=("Arial", 45), hover="false")
        self.Booklet_State = self.Button2("ON", 45, 35, command=None, master=self.State_Price_Widgets_Frame)
        self.Booklet_Price = self.Label(Booklet_Cost, 310, 38, master=self.State_Price_Widgets_Frame)
        self.Booklet_Price.configure(font=("Arial", 50))
        self.Booklet_Price1 = self.Label("₱", 375, 38, master=self.State_Price_Widgets_Frame)
        self.Booklet_Price1.configure(font=("Arial", 50))
        self.Booklet_State.configure(width=50, height=50, font=("Arial", 45), corner_radius=0, hover="false", text_color="green")
        self.Booklet_Switch = self.Switch("", 75, 30, 30, 110, "green", "red", command=Set_Booklet_State, master=self.State_Price_Widgets_Frame)
        if Booklet_State == 1:
            self.Booklet_Switch.select()
        else:
            self.Booklet_Switch.deselect()
        Set_Booklet_State()
        self.Booklet_Price_Slider = self.Slider(5, 20, 15, 300, 35, 115, 115, command=Set_Booklet_Price, master=self.State_Price_Widgets_Frame)
        self.Booklet_Price_Slider.set(Booklet_Cost)

        def Set_Paper_Price(events):
            global Paper_Cost
            Paper_Cost = int(self.Paper_Price_Slider.get())
            if Paper_Cost < 10:
                self.Paper_Price.configure(text=f" {Paper_Cost}")
            else:
                self.Paper_Price.configure(text=Paper_Cost)
        def Set_Paper_State():
            global Paper_State, Available_Papers
            if self.Paper_Switch.get() == "On" and Available_Papers != 0:
                self.Paper_State.configure(text="ON", text_color="green")
                Paper_State = 1
            else:
                self.Paper_State.configure(text="OFF", text_color="red")
                Paper_State = 0
                if Available_Papers == 0:
                    self.Paper_Switch.configure(state="disabled")
        self.Paper_Price_Name = self.Button2(f"       Paper  ", 35, 170, command=None, master=self.State_Price_Widgets_Frame)
        self.Paper_Price_Name.configure(width=100, height=50, anchor="c", font=("Arial", 45), hover="false")
        self.Paper_State = self.Button2("ON", 45, 170, command=None, master=self.State_Price_Widgets_Frame)
        self.Paper_Price = self.Label(f" {Paper_Cost}", 310, 173, master=self.State_Price_Widgets_Frame)
        self.Paper_Price.configure(font=("Arial", 50))
        self.Paper_Price1 = self.Label("₱", 375, 173, master=self.State_Price_Widgets_Frame)
        self.Paper_Price1.configure(font=("Arial", 50))
        self.Paper_State.configure(width=50, height=50, font=("Arial", 45), corner_radius=0, hover="false", text_color="green")
        self.Paper_Switch = self.Switch("", 75, 30, 30, 245, "green", "red", command=Set_Paper_State, master=self.State_Price_Widgets_Frame)
        if Paper_State == 1:
            self.Paper_Switch.select()
        else:
            self.Paper_Switch.deselect()
        Set_Paper_State()
        self.Paper_Price_Slider = self.Slider(1, 10, 9, 300, 35, 115, 250, command=Set_Paper_Price, master=self.State_Price_Widgets_Frame)
        self.Paper_Price_Slider.set(Paper_Cost)

        self.Stock_Frame = self.Frame(377, 100, 810, 170, master=self.Background)
        self.Stock_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Label("Stock", 115, 15, master=self.Stock_Frame)
        self.Stock_Widgets_Frame = self.Frame(377, 315, 810, 260, master=self.Background)
        self.Stock_Widgets_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Booklet_Stock = self.Label(Available_Booklets, 236, 30, master=self.Stock_Widgets_Frame)
        self.Booklet_Stock.configure(font=("Arial", 50))
        self.Booklet_Stock1 = self.Label("📕", 300, 26, master=self.Stock_Widgets_Frame)
        self.Booklet_Stock1.configure(font=("Arial", 50))
        self.Booklet_Progress_Bar = self.Progress_Bar(180, 35, 35, 40, master=self.Stock_Widgets_Frame)
        self.Booklet_Progress_Bar.set(Available_Booklets / Max_Booklet)
        if Available_Booklets <= 5:
            self.Booklet_Progress_Bar.configure(progress_color="red")
        elif Available_Booklets <= 10:
            self.Booklet_Progress_Bar.configure(progress_color="yellow")
        self.Paper_Stock = self.Label(Available_Papers, 220, 130, master=self.Stock_Widgets_Frame)
        self.Paper_Stock.configure(font=("Arial", 50))
        self.Paper_Stock1 = self.Label("📄", 300, 126, master = self.Stock_Widgets_Frame)
        self.Paper_Stock1.configure(font=("Arial", 50))
        self.Paper_Progress_Bar = self.Progress_Bar(180, 35, 35, 140, master=self.Stock_Widgets_Frame)
        self.Paper_Progress_Bar.set(Available_Papers / Max_Paper)
        if Available_Papers <= 15:
            self.Paper_Progress_Bar.configure(progress_color="red")
        elif Available_Papers <= 30:
            self.Paper_Progress_Bar.configure(progress_color="yellow")
        self.Coins_Stock = self.Label(Available_Coins, 220, 230, master=self.Stock_Widgets_Frame)
        self.Coins_Stock.configure(font=("Arial", 50))
        self.Coins_Stock = self.Label("🪙", 300, 226, master=self.Stock_Widgets_Frame)
        self.Coins_Stock.configure(font=("Arial", 50))
        self.Coin_Progress_Bar = self.Progress_Bar(180, 35, 35, 240, master=self.Stock_Widgets_Frame)
        self.Coin_Progress_Bar.set(Available_Coins / Max_Coin)
        if Available_Coins <= 10:
            self.Coin_Progress_Bar.configure(progress_color="red")
        elif Available_Coins <= 20:
            self.Coin_Progress_Bar.configure(progress_color="yellow")

        self.Storage_Frame = self.Frame(310, 100, 1175, 170, master=self.Background)
        self.Storage_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Label("Storage", 50, 15, master=self.Storage_Frame)
        self.Storage_Widgets_Frame = self.Frame(310, 315, 1175, 260, master=self.Background)
        self.Storage_Widgets_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Piso_Storage = self.Button2(f"Ⓘx{One}", 35, 35, command=None, master=self.Storage_Widgets_Frame)
        self.Piso_Storage.configure(width=150, height=50, anchor="w", font=("Arial", 45), hover="false")
        self.Piso_Storage1 = self.Label((One*1), 195, 35, master=self.Storage_Widgets_Frame)
        self.Piso_Storage1.configure(font=("Arial", 50))
        self.Lima_Storage = self.Button2(f"Ⓥx{Five}", 35, 100, command=None, master=self.Storage_Widgets_Frame)
        self.Lima_Storage.configure(width=150, height=50, anchor="w", font=("Arial", 45), hover="false")
        self.Lima_Storage1 = self.Label((Five * 1), 195, 100, master=self.Storage_Widgets_Frame)
        self.Lima_Storage1.configure(font=("Arial", 50))
        self.Sampu_Storage = self.Button2(f"Ⓧx{Ten}", 35, 165, command=None, master=self.Storage_Widgets_Frame)
        self.Sampu_Storage.configure(width=150, height=50, anchor="w", font=("Arial", 45), hover="false")
        self.Sampu_Storage1 = self.Label((Ten * 1), 195, 165, master=self.Storage_Widgets_Frame)
        self.Sampu_Storage1.configure(font=("Arial", 50))
        Total_Inserted = One + Five + Ten
        self.Coin_Storage_Progress_Bar = self.Progress_Bar(238, 35, 35, 245, master=self.Storage_Widgets_Frame)
        self.Coin_Storage_Progress_Bar.set((Total_Inserted) / Max_Coin_Storage)
        if Total_Inserted <= 35:
            self.Coin_Storage_Progress_Bar.configure(progress_color="green")
        elif Total_Inserted <= 75:
            self.Coin_Storage_Progress_Bar.configure(progress_color="yellow")
        elif Total_Inserted <= 110:
            self.Coin_Storage_Progress_Bar.configure(progress_color="red")

        def Skyblue_Theme():
            global WidgetColor, Main_Image, USB_Image
            WidgetColor = "Skyblue"
            Main_Image = "images/SkyBlue_Main.png"
            USB_Image = "images/SkyBlue_USB.png"
            Color_Pick()
        def Lightgreen_Theme():
            global WidgetColor, Main_Image, USB_Image
            WidgetColor = "Lightgreen"
            Main_Image = "images/LightGreen_Main.png"
            USB_Image = "images/LightGreen_USB.png"
            Color_Pick()
        def Lightcoral_Theme():
            global WidgetColor, Main_Image, USB_Image
            WidgetColor = "Lightcoral"
            Main_Image = "images/LightCoral_Main.png"
            USB_Image = "images/LightCoral_USB.png"
            Color_Pick()
        def Lightpink_Theme():
            global WidgetColor, Main_Image, USB_Image
            WidgetColor = "Lightpink"
            Main_Image = "images/LightPink_Main.png"
            USB_Image = "images/LightPink_USB.png"
            Color_Pick()
        def Plum_Theme():
            global WidgetColor, Main_Image, USB_Image
            WidgetColor = "Plum"
            Main_Image = "images/Plum_Main.png"
            USB_Image = "images/Plum_USB.png"
            Color_Pick()
        def Aqua_Theme():
            global WidgetColor, Main_Image, USB_Image
            WidgetColor = "Aqua"
            Main_Image = "images/Aqua_Main.png"
            USB_Image = "images/Aqua_USB.png"
            Color_Pick()
        def Sandybrown_Theme():
            global WidgetColor, Main_Image, USB_Image
            WidgetColor = "Sandybrown"
            Main_Image = "images/SandyBrown_Main.png"
            USB_Image = "images/SandyBrown_USB.png"
            Color_Pick()
        def Khaki_Theme():
            global WidgetColor, Main_Image, USB_Image
            WidgetColor = "Khaki"
            Main_Image = "images/Khaki_Main.png"
            USB_Image = "images/Khaki_USB.png"
            Color_Pick()
        def Mediumaquamarine_Theme():
            global WidgetColor, Main_Image, USB_Image
            WidgetColor = "Mediumaquamarine"
            Main_Image = "images/MediumAquamarine_Main.png"
            USB_Image = "images/MediumAquamarine_USB.png"
            Color_Pick()
        def Lightsalmon_Theme():
            global WidgetColor, Main_Image, USB_Image
            WidgetColor = "Lightsalmon"
            Main_Image = "images/LightSalmon_Main.png"
            USB_Image = "images/LightSalmon_USB.png"
            Color_Pick()
        def Rosybrown_Theme():
            global WidgetColor, Main_Image, USB_Image
            WidgetColor = "Rosybrown"
            Main_Image = "images/RosyBrown_Main.png"
            USB_Image = "images/RosyBrown_USB.png"
            Color_Pick()
        def Mediumturquoise_Theme():
            global WidgetColor, Main_Image, USB_Image
            WidgetColor = "Mediumturquoise"
            Main_Image = "images/MediumTurquoise_Main.png"
            USB_Image = "images/MediumTurquoise_USB.png"
            Color_Pick()

        def Color_Pick():
            global WidgetColor
            if WidgetColor == "Skyblue":
                self.Skyblue_Button.configure(border_width=5, border_color="black")
            else:
                self.Skyblue_Button.configure(border_width=0)
            if WidgetColor == "Lightgreen":
                self.Lightgreen_Button.configure(border_width=5, border_color="black")
            else:
                self.Lightgreen_Button.configure(border_width=0)
            if WidgetColor == "Lightcoral":
                self.Lightcoral_Button.configure(border_width=5, border_color="black")
            else:
                self.Lightcoral_Button.configure(border_width=0)
            if WidgetColor == "Lightpink":
                self.Lightpink_Button.configure(border_width=5, border_color="black")
            else:
                self.Lightpink_Button.configure(border_width=0)
            if WidgetColor == "Plum":
                self.Plum_Button.configure(border_width=5, border_color="black")
            else:
                self.Plum_Button.configure(border_width=0)
            if WidgetColor == "Aqua":
                self.Aqua_Button.configure(border_width=5, border_color="black")
            else:
                self.Aqua_Button.configure(border_width=0)
            if WidgetColor == "Sandybrown":
                self.Sandybrown_Button.configure(border_width=5, border_color="black")
            else:
                self.Sandybrown_Button.configure(border_width=0)
            if WidgetColor == "Khaki":
                self.Khaki_Button.configure(border_width=5, border_color="black")
            else:
                self.Khaki_Button.configure(border_width=0)
            if WidgetColor == "Mediumaquamarine":
                self.Mediumaquamarine_Button.configure(border_width=5, border_color="black")
            else:
                self.Mediumaquamarine_Button.configure(border_width=0)
            if WidgetColor == "Lightsalmon":
                self.Lightsalmon_Button.configure(border_width=5, border_color="black")
            else:
                self.Lightsalmon_Button.configure(border_width=0)
            if WidgetColor == "Rosybrown":
                self.Rosybrown_Button.configure(border_width=5, border_color="black")
            else:
                self.Rosybrown_Button.configure(border_width=0)
            if WidgetColor == "Mediumturquoise":
                self.Mediumturquoise_Button.configure(border_width=5, border_color="black")
            else:
                self.Mediumturquoise_Button.configure(border_width=0)


        self.Admin_Lower_Frame = self.Frame(810, 250, 375, 565, master=self.Background)
        self.Admin_Lower_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Theme_Color_Frame = self.Frame(310, 250, 1175, 565, master=self.Background)
        self.Theme_Color_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Skyblue_Button = self.Button2("", 31.8, 35, command=Skyblue_Theme, master=self.Theme_Color_Frame)
        self.Skyblue_Button.configure(width=50, height=50, anchor="w", font=("Arial", 45), hover="false",
                                       fg_color="Skyblue")
        self.Lightgreen_Button = self.Button2("", 96.8, 35, command=Lightgreen_Theme, master=self.Theme_Color_Frame)
        self.Lightgreen_Button.configure(width=50, height=50, anchor="w", font=("Arial", 45), hover="false",
                                       fg_color="Lightgreen")
        self.Lightcoral_Button = self.Button2("", 161.8, 35, command=Lightcoral_Theme, master=self.Theme_Color_Frame)
        self.Lightcoral_Button.configure(width=50, height=50, anchor="w", font=("Arial", 45), hover="false",
                                         fg_color="Lightcoral")
        self.Lightpink_Button = self.Button2("", 226.8, 35, command=Lightpink_Theme, master=self.Theme_Color_Frame)
        self.Lightpink_Button.configure(width=50, height=50, anchor="w", font=("Arial", 45), hover="false",
                                         fg_color="Lightpink")
        self.Plum_Button = self.Button2("", 31.8, 100, command=Plum_Theme, master=self.Theme_Color_Frame)
        self.Plum_Button.configure(width=50, height=50, anchor="w", font=("Arial", 45), hover="false",
                                         fg_color="Plum")
        self.Aqua_Button = self.Button2("", 96.8, 100, command=Aqua_Theme, master=self.Theme_Color_Frame)
        self.Aqua_Button.configure(width=50, height=50, anchor="w", font=("Arial", 45), hover="false",
                                         fg_color="Aqua")
        self.Sandybrown_Button = self.Button2("", 161.8, 100, command=Sandybrown_Theme, master=self.Theme_Color_Frame)
        self.Sandybrown_Button.configure(width=50, height=50, anchor="w", font=("Arial", 45), hover="false",
                                         fg_color="Sandybrown")
        self.Khaki_Button = self.Button2("", 226.8, 100, command=Khaki_Theme, master=self.Theme_Color_Frame)
        self.Khaki_Button.configure(width=50, height=50, anchor="w", font=("Arial", 45), hover="false",
                                        fg_color="Khaki")
        self.Mediumaquamarine_Button = self.Button2("", 31.8, 165, command=Mediumaquamarine_Theme, master=self.Theme_Color_Frame)
        self.Mediumaquamarine_Button.configure(width=50, height=50, anchor="w", font=("Arial", 45), hover="false",
                                         fg_color="Mediumaquamarine")
        self.Lightsalmon_Button = self.Button2("", 96.8, 165, command=Lightsalmon_Theme, master=self.Theme_Color_Frame)
        self.Lightsalmon_Button.configure(width=50, height=50, anchor="w", font=("Arial", 45), hover="false",
                                   fg_color="Lightsalmon")
        self.Rosybrown_Button = self.Button2("", 161.8, 165, command=Rosybrown_Theme, master=self.Theme_Color_Frame)
        self.Rosybrown_Button.configure(width=50, height=50, anchor="w", font=("Arial", 45), hover="false",
                                         fg_color="Rosybrown")
        self.Mediumturquoise_Button = self.Button2("", 226.8, 165, command=Mediumturquoise_Theme, master=self.Theme_Color_Frame)
        self.Mediumturquoise_Button.configure(width=50, height=50, anchor="w", font=("Arial", 45), hover="false",
                                    fg_color="Mediumturquoise")
        Color_Pick()

        def Show_Database():
            self.RightMain4 = self.Frame(1160, 697, 350, 145, master=self.Background)
            self.RightMain4.configure(fg_color="black")
            self.Title4 = self.Frame(1180, 130, 340, 15, master=self.Background)
            self.Title4.configure(border_width=10, border_color=WidgetColor, corner_radius=20, fg_color="black")
            self.Label(" D A T A B A S E ", 350, 33, master=self.Title4).configure(font=("Arial", 60, "bold"),fg_color="black")
            self.Main_Database_Frame = customtkinter.CTkScrollableFrame(master=self.Background, fg_color=BackgroundColor,
                                                                border_color=WidgetColor, border_width=10, width=1065,
                                                                height=584, orientation="vertical",
                                                                scrollbar_button_color=WidgetColor, corner_radius=20,
                                                                scrollbar_button_hover_color="white")
            self.Main_Database_Frame.place(x=375, y=170)
            Database_Column = [["ID", "UserID", "Date", "Time", "Output", "Quantity", "Cost", "Total", "Coin", "Change"]]
            self.Database_Table = CTkTable(master=self.Main_Database_Frame, row=20, column=10, font=("Arial", 15),
                                           values=Database_Column, colors=["gray", "gray"], border_color=WidgetColor,
                                           border_width=7, text_color="black", header_color="light gray", hover="false")

            self.Database_Table.pack(expand=True, fill="both", padx=15, pady=5)
            Table_ID = 1
            Index_ID = 1
            I = 0
            while Table_ID <= int(len(self.Vend_Database) / 10):
                if I + 9 < len(self.Vend_Database):  # Check if accessing elements is within bounds
                    self.Database_Table.add_row(
                        values=[self.Vend_Database[I], self.Vend_Database[I + 1], self.Vend_Database[I + 2],
                                self.Vend_Database[I + 3],
                                self.Vend_Database[I + 4], self.Vend_Database[I + 5], self.Vend_Database[I + 6],
                                self.Vend_Database[I + 7],
                                self.Vend_Database[I + 8], self.Vend_Database[I + 9]], index=Index_ID)
                else:
                    # Handle the case where accessing elements goes out of bounds
                    break
                I += 10
                Index_ID += 1
            def Delete_Database():
                self.RightMain4.destroy()
                self.Title4.destroy()
                self.Database_Table.pack_forget()
                self.Main_Database_Frame.place_forget()
                Return_Button.destroy()
            Return_Button = self.Button("Return", 25, 540, "images/Return.png", Delete_Database, master=self.LeftMain)
            self.Main.configure(state="disabled")

        def Shutdown_GUI():
            self.UI.destroy()

        def Save_Properties():
            self.Main_UI()

        self.Shutdown_Button = self.Button2("Shutdown", 55, 55, command=Shutdown_GUI, master=self.Admin_Lower_Frame)
        self.Shutdown_Button.configure(width=150, height=50, anchor="w", font=("Arial", 45))
        self.Save_Button = self.Button2("Save", 55, 140, command=Save_Properties, master=self.Admin_Lower_Frame)
        self.Save_Button.configure(width=150, height=50, anchor="w", font=("Arial", 45))
        self.Database_Button = self.Button2("Database", 300, 55, command=Show_Database, master=self.Admin_Lower_Frame)
        self.Database_Button.configure(width=150, height=50, anchor="w", font=("Arial", 45))

    def Request_UI(self):
        global BackgroundColor, WidgetColor, Current, User_Attempt, Entered_Passcode, USB, Service_Current
        USB = 0
        Entered_Passcode = ""
        self.RightMainM.destroy()
        if Current == "Main":
            self.Main2.destroy()
        elif Current == "Booklet":
            self.Delete_Booklet_Frames()
            self.Buy2.destroy()
        elif Current == "Transaction":
            self.Delete_Transaction_frames()
            if Service_Current == "Booklet":
                self.Buy2.destroy()
            else:
                self.Print2.destroy()
        elif Current == "Print":
            self.Delete_Print_Frames()
            self.Print2.destroy()
        elif Current == "File Choose":
            self.Delete_File_Choose_frames()
            self.Print2.destroy()
        elif Current == "Admin":
            self.Delete_Admin_Frames()
            self.Setting2.destroy()
        self.Delete()
        self.RightMain.configure(fg_color="black")
        self.Buy.configure(fg_color=BackgroundColor)
        self.Main.configure(fg_color=BackgroundColor)
        self.Print.configure(fg_color=BackgroundColor)
        self.Setting.configure(fg_color=BackgroundColor)
        self.Request.configure(fg_color=WidgetColor)
        Current = "Help"
        self.Request2 = self.Button("Request", 25, 620, "images/Request.png", command=None, master=self.LeftMain)
        self.Title = self.Frame(1180, 130, 340, 15, master=self.Background)
        self.Title.configure(border_width=10, border_color=WidgetColor, corner_radius=20, fg_color="black")
        self.Label(" R E Q U E S T ", 380, 33, master=self.Title).configure(font=("Arial", 60, "bold"),
                                                                            fg_color="black")
        self.User_State_Frame = self.Frame(1110, 130, 375, 170, master=self.Background)
        self.User_State_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        if User_Attempt != 3:
            self.Login_State = self.Label("ACTIVE", 440, 30, master=self.User_State_Frame)
            self.Login_State.configure(font=("Arial", 60, "bold"))
        else:
            self.Login_State = self.Label("LOCKED", 430, 30, master=self.User_State_Frame)
            self.Login_State.configure(font=("Arial", 60, "bold"))
        self.User_Attempt1_border = self.Frame(190, 150, 375, 325, master=self.Background)
        self.User_Attempt1_border.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.User_Attempt1 = self.Frame(170, 130, 385, 334, master=self.Background)
        self.User_Attempt1.configure(border_width=15, border_color="gray", corner_radius=20)
        self.User_Attempt2_border = self.Frame(190, 150, 555, 325, master=self.Background)
        self.User_Attempt2_border.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.User_Attempt2 = self.Frame(170, 130, 565, 334, master=self.Background)
        self.User_Attempt2.configure(border_width=15, border_color="gray", corner_radius=20)
        self.User_Attempt3_border = self.Frame(190, 150, 735, 325, master=self.Background)
        self.User_Attempt3_border.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.User_Attempt3 = self.Frame(170, 130, 745, 334, master=self.Background)
        self.User_Attempt3.configure(border_width=15, border_color="gray", corner_radius=20)
        if User_Attempt >= 1:
            self.User_Attempt1.configure(fg_color="red")
            if User_Attempt >= 2:
                self.User_Attempt2.configure(fg_color="red")
                if User_Attempt == 3:
                    self.User_Attempt3.configure(fg_color="red")
        self.User_Code_Frame = self.Frame(550, 200, 375, 465, master=self.Background)
        self.User_Code_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Passcode = self.Button2(" ", 55, 52, command=None, master=self.User_Code_Frame, state="normal")
        self.Passcode.configure(width=435, height=100, anchor="c", font=("Arial", 40, "bold"), hover="False")
        self.User_Frame = self.Frame(550, 160, 375, 655, master=self.Background)
        self.User_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.User_Timer_Frame = self.Frame(535, 150, 950, 325, master=self.Background)
        self.User_Timer_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        if User_Attempt != 3:
            self.User_Login_Message = self.Label("Enter User ID", 50, 40, master=self.User_Timer_Frame)
        else:
            self.User_Login_Message = self.Label("", 50, 40, master=self.User_Timer_Frame)
        self.User_Login_Message.configure(text="Enter User ID")

        def Countdown():
            global User_Attempt
            delay = 0
            for Hundreds in range(0, -1, -1):
                for Tens in range(5, -1, -1):
                    for Ones in range(9, -1, -1):
                        self.UI.after(delay, lambda h=Hundreds, t=Tens, o=Ones:
                        self.User_Login_Message.configure(text=f"   Timer - {h}:{t}{o}"))
                        delay += 1000
            self.UI.after(delay, After_Countdown)

        def After_Countdown():
            global User_Attempt
            User_Attempt = 0
            self.Main_UI()

        def Key_1_Press():
            global Entered_Passcode
            if len(Entered_Passcode) <= 9:
                Entered_Passcode += self.Key_1.cget("text")
                self.Passcode.configure(text=Entered_Passcode)

        def Key_2_Press():
            global Entered_Passcode
            if len(Entered_Passcode) <= 9:
                Entered_Passcode += self.Key_2.cget("text")
                self.Passcode.configure(text=Entered_Passcode)

        def Key_3_Press():
            global Entered_Passcode
            if len(Entered_Passcode) <= 9:
                Entered_Passcode += self.Key_3.cget("text")
                self.Passcode.configure(text=Entered_Passcode)

        def Key_4_Press():
            global Entered_Passcode
            if len(Entered_Passcode) <= 9:
                Entered_Passcode += self.Key_4.cget("text")
                self.Passcode.configure(text=Entered_Passcode)

        def Key_5_Press():
            global Entered_Passcode
            if len(Entered_Passcode) <= 9:
                Entered_Passcode += self.Key_5.cget("text")
                self.Passcode.configure(text=Entered_Passcode)

        def Key_6_Press():
            global Entered_Passcode
            if len(Entered_Passcode) <= 9:
                Entered_Passcode += self.Key_6.cget("text")
                self.Passcode.configure(text=Entered_Passcode)

        def Key_7_Press():
            global Entered_Passcode
            if len(Entered_Passcode) <= 9:
                Entered_Passcode += self.Key_7.cget("text")
                self.Passcode.configure(text=Entered_Passcode)

        def Key_8_Press():
            global Entered_Passcode
            if len(Entered_Passcode) <= 9:
                Entered_Passcode += self.Key_8.cget("text")
                self.Passcode.configure(text=Entered_Passcode)

        def Key_9_Press():
            global Entered_Passcode
            if len(Entered_Passcode) <= 9:
                Entered_Passcode += self.Key_9.cget("text")
                self.Passcode.configure(text=Entered_Passcode)

        def Key_0_Press():
            global Entered_Passcode
            if len(Entered_Passcode) <= 9:
                Entered_Passcode += self.Key_0.cget("text")
                self.Passcode.configure(text=Entered_Passcode)

        def Key_d_Press():
            global Entered_Passcode
            Entered_Passcode = Entered_Passcode[:-1]
            Key_Press()
            self.Passcode.configure(text=Entered_Passcode)

        def Key_c_Press():
            global Entered_Passcode
            Entered_Passcode = ""
            Key_Press()
            self.Passcode.configure(text=Entered_Passcode)

        def Key_E_Press():
            global Entered_Passcode, User_Attempt, BackgroundColor, Current_UserCode

            def Entered_Correct():
                global Entered_Passcode, User_Attempt, BackgroundColor
                User_Attempt = 0
                Entered_Passcode = ""
                Key_Press()
                self.Main.configure(state="disabled")
                self.Buy.configure(state="disabled")
                self.Print.configure(state="disabled")
                self.Setting.configure(state="disabled")
                self.Disable_Keys()
                self.Login_State.configure(font=("Arial", 60, "bold"), text_color=BackgroundColor)
                self.UI.after(1000, lambda: self.User_Attempt1.configure(fg_color="green"))
                self.UI.after(2000, lambda: self.User_Attempt2.configure(fg_color="green"))
                self.UI.after(3000, lambda: self.User_Attempt3.configure(fg_color="green"))
                self.UI.after(4000, lambda: self.User_Login_Message.configure(text="     Welcome"))
                self.UI.after(4000, lambda: self.Login_State.configure(text_color=WidgetColor))

            def Entered_Incorrect():
                global Entered_Passcode, User_Attempt, BackgroundColor
                User_Attempt += 1
                if User_Attempt >= 1:
                    self.User_Attempt1.configure(fg_color="red")
                    if User_Attempt >= 2:
                        self.User_Attempt2.configure(fg_color="red")
                        if User_Attempt == 3:
                            self.User_Attempt3.configure(fg_color="red")
                            self.Login_State.destroy()
                            self.Disable_Keys()
                            self.Login_State = self.Label("LOCKED", 430, 30, master=self.User_State_Frame)
                            self.Login_State.configure(font=("Arial", 60, "bold"))
                            Countdown()
                Entered_Passcode = ""
                Key_Press()

            if len(Entered_Passcode) != 0:
                User_ID_Dectected = 0
                # self.UI.after(1000, self.User_Request_Help)  # DELETE THIS
                for i in range(0, len(self.User_ID)):
                    if Entered_Passcode == self.User_ID[i]:
                        User_ID_Dectected = 1
                if User_ID_Dectected == 1:
                    self.Login_State.destroy()
                    self.Login_State = self.Label("USER ID DETECTED", 240, 30, master=self.User_State_Frame)
                    Current_UserCode = Entered_Passcode
                    Entered_Correct()
                    self.UI.after(5500, self.User_Request_Help)
                else:
                    Entered_Incorrect()

        def Key_Press():
            global Entered_Passcode
            Entered_User_ID = ""
            self.Passcode.configure(text=Entered_User_ID)

        self.User_Keypad_Frame = self.Frame(535, 350, 950, 465, master=self.Background)
        self.User_Keypad_Frame.configure(border_width=10, border_color=WidgetColor, corner_radius=20)
        self.Key_1 = self.Button2("1", 35, 37, Key_1_Press, master=self.User_Keypad_Frame)
        self.Key_1.configure(width=75, height=75, anchor="c", font=("Arial", 40, "bold"))
        self.Key_4 = self.Button2("4", 35, 137, Key_4_Press, master=self.User_Keypad_Frame)
        self.Key_4.configure(width=75, height=75, anchor="c", font=("Arial", 40, "bold"))
        self.Key_7 = self.Button2("7", 35, 237, Key_7_Press, master=self.User_Keypad_Frame)
        self.Key_7.configure(width=75, height=75, anchor="c", font=("Arial", 40, "bold"))
        self.Key_2 = self.Button2("2", 135, 37, Key_2_Press, master=self.User_Keypad_Frame)
        self.Key_2.configure(width=75, height=75, anchor="c", font=("Arial", 40, "bold"))
        self.Key_5 = self.Button2("5", 135, 137, Key_5_Press, master=self.User_Keypad_Frame)
        self.Key_5.configure(width=75, height=75, anchor="c", font=("Arial", 40, "bold"))
        self.Key_8 = self.Button2("8", 135, 237, Key_8_Press, master=self.User_Keypad_Frame)
        self.Key_8.configure(width=75, height=75, anchor="c", font=("Arial", 40, "bold"))
        self.Key_3 = self.Button2("3", 235, 37, Key_3_Press, master=self.User_Keypad_Frame)
        self.Key_3.configure(width=75, height=75, anchor="c", font=("Arial", 40, "bold"))
        self.Key_6 = self.Button2("6", 235, 137, Key_6_Press, master=self.User_Keypad_Frame)
        self.Key_6.configure(width=75, height=75, anchor="c", font=("Arial", 40, "bold"))
        self.Key_9 = self.Button2("9", 235, 237, Key_9_Press, master=self.User_Keypad_Frame)
        self.Key_9.configure(width=75, height=75, anchor="c", font=("Arial", 40, "bold"))
        self.Key_Delete = self.Button2("←", 335, 37, Key_d_Press, master=self.User_Keypad_Frame)
        self.Key_Delete.configure(width=75, height=75, anchor="c", font=("Arial", 40, "bold"))
        self.Key_Clear = self.Button2("c", 335, 137, Key_c_Press, master=self.User_Keypad_Frame)
        self.Key_Clear.configure(width=75, height=75, anchor="c", font=("Arial", 40, "bold"))
        self.Key_0 = self.Button2("0", 335, 237, Key_0_Press, master=self.User_Keypad_Frame)
        self.Key_0.configure(width=75, height=75, anchor="c", font=("Arial", 40, "bold"))
        self.Key_Enter = self.Button2("E", 435, 37, Key_E_Press, master=self.User_Keypad_Frame)
        self.Key_Enter.configure(width=65, height=275, anchor="c", font=("Arial", 40, "bold"))
        if User_Attempt == 3:
            self.Disable_Keys()

    def Service_State(self):
        global Booklet_State, Paper_State, Available_Booklets, Available_Papers, Available_Coins
        if Booklet_State == 1 and Available_Booklets != 0 and Available_Coins != 0:
            self.Buy.configure(state="normal")
        else:
            Booklet_State = 0
            self.Buy.configure(state="disabled")
        if Paper_State == 1 and Available_Papers != 0 and Available_Coins != 0:
            self.Print.configure(state="normal")
        else:
            Paper_State = 0
            self.Print.configure(state="disabled")

    def Disable_Keys(self):
        self.Key_1.configure(state="disabled")
        self.Key_2.configure(state="disabled")
        self.Key_3.configure(state="disabled")
        self.Key_4.configure(state="disabled")
        self.Key_5.configure(state="disabled")
        self.Key_6.configure(state="disabled")
        self.Key_7.configure(state="disabled")
        self.Key_8.configure(state="disabled")
        self.Key_9.configure(state="disabled")
        self.Key_0.configure(state="disabled")
        self.Key_Delete.configure(state="disabled")
        self.Key_Clear.configure(state="disabled")
        self.Key_Enter.configure(state="disabled")

    def Enable_Keys(self):
        self.Key_1.configure(state="enable")
        self.Key_2.configure(state="enable")
        self.Key_3.configure(state="enable")
        self.Key_4.configure(state="enable")
        self.Key_5.configure(state="enable")
        self.Key_6.configure(state="enable")
        self.Key_7.configure(state="enable")
        self.Key_8.configure(state="enable")
        self.Key_9.configure(state="enable")
        self.Key_0.configure(state="enable")
        self.Key_Delete.configure(state="enable")
        self.Key_Clear.configure(state="enable")
        self.Key_Enter.configure(state="enable")

    def Delete(self):
        for widget in self.RightMain.winfo_children():
            widget.destroy()


    def Frame(self, width, height, x, y, master=None):
        global BackgroundColor
        if master is None:
            master = self.UI
        Frame = customtkinter.CTkFrame(master=master,
                                       fg_color=BackgroundColor,
                                       width=width,
                                       height=height)
        Frame.place(x=x,y=y)
        return Frame

    def Button(self, text, x, y, icon, command, master=None, state="normal"):
        global WidgetColor
        if master is None:
            master = self.UI
        Icon_Path = os.path.join(os.path.dirname(__file__), icon)
        Button_Icon = Image.open(Icon_Path)
        Button = customtkinter.CTkButton(master=master,
                                         text=text,
                                         font=("Arial", 40),
                                         width=250,
                                         corner_radius=32,
                                         text_color="black",
                                         fg_color=WidgetColor,
                                         hover_color="snow",
                                         image=customtkinter.CTkImage(dark_image=Button_Icon,size=(45, 45)),
                                         command=command,
                                         anchor="w",
                                         state=state)
        Button.place(x=x, y=y)
        return Button

    def Button2(self, text, x, y, command, master=None, state="normal"):
        global WidgetColor
        if master is None:
            master = self.UI
        Button = customtkinter.CTkButton(master=master,
                                         text=text,
                                         font=("Arial", 40),
                                         width=250,
                                         corner_radius=32,
                                         text_color="black",
                                         fg_color=WidgetColor,
                                         hover_color="snow",
                                         command=command,
                                         anchor="w",
                                         state=state)
        Button.place(x=x, y=y)
        return Button

    def Label(self, text, x, y, master=None):
        global BackgroundColor, WidgetColor
        if master is None:
            master = self.UI
        Label = customtkinter.CTkLabel(master=master,
                                       text=text,
                                       font=("Arial", 60),
                                       fg_color=BackgroundColor,
                                       text_color=WidgetColor)
        Label.place(x=x,y=y)
        return Label

    def Image(self, path, width, height, x, y, master=None):
        global BackgroundColor
        if master is None:
            master = self.UI
        Icon_Path = os.path.join(os.path.dirname(__file__), path)
        Button_Icon = Image.open(Icon_Path)
        Graphics = customtkinter.CTkButton(master=master,
                                           text="",
                                           corner_radius=32,
                                           fg_color=BackgroundColor,
                                           image=customtkinter.CTkImage(dark_image=Button_Icon, size=(width, height)),
                                           state="disabled")
        Graphics.place(x=x, y=y)
        return Graphics

    def Combobox(self, values, x, y, state=None, master=None, command=None):
        global BackgroundColor, WidgetColor
        if master is None:
            master = self.UI
        if command is None:
            command = None
        if state is None:
            state = "readonly"
        Combobox = customtkinter.CTkComboBox(master=master,
                                             font=("Arial", 40),
                                             values=values,
                                             fg_color=WidgetColor,
                                             dropdown_hover_color=WidgetColor,
                                             text_color="black",
                                             state=state,
                                             justify="center",
                                             dropdown_fg_color=["gray", "gray"],
                                             border_color=BackgroundColor,
                                             command=command)
        Combobox.place(x=x, y=y)
        return Combobox

    def Switch(self, text, width, height, x, y, pg, fg, master=None, command=None, state=None):
        global BackgroundColor, WidgetColor
        if master is None:
            master = self.UI
        if state is None:
            state = "normal"
        if command is None:
            command = None
        switch = customtkinter.CTkSwitch(master=master,
                                         text=text,
                                         command=command,
                                         state=state,
                                         onvalue="On",
                                         offvalue="Off",
                                         font=("Arial", 40),
                                         fg_color=fg,
                                         border_color=BackgroundColor,
                                         button_color="snow",
                                         switch_width=width,
                                         switch_height=height,
                                         button_hover_color="snow",
                                         progress_color=pg,
                                         text_color=WidgetColor)
        switch.place(x=x,y=y)
        return switch

    def Slider(self, min, max, steps, width, height, x, y, command = None, master=None, state=None, orientation=None):
        global WidgetColor
        if master is None:
            master = self.UI
        if state is None:
            state = "normal"
        if command is None:
            command = None
        if orientation is None:
            orientation = "horizontal"
        slider = customtkinter.CTkSlider(master=master,
                                         from_=min,
                                         to=max,
                                         number_of_steps=steps,
                                         button_hover_color="snow",
                                         button_color="snow",
                                         progress_color=WidgetColor,
                                         width=width,
                                         height=height,
                                         orientation=orientation,
                                         state=state,
                                         command=command)
        slider.place(x=x, y=y)
        return slider

    def Progress_Bar(self, width, height, x, y, master=None, orientation=None):
        if master is None:
            master = self.UI
        if orientation is None:
            orientation = "horizontal"
        Progress_Bar = customtkinter.CTkProgressBar(master=master,
                                                     width=width,
                                                     height=height,
                                                     progress_color="green",
                                                     border_color=WidgetColor,
                                                     border_width=5,
                                                     orientation=orientation)
        Progress_Bar.place(x=x, y=y)
        return Progress_Bar

    def run(self):
        self.UI.mainloop()

if __name__ == "__main__":
    app = Vending_Machine()
    app.run()

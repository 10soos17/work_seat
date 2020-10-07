#import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager, WipeTransition
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.button import ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.uix.scatter import Scatter
from kivy.graphics import *
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.progressbar import ProgressBar
from kivy.uix.slider import Slider
import urllib.request
import threading
import os
import sys
import time
import random
import threading
from multiprocessing import Process, Queue
from multiprocessing.pool import ThreadPool
#import multiprocessing
#from queue import Queue
import subprocess
import signal

import fourth_seat as fs
import fourth_circle as circle

#kivy.require("1.19.1")

winColor = [0, 0, 0, 1]
boxColor = [1, 1.1, 1.3, 1]
textColor = [1, 1, 1, 1]

class Root(BoxLayout):
    def __init__(self, **kwargs):
        super(Root, self).__init__(**kwargs)
        winWidth = 640
        winHeight = 480
        self.orientation = "vertical"
        #self.pos_hint: {"x": .3, "top": .9}
        self.size = (winWidth,winHeight)

class ImageButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(ImageButton, self).__init__(**kwargs)

class UpperMenu(StackLayout):
    def __init__(self, **kwargs):
        super(UpperMenu, self).__init__(**kwargs)
        self.stackLayout = StackLayout(padding=10,spacing=10)
        self.seatDrop = DropDown()
        btnText=["Main","Seat", "Exit"]
        btnDic={}
        seatBtnText = ["Random","Class1","Class2","Class3","Class4", "Class5"]
        seatBtnDic = {}

        toMain=Fourth_mine_kv2()

        self.img_btn = ImageButton(source='fourth_mine_imgs/nothing.png')
        self.img_btn.size_hint = (0.14, 0.9)
        self.img_btn.bind(on_press=self.ready_widget,on_release=toMain.show_screen_main)

        self.stackLayout.add_widget(self.img_btn)

        for i in range(len(btnText)):
            btn = Button(text=btnText[i], width=40, height=30, size_hint=(0.14, 0.9), background_color=boxColor,color=textColor)
            btnDic[btnText[i]]=btn
            if btnText[i] == "Main":
                btn.bind(on_press=self.ready_widget,on_release=toMain.show_screen_main)
            if btnText[i] == "Seat":
                for j in range(len(seatBtnText)):
                    seatDropBtn = Button(text=seatBtnText[j], height=40, size_hint_y=None, background_color=boxColor,color=textColor)
                    seatBtnDic[seatBtnText[j]] = seatDropBtn
                    seatDropBtn.bind(on_release=lambda instance: self.seatDrop.select(seatDropBtn.text))
                    self.seatDrop.add_widget(seatDropBtn)

                    if seatBtnText[j] == "Random":
                        seatDropBtn.bind(on_press=self.ready_widget,on_release=self.seatPop)
                    if seatBtnText[j] == "Class1":
                        seatDropBtn.bind(on_press=self.ready_widget,on_release=toMain.show_screen_one)
                    if seatBtnText[j] == "Class2":
                        seatDropBtn.bind(on_press=self.ready_widget,on_release=toMain.show_screen_two)
                    if seatBtnText[j] == "Class3":
                        seatDropBtn.bind(on_press=self.ready_widget,on_release=toMain.show_screen_three)
                    if seatBtnText[j] == "Class4":
                        seatDropBtn.bind(on_press=self.ready_widget,on_release=toMain.show_screen_four)
                    if seatBtnText[j] == "Class5":
                        seatDropBtn.bind(on_press=self.ready_widget,on_release=toMain.show_screen_five)
                btn.bind(on_release=self.seatDrop.open)
                self.seatDrop.bind(on_select=lambda instance, x: setattr(seatDropBtn, 'text', x))

            if btnText[i] == "Exit":
                btn.bind(on_press=self.ready_widget, on_release=self.closeAll)

            self.stackLayout.add_widget(btn)
        self.add_widget(self.stackLayout)

    def closeAll(self,obj):
        #Fourth_mine_kv2().stop()
        #App().get_running_app().stop()
        Fourth_mine_kv2().get_running_app().stop()

    def ready_widget(self,obj):
        print("ready")

    def seatPop(self, obj):
        self.seatPopup = Popup(title='',
              size_hint=(0.4, 0.4), size=(400, 400), auto_dismiss=True,
              title_font='Roboto',title_size=20, title_align='center',
              title_color=textColor,
              separator_height=0.5,
              separator_color=textColor)

        self.lowerContent = StackLayout(orientation="lr-tb",padding=10,spacing=10)
        self.seatTextLine=Label(text = 'Write class, seat limit, name.',width=40, height=30,size_hint=(1, 0.2),color=textColor)
        self.lowerContent.add_widget(self.seatTextLine)

        self.lowerContent.add_widget(Label(text='class?',width=40, height=30,size_hint=(0.5, 0.16),color=textColor))
        self.classNum = TextInput(multiline = False,width=40, height=30,size_hint=(0.5, 0.16))
        self.lowerContent.add_widget(self.classNum)

        self.lowerContent.add_widget(Label(text='seat limit?',width=40, height=30,size_hint=(0.5, 0.16),color=textColor))
        self.seatLimit = TextInput(multiline = False,width=40, height=30,size_hint=(0.5, 0.16))
        self.lowerContent.add_widget(self.seatLimit)

        self.lowerContent.add_widget(Label(text = 'name?',width=40, height=30,size_hint=(0.5, 0.16),color=textColor))
        self.name = TextInput(multiline = False,width=40, height=30,size_hint=(0.5, 0.16))
        self.lowerContent.add_widget(self.name)

        self.seatSubmit = Button(text="Submit",width=40, height=30,size_hint=(0.5, 0.16),background_color=boxColor,color=textColor)
        self.seatSubmit.bind(on_press = self.seat_pressed) #bind 콜벡함수연결함수
        self.lowerContent.add_widget(self.seatSubmit)

        self.seatDelete = Button(text="Delete",width=40, height=30,size_hint=(0.5, 0.16),background_color=boxColor,color=textColor)
        self.seatDelete.bind(on_press = self.delete_pressed) #bind 콜벡함수연결함수
        self.lowerContent.add_widget(self.seatDelete)

        self.seatPopup.add_widget(self.lowerContent)

        self.seatPopup.open()

    def seat_pressed(self,instance):
        print("class:", self.classNum.text,"name:", "seatLimit:", self.seatLimit.text, self.name.text)
        self.seatPopup.dismiss()
        try:
            if type(int(self.seatLimit.text)) == int:
                res = fs.randomSelectSeat(int(self.classNum.text), self.name.text, int(self.seatLimit.text))
                classNum = int(self.classNum.text)
                if res == False:
                    print("retry")
                else:
                    if classNum == 1:
                        class1_btnDic[str(res[0])].text = f"{res[0]}: {res[1]}"
                        class1_btnDic[str(res[0])].background_color = [255,255,255,1]
                        class1_btnDic[str(res[0])].color = [0,0,0,1]
                    elif classNum == 2:
                        class2_btnDic[str(res[0])].text = f"{res[0]}: {res[1]}"
                        class2_btnDic[str(res[0])].background_color = [255,255,255,1]
                        class2_btnDic[str(res[0])].color = [0,0,0,1]
                    elif classNum == 3:
                        class3_btnDic[str(res[0])].text = f"{res[0]}: {res[1]}"
                        class3_btnDic[str(res[0])].background_color = [255,255,255,1]
                        class3_btnDic[str(res[0])].color = [0,0,0,1]
                    elif classNum == 4:
                        class4_btnDic[str(res[0])].text = f"{res[0]}: {res[1]}"
                        class4_btnDic[str(res[0])].background_color = [255,255,255,1]
                        class4_btnDic[str(res[0])].color = [0,0,0,1]
                    manager.current = f"Class{classNum}"
                    #Fourth_mine_kv2().show_class(self,classNum)
        except Exception as msg:
                self.seatPopup.title = f"{msg}retry."
                #self.seatTextLine.text = f"{msg}retry."
                #self.seatTextLine.texture_update()

        self.name.text = ""
        self.seatLimit.text = ""
        self.classNum.text = ""

    def delete_pressed(self,obj):
            print("class:", self.classNum.text,"name:", self.name.text)
            #self.seatPopup.dismiss()
            try:
                res = fs.randomDeleteSeat(int(self.classNum.text), self.name.text)
                classNum = int(self.classNum.text)

                manager.current = f"Class{classNum}"
                #Fourth_mine_kv2().show_class(self,classNum)
                if res == False:
                    print("There is no name. Do check.")

            except Exception as msg:
                    self.seatPopup.title = f"{msg}retry."
                    #self.seatTextLine.text = f"{msg}retry."
                    #self.seatTextLine.texture_update()

            self.name.text = ""
            self.seatLimit.text = ""
            self.classNum.text = ""

class ScreenMain(Screen):
    def __init__(self, **kwargs):
        super(ScreenMain, self).__init__(**kwargs)
        #self.name = "screen_main"
        self.mainScreen = GridLayout(rows=5,row_force_default=True,row_default_height=180,
                                        padding=[0,0,0,0],spacing=[0,0])
        #self.scatter = Scatter(do_rotation=True, do_scale=True,
    #              do_translation_y=True)
    #    self.mainScreen.add_widget(self.scatter)

        self.emptyLabel = Label(size_hint=(0.14, 0.1),color=[0,0,0,0])
        self.timeLabel = Label(font_size = '78sp',font_name="Times New Roman Bold",
                                halign='center',valign="bottom",bold=False,italic=False,
                                size_hint=(0.14, 0.15),pos_hint=(0.5,0.3),color=textColor)
        #self.scatter.add_widget(self.timeLabel)
        self.emptySecLabel = Label(size_hint=(0.14, 0.2),color=[0,0,0,0])

        self.mainScreen.add_widget(self.emptyLabel)
        self.mainScreen.add_widget(self.timeLabel)
        self.mainScreen.add_widget(self.emptySecLabel)
        #==============
        self.add_widget(self.mainScreen)
        Clock.schedule_interval(self.timeAdd, 0.5)

    def timeAdd(self,obj):
        timeText=circle.current_time()
        self.timeLabel.text = timeText
        self.timeLabel.texture_update()

class ScreenOne(Screen):
    def __init__(self, **kwargs):
        super(ScreenOne, self).__init__(**kwargs)
        global class1_btnDic
        #self.name = "Class1"
        self.layout1 = StackLayout(orientation="bt-lr",padding=10,spacing=5)
        #self.layout1 = GridLayout(rows=13,cols=6,padding=10,spacing=10)
        class1_btnDic={}
        btnCount=0
        beforeNum = {3:1,4:2,5:3,6:4,7:5,8:6,9:7,
                10:8,11:9,12:"x",24:10,36:11,48:12,60:13,
                72:"x",71:14,70:15,69:16,68:17,67:18,66:19,65:20,64:21,63:22,62:23,61:24}
        for i in range(1,73):
            if 3 <= i <= 12 or 61 <= i <= 72 or i in [24,36,48,60]:
                btnCount+=1
                #font_name="Times New Roman","Verdana"
                self.class1_btn = Button(text=str(beforeNum[i]),font_size=18,font_name="Arial",bold=True,
                                    size_hint=(0.1, 0.08),halign="justify",valign="middle",
                                    background_color=boxColor,color=textColor)
                class1_btnDic[str(beforeNum[i])]=self.class1_btn
                if beforeNum[i] != "x":
                    class1_btnDic[str(beforeNum[i])].bind(on_press = self.seatBtn_pop)
            else:
                self.class1_btn = Button(text=str(i),width=40, height=30, size_hint=(0.1, 0.08),
                                    background_color=[0,0,0,0],color=[0,0,0,0])

            self.layout1.add_widget(self.class1_btn)

        self.layout1.add_widget(Label(text='Class1',font_size=50,
                                    halign="right",valign="bottom",bold=True,
                                    size_hint=(0.5, 0.3),color=textColor))

        self.add_widget(self.layout1)
        self.showSeat()

    def seatBtn_pop(self,seatNum):
        print(type(self),type(seatNum))
        for keys in class1_btnDic:
            if class1_btnDic[keys] == seatNum:
                self.seatNum = keys
        self.seatBtnPopup = Popup(title='',
              size_hint=(0.3, 0.4), size=(200, 200), auto_dismiss=True,
              title_font='Roboto',title_size=20, title_align='center',
              title_color=textColor,
              separator_height=0.5,
              separator_color=textColor)

        self.seatBtn_layout = StackLayout(orientation="lr-tb",padding=10,spacing=10)
        self.textLine=Label(text = 'Choose.',width=40, height=30,size_hint=(1, 0.2),color=textColor)
        self.seatBtn_layout.add_widget(self.textLine)

        self.save_submit = Button(text="1. Save",width=40, height=30,size_hint=(1, 0.2),background_color=boxColor,color=textColor)
        #self.save_submit.bind(on_press=lambda x: self.seatBtn_save_popup(seatNum)) #bind 콜벡함수연결함수
        self.save_submit.bind(on_press=self.seatBtn_save_pop)
        self.seatBtn_layout.add_widget(self.save_submit)

        self.delete_submit = Button(text="2. Delete",width=40, height=30,size_hint=(1, 0.2),background_color=boxColor,color=textColor)
        self.delete_submit.bind(on_press = self.seatBtn_delete) #bind 콜벡함수연결함수
        self.seatBtn_layout.add_widget(self.delete_submit)

        self.close_submit = Button(text="3. Close",width=40, height=30,size_hint=(1, 0.2),background_color=boxColor,color=textColor)
        self.close_submit.bind(on_press = self.seatBtnPopup.dismiss) #bind 콜벡함수연결함수
        self.seatBtn_layout.add_widget(self.close_submit)

        self.seatBtnPopup.add_widget(self.seatBtn_layout)

        self.seatBtnPopup.open()

    def seatBtn_save_pop(self,obj):
        self.seatBtn_save_popup = Popup(title='',
              size_hint=(0.3, 0.2), size=(400, 400), auto_dismiss=True,
              title_font='Roboto',title_size=20, title_align='center',
              title_color=textColor,
              separator_height=0.5,
              separator_color=textColor)

        self.seatBtn_save_layout = StackLayout(orientation="lr-tb",padding=10,spacing=10)

        self.seatBtn_save_layout.add_widget(Label(text = 'Name?', size_hint=(0.3, 0.5),color=textColor))
        self.seatBtn_save_name = TextInput(multiline = False,size_hint=(0.7, 0.5))
        self.seatBtn_save_layout.add_widget(self.seatBtn_save_name)

        self.save_name_submit = Button(text="Submit",size_hint=(0.5, 0.5),background_color=boxColor,color=textColor)
        self.save_name_submit.bind(on_press = self.seatBtn_save) #bind 콜벡함수연결함수
        self.seatBtn_save_layout.add_widget(self.save_name_submit)

        self.save_close_submit = Button(text="Close",size_hint=(0.5, 0.5),background_color=boxColor,color=textColor)
        self.save_close_submit.bind(on_press = self.seatBtn_save_popup.dismiss) #bind 콜벡함수연결함수
        self.seatBtn_save_layout.add_widget(self.save_close_submit)

        self.seatBtn_save_popup.add_widget(self.seatBtn_save_layout)

        self.seatBtn_save_popup.open()

    def seatBtn_save(self,obj):
        proc = os.getpid()
        print("seatBtn_save: ", proc,self,obj)

        self.seatBtnPopup.dismiss()
        self.seatBtn_save_popup.dismiss()

        res = fs.selectSeat("1",str(self.seatNum),self.seatBtn_save_name.text)
        if res == False:
            ("retry")
        else:
            class1_btnDic[str(self.seatNum)].text = f"{str(self.seatNum)}: {self.seatBtn_save_name.text}"
            class1_btnDic[str(self.seatNum)].background_color = [255,255,255,1]
            class1_btnDic[str(self.seatNum)].color = [0,0,0,1]

        #threading.Timer(1.5, self.showSeat).start()
        #self.showSeat()
    def seatBtn_delete(self,obj):
        proc = os.getpid()
        print("seatBtn_delete: ", proc)

        if class1_btnDic[str(self.seatNum)].background_color == boxColor:
            self.seatBtnPopup.title = "empty seat."
        else:
            fs.deleteSeat("1",str(self.seatNum))
            class1_btnDic[str(self.seatNum)].text = str(self.seatNum)
            class1_btnDic[str(self.seatNum)].background_color = boxColor
            class1_btnDic[str(self.seatNum)].color = textColor

            self.seatBtnPopup.dismiss()

    def showSeat(self):
        print("class1 showSeat",self)
        res=fs.readSeat("1")

        if res == False:
            ("Empty")
        else:
            for i in range(len(res)):
                realNum = int(res[i][0])
                class1_btnDic[str(realNum)].text = f"{res[i][0]}: {res[i][1]}"
                class1_btnDic[str(realNum)].background_color = [255,255,255,1]
                class1_btnDic[str(realNum)].color = [0,0,0,1]
        #self.class1_btnDic["13\ndisorder"].background_color = [255,255,255,1]
        #self.class1_btnDic["13\ndisorder"].color = [0,0,0,1]

class ScreenTwo(Screen): #grid
    def __init__(self, **kwargs):
        super(ScreenTwo, self).__init__(**kwargs)
        global class2_btnDic
        #self.name = "Class2"
        #self.layout2 = StackLayout(orientation="bt-lr",padding=10,spacing=5)
        self.layout2 = GridLayout(rows=12,cols=7,padding=10,spacing=5)
        class2_btnDic={}
        btnCount=0
        beforeNum = {64:1,57:2,50:3,43:4,36:5,29:6,22:7,15:8,8:9,1:"x",
                        2:10,3:11,4:12,5:13,6:"x",13:14,20:15,
                        27:16,34:17,41:18,48:19,55:20,62:21,69:22,76:23,83:24}
        for i in range(1,84):
            if 1 <= i <= 6 or i in [64,57,50,43,36,29,22,15,8,13,20,27,34,41,48,55,62,69,76,83]:
                btnCount+=1
                #font_name="Times New Roman","Verdana"
                self.class2_btn = Button(text=str(beforeNum[i]),font_size=18,font_name="Arial",bold=True,
                                    size_hint=(0.1, 0.08),halign="justify",valign="middle",
                                    background_color=boxColor,color=textColor)
                class2_btnDic[str(beforeNum[i])]=self.class2_btn
                if beforeNum[i] != "x":
                    class2_btnDic[str(beforeNum[i])].bind(on_press = self.seatBtn_pop)
            else:
                self.class2_btn = Button(text=str(i),width=40, height=30, size_hint=(0.1, 0.08),
                                    background_color=[0,0,0,0],color=[0,0,0,0])

            self.layout2.add_widget(self.class2_btn)

        self.layout2.add_widget(Label(text='Class2',font_size=50,
                                    halign="right",valign="bottom",bold=True,
                                    size_hint=(0.5, 0.08),color=textColor))

        self.add_widget(self.layout2)
        self.showSeat()

    def seatBtn_pop(self,seatNum):
        print(type(self),type(seatNum))
        for keys in class2_btnDic:
            if class2_btnDic[keys] == seatNum:
                self.seatNum = keys
        self.seatBtnPopup = Popup(title='',
              size_hint=(0.3, 0.4), size=(200, 200), auto_dismiss=True,
              title_font='Roboto',title_size=20, title_align='center',
              title_color=textColor,
              separator_height=0.5,
              separator_color=textColor)

        self.seatBtn_layout = StackLayout(orientation="lr-tb",padding=10,spacing=10)
        self.textLine=Label(text = 'Choose.',width=40, height=30,size_hint=(1, 0.2),color=textColor)
        self.seatBtn_layout.add_widget(self.textLine)

        self.save_submit = Button(text="1. Save",width=40, height=30,size_hint=(1, 0.2),background_color=boxColor,color=textColor)
        #self.save_submit.bind(on_press=lambda x: self.seatBtn_save_popup(seatNum)) #bind 콜벡함수연결함수
        self.save_submit.bind(on_press=self.seatBtn_save_pop)
        self.seatBtn_layout.add_widget(self.save_submit)

        self.delete_submit = Button(text="2. Delete",width=40, height=30,size_hint=(1, 0.2),background_color=boxColor,color=textColor)
        self.delete_submit.bind(on_press = self.seatBtn_delete) #bind 콜벡함수연결함수
        self.seatBtn_layout.add_widget(self.delete_submit)

        self.close_submit = Button(text="3. Close",width=40, height=30,size_hint=(1, 0.2),background_color=boxColor,color=textColor)
        self.close_submit.bind(on_press = self.seatBtnPopup.dismiss) #bind 콜벡함수연결함수
        self.seatBtn_layout.add_widget(self.close_submit)

        self.seatBtnPopup.add_widget(self.seatBtn_layout)

        self.seatBtnPopup.open()

    def seatBtn_save_pop(self,obj):
        self.seatBtn_save_popup = Popup(title='',
              size_hint=(0.3, 0.2), size=(400, 400), auto_dismiss=True,
              title_font='Roboto',title_size=20, title_align='center',
              title_color=textColor,
              separator_height=0.5,
              separator_color=textColor)

        self.seatBtn_save_layout = StackLayout(orientation="lr-tb",padding=10,spacing=10)

        self.seatBtn_save_layout.add_widget(Label(text = 'Name?', size_hint=(0.3, 0.5),color=textColor))
        self.seatBtn_save_name = TextInput(multiline = False,size_hint=(0.7, 0.5))
        self.seatBtn_save_layout.add_widget(self.seatBtn_save_name)

        self.save_name_submit = Button(text="Submit",size_hint=(0.5, 0.5),background_color=boxColor,color=textColor)
        self.save_name_submit.bind(on_press = self.seatBtn_save) #bind 콜벡함수연결함수
        self.seatBtn_save_layout.add_widget(self.save_name_submit)

        self.save_close_submit = Button(text="Close",size_hint=(0.5, 0.5),background_color=boxColor,color=textColor)
        self.save_close_submit.bind(on_press = self.seatBtn_save_popup.dismiss) #bind 콜벡함수연결함수
        self.seatBtn_save_layout.add_widget(self.save_close_submit)

        self.seatBtn_save_popup.add_widget(self.seatBtn_save_layout)

        self.seatBtn_save_popup.open()

    def seatBtn_save(self,obj):
        proc = os.getpid()

        self.seatBtnPopup.dismiss()
        self.seatBtn_save_popup.dismiss()

        res = fs.selectSeat("2",str(self.seatNum),self.seatBtn_save_name.text)
        if res == False:
            ("retry")
        else:
            class2_btnDic[str(self.seatNum)].text = f"{str(self.seatNum)}: {self.seatBtn_save_name.text}"
            class2_btnDic[str(self.seatNum)].background_color = [255,255,255,1]
            class2_btnDic[str(self.seatNum)].color = [0,0,0,1]

        #threading.Timer(1.5, self.showSeat).start()
        #self.showSeat()
    def seatBtn_delete(self,obj):
        proc = os.getpid()
        print("seatBtn_delete: ", proc)

        if class2_btnDic[str(self.seatNum)].background_color == boxColor:
            self.seatBtnPopup.title = "empty seat."
        else:
            fs.deleteSeat("2",str(self.seatNum))
            class2_btnDic[str(self.seatNum)].text = str(self.seatNum)
            class2_btnDic[str(self.seatNum)].background_color = boxColor
            class2_btnDic[str(self.seatNum)].color = textColor

            self.seatBtnPopup.dismiss()

    def showSeat(self):
        print("class2 showSeat",self)
        res=fs.readSeat("2")

        if res == False:
            ("Empty")
        else:
            for i in range(len(res)):
                realNum = int(res[i][0])
                class2_btnDic[str(realNum)].text = f"{res[i][0]}: {res[i][1]}"
                class2_btnDic[str(realNum)].background_color = [255,255,255,1]
                class2_btnDic[str(realNum)].color = [0,0,0,1]
        #self.class2_btnDic["13\ndisorder"].background_color = [255,255,255,1]
        #self.class2_btnDic["13\ndisorder"].color = [0,0,0,1]
class ScreenThree(Screen):
    def __init__(self, **kwargs):
        super(ScreenThree, self).__init__(**kwargs)
        global class3_btnDic
        #self.name = "Class3"
        self.layout3 = StackLayout(orientation="bt-lr",padding=10,spacing=5)
        #self.layout1 = GridLayout(rows=13,cols=6,padding=10,spacing=10)
        class3_btnDic={}
        btnCount=0
        beforeNum = {3:1,4:2,5:3,6:4,7:5,8:6,9:7,
                10:8,11:9,12:"x",24:10,36:11,48:12,60:"13\ndisorder",
                72:"x",71:14,70:15,69:16,68:17,67:18,66:19,65:20,64:21,63:22,62:23,61:24}
        for i in range(1,73):
            if 3 <= i <= 12 or 61 <= i <= 72 or i in [24,36,48,60]:
                btnCount+=1
                #font_name="Times New Roman","Verdana"
                self.class3_btn = Button(text=str(beforeNum[i]),font_size=18,font_name="Arial",bold=True,
                                    size_hint=(0.1, 0.08),halign="justify",valign="middle",
                                    background_color=boxColor,color=textColor)
                class3_btnDic[str(beforeNum[i])]=self.class3_btn
                if beforeNum[i] != "x":
                    class3_btnDic[str(beforeNum[i])].bind(on_press = self.seatBtn_pop)
            else:
                self.class3_btn = Button(text=str(i),width=40, height=30, size_hint=(0.1, 0.08),
                                    background_color=[0,0,0,0],color=[0,0,0,0])

            self.layout3.add_widget(self.class3_btn)

        self.layout3.add_widget(Label(text='Class3',font_size=50,
                                    halign="right",valign="bottom",bold=True,
                                    size_hint=(0.5, 0.3),color=textColor))

        self.add_widget(self.layout3)
        self.showSeat()

    def seatBtn_pop(self,seatNum):
        print(type(self),type(seatNum))
        for keys in class3_btnDic:
            if class3_btnDic[keys] == seatNum:
                self.seatNum = keys
        self.seatBtnPopup = Popup(title='',
              size_hint=(0.3, 0.4), size=(200, 200), auto_dismiss=True,
              title_font='Roboto',title_size=20, title_align='center',
              title_color=textColor,
              separator_height=0.5,
              separator_color=textColor)

        self.seatBtn_layout = StackLayout(orientation="lr-tb",padding=10,spacing=10)
        self.textLine=Label(text = 'Choose.',width=40, height=30,size_hint=(1, 0.2),color=textColor)
        self.seatBtn_layout.add_widget(self.textLine)

        self.save_submit = Button(text="1. Save",width=40, height=30,size_hint=(1, 0.2),background_color=boxColor,color=textColor)
        #self.save_submit.bind(on_press=lambda x: self.seatBtn_save_popup(seatNum)) #bind 콜벡함수연결함수
        self.save_submit.bind(on_press=self.seatBtn_save_pop)
        self.seatBtn_layout.add_widget(self.save_submit)

        self.delete_submit = Button(text="2. Delete",width=40, height=30,size_hint=(1, 0.2),background_color=boxColor,color=textColor)
        self.delete_submit.bind(on_press = self.seatBtn_delete) #bind 콜벡함수연결함수
        self.seatBtn_layout.add_widget(self.delete_submit)

        self.close_submit = Button(text="3. Close",width=40, height=30,size_hint=(1, 0.2),background_color=boxColor,color=textColor)
        self.close_submit.bind(on_press = self.seatBtnPopup.dismiss) #bind 콜벡함수연결함수
        self.seatBtn_layout.add_widget(self.close_submit)

        self.seatBtnPopup.add_widget(self.seatBtn_layout)

        self.seatBtnPopup.open()

    def seatBtn_save_pop(self,obj):
        self.seatBtn_save_popup = Popup(title='',
              size_hint=(0.3, 0.2), size=(400, 400), auto_dismiss=True,
              title_font='Roboto',title_size=20, title_align='center',
              title_color=textColor,
              separator_height=0.5,
              separator_color=textColor)

        self.seatBtn_save_layout = StackLayout(orientation="lr-tb",padding=10,spacing=10)

        self.seatBtn_save_layout.add_widget(Label(text = 'Name?', size_hint=(0.3, 0.5),color=textColor))
        self.seatBtn_save_name = TextInput(multiline = False,size_hint=(0.7, 0.5))
        self.seatBtn_save_layout.add_widget(self.seatBtn_save_name)

        self.save_name_submit = Button(text="Submit",size_hint=(0.5, 0.5),background_color=boxColor,color=textColor)
        self.save_name_submit.bind(on_press = self.seatBtn_save) #bind 콜벡함수연결함수
        self.seatBtn_save_layout.add_widget(self.save_name_submit)

        self.save_close_submit = Button(text="Close",size_hint=(0.5, 0.5),background_color=boxColor,color=textColor)
        self.save_close_submit.bind(on_press = self.seatBtn_save_popup.dismiss) #bind 콜벡함수연결함수
        self.seatBtn_save_layout.add_widget(self.save_close_submit)

        self.seatBtn_save_popup.add_widget(self.seatBtn_save_layout)

        self.seatBtn_save_popup.open()

    def seatBtn_save(self,obj):
        proc = os.getpid()

        self.seatBtnPopup.dismiss()
        self.seatBtn_save_popup.dismiss()

        res = fs.selectSeat("3",str(self.seatNum),self.seatBtn_save_name.text)
        if res == False:
            ("retry")
        else:
            class3_btnDic[str(self.seatNum)].text = f"{str(self.seatNum)}: {self.seatBtn_save_name.text}"
            class3_btnDic[str(self.seatNum)].background_color = [255,255,255,1]
            class3_btnDic[str(self.seatNum)].color = [0,0,0,1]

        #threading.Timer(1.5, self.showSeat).start()
        #self.showSeat()
    def seatBtn_delete(self,obj):
        proc = os.getpid()
        print("seatBtn_delete: ", proc)

        if class3_btnDic[str(self.seatNum)].background_color == boxColor:
            self.seatBtnPopup.title = "empty seat."
        else:
            fs.deleteSeat("3",str(self.seatNum))
            class3_btnDic[str(self.seatNum)].text = str(self.seatNum)
            class3_btnDic[str(self.seatNum)].background_color = boxColor
            class3_btnDic[str(self.seatNum)].color = textColor
            self.seatBtnPopup.dismiss()

    def showSeat(self):
        print("class3 showSeat",self)
        res=fs.readSeat("3")

        if res == False:
            ("Empty")
        else:
            for i in range(len(res)):
                realNum = int(res[i][0])
                class3_btnDic[str(realNum)].text = f"{res[i][0]}: {res[i][1]}"
                class3_btnDic[str(realNum)].background_color = [255,255,255,1]
                class3_btnDic[str(realNum)].color = [0,0,0,1]
        #self.class3_btnDic["13\ndisorder"].background_color = [255,255,255,1]
        #self.class3_btnDic["13\ndisorder"].color = [0,0,0,1]
class ScreenFour(Screen):
    def __init__(self, **kwargs):
        super(ScreenFour, self).__init__(**kwargs)
        global class4_btnDic
        #self.name = "Class4"
        self.layout4 = StackLayout(orientation="bt-lr",padding=10,spacing=5)
        #self.layout4 = GridLayout(rows=13,cols=6,padding=10,spacing=5)
        class4_btnDic={}
        btnCount=0
        beforeNum = {3:1,4:2,5:3,6:4,7:5,8:6,9:7,
                10:8,11:9,12:"x",24:10,36:11,48:12,60:13,
                72:"x",71:14,70:15,69:16,68:17,67:18,66:19,65:20,64:21,63:22,62:23,61:24}
        for i in range(1,73):
            if 3 <= i <= 12 or 61 <= i <= 72 or i in [24,36,48,60]:
                btnCount+=1
                #font_name="Times New Roman","Verdana"
                self.class4_btn = Button(text=str(beforeNum[i]),font_size=18,font_name="Arial",bold=True,
                                    size_hint=(0.1, 0.08),halign="justify",valign="middle",
                                    background_color=boxColor,color=textColor)
                class4_btnDic[str(beforeNum[i])]=self.class4_btn
                if beforeNum[i] != "x":
                    class4_btnDic[str(beforeNum[i])].bind(on_press = self.seatBtn_pop)
            else:
                self.class4_btn = Button(text=str(i),width=40, height=30, size_hint=(0.1, 0.08),
                                    background_color=[0,0,0,0],color=[0,0,0,0])

            self.layout4.add_widget(self.class4_btn)

        self.layout4.add_widget(Label(text='Class4',font_size=50,
                                    halign="right",valign="bottom",bold=True,
                                    size_hint=(0.5, 0.3),color=textColor))

        self.add_widget(self.layout4)
        self.showSeat()

    def seatBtn_pop(self,seatNum):
        print(type(self),type(seatNum))
        for keys in class4_btnDic:
            if class4_btnDic[keys] == seatNum:
                self.seatNum = keys
        self.seatBtnPopup = Popup(title='',
              size_hint=(0.3, 0.4), size=(200, 200), auto_dismiss=True,
              title_font='Roboto',title_size=20, title_align='center',
              title_color=textColor,
              separator_height=0.5,
              separator_color=textColor)

        self.seatBtn_layout = StackLayout(orientation="lr-tb",padding=10,spacing=10)
        self.textLine=Label(text = 'Choose.',width=40, height=30,size_hint=(1, 0.2),color=textColor)
        self.seatBtn_layout.add_widget(self.textLine)

        self.save_submit = Button(text="1. Save",width=40, height=30,size_hint=(1, 0.2),background_color=boxColor,color=textColor)
        #self.save_submit.bind(on_press=lambda x: self.seatBtn_save_popup(seatNum)) #bind 콜벡함수연결함수
        self.save_submit.bind(on_press=self.seatBtn_save_pop)
        self.seatBtn_layout.add_widget(self.save_submit)

        self.delete_submit = Button(text="2. Delete",width=40, height=30,size_hint=(1, 0.2),background_color=boxColor,color=textColor)
        self.delete_submit.bind(on_press = self.seatBtn_delete) #bind 콜벡함수연결함수
        self.seatBtn_layout.add_widget(self.delete_submit)

        self.close_submit = Button(text="3. Close",width=40, height=30,size_hint=(1, 0.2),background_color=boxColor,color=textColor)
        self.close_submit.bind(on_press = self.seatBtnPopup.dismiss) #bind 콜벡함수연결함수
        self.seatBtn_layout.add_widget(self.close_submit)

        self.seatBtnPopup.add_widget(self.seatBtn_layout)

        self.seatBtnPopup.open()

    def seatBtn_save_pop(self,obj):
        self.seatBtn_save_popup = Popup(title='',
              size_hint=(0.3, 0.2), size=(400, 400), auto_dismiss=True,
              title_font='Roboto',title_size=20, title_align='center',
              title_color=textColor,
              separator_height=0.5,
              separator_color=textColor)

        self.seatBtn_save_layout = StackLayout(orientation="lr-tb",padding=10,spacing=10)

        self.seatBtn_save_layout.add_widget(Label(text = 'Name?', size_hint=(0.3, 0.5),color=textColor))
        self.seatBtn_save_name = TextInput(multiline = False,size_hint=(0.7, 0.5))
        self.seatBtn_save_layout.add_widget(self.seatBtn_save_name)

        self.save_name_submit = Button(text="Submit",size_hint=(0.5, 0.5),background_color=boxColor,color=textColor)
        self.save_name_submit.bind(on_press = self.seatBtn_save) #bind 콜벡함수연결함수
        self.seatBtn_save_layout.add_widget(self.save_name_submit)

        self.save_close_submit = Button(text="Close",size_hint=(0.5, 0.5),background_color=boxColor,color=textColor)
        self.save_close_submit.bind(on_press = self.seatBtn_save_popup.dismiss) #bind 콜벡함수연결함수
        self.seatBtn_save_layout.add_widget(self.save_close_submit)

        self.seatBtn_save_popup.add_widget(self.seatBtn_save_layout)

        self.seatBtn_save_popup.open()

    def seatBtn_save(self,obj):
        proc = os.getpid()

        self.seatBtnPopup.dismiss()
        self.seatBtn_save_popup.dismiss()

        res = fs.selectSeat("4",str(self.seatNum),self.seatBtn_save_name.text)
        if res == False:
            ("retry")
        else:
            class4_btnDic[str(self.seatNum)].text = f"{str(self.seatNum)}: {self.seatBtn_save_name.text}"
            class4_btnDic[str(self.seatNum)].background_color = [255,255,255,1]
            class4_btnDic[str(self.seatNum)].color = [0,0,0,1]

        #threading.Timer(1.5, self.showSeat).start()
        #self.showSeat()
    def seatBtn_delete(self,obj):
        proc = os.getpid()
        print("seatBtn_delete: ", proc)

        if class4_btnDic[str(self.seatNum)].background_color == boxColor:
            self.seatBtnPopup.title = "empty seat."
        else:
            fs.deleteSeat("4",str(self.seatNum))
            class4_btnDic[str(self.seatNum)].text = str(self.seatNum)
            class4_btnDic[str(self.seatNum)].background_color = boxColor
            class4_btnDic[str(self.seatNum)].color = textColor
            self.seatBtnPopup.dismiss()

    def showSeat(self):
        print("class4 showSeat",self)
        res=fs.readSeat("4")

        if res == False:
            ("Empty")
        else:
            for i in range(len(res)):
                realNum = int(res[i][0])
                class4_btnDic[str(realNum)].text = f"{res[i][0]}: {res[i][1]}"
                class4_btnDic[str(realNum)].background_color = [255,255,255,1]
                class4_btnDic[str(realNum)].color = [0,0,0,1]
        #self.class4_btnDic["13\ndisorder"].background_color = [255,255,255,1]
        #self.class4_btnDic["13\ndisorder"].color = [0,0,0,1]
class ScreenFive(Screen):
    def __init__(self, **kwargs):
        super(ScreenFive, self).__init__(**kwargs)
        global class5_btnDic
        #self.name = "Class4"
        self.layout5 = StackLayout(orientation="bt-lr",padding=10,spacing=5)
        #self.layout4 = GridLayout(rows=13,cols=6,padding=10,spacing=5)
        class5_btnDic={}
        btnCount=0
        beforeNum = {3:1,4:2,5:3,6:4,7:5,8:6,9:7,
                10:8,11:9,12:"x",24:10,36:11,48:12,60:13,
                72:"x",71:14,70:15,69:16,68:17,67:18,66:19,65:20,64:21,63:22,62:23,61:24}
        for i in range(1,73):
            if 3 <= i <= 12 or 61 <= i <= 72 or i in [24,36,48,60]:
                btnCount+=1
                #font_name="Times New Roman","Verdana"
                self.class5_btn = Button(text=str(beforeNum[i]),font_size=18,font_name="Arial",bold=True,
                                    size_hint=(0.1, 0.08),halign="justify",valign="middle",
                                    background_color=boxColor,color=textColor)
                class5_btnDic[str(beforeNum[i])]=self.class5_btn
                if beforeNum[i] != "x":
                    class5_btnDic[str(beforeNum[i])].bind(on_press = self.seatBtn_pop)
            else:
                self.class5_btn = Button(text=str(i),width=40, height=30, size_hint=(0.1, 0.08),
                                    background_color=[0,0,0,0],color=[0,0,0,0])

            self.layout5.add_widget(self.class5_btn)

        self.layout5.add_widget(Label(text='Class5',font_size=50,
                                    halign="right",valign="bottom",bold=True,
                                    size_hint=(0.5, 0.3),color=textColor))

        self.add_widget(self.layout5)
        self.showSeat()

    def seatBtn_pop(self,seatNum):
        print(type(self),type(seatNum))
        for keys in class5_btnDic:
            if class5_btnDic[keys] == seatNum:
                self.seatNum = keys
        self.seatBtnPopup = Popup(title='',
              size_hint=(0.3, 0.4), size=(200, 200), auto_dismiss=True,
              title_font='Roboto',title_size=20, title_align='center',
              title_color=textColor,
              separator_height=0.5,
              separator_color=textColor)

        self.seatBtn_layout = StackLayout(orientation="lr-tb",padding=10,spacing=10)
        self.textLine=Label(text = 'Choose.',width=40, height=30,size_hint=(1, 0.2),color=textColor)
        self.seatBtn_layout.add_widget(self.textLine)

        self.save_submit = Button(text="1. Save",width=40, height=30,size_hint=(1, 0.2),background_color=boxColor,color=textColor)
        #self.save_submit.bind(on_press=lambda x: self.seatBtn_save_popup(seatNum)) #bind 콜벡함수연결함수
        self.save_submit.bind(on_press=self.seatBtn_save_pop)
        self.seatBtn_layout.add_widget(self.save_submit)

        self.delete_submit = Button(text="2. Delete",width=40, height=30,size_hint=(1, 0.2),background_color=boxColor,color=textColor)
        self.delete_submit.bind(on_press = self.seatBtn_delete) #bind 콜벡함수연결함수
        self.seatBtn_layout.add_widget(self.delete_submit)

        self.close_submit = Button(text="3. Close",width=40, height=30,size_hint=(1, 0.2),background_color=boxColor,color=textColor)
        self.close_submit.bind(on_press = self.seatBtnPopup.dismiss) #bind 콜벡함수연결함수
        self.seatBtn_layout.add_widget(self.close_submit)

        self.seatBtnPopup.add_widget(self.seatBtn_layout)

        self.seatBtnPopup.open()

    def seatBtn_save_pop(self,obj):
        self.seatBtn_save_popup = Popup(title='',
              size_hint=(0.3, 0.2), size=(400, 400), auto_dismiss=True,
              title_font='Roboto',title_size=20, title_align='center',
              title_color=textColor,
              separator_height=0.5,
              separator_color=textColor)

        self.seatBtn_save_layout = StackLayout(orientation="lr-tb",padding=10,spacing=10)

        self.seatBtn_save_layout.add_widget(Label(text = 'Name?', size_hint=(0.3, 0.5),color=textColor))
        self.seatBtn_save_name = TextInput(multiline = False,size_hint=(0.7, 0.5))
        self.seatBtn_save_layout.add_widget(self.seatBtn_save_name)

        self.save_name_submit = Button(text="Submit",size_hint=(0.5, 0.5),background_color=boxColor,color=textColor)
        self.save_name_submit.bind(on_press = self.seatBtn_save) #bind 콜벡함수연결함수
        self.seatBtn_save_layout.add_widget(self.save_name_submit)

        self.save_close_submit = Button(text="Close",size_hint=(0.5, 0.5),background_color=boxColor,color=textColor)
        self.save_close_submit.bind(on_press = self.seatBtn_save_popup.dismiss) #bind 콜벡함수연결함수
        self.seatBtn_save_layout.add_widget(self.save_close_submit)

        self.seatBtn_save_popup.add_widget(self.seatBtn_save_layout)

        self.seatBtn_save_popup.open()

    def seatBtn_save(self,obj):
        proc = os.getpid()

        self.seatBtnPopup.dismiss()
        self.seatBtn_save_popup.dismiss()

        res = fs.selectSeat("5",str(self.seatNum),self.seatBtn_save_name.text)
        if res == False:
            ("retry")
        else:
            class5_btnDic[str(self.seatNum)].text = f"{str(self.seatNum)}: {self.seatBtn_save_name.text}"
            class5_btnDic[str(self.seatNum)].background_color = [255,255,255,1]
            class5_btnDic[str(self.seatNum)].color = [0,0,0,1]

        #threading.Timer(1.5, self.showSeat).start()
        #self.showSeat()
    def seatBtn_delete(self,obj):
        proc = os.getpid()
        print("seatBtn_delete: ", proc)

        if class5_btnDic[str(self.seatNum)].background_color == boxColor:
            self.seatBtnPopup.title = "empty seat."
        else:
            fs.deleteSeat("5",str(self.seatNum))
            class5_btnDic[str(self.seatNum)].text = str(self.seatNum)
            class5_btnDic[str(self.seatNum)].background_color = boxColor
            class5_btnDic[str(self.seatNum)].color = textColor
            self.seatBtnPopup.dismiss()

    def showSeat(self):
        print("class5 showSeat",self)
        res=fs.readSeat("5")

        if res == False:
            ("Empty")
        else:
            for i in range(len(res)):
                realNum = int(res[i][0])
                class5_btnDic[str(realNum)].text = f"{res[i][0]}: {res[i][1]}"
                class5_btnDic[str(realNum)].background_color = [255,255,255,1]
                class5_btnDic[str(realNum)].color = [0,0,0,1]
        #self.class5_btnDic["13\ndisorder"].background_color = [255,255,255,1]
        #self.class5_btnDic["13\ndisorder"].color = [0,0,0,1]

class Manager(ScreenManager):
    #screen_main = ObjectProperty(None)
    #screen_drawing = ObjectProperty(None)
    #screen_one = ObjectProperty(None)
    #screen_two = ObjectProperty(None)
    #screen_three = ObjectProperty(None)
    #screen_four = ObjectProperty(None)
    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)
        self.screen_main = ScreenMain(name="Screen_main", size_hint = (1, 0.9))
        self.screen_one = ScreenOne(name="Class1", size_hint = (1, 0.9))
        self.screen_two = ScreenTwo(name="Class2", size_hint = (1, 0.9))
        self.screen_three = ScreenThree(name="Class3", size_hint = (1, 0.9))
        self.screen_four = ScreenFour(name="Class4", size_hint = (1,0.9))
        self.screen_five = ScreenFive(name="Class5", size_hint = (1,0.9))
        self.add_widget(self.screen_main)
        self.add_widget(self.screen_one)
        self.add_widget(self.screen_two)
        self.add_widget(self.screen_three)
        self.add_widget(self.screen_four)
        self.add_widget(self.screen_five)

    def manager_clear(self,obj):
        self.clear_widgets()
#################################################################################
class Fourth_mine_kv2(App):
    global manager
    proc = os.getpid()
    print("Fourth_mine_kv2: ",proc)
   # Window.clearcolor = winColor
    #manager = Manager(transition=WipeTransition())
    manager = Manager()
    def build(self):
        proc = os.getpid()
        print("Appbuild: ", proc)
        self.root = Root()
        self.upperMenu = UpperMenu(size_hint = (1,0.1))
        self.root.add_widget(self.upperMenu)
        self.root.add_widget(manager)

        return self.root

    def show_clear(self,obj):
        manager.clear_widgets()
        manager.screen_main.clear_widgets()
        manager.screen_one.clear_widgets()
        manager.screen_two.clear_widgets()
        manager.screen_three.clear_widgets()
        manager.screen_four.clear_widgets()
        manager.screen_five.clear_widgets()

    def show_remove(self,obj):
        manager.remove_widget(manager.screen_main)
        manager.remove_widget(manager.screen_one)
        manager.remove_widget(manager.screen_two)
        manager.remove_widget(manager.screen_three)
        manager.remove_widget(manager.screen_four)
        manager.remove_widget(manager.screen_five)

    def show_screen_main(self,obj):
        manager.current = "Screen_main"
    def show_class(self,obj,classNum):
        manager.current = f"Class{classNum}"
    def show_screen_one(self,obj):
        manager.current = "Class1"
    def show_screen_two(self,obj):
        manager.current = "Class2"
    def show_screen_three(self,obj):
        manager.current = "Class3"
    def show_screen_four(self,obj):
        manager.current = "Class4"
    def show_screen_five(self,obj):
        manager.current = "Class5"
if __name__ == '__main__':
    proc = os.getpid()
    print("AppSTart: ", proc)

    Fourth_mine_kv2().run()

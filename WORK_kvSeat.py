#!/usr/bin/python3
# -*- coding:utf-8 -*-
#kivy.require("1.19.1")
from kivy import Config
Config.set("graphics", "multisamples", "0")
from kivy.app import App
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.uix.button import Button, ButtonBehavior
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.clock import Clock
from kivy.uix.colorpicker import ColorPicker

import os, sys
import time
import random

import work_seat as ws
import work_circle as circle
import work_geoWeather as weather

baseDir = os.getcwd()#current folder
imgDir = os.path.join(baseDir, "mine_imgs")#image folder
dataDir = os.path.join(baseDir, "work_seatData")#seat csv folder

white = [1,1,1,1]
black = [0,0,0,1]
invisible = [0,0,0,0]#transparent

winColor =[240/255,240/255,250/255,1]#light blue
boxColor = [90/255,130/255,170/255,1]#pastel blue
textColor = white

chageboxColor = [10/255,40/255,70/255,1]#navy
chagetextColor = white

################################################################################
class Root(BoxLayout):
    def __init__(self, **kwargs):
        super(Root, self).__init__(**kwargs)
        winWidth = 640
        winHeight = 480
        self.orientation = "vertical"
        #self.pos_hint: {"x": .3, "top": .9}
        self.size = (winWidth,winHeight)

################################################################################
class ImageButton(ButtonBehavior, Image):
    def __init__(self, **kwargs):
        super(ImageButton, self).__init__(**kwargs)

################################################################################
class UpperMenu(StackLayout):
    def __init__(self, **kwargs):
        super(UpperMenu, self).__init__(**kwargs)
        self.boxLayout = BoxLayout(size_hint=(1,1),spacing=30,orientation='horizontal')

        self.seatDrop = DropDown()

        btnText=["Main", "Random", "Seat", "Board", "Exit"]
        btnDic={}
        seatBtnText = ["Class1","Class2","Class3","Class4", "Class5"]
        seatBtnDic = {}

        self.img_btn = ImageButton(source=f'{imgDir}/seat_img.png')
        self.img_btn.size_hint = (0.1,1)
        self.img_btn.bind(on_release=self.show_screen_main)

        self.boxLayout.add_widget(self.img_btn)

        for i in range(len(btnText)):
            btn = Button(text=btnText[i], size_hint=(0.1, 0.9), background_color=boxColor,color=textColor,background_normal = "", background_down = "")
            btnDic[btnText[i]]=btn
            if btnText[i] == "Main":
                btn.bind(on_release=self.show_screen_main)
            if btnText[i] == "Random":
                btn.bind(on_release=self.seatPop)
            if btnText[i] == "Board":
                btn.bind(on_release=self.show_screen_drawing)
            if btnText[i] == "Seat":
                for j in range(len(seatBtnText)):
                    seatDropBtn = Button(text=seatBtnText[j], height=70, size_hint_y=None, background_color=boxColor,color=textColor,background_normal = "", background_down = "")
                    seatBtnDic[seatBtnText[j]] = seatDropBtn
                    seatDropBtn.bind(on_release=lambda instance: self.seatDrop.select(seatDropBtn.text))
                    self.seatDrop.add_widget(seatDropBtn)

                    if seatBtnText[j] == "Class1":
                        seatDropBtn.bind(on_release=self.show_screen_one)
                    if seatBtnText[j] == "Class2":
                        seatDropBtn.bind(on_release=self.show_screen_two)
                    if seatBtnText[j] == "Class3":
                        seatDropBtn.bind(on_release=self.show_screen_three)
                    if seatBtnText[j] == "Class4":
                        seatDropBtn.bind(on_release=self.show_screen_four)
                    if seatBtnText[j] == "Class5":
                        seatDropBtn.bind(on_release=self.show_screen_five)
                btn.bind(on_release=self.seatDrop.open)
                self.seatDrop.bind(on_select=lambda instance, x: setattr(seatDropBtn, 'text', x))

            if btnText[i] == "Exit":
                btn.bind(on_release=self.closeAll)

            self.boxLayout.add_widget(btn)

        self.empty = Button(text="", size_hint=(0.05, 0.9), background_color=invisible,color=invisible)
        self.boxLayout.add_widget(self.empty)

        self.add_widget(self.boxLayout)


    def closeAll(self,obj):
        WORK_kvSeat().get_running_app().stop()


    def show_screen_main(self,obj):
        manager.current = "Screen_main"
    def show_screen_drawing(self,obj):
        manager.current = "Screen_board"
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


    def seatPop(self, obj):
        self.seatPopup = Popup(title='',
              size_hint=(0.4, 0.4), size=(400, 400), auto_dismiss=True,
              title_font='Roboto',title_size=20, title_align='center',
              title_color=textColor,
              separator_height=0.5,
              separator_color=textColor)

        self.lowerContent = StackLayout(orientation="lr-tb",padding=10,spacing=10)
        self.seatTextLine=Label(text = 'Write class, seat limit, name.',size_hint=(1, 0.2),color=textColor)
        self.lowerContent.add_widget(self.seatTextLine)

        self.lowerContent.add_widget(Label(text='class?',size_hint=(0.5, 0.16),color=textColor))
        self.classNum = TextInput(multiline = False,size_hint=(0.5, 0.16))
        self.lowerContent.add_widget(self.classNum)

        self.lowerContent.add_widget(Label(text='seat limit?',size_hint=(0.5, 0.16),color=textColor))
        self.seatLimit = TextInput(multiline = False,size_hint=(0.5, 0.16))
        self.lowerContent.add_widget(self.seatLimit)

        self.lowerContent.add_widget(Label(text = 'name?',size_hint=(0.5, 0.16),color=textColor))
        self.name = TextInput(multiline = False,size_hint=(0.5, 0.16))
        self.lowerContent.add_widget(self.name)

        self.seatSubmit = Button(text="Submit",size_hint=(0.5, 0.16),background_color=boxColor,color=textColor,background_normal = "", background_down = "")
        self.seatSubmit.bind(on_press = self.seat_pressed)
        self.lowerContent.add_widget(self.seatSubmit)

        self.seatDelete = Button(text="Delete",size_hint=(0.5, 0.16),background_color=boxColor,color=textColor,background_normal = "", background_down = "")
        self.seatDelete.bind(on_press = self.delete_pressed)
        self.lowerContent.add_widget(self.seatDelete)

        self.seatPopup.add_widget(self.lowerContent)

        self.seatPopup.open()

    def seat_pressed(self,instance):
        print("class:", self.classNum.text,"name:", "seatLimit:", self.seatLimit.text, self.name.text)
        self.seatPopup.dismiss()
        try:
            if type(int(self.seatLimit.text)) == int:
                res = ws.randomSelectSeat(int(self.classNum.text), self.name.text, int(self.seatLimit.text))
                classNum = int(self.classNum.text)
                if res == False:
                    print("retry")
                else:
                    if classNum == 1:
                        class1_btnDic[str(res[0])].text = f"{res[0]}: {res[1]}"
                        class1_btnDic[str(res[0])].background_color = chageboxColor
                        class1_btnDic[str(res[0])].color = chagetextColor
                    elif classNum == 2:
                        class2_btnDic[str(res[0])].text = f"{res[0]}: {res[1]}"
                        class2_btnDic[str(res[0])].background_color = chageboxColor
                        class2_btnDic[str(res[0])].color = chagetextColor
                    elif classNum == 3:
                        class3_btnDic[str(res[0])].text = f"{res[0]}: {res[1]}"
                        class3_btnDic[str(res[0])].background_color = chageboxColor
                        class3_btnDic[str(res[0])].color = chagetextColor
                    elif classNum == 4:
                        class4_btnDic[str(res[0])].text = f"{res[0]}: {res[1]}"
                        class4_btnDic[str(res[0])].background_color = chageboxColor
                        class4_btnDic[str(res[0])].color = chagetextColor
                    manager.current = f"Class{classNum}"

        except Exception as msg:
                self.seatPopup.title = f"{msg}retry."

        self.name.text = ""
        self.seatLimit.text = ""
        self.classNum.text = ""

    def delete_pressed(self,obj):
            print("class:", self.classNum.text,"name:", self.name.text)

            try:
                res = ws.randomDeleteSeat(int(self.classNum.text), self.name.text)
                classNum = int(self.classNum.text)

                manager.current = f"Class{classNum}"

                if res == False:
                    print("There is no name. Do check.")

            except Exception as msg:
                    self.seatPopup.title = f"{msg}retry."

            self.name.text = ""
            self.seatLimit.text = ""
            self.classNum.text = ""

################################################################################
class ScreenMain(Screen):
    def __init__(self, **kwargs):
        super(ScreenMain, self).__init__(**kwargs)

        self.mainScreen = GridLayout(rows=5,row_force_default=True,row_default_height=180,
                                        padding=invisible,spacing=[0,0])

        self.emptyLabel = Label(size_hint=(0.14, 0.1),color=invisible)
        self.timeLabel = Label(font_size = '78sp',font_name="Times New Roman Bold",
                                halign='center',valign="bottom",bold=False,italic=False,
                                size_hint=(0.14, 0.15),pos_hint=(0.5,0.3),color=textColor)

        self.emptySecLabel = Label(size_hint=(0.14, 0.2),color=invisible)
        self.hereWeatherLabel = Label(font_size = '30sp',font_name="Times New Roman Italic",
                                    halign='justify',valign="bottom",bold=True,italic=True,
                                    size_hint=(0.14, 0.15),color=textColor)
        self.searchWeatherLabel = Label(font_size = '30sp',font_name="Times New Roman Italic",
                                    halign='justify',valign="center",bold=True,italic=True,
                                    size_hint=(0.14, 0.15),color=textColor)
        self.mainScreen.add_widget(self.emptyLabel)
        self.mainScreen.add_widget(self.timeLabel)
        self.mainScreen.add_widget(self.emptySecLabel)
        self.mainScreen.add_widget(self.hereWeatherLabel)
        self.mainScreen.add_widget(self.searchWeatherLabel)
        #==============
        self.mainSecScreen = StackLayout(orientation="rl-bt",padding=10,spacing=10)

        self.citySubmit = Button(text="Click",size_hint=(0.07, 0.055),background_color=boxColor,color=textColor,background_normal = "", background_down = "")
        self.citySubmit.bind(on_press = self.city_pressed)
        self.mainSecScreen.add_widget(self.citySubmit)
        self.city = TextInput(hint_text="Write city.",multiline = False,size_hint=(0.3, 0.06))
        self.mainSecScreen.add_widget(self.city)

        #==============
        self.add_widget(self.mainScreen)
        self.add_widget(self.mainSecScreen)

        Clock.schedule_interval(self.timeAdd, 0.5)

        self.weatherAdd(self)
        Clock.schedule_interval(self.weatherAdd,3600)

    def city_pressed(self,obj):
        print("city:", self.city.text)
        try:
            res = weather.Weather().geopyLatLonWeather(str(self.city.text))
            self.searchWeatherLabel.text = str(res)
            self.searchWeatherLabel.color = boxColor
            self.searchWeatherLabel.texture_update()
        except Exception as msg:
                self.city.hint_text = f"{msg}."

        self.city.text = ""

    def timeAdd(self,obj):
        timeText=circle.current_time()
        self.timeLabel.text = timeText
        self.timeLabel.color = boxColor
        self.timeLabel.texture_update()

    def weatherAdd(self,obj):
        weatherSecText = weather.Weather().urlIpRegionWeather()
        self.hereWeatherLabel.text = str(weatherSecText)
        self.hereWeatherLabel.color = boxColor
        self.hereWeatherLabel.texture_update()

################################################################################
class ScreenBoard(Screen):
    global PENTEXT, PENSLIDER, SLIDERTEXT, COLORPICKER, RGBA, HSV, HEX

    PENSLIDER = Slider(padding=5,value=10)
    PENSLIDER.size_hint=(0.1,0.1)
    PENSLIDER.value_track=True
    PENSLIDER.value_track_width="1sp"
    PENSLIDER.value_track_color=boxColor
    PENSLIDER.cursor_size=("10sp","10sp")
    PENSLIDER.cursor_image=f'{imgDir}/seat_img.png'
    PENSLIDER.background_width = "10sp"
    PENSLIDER.sensitivity = "all"

    SLIDERTEXT = Label(text="0",size_hint=(0.05, 0.1),color=boxColor)
    COLORPICKER = ColorPicker(size_hint=(1,1))

    def __init__(self, **kwargs):
        super(ScreenBoard, self).__init__(**kwargs)
        self.layout = GridLayout(rows=2,cols=1,padding=10,spacing=10,size_hint=(1,0.8))

        self.drawLayout = GridLayout(rows=2,cols=1,padding=10,spacing=10,size_hint=(1,0.8))
        self.painter=PaintWindow()
        self.drawLayout.add_widget(self.painter)
        self.layout.add_widget(self.drawLayout)

        self.drawLayout2 = GridLayout(rows=1,cols=7,padding=10,spacing=10,size_hint=(1,0.1))

        self.penLabel = Label(text="pen thinkness",font_size = '20sp',font_name="Times New Roman Italic",
                                        halign='justify',valign="bottom",bold=True,italic=True,
                                    size_hint=(0.1, 0.1),color=boxColor)

        self.clearBtn = Button(text='Clear',width=40, height=30, size_hint=(0.05, 0.1),
                                font_size = '20sp',font_name="Times New Roman Italic",
                                halign='justify',valign="bottom",bold=True,italic=False,
                                background_color=winColor,color=boxColor,background_normal = "", background_down = "")
        self.clearBtn.bind(on_release=self.clear_canvas)
        self.colorBtn = Button(text='Color',width=40, height=30, size_hint=(0.05, 0.1),
                                font_size = '20sp',font_name="Times New Roman Italic",
                                halign='justify',valign="bottom",bold=True,italic=False,
                                background_color=winColor,color=boxColor,background_normal = "", background_down = "")
        self.colorBtn.bind(on_release=self.colorPopup)
        PENSLIDER.bind(value=getPenVal)

        self.drawLayout2.add_widget(self.penLabel)
        self.drawLayout2.add_widget(PENSLIDER)
        self.drawLayout2.add_widget(SLIDERTEXT)
        self.drawLayout2.add_widget(self.colorBtn)
        self.drawLayout2.add_widget(self.clearBtn)

        self.layout.add_widget(self.drawLayout2)

        self.add_widget(self.layout)

    def colorPopup(self,obj):
        proc = os.getpid()
        print("colorPop:", proc)

        self.colorPop = Popup(title='Choose color',
              size_hint=(0.5, 0.5), auto_dismiss=False,
              title_font='Roboto',title_size=20, title_align='center',
              title_color=textColor,
              separator_height=0.5,
              separator_color=textColor)
        self.layout = BoxLayout(orientation="horizontal",padding=5,spacing=5,size_hint=(1,1))
        self.closeBtn = Button(text='Close',size_hint=(0.15, 0.15),halign="justify",valign="middle",
                                background_color=boxColor,color=textColor,background_normal = "", background_down = "")
        self.closeBtn.bind(on_release=self.closeColorPopup)

        COLORPICKER.bind(color=onColor)
        self.layout.add_widget(COLORPICKER)
        self.layout.add_widget(self.closeBtn)
        self.colorPop.add_widget(self.layout)
        self.colorPop.open()

    def closeColorPopup(self,obj):
        self.colorPop.remove_widget(self.layout)
        self.layout.remove_widget(COLORPICKER)
        self.layout.remove_widget(self.closeBtn)
        self.colorPop.dismiss()

    def clear_canvas(self, obj):
        self.painter.canvas.clear()

################################################################################
class ScreenOne(Screen):
    def __init__(self, **kwargs):
        super(ScreenOne, self).__init__(**kwargs)
        global class1_btnDic

        self.layout1 = StackLayout(orientation="bt-lr",padding=10,spacing=5)

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
                                    background_color=boxColor,color=textColor
                                    ,background_normal = "", background_down = "")
                class1_btnDic[str(beforeNum[i])]=self.class1_btn
                if beforeNum[i] != "x":
                    class1_btnDic[str(beforeNum[i])].bind(on_press = self.seatBtn_pop)
            else:
                self.class1_btn = Button(text=str(i),size_hint=(0.1, 0.08),
                                    background_color=invisible,color=invisible
                                    ,background_normal = "", background_down = "")

            self.layout1.add_widget(self.class1_btn)

        self.layout1.add_widget(Label(text='Class1',font_size=50,
                                    halign="right",valign="bottom",bold=True,
                                    size_hint=(0.5, 0.3),color=boxColor))

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
        self.textLine=Label(text = 'Choose.',size_hint=(1, 0.2),color=textColor)
        self.seatBtn_layout.add_widget(self.textLine)

        self.save_submit = Button(text="1. Save",size_hint=(1, 0.2),background_color=boxColor,color=textColor,background_normal = "", background_down = "")
        self.save_submit.bind(on_press=self.seatBtn_save_pop)
        self.seatBtn_layout.add_widget(self.save_submit)

        self.delete_submit = Button(text="2. Delete",size_hint=(1, 0.2),background_color=boxColor,color=textColor,background_normal = "", background_down = "")
        self.delete_submit.bind(on_press = self.seatBtn_delete)
        self.seatBtn_layout.add_widget(self.delete_submit)

        self.close_submit = Button(text="3. Close",size_hint=(1, 0.2),background_color=boxColor,color=textColor,background_normal = "", background_down = "")
        self.close_submit.bind(on_press = self.seatBtnPopup.dismiss)
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

        self.save_name_submit = Button(text="Submit",size_hint=(0.5, 0.5),background_color=boxColor,color=textColor,background_normal = "", background_down = "")
        self.save_name_submit.bind(on_press = self.seatBtn_save)
        self.seatBtn_save_layout.add_widget(self.save_name_submit)

        self.save_close_submit = Button(text="Close",size_hint=(0.5, 0.5),background_color=boxColor,color=textColor,background_normal = "", background_down = "")
        self.save_close_submit.bind(on_press = self.seatBtn_save_popup.dismiss)
        self.seatBtn_save_layout.add_widget(self.save_close_submit)

        self.seatBtn_save_popup.add_widget(self.seatBtn_save_layout)

        self.seatBtn_save_popup.open()

    def seatBtn_save(self,obj):
        proc = os.getpid()
        print("seatBtn_save: ", proc,self,obj)

        self.seatBtnPopup.dismiss()
        self.seatBtn_save_popup.dismiss()

        res = ws.selectSeat("1",str(self.seatNum),self.seatBtn_save_name.text)
        if res == False:
            ("retry")
        else:
            class1_btnDic[str(self.seatNum)].text = f"{str(self.seatNum)}: {self.seatBtn_save_name.text}"
            class1_btnDic[str(self.seatNum)].background_color = chageboxColor
            class1_btnDic[str(self.seatNum)].color = chagetextColor

    def seatBtn_delete(self,obj):
        proc = os.getpid()
        print("seatBtn_delete: ", proc)

        if class1_btnDic[str(self.seatNum)].background_color == boxColor:
            self.seatBtnPopup.title = "empty seat."
        else:
            ws.deleteSeat("1",str(self.seatNum))
            class1_btnDic[str(self.seatNum)].text = str(self.seatNum)
            class1_btnDic[str(self.seatNum)].background_color = boxColor
            class1_btnDic[str(self.seatNum)].color = textColor

            self.seatBtnPopup.dismiss()

    def showSeat(self):
        print("class1 showSeat",self)
        res=ws.readSeat("1")

        if res == False:
            ("Empty")
        else:
            for i in range(len(res)):
                realNum = int(res[i][0])
                class1_btnDic[str(realNum)].text = f"{res[i][0]}: {res[i][1]}"
                class1_btnDic[str(realNum)].background_color = chageboxColor
                class1_btnDic[str(realNum)].color = chagetextColor

################################################################################
class ScreenTwo(Screen): #grid
    def __init__(self, **kwargs):
        super(ScreenTwo, self).__init__(**kwargs)
        global class2_btnDic

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
                                    background_color=boxColor,color=textColor
                                    ,background_normal = "", background_down = "")
                class2_btnDic[str(beforeNum[i])]=self.class2_btn
                if beforeNum[i] != "x":
                    class2_btnDic[str(beforeNum[i])].bind(on_press = self.seatBtn_pop)
            else:
                self.class2_btn = Button(text=str(i),size_hint=(0.1, 0.08),
                                    background_color=invisible,color=invisible
                                    ,background_normal = "", background_down = "")

            self.layout2.add_widget(self.class2_btn)

        self.layout2.add_widget(Label(text='Class2',font_size=50,
                                    halign="right",valign="bottom",bold=True,
                                    size_hint=(0.5, 0.08),color=boxColor))

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
        self.textLine=Label(text = 'Choose.',size_hint=(1, 0.2),color=textColor)
        self.seatBtn_layout.add_widget(self.textLine)

        self.save_submit = Button(text="1. Save",size_hint=(1, 0.2),background_color=boxColor,color=textColor,background_normal = "", background_down = "")
        self.save_submit.bind(on_press=self.seatBtn_save_pop)
        self.seatBtn_layout.add_widget(self.save_submit)

        self.delete_submit = Button(text="2. Delete",size_hint=(1, 0.2),background_color=boxColor,color=textColor,background_normal = "", background_down = "")
        self.delete_submit.bind(on_press = self.seatBtn_delete)
        self.seatBtn_layout.add_widget(self.delete_submit)

        self.close_submit = Button(text="3. Close",size_hint=(1, 0.2),background_color=boxColor,color=textColor,background_normal = "", background_down = "")
        self.close_submit.bind(on_press = self.seatBtnPopup.dismiss)
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

        self.save_name_submit = Button(text="Submit",size_hint=(0.5, 0.5),background_color=boxColor,color=textColor,background_normal = "", background_down = "")
        self.save_name_submit.bind(on_press = self.seatBtn_save)
        self.seatBtn_save_layout.add_widget(self.save_name_submit)

        self.save_close_submit = Button(text="Close",size_hint=(0.5, 0.5),background_color=boxColor,color=textColor,background_normal = "", background_down = "")
        self.save_close_submit.bind(on_press = self.seatBtn_save_popup.dismiss)
        self.seatBtn_save_layout.add_widget(self.save_close_submit)

        self.seatBtn_save_popup.add_widget(self.seatBtn_save_layout)

        self.seatBtn_save_popup.open()

    def seatBtn_save(self,obj):
        proc = os.getpid()

        self.seatBtnPopup.dismiss()
        self.seatBtn_save_popup.dismiss()

        res = ws.selectSeat("2",str(self.seatNum),self.seatBtn_save_name.text)
        if res == False:
            ("retry")
        else:
            class2_btnDic[str(self.seatNum)].text = f"{str(self.seatNum)}: {self.seatBtn_save_name.text}"
            class2_btnDic[str(self.seatNum)].background_color = chageboxColor
            class2_btnDic[str(self.seatNum)].color = chagetextColor

    def seatBtn_delete(self,obj):
        proc = os.getpid()
        print("seatBtn_delete: ", proc)

        if class2_btnDic[str(self.seatNum)].background_color == boxColor:
            self.seatBtnPopup.title = "empty seat."
        else:
            ws.deleteSeat("2",str(self.seatNum))
            class2_btnDic[str(self.seatNum)].text = str(self.seatNum)
            class2_btnDic[str(self.seatNum)].background_color = boxColor
            class2_btnDic[str(self.seatNum)].color = textColor

            self.seatBtnPopup.dismiss()

    def showSeat(self):
        print("class2 showSeat",self)
        res=ws.readSeat("2")

        if res == False:
            ("Empty")
        else:
            for i in range(len(res)):
                realNum = int(res[i][0])
                class2_btnDic[str(realNum)].text = f"{res[i][0]}: {res[i][1]}"
                class2_btnDic[str(realNum)].background_color = chageboxColor
                class2_btnDic[str(realNum)].color = chagetextColor

################################################################################
class ScreenThree(Screen):
    def __init__(self, **kwargs):
        super(ScreenThree, self).__init__(**kwargs)
        global class3_btnDic

        self.layout3 = StackLayout(orientation="bt-lr",padding=10,spacing=5)

        class3_btnDic={}
        btnCount=0
        beforeNum = {3:1,4:2,5:3,6:4,7:5,8:6,9:7,
                10:8,11:9,12:"x",24:10,36:11,48:12,60:13,
                72:"x",71:14,70:15,69:16,68:17,67:18,66:19,65:20,64:21,63:22,62:23,61:24}
        for i in range(1,73):
            if 3 <= i <= 12 or 61 <= i <= 72 or i in [24,36,48,60]:
                btnCount+=1
                #font_name="Times New Roman","Verdana"
                self.class3_btn = Button(text=str(beforeNum[i]),font_size=18,font_name="Arial",bold=True,
                                    size_hint=(0.1, 0.08),halign="justify",valign="middle",
                                    background_color=boxColor,color=textColor
                                    ,background_normal = "", background_down = "")
                class3_btnDic[str(beforeNum[i])]=self.class3_btn
                if beforeNum[i] != "x":
                    class3_btnDic[str(beforeNum[i])].bind(on_press = self.seatBtn_pop)
            else:
                self.class3_btn = Button(text=str(i),size_hint=(0.1, 0.08),
                                    background_color=invisible,color=invisible
                                    ,background_normal = "", background_down = "")

            self.layout3.add_widget(self.class3_btn)

        self.layout3.add_widget(Label(text='Class3',font_size=50,
                                    halign="right",valign="bottom",bold=True,
                                    size_hint=(0.5, 0.3),color=boxColor))

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
        self.textLine=Label(text = 'Choose.',size_hint=(1, 0.2),color=textColor)
        self.seatBtn_layout.add_widget(self.textLine)

        self.save_submit = Button(text="1. Save",size_hint=(1, 0.2),background_color=boxColor,color=textColor,background_normal = "", background_down = "")
        self.save_submit.bind(on_press=self.seatBtn_save_pop)
        self.seatBtn_layout.add_widget(self.save_submit)

        self.delete_submit = Button(text="2. Delete",size_hint=(1, 0.2),background_color=boxColor,color=textColor,background_normal = "", background_down = "")
        self.delete_submit.bind(on_press = self.seatBtn_delete)
        self.seatBtn_layout.add_widget(self.delete_submit)

        self.close_submit = Button(text="3. Close",size_hint=(1, 0.2),background_color=boxColor,color=textColor,background_normal = "", background_down = "")
        self.close_submit.bind(on_press = self.seatBtnPopup.dismiss)
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

        self.save_name_submit = Button(text="Submit",size_hint=(0.5, 0.5),background_color=boxColor,color=textColor,background_normal = "", background_down = "")
        self.save_name_submit.bind(on_press = self.seatBtn_save)
        self.seatBtn_save_layout.add_widget(self.save_name_submit)

        self.save_close_submit = Button(text="Close",size_hint=(0.5, 0.5),background_color=boxColor,color=textColor,background_normal = "", background_down = "")
        self.save_close_submit.bind(on_press = self.seatBtn_save_popup.dismiss)
        self.seatBtn_save_layout.add_widget(self.save_close_submit)

        self.seatBtn_save_popup.add_widget(self.seatBtn_save_layout)

        self.seatBtn_save_popup.open()

    def seatBtn_save(self,obj):
        proc = os.getpid()

        self.seatBtnPopup.dismiss()
        self.seatBtn_save_popup.dismiss()

        res = ws.selectSeat("3",str(self.seatNum),self.seatBtn_save_name.text)
        if res == False:
            ("retry")
        else:
            class3_btnDic[str(self.seatNum)].text = f"{str(self.seatNum)}: {self.seatBtn_save_name.text}"
            class3_btnDic[str(self.seatNum)].background_color = chageboxColor
            class3_btnDic[str(self.seatNum)].color = chagetextColor

    def seatBtn_delete(self,obj):
        proc = os.getpid()
        print("seatBtn_delete: ", proc)

        if class3_btnDic[str(self.seatNum)].background_color == boxColor:
            self.seatBtnPopup.title = "empty seat."
        else:
            ws.deleteSeat("3",str(self.seatNum))
            class3_btnDic[str(self.seatNum)].text = str(self.seatNum)
            class3_btnDic[str(self.seatNum)].background_color = boxColor
            class3_btnDic[str(self.seatNum)].color = textColor
            self.seatBtnPopup.dismiss()

    def showSeat(self):
        print("class3 showSeat",self)
        res=ws.readSeat("3")

        if res == False:
            ("Empty")
        else:
            for i in range(len(res)):
                realNum = int(res[i][0])
                class3_btnDic[str(realNum)].text = f"{res[i][0]}: {res[i][1]}"
                class3_btnDic[str(realNum)].background_color = chageboxColor
                class3_btnDic[str(realNum)].color = chagetextColor

################################################################################
class ScreenFour(Screen):
    def __init__(self, **kwargs):
        super(ScreenFour, self).__init__(**kwargs)
        global class4_btnDic

        self.layout4 = StackLayout(orientation="bt-lr",padding=10,spacing=5)

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
                                    background_color=boxColor,color=textColor
                                    ,background_normal = "", background_down = "")
                class4_btnDic[str(beforeNum[i])]=self.class4_btn
                if beforeNum[i] != "x":
                    class4_btnDic[str(beforeNum[i])].bind(on_press = self.seatBtn_pop)
            else:
                self.class4_btn = Button(text=str(i),size_hint=(0.1, 0.08),
                                    background_color=invisible,color=invisible
                                    ,background_normal = "", background_down = "")

            self.layout4.add_widget(self.class4_btn)

        self.layout4.add_widget(Label(text='Class4',font_size=50,
                                    halign="right",valign="bottom",bold=True,
                                    size_hint=(0.5, 0.3),color=boxColor))

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
        self.textLine=Label(text = 'Choose.',size_hint=(1, 0.2),color=textColor)
        self.seatBtn_layout.add_widget(self.textLine)

        self.save_submit = Button(text="1. Save",size_hint=(1, 0.2),background_color=boxColor,color=textColor,background_normal = "", background_down = "")
        self.save_submit.bind(on_press=self.seatBtn_save_pop)
        self.seatBtn_layout.add_widget(self.save_submit)

        self.delete_submit = Button(text="2. Delete",size_hint=(1, 0.2),background_color=boxColor,color=textColor,background_normal = "", background_down = "")
        self.delete_submit.bind(on_press = self.seatBtn_delete)
        self.seatBtn_layout.add_widget(self.delete_submit)

        self.close_submit = Button(text="3. Close",size_hint=(1, 0.2),background_color=boxColor,color=textColor,background_normal = "", background_down = "")
        self.close_submit.bind(on_press = self.seatBtnPopup.dismiss)
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

        self.save_name_submit = Button(text="Submit",size_hint=(0.5, 0.5),background_color=boxColor,color=textColor,background_normal = "", background_down = "")
        self.save_name_submit.bind(on_press = self.seatBtn_save)
        self.seatBtn_save_layout.add_widget(self.save_name_submit)

        self.save_close_submit = Button(text="Close",size_hint=(0.5, 0.5),background_color=boxColor,color=textColor,background_normal = "", background_down = "")
        self.save_close_submit.bind(on_press = self.seatBtn_save_popup.dismiss)
        self.seatBtn_save_layout.add_widget(self.save_close_submit)

        self.seatBtn_save_popup.add_widget(self.seatBtn_save_layout)

        self.seatBtn_save_popup.open()

    def seatBtn_save(self,obj):
        proc = os.getpid()

        self.seatBtnPopup.dismiss()
        self.seatBtn_save_popup.dismiss()

        res = ws.selectSeat("4",str(self.seatNum),self.seatBtn_save_name.text)
        if res == False:
            ("retry")
        else:
            class4_btnDic[str(self.seatNum)].text = f"{str(self.seatNum)}: {self.seatBtn_save_name.text}"
            class4_btnDic[str(self.seatNum)].background_color = chageboxColor
            class4_btnDic[str(self.seatNum)].color = chagetextColor

    def seatBtn_delete(self,obj):
        proc = os.getpid()
        print("seatBtn_delete: ", proc)

        if class4_btnDic[str(self.seatNum)].background_color == boxColor:
            self.seatBtnPopup.title = "empty seat."
        else:
            ws.deleteSeat("4",str(self.seatNum))
            class4_btnDic[str(self.seatNum)].text = str(self.seatNum)
            class4_btnDic[str(self.seatNum)].background_color = boxColor
            class4_btnDic[str(self.seatNum)].color = textColor
            self.seatBtnPopup.dismiss()

    def showSeat(self):
        print("class4 showSeat",self)
        res=ws.readSeat("4")

        if res == False:
            ("Empty")
        else:
            for i in range(len(res)):
                realNum = int(res[i][0])
                class4_btnDic[str(realNum)].text = f"{res[i][0]}: {res[i][1]}"
                class4_btnDic[str(realNum)].background_color = chageboxColor
                class4_btnDic[str(realNum)].color = chagetextColor

################################################################################
class ScreenFive(Screen):
    def __init__(self, **kwargs):
        super(ScreenFive, self).__init__(**kwargs)
        global class5_btnDic

        self.layout5 = StackLayout(orientation="bt-lr",padding=10,spacing=5)

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
                                    background_color=boxColor,color=textColor
                                    ,background_normal = "", background_down = "")
                class5_btnDic[str(beforeNum[i])]=self.class5_btn
                if beforeNum[i] != "x":
                    class5_btnDic[str(beforeNum[i])].bind(on_press = self.seatBtn_pop)
            else:
                self.class5_btn = Button(text=str(i),size_hint=(0.1, 0.08),
                                    background_color=invisible,color=invisible
                                    ,background_normal = "", background_down = "")

            self.layout5.add_widget(self.class5_btn)

        self.layout5.add_widget(Label(text='Class5',font_size=50,
                                    halign="right",valign="bottom",bold=True,
                                    size_hint=(0.5, 0.3),color=boxColor))

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
        self.textLine=Label(text = 'Choose.',size_hint=(1, 0.2),color=textColor)
        self.seatBtn_layout.add_widget(self.textLine)

        self.save_submit = Button(text="1. Save",size_hint=(1, 0.2),background_color=boxColor,color=textColor,background_normal = "", background_down = "")
        self.save_submit.bind(on_press=self.seatBtn_save_pop)
        self.seatBtn_layout.add_widget(self.save_submit)

        self.delete_submit = Button(text="2. Delete",size_hint=(1, 0.2),background_color=boxColor,color=textColor,background_normal = "", background_down = "")
        self.delete_submit.bind(on_press = self.seatBtn_delete)
        self.seatBtn_layout.add_widget(self.delete_submit)

        self.close_submit = Button(text="3. Close",size_hint=(1, 0.2),background_color=boxColor,color=textColor,background_normal = "", background_down = "")
        self.close_submit.bind(on_press = self.seatBtnPopup.dismiss)
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

        self.save_name_submit = Button(text="Submit",size_hint=(0.5, 0.5),background_color=boxColor,color=textColor,background_normal = "", background_down = "")
        self.save_name_submit.bind(on_press = self.seatBtn_save)
        self.seatBtn_save_layout.add_widget(self.save_name_submit)

        self.save_close_submit = Button(text="Close",size_hint=(0.5, 0.5),background_color=boxColor,color=textColor,background_normal = "", background_down = "")
        self.save_close_submit.bind(on_press = self.seatBtn_save_popup.dismiss)
        self.seatBtn_save_layout.add_widget(self.save_close_submit)

        self.seatBtn_save_popup.add_widget(self.seatBtn_save_layout)

        self.seatBtn_save_popup.open()

    def seatBtn_save(self,obj):
        proc = os.getpid()

        self.seatBtnPopup.dismiss()
        self.seatBtn_save_popup.dismiss()

        res = ws.selectSeat("5",str(self.seatNum),self.seatBtn_save_name.text)
        if res == False:
            ("retry")
        else:
            class5_btnDic[str(self.seatNum)].text = f"{str(self.seatNum)}: {self.seatBtn_save_name.text}"
            class5_btnDic[str(self.seatNum)].background_color = chageboxColor
            class5_btnDic[str(self.seatNum)].color = chagetextColor

    def seatBtn_delete(self,obj):
        proc = os.getpid()
        print("seatBtn_delete: ", proc)

        if class5_btnDic[str(self.seatNum)].background_color == boxColor:
            self.seatBtnPopup.title = "empty seat."
        else:
            ws.deleteSeat("5",str(self.seatNum))
            class5_btnDic[str(self.seatNum)].text = str(self.seatNum)
            class5_btnDic[str(self.seatNum)].background_color = boxColor
            class5_btnDic[str(self.seatNum)].color = textColor
            self.seatBtnPopup.dismiss()

    def showSeat(self):
        print("class5 showSeat",self)
        res=ws.readSeat("5")

        if res == False:
            ("Empty")
        else:
            for i in range(len(res)):
                realNum = int(res[i][0])
                class5_btnDic[str(realNum)].text = f"{res[i][0]}: {res[i][1]}"
                class5_btnDic[str(realNum)].background_color = chageboxColor
                class5_btnDic[str(realNum)].color = chagetextColor

################################################################################
class Manager(ScreenManager):

    def __init__(self, **kwargs):
        super(Manager, self).__init__(**kwargs)
        self.screen_main = ScreenMain(name="Screen_main", size_hint = (1, 0.9))
        self.screen_board = ScreenBoard(name="Screen_board", size_hint = (1, 0.9))
        self.screen_one = ScreenOne(name="Class1", size_hint = (1, 0.9))
        self.screen_two = ScreenTwo(name="Class2", size_hint = (1, 0.9))
        self.screen_three = ScreenThree(name="Class3", size_hint = (1, 0.9))
        self.screen_four = ScreenFour(name="Class4", size_hint = (1,0.9))
        self.screen_five = ScreenFive(name="Class5", size_hint = (1,0.9))
        self.add_widget(self.screen_main)
        self.add_widget(self.screen_board)
        self.add_widget(self.screen_one)
        self.add_widget(self.screen_two)
        self.add_widget(self.screen_three)
        self.add_widget(self.screen_four)
        self.add_widget(self.screen_five)

    def manager_clear(self,obj):
        self.clear_widgets()

################################################################################
class PaintWindow(Widget):

    def on_touch_down(self, touch):
        RGBA, HSV, HEX = getColor()
        self.canvas.add(Color(rgb=RGBA))
        try:
            PENTEXT=getPentext()
            print("touched",PENTEXT)

            self.canvas.add(Ellipse(pos=(touch.x - PENTEXT / 2, touch.y - PENTEXT / 2), size=(PENTEXT, PENTEXT)))
            touch.ud['line'] = Line(points=(touch.x, touch.y),width=PENTEXT)
            self.canvas.add(touch.ud['line'])
        except Exception as msg:
                print(f"getVal fail.{msg}retry.")

    def on_touch_move(self, touch):
        try:
            touch.ud['line'].points += [touch.x, touch.y]
        except Exception as msg:
                print(f"{msg}retry.")

def getPenVal(instance,value):
    PENTEXT = PENSLIDER.value
    SLIDERTEXT.text = str(int(PENTEXT))
    SLIDERTEXT.texture_update()
    print("PENTEXT:",PENTEXT)
    return PENTEXT

def getPentext():
    PENTEXT = getPenVal(PENSLIDER,PENSLIDER.value)
    return PENTEXT

def onColor(instance, value):
    RGBA = value
    HSV = instance.hsv
    HEX = instance.hex_color
    print("RGBA = ", str(value))
    print("HSV = ", str(instance.hsv))
    print("HEX = ", str(instance.hex_color))

    return RGBA, HSV, HEX

def getColor():
    RGBA, HSV, HEX = onColor(COLORPICKER,COLORPICKER.color)
    return RGBA, HSV, HEX

#################################################################################
class WORK_kvSeat(App):

    global manager

    Window.clearcolor = winColor
    manager = Manager()

    def build(self):
        self.root = Root()
        self.upperMenu = UpperMenu(size_hint = (1,0.1))
        self.root.add_widget(self.upperMenu)
        self.root.add_widget(manager)

        return self.root


if __name__ == '__main__':
    proc = os.getpid()
    print("AppSTart: ", proc)

    WORK_kvSeat().run()

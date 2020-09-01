import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, NumericProperty, StringProperty
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.animation import Animation
from kivy.uix.floatlayout import FloatLayout
import mysql.connector
from mysql.connector import Error
import getpass
from MBlogicVrsta import pictures_matrix4, pictures_matrix5
import hashlib
import requests
import json


def md5(string):
    return (hashlib.md5(string.encode('utf-8')).hexdigest())


Window.clearcolor = (1, 0.3, 0, 1)


class MyGrid(Widget):
    def CompBtn(self):
        Pop6.show_popup(self)


class MyGridS(Widget):  # sign up
    def clear_inputs(self, text_inputs):
        for text_input in text_inputs:
            text_input.text = ""

    def DBsend(self, User, Pass, Mail, Sa):
        data = {'user': User.text,
                'password': md5(Pass.text),
                'email': Mail.text,
                'scrt': md5(Sa.text)}
        headers = {'content-type': 'application/json'}
        if Pass.text == "" or User.text == "" or Mail.text == "" or Sa.text == "":
            Pop5.show_popup(self)
            # da se mi drugo ne izvede (ce ne mi pošlje v bazo prazne stringe)
            return
        try:
            r = requests.post("http://10.0.2.2:8100/login",
                              data=json.dumps(data), headers=headers)
            Pop8.show_popup(self)
        except Error as e:
            print(e)
            Pop1.show_popup1(self)


class MyGridT(Widget):  # Log in
    def clear_inputs(self, text_inputs):
        for text_input in text_inputs:
            text_input.text = ""

    def DBrecieve(self, User, Pass):
        mycursor = requests.get("http://10.0.2.2:8100/login").json()
        global UserID_L
        global userL
        global userIndex
        userL = []
        passL = []
        UserID_L = []
        for i in mycursor:
            userL.append(i[0])
            passL.append(i[1])
            UserID_L.append(i[2])
        if User.text not in userL:
            Pop2.show_popup2(self)
        else:
            ind = userL.index(User.text)
            userIndex = ind  # del namenjen samo za uporabo pri mainlogscreen
            if md5(Pass.text) == passL[ind]:
                Pop4.switch(self)
                Pop4.show_popup(self)
            else:
                Pop3.show_popup(self)


class AboutWindowLog(Screen):
    pass


class ForgotPass(Widget):
    def clear_inputs(self, text_inputs):
        for text_input in text_inputs:
            text_input.text = ""

    def newsend(self, User, Scrt, Pass):
        mycursor = requests.get("http://10.0.2.2:8100/scrt").json()
        userL = []
        scrtL = []
        for i in mycursor:
            userL.append(i[0])
            scrtL.append(i[1])
        if User.text not in userL:
            Pop2.show_popup2(self)
        else:
            ind = userL.index(User.text)
            if md5(Scrt.text) == scrtL[ind]:
                data = {'password': md5(Pass.text),
                        'user': User.text}
                headers = {'content-type': 'application/json'}
                r = requests.post("http://10.0.2.2:8100/scrt",
                                  data=json.dumps(data), headers=headers)

                Pop7.show_popup(self)
            else:
                Pop5.show_popup(self)


class SellectionGrid(Widget):
    difficulty = ""
    # tega ne dajem na nič ker rabim za pošiljanje v bazo, vrednost bo spremenilo pri novi igri
    difficultyBase = ""
    nop = ""
    nopBase = ""  # tega ne dajem na nič ker rabim za pošiljanje v bazo, vrednost bo spremenilo pri novi igri
    # zaradi težavnsti prenosa(v drugi class) uporabljam listo
    difficultyBaselist = []
    nopBaselist = []

    def if_actived(self, text):
        self.difficulty = text
        self.difficultyBase = text
        if self.difficulty != "" and self.nop != "":
            self.ids.readygo.disabled = False
        return self.difficultyBase

    def if_activeNOP(self, text):
        self.nop = text
        self.nopBase = text
        if self.difficulty != "" and self.nop != "":
            self.ids.readygo.disabled = False
        return self.nopBase

    def if_under(self):
        diff = self.if_actived(self.difficultyBase)
        nplay = self.if_activeNOP(self.nopBase)
        self.difficultyBaselist.append(diff)
        self.nopBaselist.append(nplay)
        if len(self.difficultyBaselist) == 2:
            self.difficultyBaselist.pop(0)
        if len(self.nopBaselist) == 2:
            self.nopBaselist.pop(0)
        return self.nopBaselist, self.difficultyBaselist

    def ClearText(self, *args):
        if self.difficulty == '4':
            self.ids.dchoicebox.children[2].active = False
            self.difficulty = ""
        else:
            self.ids.dchoicebox.children[0].active = False
            self.difficulty = ""

    def ClearText2(self, *args):
        if self.nop == 'dva':
            self.ids.pchoicebox.children[4].active = False
            self.nop = ""
        elif self.difficulty == 'tri':
            self.ids.pchoicebox.children[2].active = False
            self.nop = ""
        else:
            self.ids.pchoicebox.children[0].active = False
            self.nop = ""


class MyGridLog(Widget):
    def CompBtn(self):
        Pop9.show_popup(self)


class ForgotPassSc(Screen):
    pass


class WindowMan(ScreenManager):
    pass


class SecondWindow(Screen):
    pass


class ThirdWindow(Screen):
    pass


class AboutWindow(Screen):
    pass


class TransitionWindow(Screen):
    pass


class SelectionWindow(Screen):
    pass

    def on_pre_enter(self, *args):
        for index in range(len(self.ids.slct.ids.pchoicebox.children[:])):
            if index % 2 == 0:
                self.ids.slct.ids.pchoicebox.children[index].active = False
        for index in range(len(self.ids.slct.ids.dchoicebox.children[:])):
            if index % 2 == 0:
                self.ids.slct.ids.dchoicebox.children[index].active = False
        self.ids.slct.ids.readygo.disabled = True


class PracticeWindow(Screen):
    pass


class CompWindow(Screen):
    pass


class MainWindow(Screen):
    pass


class MainLogWindow(Screen):
    def on_enter(self):
        self.ids.logpuzz.ids.logedin.text = 'Logged in as: ' + \
            (userL[userIndex])


class StarScWindow(Screen):
    def on_enter(self, *args):
        self.count = 3
        self.countdown_label = Label(
            font_size=150, bold=True, color=(0.2, 0.9, 0.9, 1))
        self.countdown_label.text = str(self.count)
        Clock.schedule_once(self.update_count, 1)
        self.ids.hello.add_widget(self.countdown_label)
        Clock.schedule_once(self.switch, 3)

    def update_count(self, *args):
        self.count -= 1
        if self.count > -1:
            self.countdown_label.text = str(self.count)
            Clock.schedule_once(self.update_count, 1)

    def switch(self, *args):
        self.parent.current = 'puzzle'
        self.ids.hello.remove_widget(self.countdown_label)

# COMPETATIVE


class StarScWindowC(Screen):
    class_instance = SellectionGrid().if_under()
    countswich = 0

    def on_enter(self, *args):
        self.count = 3
        self.countdown_label = Label(
            font_size=150, bold=True, color=(0.2, 0.9, 0.9, 1))
        self.countdown_label.text = str(self.count)
        Clock.schedule_once(self.update_count, 1)
        self.ids.helloC.add_widget(self.countdown_label)
        Clock.schedule_once(self.switchC, 3)

    def update_count(self, *args):
        self.count -= 1
        if self.count > -1:
            self.countdown_label.text = str(self.count)
            Clock.schedule_once(self.update_count, 1)

    def switchC(self, *args):
        print(self.class_instance[1][0])
        if self.class_instance[1][0] == "Easy: 4x4":
            self.parent.current = 'puzzleComp4'
            self.ids.helloC.remove_widget(self.countdown_label)
        else:
            self.parent.current = 'puzzleComp'
            self.ids.helloC.remove_widget(self.countdown_label)


class Pop(FloatLayout):
    def show_popup(self):
        show = Pop()
        popupWindow = Popup(title="Note", content=show,
                            size_hint=(None, None), size=(200, 100))
        popupWindow.open()


class Pop1(FloatLayout):
    def show_popup1(self):
        show = Pop1()
        popupWindow = Popup(title="Note", content=show,
                            size_hint=(None, None), size=(250, 100))
        popupWindow.open()


class Pop2(FloatLayout):
    def show_popup2(self):
        show = Pop2()
        popupWindow = Popup(title="Note", content=show,
                            size_hint=(None, None), size=(200, 100))
        popupWindow.open()


class Pop3(FloatLayout):
    def show_popup(self):
        show = Pop3()
        popupWindow = Popup(title="Note", content=show,
                            size_hint=(None, None), size=(250, 110))
        popupWindow.open()


class Pop4(FloatLayout):
    def show_popup(self):
        show = Pop4()
        popupWindow = Popup(title="Note", content=show,
                            size_hint=(None, None), size=(190, 100))
        popupWindow.open()

    def switch(self, *args):
        self.parent.parent.current = 'mainlogin'
        self.parent.parent.transition.direction = 'right'


class Pop5(FloatLayout):
    def show_popup(self):
        show = Pop5()
        popupWindow = Popup(title="Note", content=show,
                            size_hint=(None, None), size=(225, 105))
        popupWindow.open()


class Pop6(FloatLayout):
    def show_popup(self):
        show = Pop6()
        popupWindow = Popup(title="Note", content=show,
                            size_hint=(None, None), size=(200, 110))
        popupWindow.open()


class Pop7(FloatLayout):
    def show_popup(self):
        show = Pop7()
        popupWindow = Popup(title="Note", content=show,
                            size_hint=(None, None), size=(210, 110))
        popupWindow.open()


class Pop8(FloatLayout):
    def show_popup(self):
        show = Pop8()
        popupWindow = Popup(title="Note", content=show,
                            size_hint=(None, None), size=(235, 100))
        popupWindow.open()


class Pop9(FloatLayout):
    def show_popup(self):
        show = Pop9()
        popupWindow = Popup(title="Note", content=show,
                            size_hint=(None, None), size=(190, 110))
        popupWindow.open()


class Pop10(FloatLayout):
    def show_popup(self):
        popupWindow = Popup(title='RESULTS', title_color=(247/255, 242/255, 77/238, 1), title_size=21, title_align='center', content=Label(text=(
            userL[userIndex]+':    '+self.gameScore_list[0]+'\nPlayer1:    '+self.gameScore_list[1]), color=(83/255, 207/255, 186/238, 1), font_size=18), size_hint=(None, None), size=(210, 150), auto_dismiss=True)
        popupWindow.open()


class Pop11(FloatLayout):
    def show_popup(self):
        popupWindow = Popup(title='RESULTS', title_color=(247 / 255, 242 / 255, 77 / 238, 1), title_size=21, title_align='center', content=Label(text=(
            userL[userIndex] + ':    ' + self.gameScore_list[0] + '\nPlayer1:    ' + self.gameScore_list[1] + '\nPlayer2:    ' + self.gameScore_list[2]), color=(83 / 255, 207 / 255, 186 / 238, 1), font_size=18), size_hint=(None, None), size=(210, 160), auto_dismiss=True)
        popupWindow.open()


class Pop12(FloatLayout):
    def show_popup(self):
        popupWindow = Popup(title='RESULTS', title_color=(247 / 255, 242 / 255, 77 / 238, 1), title_size=21, title_align='center', content=Label(text=(userL[userIndex] + ':    ' + self.gameScore_list[0] + '\nPlayer1:    ' + self.gameScore_list[
                            1] + '\nPlayer2:    ' + self.gameScore_list[2] + '\nPlayer3:    ' + self.gameScore_list[3]), color=(83 / 255, 207 / 255, 186 / 238, 1), font_size=18), size_hint=(None, None), size=(210, 170), auto_dismiss=True)
        popupWindow.open()


class MemBattleV1(App):
    def build(self):
        return kv


class PuzzleWindow(Screen):
    pict_list = []
    index_list = []
    correct_index_list = []
    score = 0
    check_press = True

    def on_enter(self):
        self.ran_list4 = ran_list4 = pictures_matrix4()[1]
        ran_list4str = pictures_matrix4()[0]
        list_btn_pic = []
        for i in range(len(self.ids.puzz.ids.puzzG.children[:])):
            self.ids.puzz.ids.puzzG.children[i].disabled = False
            self.ids.puzz.ids.puzzG.children[i].a = ran_list4[i]
            self.ids.puzz.ids.puzzG.children[i].text = ran_list4str[i]
            self.ids.puzz.ids.puzzG.children[i].color = 0, 0, 0, 0
            self.ids.puzz.ids.puzzG.children[i].font_size = 0
            if self.check_press:
                self.ids.puzz.ids.puzzG.children[i].bind(
                    on_press=lambda x, child=self.ids.puzz.ids.puzzG.children[i], st=i: self.newspress(child, st))
        self.score = 0
        Clock.schedule_once(self.clocka, 2)

    def on_leave(self):
        for i in range(len(self.ids.puzz.ids.puzzG.children[:])):
            self.ids.puzz.ids.puzzG.children[i].a = "C:/Users/Maj/Desktop/markF.jpg"
            self.pict_list = []
            self.index_list = []
            self.correct_index_list = []
            self.ids.puzz.ids.puzzS.children[0].text = '0'
            self.check_press = False

    def newspress(self, child, i):
        child.a = self.ran_list4[i]
        pict = child.text
        self.index = i
        self.pict_list.append(pict)
        self.index_list.append(self.index)
        try:
            if self.index_list[0] != self.index_list[1] and self.pict_list[0] == self.pict_list[1]:
                self.correct_index_list.extend(self.index_list)
                Clock.schedule_once(self.clockcorrect, 0)
            else:
                Clock.schedule_once(self.clockcorrectdis, 0)
                Clock.schedule_once(self.clockcorrectenable, 2)
                Clock.schedule_once(self.clockcorrectdisable, 2)
                Clock.schedule_once(self.clockturn, 2)
        except IndexError:
            pass

    def clockturn(self, *args):
        self.ids.puzz.ids.puzzG.children[self.index_list[1]
                                         ].a = "C:/Users/Maj/Desktop/markF.jpg"
        self.ids.puzz.ids.puzzG.children[self.index_list[0]
                                         ].a = "C:/Users/Maj/Desktop/markF.jpg"
        self.pict_list = []
        self.index_list = []

    def clockcorrect(self, *args):
        self.score += 1
        self.ids.puzz.ids.puzzS.children[0].text = str(self.score)
        self.ids.puzz.ids.puzzG.children[self.index_list[1]].disabled = True
        self.ids.puzz.ids.puzzG.children[self.index_list[0]].disabled = True
        self.pict_list = []
        self.index_list = []

    # da ne dobim errorja za igralce, ki radi hitro igrajo
    def clockcorrectdis(self, *args):
        self.score -= 0.5
        self.ids.puzz.ids.puzzS.children[0].text = str(self.score)
        self.ids.puzz.ids.done.children[0].disabled = True
        for i in range(len(self.ids.puzz.ids.puzzG.children[:])):
            self.ids.puzz.ids.puzzG.children[i].disabled = True

    # da ne dobim errorja za igralce, ki radi hitro igrajo
    def clockcorrectenable(self, *args):
        for i in range(len(self.ids.puzz.ids.puzzG.children[:])):
            self.ids.puzz.ids.puzzG.children[i].disabled = False
            # to je za to da ne grem pre hitro nazaj, v kolikor to storim game crasha
            self.ids.puzz.ids.done.children[0].disabled = False

    # da ne dobim errorja za igralce, ki radi hitro igrajo
    def clockcorrectdisable(self, *args):
        for i in self.correct_index_list:
            self.ids.puzz.ids.puzzG.children[i].disabled = True

    def clocka(self, *args):
        for i in range(len(self.ids.puzz.ids.puzzG.children[:])):
            self.ids.puzz.ids.puzzG.children[i].a = "C:/Users/Maj/Desktop/markF.jpg"


class PuzzleWindowComp(Screen):
    pict_list = []
    index_list = []
    correct_index_list = []
    score = 0
    check_press = True

    def on_enter(self):
        self.ran_list5 = ran_list5 = pictures_matrix5()[1]
        ran_list5str = pictures_matrix5()[0]
        list_btn_pic = []
        for i in range(len(self.ids.puzzc.ids.puzzGC.children[:])):
            self.ids.puzzc.ids.puzzGC.children[i].disabled = False
            self.ids.puzzc.ids.puzzGC.children[i].a = ran_list5[i]
            self.ids.puzzc.ids.puzzGC.children[i].text = ran_list5str[i]
            self.ids.puzzc.ids.puzzGC.children[i].color = 1, 0, 0, 0
            self.ids.puzzc.ids.puzzGC.children[i].font_size = 0
            if self.check_press:
                self.ids.puzzc.ids.puzzGC.children[i].bind(
                    on_press=lambda x, child=self.ids.puzzc.ids.puzzGC.children[i], st=i: self.newspress(child, st))
        self.score = 0
        Clock.schedule_once(self.clocka, 3)

    def on_leave(self):
        for i in range(len(self.ids.puzzc.ids.puzzGC.children[:])):
            self.ids.puzzc.ids.puzzGC.children[i].a = "C:/Users/Maj/Desktop/markF.jpg"
            self.pict_list = []
            self.index_list = []
            self.correct_index_list = []
            self.ids.puzzc.ids.puzzSC.children[0].text = '0'
            self.check_press = False

    def newspress(self, child, i):
        child.a = self.ran_list5[i]
        pict = child.text
        self.index = i
        self.pict_list.append(pict)
        self.index_list.append(self.index)
        try:
            if self.index_list[0] != self.index_list[1] and self.pict_list[0] == self.pict_list[1]:
                print(self.pict_list, self.index_list)
                self.correct_index_list.extend(self.index_list)
                Clock.schedule_once(self.clockcorrect, 0)
            else:
                Clock.schedule_once(self.clockcorrectdis, 0)
                Clock.schedule_once(self.clockcorrectenable, 2)
                Clock.schedule_once(self.clockcorrectdisable, 2)
                Clock.schedule_once(self.clockturn, 2)
        except IndexError:
            pass

    def clockturn(self, *args):
        self.ids.puzzc.ids.puzzGC.children[self.index_list[1]
                                           ].a = "C:/Users/Maj/Desktop/markF.jpg"
        self.ids.puzzc.ids.puzzGC.children[self.index_list[0]
                                           ].a = "C:/Users/Maj/Desktop/markF.jpg"
        self.pict_list = []
        self.index_list = []

    def clockcorrect(self, *args):
        self.score += 1
        self.ids.puzzc.ids.puzzSC.children[0].text = str(self.score)
        self.ids.puzzc.ids.puzzGC.children[self.index_list[1]].disabled = True
        self.ids.puzzc.ids.puzzGC.children[self.index_list[0]].disabled = True
        self.pict_list = []
        self.index_list = []

    # da ne dobim errorja za igralce, ki radi hitro igrajo
    def clockcorrectdis(self, *args):
        self.score -= 0.5
        self.ids.puzzc.ids.puzzSC.children[0].text = str(self.score)
        self.ids.puzzc.ids.resign5.children[0].disabled = True
        self.ids.puzzc.ids.finish5.children[0].disabled = True
        for i in range(len(self.ids.puzzc.ids.puzzGC.children[:])):
            self.ids.puzzc.ids.puzzGC.children[i].disabled = True

    # da ne dobim errorja za igralce, ki radi hitro igrajo
    def clockcorrectenable(self, *args):
        self.ids.puzzc.ids.resign5.children[0].disabled = False
        self.ids.puzzc.ids.finish5.children[0].disabled = False
        for i in range(len(self.ids.puzzc.ids.puzzGC.children[:])):
            self.ids.puzzc.ids.puzzGC.children[i].disabled = False

    # da ne dobim errorja za igralce, ki radi hitro igrajo
    def clockcorrectdisable(self, *args):
        for i in self.correct_index_list:
            self.ids.puzzc.ids.puzzGC.children[i].disabled = True

    def clocka(self, *args):
        for i in range(len(self.ids.puzzc.ids.puzzGC.children[:])):
            self.ids.puzzc.ids.puzzGC.children[i].a = "C:/Users/Maj/Desktop/markF.jpg"


class PuzzleWindowComp4(Screen):
    pict_list = []
    index_list = []
    correct_index_list = []
    score = 0
    check_press = True

    def on_enter(self):
        self.ran_list4 = ran_list4 = pictures_matrix4()[1]
        ran_list4str = pictures_matrix4()[0]
        list_btn_pic = []
        for i in range(len(self.ids.puzzc4.ids.puzzGC4.children[:])):
            self.ids.puzzc4.ids.puzzGC4.children[i].disabled = False
            self.ids.puzzc4.ids.puzzGC4.children[i].a = ran_list4[i]
            self.ids.puzzc4.ids.puzzGC4.children[i].text = ran_list4str[i]
            self.ids.puzzc4.ids.puzzGC4.children[i].color = 1, 0, 0, 0
            self.ids.puzzc4.ids.puzzGC4.children[i].font_size = 0
            if self.check_press:
                self.ids.puzzc4.ids.puzzGC4.children[i].bind(
                    on_press=lambda x, child=self.ids.puzzc4.ids.puzzGC4.children[i], st=i: self.newspress(child, st))
        self.score = 0
        Clock.schedule_once(self.clocka, 2)

    def on_leave(self):
        for i in range(len(self.ids.puzzc4.ids.puzzGC4.children[:])):
            self.ids.puzzc4.ids.puzzGC4.children[i].a = "C:/Users/Maj/Desktop/markF.jpg"
            self.pict_list = []
            self.index_list = []
            self.correct_index_list = []
            self.ids.puzzc4.ids.puzzSC4.children[0].text = '0'
            self.check_press = False

    def newspress(self, child, i):
        child.a = self.ran_list4[i]
        pict = child.text
        self.index = i
        self.pict_list.append(pict)
        self.index_list.append(self.index)
        try:
            if self.index_list[0] != self.index_list[1] and self.pict_list[0] == self.pict_list[1]:
                self.correct_index_list.extend(self.index_list)
                Clock.schedule_once(self.clockcorrect, 0)
            else:
                Clock.schedule_once(self.clockcorrectdis, 0)
                Clock.schedule_once(self.clockcorrectenable, 2)
                Clock.schedule_once(self.clockcorrectdisable, 2)
                Clock.schedule_once(self.clockturn, 2)
        except IndexError:
            pass

    def clockturn(self, *args):
        self.ids.puzzc4.ids.puzzGC4.children[self.index_list[1]
                                             ].a = "C:/Users/Maj/Desktop/markF.jpg"
        self.ids.puzzc4.ids.puzzGC4.children[self.index_list[0]
                                             ].a = "C:/Users/Maj/Desktop/markF.jpg"
        self.pict_list = []
        self.index_list = []

    def clockcorrect(self, *args):
        self.score += 1
        self.ids.puzzc4.ids.puzzSC4.children[0].text = str(self.score)
        self.ids.puzzc4.ids.puzzGC4.children[self.index_list[1]
                                             ].disabled = True
        self.ids.puzzc4.ids.puzzGC4.children[self.index_list[0]
                                             ].disabled = True
        self.pict_list = []
        self.index_list = []

    # da ne dobim errorja za igralce, ki radi hitro igrajo
    def clockcorrectdis(self, *args):
        self.score -= 0.5
        self.ids.puzzc4.ids.puzzSC4.children[0].text = str(self.score)
        self.ids.puzzc4.ids.resign.children[0].disabled = True
        self.ids.puzzc4.ids.finish.children[0].disabled = True
        for i in range(len(self.ids.puzzc4.ids.puzzGC4.children[:])):
            self.ids.puzzc4.ids.puzzGC4.children[i].disabled = True

    # da ne dobim errorja za igralce, ki radi hitro igrajo
    def clockcorrectenable(self, *args):
        self.ids.puzzc4.ids.resign.children[0].disabled = False
        self.ids.puzzc4.ids.finish.children[0].disabled = False
        for i in range(len(self.ids.puzzc4.ids.puzzGC4.children[:])):
            self.ids.puzzc4.ids.puzzGC4.children[i].disabled = False

    # da ne dobim errorja za igralce, ki radi hitro igrajo
    def clockcorrectdisable(self, *args):
        for i in self.correct_index_list:
            self.ids.puzzc4.ids.puzzGC4.children[i].disabled = True

    def clocka(self, *args):
        for i in range(len(self.ids.puzzc4.ids.puzzGC4.children[:])):
            self.ids.puzzc4.ids.puzzGC4.children[i].a = "C:/Users/Maj/Desktop/markF.jpg"


class Puzzless2(Widget):
    class_instance = SellectionGrid().if_under()
    countswich = 0
    gameScore_list = []

    def finishDir(self):
        data = {'userid': UserID_L[userIndex],
                'diff': self.class_instance[1][0],
                'nof': self.class_instance[0][0]}
        headers = {'content-type': 'application/json'}
        if self.class_instance[0][0] == "2":
            if self.countswich == 0:
                self.countswich += 1
                self.parent.parent.current = 'startscC'
                self.gameScore_list.append(self.ids.resultscore.text)
            else:
                self.gameScore_list.append(self.ids.resultscore.text)
                Pop10.show_popup(self)
                data['gamescore'] = userL[userIndex] + ': ' + \
                    self.gameScore_list[0] + '  ' + \
                    'P2: ' + self.gameScore_list[1]
                r = requests.post("http://10.0.2.2:8100/rezultati",
                                  data=json.dumps(data), headers=headers)
                self.gameScore_list = []
                self.parent.parent.current = 'mainlogin'
                self.countswich = 0
        elif self.class_instance[0][0] == "3":
            if self.countswich <= 1:
                self.countswich += 1
                self.parent.parent.current = 'startscC'
                self.gameScore_list.append(self.ids.resultscore.text)
            else:
                self.gameScore_list.append(self.ids.resultscore.text)
                Pop11.show_popup(self)
                data['gamescore'] = userL[userIndex] + ': ' + self.gameScore_list[0] + '  ' + \
                    'P2: ' + self.gameScore_list[1] + \
                    '  ' + 'P3: ' + self.gameScore_list[2]
                r = requests.post("http://10.0.2.2:8100/rezultati",
                                  data=json.dumps(data), headers=headers)
                self.gameScore_list = []
                self.parent.parent.current = 'mainlogin'
                self.countswich = 0
        elif self.class_instance[0][0] == "4":
            if self.countswich <= 2:
                self.countswich += 1
                self.parent.parent.current = 'startscC'
                self.gameScore_list.append(self.ids.resultscore.text)
            else:
                self.gameScore_list.append(self.ids.resultscore.text)
                Pop12.show_popup(self)
                data['gamescore'] = userL[userIndex] + ': ' + self.gameScore_list[0] + '  ' + 'P2: ' + \
                    self.gameScore_list[1] + '  ' + 'P3: ' + \
                    self.gameScore_list[2] + '  ' + \
                    'P4: ' + self.gameScore_list[3]
                r = requests.post("http://10.0.2.2:8100/rezultati",
                                  data=json.dumps(data), headers=headers)
                self.gameScore_list = []
                self.parent.parent.current = 'mainlogin'
                self.countswich = 0

    def resignReset(self):
        self.countswich = 0
        gameScore_list = []
        self.parent.parent.current = 'mainlogin'


class Puzzless1Comp(Widget):
    class_instance = SellectionGrid().if_under()
    countswich = 0
    gameScore_list = []

    def finishDir(self):
        data = {'userid': UserID_L[userIndex],
                'diff': self.class_instance[1][0],
                'nof': self.class_instance[0][0]}
        headers = {'content-type': 'application/json'}
        if self.class_instance[0][0] == "2":
            if self.countswich == 0:
                self.countswich += 1
                self.parent.parent.current = 'startscC'
                self.gameScore_list.append(self.ids.resultscore4.text)
            else:
                self.gameScore_list.append(self.ids.resultscore4.text)
                Pop10.show_popup(self)
                data['gamescore'] = userL[userIndex] + ': ' + \
                    self.gameScore_list[0] + '  ' + \
                    'P2: ' + self.gameScore_list[1]
                r = requests.post("http://10.0.2.2:8100/rezultati",
                                  data=json.dumps(data), headers=headers)
                self.gameScore_list = []
                self.parent.parent.current = 'mainlogin'
                self.countswich = 0
        elif self.class_instance[0][0] == "3":
            if self.countswich <= 1:
                self.countswich += 1
                self.parent.parent.current = 'startscC'
                self.gameScore_list.append(self.ids.resultscore4.text)
            else:
                self.gameScore_list.append(self.ids.resultscore4.text)
                Pop11.show_popup(self)
                data['gamescore'] = userL[userIndex] + ': ' + self.gameScore_list[0] + '  ' + 'P2: ' + \
                    self.gameScore_list[1] + '  ' + 'P3: ' + \
                    self.gameScore_list[2] + '  ' + \
                    'P4: ' + self.gameScore_list[3]
                r = requests.post("http://10.0.2.2:8100/rezultati",
                                  data=json.dumps(data), headers=headers)
                self.gameScore_list = []
                self.parent.parent.current = 'mainlogin'
                self.countswich = 0
        elif self.class_instance[0][0] == "4":
            if self.countswich <= 2:
                self.countswich += 1
                self.parent.parent.current = 'startscC'
                self.gameScore_list.append(self.ids.resultscore4.text)
            else:
                self.gameScore_list.append(self.ids.resultscore4.text)
                Pop12.show_popup(self)
                data['gamescore'] = userL[userIndex] + ': ' + self.gameScore_list[0] + '  ' + 'P2: ' + \
                    self.gameScore_list[1] + '  ' + 'P3: ' + \
                    self.gameScore_list[2] + '  ' + \
                    'P4: ' + self.gameScore_list[3]
                r = requests.post("http://10.0.2.2:8100/rezultati",
                                  data=json.dumps(data), headers=headers)
                self.gameScore_list = []
                self.parent.parent.current = 'mainlogin'
                self.countswich = 0

    def resignReset(self):
        self.countswich = 0
        gameScore_list = []
        self.parent.parent.current = 'mainlogin'


kv = Builder.load_file("membattlev1.kv")

if __name__ == "__main__":
    MemBattleV1().run()

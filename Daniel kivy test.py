Enter file contents here#!/usr/bin/python
#Yazmeen's App, a scouting app for FIRST robotics
#Copyright (C) 2014 Camden County Technical Schools FRC Team 203
#Written by Juliet Summers
# This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.

#THE TABLET'S HEIGHT IS 720
import kivy
from kivy.lang import Builder
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
from kivy.properties import ObjectProperty
from collections import OrderedDict
from widgets import *
import os
Builder.load_file('layout-creator.kv')

TMP_PATH=os.path.join(os.getcwd(),'.tmp/tmp')
if not os.path.exists(os.path.dirname(TMP_PATH)): os.mkdir(os.path.dirname(TMP_PATH))

class FileChooserDialogue(FloatLayout):
    def chooseFile(self, file):
        self.file = file
        self.parent.parent.parent.dismiss()

class MainScreen(FloatLayout):
    def __init__(self, **kwards):
        super(MainScreen, self).__init__(**kwargs)

class LayoutCreator(FloatLayout):
    def __init__(self, **kwargs):
        super(LayoutCreator, self).__init__(**kwargs)
        self.matchRowSize=0 #counter for current width of widgets on the current match row
        self.teamRowSize=0 #counter for current width of widgets on the current team row
        self.matchWidgets=[]#list to be filled with the match widgets
        self.teamWidgets=[]#list to be filled with the team widgets
        self.matchWidgetsDict=OrderedDict({})#filled with all of our match widgets
        self.teamWidgetsDict=OrderedDict({})#filled with all of our team widgets
        self.workingList=self.matchWidgets#assigned to one of the two lists
        self.workingDict=self.matchWidgetsDict#assigned to one of the two dictionaries
        self.workingPreview=self.matchPreview
        self.deleteMode=False#when set to true, allows widgets to be deleted on touch
        self.saved=True

    def tabSwitch(self,tab):
        self.workingDict=tab.dict
        self.workingList=tab.list
        self.workingPreview=tab.preview

    def on_touch_up(self, touch):
        if self.closed and self.deleteMode:#if delete mode is on and the sidebar is closed
            for x in self.workingList[:]:#loop through the list of widgets
                if x.collide_point(*x.parent.to_widget(*touch.pos,relative=True)):#if you touched a widget,
                    if self.workingList is self.matchWidgets:#check which tab we're on,
                        self.matchRowSize -= x.width #subtract its width from the current row width
                    else:
                        self.teamRowSize -= x.width
                    del self.workingDict[x.label.text]#remove it from the dictionary
                    x.removeSelf()#call its removeSelf method
                    self.workingList.remove(x)#and remove it from our list of widgets
                    return True
            return super(LayoutCreator, self).on_touch_up(touch) #let the touch propogate
        else:#we didn't click on any widgets
            return super(LayoutCreator, self).on_touch_up(touch) #let the touch propogate

    def deleteAll(self):
        self.saved=False
        for x in self.workingList[:]:#empties everything out
            if self.workingList is self.matchWidgets:#check which tab we're on
                self.matchRowSize -= x.width
            else:
                self.teamRowSize -= x.width
            del self.workingDict[x.label.text]
            x.removeSelf()
            self.workingList.remove(x)
        self.workingPreview.height=200 #resets the height to default

    def clickEdit(self,widgetToAdd):
        if widgetToAdd == 'counter':
            self.workingList.append(Counter(self,size_hint=(None,None)))
        elif widgetToAdd == 'checkbox':
            self.workingList.append(YesNo(self,size_hint=(None,None)))
        elif widgetToAdd == 'textbox':
            self.workingList.append(TextBox(self,size_hint=(None,None)))
        self.workingPreview.add_widget(self.workingList[-1])

    def saveLayout(self):
        fileChooser=FileChooserDialogue()
        Popup(title='Save',content=fileChooser,size_hint=(.5,.5),
            on_dismiss=lambda x,y=fileChooser: self.saveToFile(y.file)).open()

    def saveToFile(self,file):
        if not file: return None #if file is empty, the popup was canceled and we shouldn't do anything
        if not file.endswith('.layout'):
            file = file + '.layout'
        with open(file,'w') as f:
            f.write(repr(self.teamWidgetsDict))#write the string representation of the dictionaries
            f.write('\n')#newline required so it'll separate the lines
            f.write(repr(self.matchWidgetsDict))
        self.saved=True

    def loadLayout(self):
        fileChooser=FileChooserDialogue()
        Popup(title='Load',content=fileChooser,size_hint=(.5,.5),
            on_dismiss=lambda x,y=fileChooser: self.loadFromFile(y.file)).open()

    def loadFromFile(self,file):
        if not file: return None #if file is empty, the popup was canceled and we shouldn't do anything
        if not os.path.isfile(file):
            return None #not a file, don't open it

        f=open(file,'r')

        for x in self.panel.tab_list:
            self.panel.switch_to(x)
            self.deleteAll()

            try:
                line=f.readline()

                #check which tab we're on, and add the line to the proper dictionary
                if self.workingDict is self.matchWidgetsDict:
                    self.matchWidgetsDict=eval(line)
                    self.workingDict=self.matchWidgetsDict
                elif self.workingDict is self.teamWidgetsDict:
                    self.teamWidgetsDict=eval(line)
                    self.workingDict=self.teamWidgetsDict

                for name,data in self.workingDict.iteritems():
                    if data['type'] == 'counter':
                        self.workingList.append(LoadedCounter(self,(lambda: name,
                            lambda: data['buttons']),size_hint=(None,None)))

                    elif data['type'] == 'checkbox':
                        self.workingList.append(LoadedYesNo(self,(lambda: name,),size_hint=(None,None)))

                    elif data['type'] == 'textbox':
                        self.workingList.append(LoadedTextBox(self,(lambda: name,),size_hint=(None,None)))

                    self.workingPreview.add_widget(self.workingList[-1])

                    if self.workingList is self.matchWidgets:#check which tab we're on
                        if self.matchRowSize+self.workingList[-1].width > 1024:
                            self.workingPreview.height+=225
                            self.matchRowSize = self.workingList[-1].width
                        else:
                            self.matchRowSize+=self.workingList[-1].width
                    else:
                        if self.teamRowSize+self.workingList[-1].width > 1024:
                            self.workingPreview.height+=225
                            self.teamRowSize = self.workingList[-1].width
                        else:
                            self.teamRowSize+=self.workingList[-1].width
            except:
                Popup(title='Error',size_hint=(.5,.5),content=Label(
                    text='Something went wrong and this is all Yazmeen\'s fault.')).open()

        f.close()


class AppThing(App):
    def __init__(self):
        super(AppThing, self).__init__()
        self.layoutCreator=LayoutCreator()

    def on_start(self):#loadFromFile handles checking if the file exists for us, so we're good
        self.layoutCreator.loadFromFile(TMP_PATH)
        if os.path.isfile(TMP_PATH): os.remove(TMP_PATH)

    def on_stop(self):
        if not self.layoutCreator.saved:
            with open(TMP_PATH,'w') as f:
                f.write(repr(self.layoutCreator.teamWidgetsDict))
                f.write('\n')#newline required for it to recognize separated lines
                f.write(repr(self.layoutCreator.matchWidgetsDict))

    def on_pause(self):
        if not self.layoutCreator.saved:#there's no guarantee we'll be resumed, so save
            with open(TMP_PATH,'w') as f:
                f.write(repr(self.layoutCreator.teamWidgetsDict))
                f.write('\n')
                f.write(repr(self.layoutCreator.matchWidgetsDict))
        return True

    def on_resume(self):
        pass

    def build(self):
        self.title="Yazmeen's App"
        return self.layoutCreator

if __name__=='__main__':
    AppThing().run()


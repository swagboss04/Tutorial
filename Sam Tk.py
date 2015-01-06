#Making Mahself A GUI

import Tkinter

class simpleapp_tk(Tkinter.Tk):
  def__init__(self,parent):
  Tkinter.Tk.__init__(self,parent)
  self.parent = parent
  self.initialize()
  
  def initialize(self):
  self.grid()
  
  self.entry = Tkinter.Entry(self)
  self.entry.grid(column=0, row=0, sticky='EW')
  
  button = Tkinter.Button(self, text=u"Click me !")
  
if__name__="__main__"
  app = simpleapp_tk(None)
  app.title('myapplicationj')
  app.mainloop()
  
    
    

#Making Mahself A GUI

import Tkinter

class simpleapp_tk(Tkinter.Tk):
  def_init(self,parent):
    Tkinter.Tk._init_(self,parent)
    self.parent = parent
    self.initialize()
  
  def initialize(self):
    self.grid()

if__name__="__main__"
  app = app.simpleapp_tk(None)
  app.title('myapplicationj')
  app.mainloop()
  
    
    

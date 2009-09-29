#! /usr/bin/env python
#***********************************************************
#* Software License Agreement (BSD License)
#*
#*  Copyright (c) 2009, Willow Garage, Inc.
#*  All rights reserved.
#*
#*  Redistribution and use in source and binary forms, with or without
#*  modification, are permitted provided that the following conditions
#*  are met:
#*
#*   * Redistributions of source code must retain the above copyright
#*     notice, this list of conditions and the following disclaimer.
#*   * Redistributions in binary form must reproduce the above
#*     copyright notice, this list of conditions and the following
#*     disclaimer in the documentation and/or other materials provided
#*     with the distribution.
#*   * Neither the name of the Willow Garage nor the names of its
#*     contributors may be used to endorse or promote products derived
#*     from this software without specific prior written permission.
#*
#*  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#*  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#*  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
#*  FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
#*  COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#*  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
#*  BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#*  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
#*  CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
#*  LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
#*  ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
#*  POSSIBILITY OF SUCH DAMAGE.
#***********************************************************


import roslib; roslib.load_manifest('dynamic_reconfigure')
import rospy
import dynamic_reconfigure.dynamic_reconfigure as dynamic_reconfigure
import wx

class DynamicReconfigureBoolean(wx.CheckBox):
    def __init__(self, parent, name, value, min, max):
        self.name = name
        wx.CheckBox.__init__(self, parent, wx.ID_ANY)
        self.SetValue(value)
        self.Bind(wx.EVT_CHECKBOX, self.update)

    def update(self, event):
        print self.name, self.GetValue()
        rslt = self.GetParent().reconf.update_configuration({ self.name:self.GetValue() }).config
        self.SetValue(rslt.__getattribute__(self.name))

class DynamicReconfigureString(wx.TextCtrl):
    def __init__(self, parent, name, value, min, max):
        self.name = name
        wx.TextCtrl.__init__(self, parent, wx.ID_ANY, style = wx.TE_PROCESS_ENTER)
        self.SetValue(value)
        self.Bind(wx.EVT_TEXT_ENTER, self.update)
        self.Bind(wx.EVT_KILL_FOCUS, self.update)
    
    def SetValue(self, value):
        wx.TextCtrl.SetValue(self, value)
        self.old_value = value

    def update(self, event):
        new_value = self.GetValue()
        if self.old_value == new_value:
            return
        rslt = self.GetParent().reconf.update_configuration({ self.name:new_value }).config
        self.SetValue(rslt.__getattribute__(self.name))
        print rslt

class DynamicReconfigureDouble(wx.TextCtrl):
    def __init__(self, parent, name, value, min, max):
        wx.TextCtrl.__init__(self, parent, wx.ID_ANY)
        self.SetValue(str(value))

class DynamicReconfigureInteger(wx.Slider):
    def __init__(self, parent, name, value, min, max):
        wx.Slider.__init__(self, parent, wx.ID_ANY, value, min, max,
                style = wx.SL_AUTOTICKS | wx.SL_HORIZONTAL | wx.SL_LABELS)
        print name, value, min, max

DynamicReconfigureWidget = {
        'int8':DynamicReconfigureBoolean,
        'int32':DynamicReconfigureInteger,
        'float64':DynamicReconfigureDouble,
        'string':DynamicReconfigureString,
        }
                    
class DynamicReconfigurePanel(wx.Panel):
    def __init__(self, parent, node):
        wx.Panel.__init__(self, parent, wx.ID_ANY)
        self.reconf = dynamic_reconfigure.DynamicReconfigure(node)
        config = self.reconf.get_configuration()
        
        sizer = wx.FlexGridSizer(0, 2)
        sizer.SetFlexibleDirection(wx.BOTH)
        #sizer.SetFlexibleDirection(wx.HORIZONTAL)
        #sizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_ALL)
        sizer.AddGrowableCol(1, 1)
        flags = {
                'int8':wx.ALIGN_LEFT,
                'int32':wx.EXPAND,
                'string':wx.EXPAND,
                'float64':wx.EXPAND,
                }
        for name, type in zip(config.config.__slots__, config.config._slot_types):
            dir(config.config)
            val = config.config.__getattribute__(name)
            min = config.min.__getattribute__(name)
            max = config.max.__getattribute__(name)
            sizer.Add(wx.StaticText(self, wx.ID_ANY, name+":"),1,
                    wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_RIGHT)
            sizer.Add(DynamicReconfigureWidget[type](self, name, val, min, max),0,flags[type])
            #sizer.Add(wx.StaticLine(self), 1, wx.EXPAND)
            #sizer.Add(wx.StaticLine(self), 1, wx.EXPAND)

        self.SetSizer(sizer)
        #self.Center()

class MainWindow(wx.Frame):
    def __init__(self, node):
        wx.Frame.__init__(self, None, wx.ID_ANY, 'Reconfigure '+node)
        print node
        self.filemenu = wx.Menu()
        self.filemenu.Append(wx.ID_EXIT, "E&xit"," Exit the program")
        self.menubar = wx.MenuBar()
        self.menubar.Append(self.filemenu,"&File")
        self.SetMenuBar(self.menubar)
        wx.EVT_MENU(self, wx.ID_EXIT, self.on_exit)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(DynamicReconfigurePanel(self, node), 1, wx.EXPAND|wx.ALL, 5)
        self.SetSizer(sizer)
        #self.SetMaxSize(wx.Size(1500,1500))

    def on_exit(self, e):
        self.Close(True)
            
    def on_error(self):
        self.Raise()
    
if __name__ == '__main__':
    argv = rospy.myargv()
    if (len(argv) != 2):
        print "usage: reconfigure_gui.py <node_name>"
        exit(1)
    rospy.init_node('reconfigure_gui', anonymous = True)
    app = wx.PySimpleApp()
    frame=MainWindow(argv[1])
    frame.Show()
    frame.SetMinSize(frame.GetEffectiveMinSize())
    app.MainLoop()

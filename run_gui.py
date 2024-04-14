import wx
class MyFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="My GUI Application", size=(400, 300))
        panel = wx.Panel(self)
        label = wx.StaticText(panel, label="Hello, WxPython!", pos=(100, 50))
        button = wx.Button(panel, label="Click Me!", pos=(150, 100))
        button.Bind(wx.EVT_BUTTON, self.on_button_click)
    def on_button_click(self, event):
        wx.MessageBox("Button clicked!", "Info", wx.OK | wx.ICON_INFORMATION)
if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    frame.Show()
app.MainLoop()
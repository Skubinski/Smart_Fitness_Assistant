import wx
from UI.login_GUI import LoginApp

def main():
    app = wx.App(False)
    frame = LoginApp(None)
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
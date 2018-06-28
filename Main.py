# -*-coding:utf-8 -*-

import wx
import time
import datetime


class MyFrame1(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, id=wx.ID_ANY, title=u"極簡鬧鐘", pos=wx.DefaultPosition, size=wx.Size(300, 350),
                          style=wx.CAPTION | wx.CLOSE_BOX | wx.MINIMIZE_BOX | wx.TAB_TRAVERSAL)


        self.SetBackgroundColour('White')


        # --- Default
        self.Msg = u"起床拉~"  # 提醒內容
        self.BeepPath = r"C:\Windows\Media\tada.wav"  # 鬧鈴聲音
        self.Sound = wx.Sound(self.BeepPath)
        self.Stime = 5  # 貪睡時間
        self.CDtime = None  # 倒計時時間
        self.Label_SWcontentlist = []  # 碼表紀錄

        # --- Menu
        self.m_menubar = wx.MenuBar(0)
        self.Menu = wx.Menu()
        self.menuSetting = wx.MenuItem(self.Menu, 1, u"鬧鈴聲音", help="")
        self.Menu.AppendItem(self.menuSetting)
        self.menuItem1 = wx.MenuItem(self.Menu, 2, u"提醒內容", help="")
        self.Menu.AppendItem(self.menuItem1)

        self.m_menubar.Append(self.Menu, u"設定")

        self.SetMenuBar(self.m_menubar)

        # --- statusBar
        # self.m_statusBar = self.CreateStatusBar(1, wx.ST_SIZEGRIP, wx.ID_ANY)



        # --- 系統時間 小區塊

        self.Label_Nowtime = wx.StaticText(self, wx.ID_ANY, time.strftime("%Y/%m/%d %H:%M:%S"), (30, 5),
                                           wx.Size(-1, -1), 0)

        self.Label_Nowtime.SetFont(wx.Font(18, wx.DECORATIVE, wx.ITALIC, wx.NORMAL))

        #  ---  Choice 小區塊
        m_choice1Choices = [u"倒數計時", u"鬧鐘", u"碼表"]
        self.m_choice1 = wx.Choice(self, wx.ID_ANY, (104, 40), wx.DefaultSize, m_choice1Choices, 0)
        self.m_choice1.SetSelection(1)  # 鬧鐘

        # --- 功能


        #  鬧鐘  AlarmClock

        self.Ctrl_ACCustom = wx.TextCtrl(self, wx.ID_ANY, time.strftime("%H:%M:%S"), (35, 90), wx.Size(200, 40),
                                         wx.TE_CENTRE)
        self.Ctrl_ACCustom.SetFont(wx.Font(24, wx.DECORATIVE, wx.ITALIC, wx.NORMAL))

        self.ChkBox_ACSnooze = wx.CheckBox(self, wx.ID_ANY, u"貪睡功能", (90, 140), wx.Size(-1, -1))
        self.Label_ACcontent = wx.StaticText(self, wx.ID_ANY, u"設定鬧鈴時間", (105, 70), wx.Size(-1, -1))

        Snoozelist = [str(i) for i in range(1, 16)]
        self.Choice_Snooze = wx.Choice(self, wx.ID_ANY, (170, 138), wx.Size(40, 20), Snoozelist, 0)
        self.Choice_Snooze.SetSelection(0)  # 鬧鐘
        self.Choice_Snooze.Disable()

        self.GroupAC = [
            self.Ctrl_ACCustom,
            self.ChkBox_ACSnooze,
            self.Label_ACcontent,
            self.Choice_Snooze
        ]
        # [i.Hide() for i in [self.Ctrl_ACCustom, self.ChkBox_ACSnooze]]


        # 倒數計時 CountDown

        # 單選項
        self.Radio_Min5 = wx.RadioButton(self, wx.ID_ANY, u"5分", (15, 70), wx.Size(-1, -1))
        self.Radio_Min10 = wx.RadioButton(self, wx.ID_ANY, u"10分", (80, 70), wx.Size(-1, -1))
        self.Radio_Min15 = wx.RadioButton(self, wx.ID_ANY, u"15分", (80 + 65, 70), wx.Size(-1, -1))
        self.Radio_MinCustom = wx.RadioButton(self, wx.ID_ANY, u"自定義", (80 + 65 + 65, 70), wx.Size(-1, -1))

        self.Ctrl_CDCustom = wx.TextCtrl(self, wx.ID_ANY, u"00:05:00", (35, 90), wx.Size(200, 40), wx.TE_CENTRE)
        self.Ctrl_CDCustom.SetFont(wx.Font(24, wx.DECORATIVE, wx.ITALIC, wx.NORMAL))

        self.ChkBox_CDRepeat = wx.CheckBox(self, wx.ID_ANY, u"自動重複", (70, 140), wx.Size(-1, -1))
        self.ChkBox_CDAlart = wx.CheckBox(self, wx.ID_ANY, u"彈窗提醒", (150, 140), wx.Size(-1, -1))

        self.GroupCD = [
            self.Radio_Min5,
            self.Radio_Min10,
            self.Radio_Min15,
            self.Radio_MinCustom,
            self.Ctrl_CDCustom,
            self.ChkBox_CDRepeat,
            self.ChkBox_CDAlart
        ]

        [i.Hide() for i in self.GroupCD]

        # 碼表
        self.Label_Stopwatch = wx.StaticText(self, wx.ID_ANY, u"00:00:00", (35, 90), wx.Size(200, 40), wx.TE_CENTRE)
        self.Label_Stopwatch.SetFont(wx.Font(24, wx.DECORATIVE, wx.ITALIC, wx.NORMAL))

        self.Label_SWcontent = wx.StaticText(self, wx.ID_ANY, u"", (110, 200), wx.Size(60, 85), wx.ST_NO_AUTORESIZE)

        self.GroupSW = [
            self.Label_Stopwatch,
            self.Label_SWcontent
        ]

        [i.Hide() for i in self.GroupSW]

        #  --- Play_btn Stop_btn
        self.btn_Play = wx.Button(self, wx.ID_ANY, u"開始", (77, 170), wx.Size(60, -1), 0)

        self.btn_Stop = wx.Button(self, wx.ID_ANY, u"停止", (100, 170), wx.Size(60, -1), 0)
        self.btn_Reset = wx.Button(self, wx.ID_ANY, u"重設", (147, 170), wx.Size(60, -1), 0)
        self.btn_Pause = wx.Button(self, wx.ID_ANY, u"暫停", (77, 170), wx.Size(60, -1), 0)

        [i.Hide() for i in [self.btn_Stop, self.btn_Pause]]

        self.createTimer()
        self.bindEvent()
        self.bindMenuEvent()



    def bindMenuEvent(self):
        self.Bind(wx.EVT_MENU, self.OnBeepSetting, id=1)
        self.Bind(wx.EVT_MENU, self.OnMsgSetting, id=2)

    def bindEvent(self):
        self.btn_Pause.Bind(wx.EVT_BUTTON, self.OnPause)
        self.btn_Play.Bind(wx.EVT_BUTTON, self.OnPlay)
        self.btn_Stop.Bind(wx.EVT_BUTTON, self.OnStop)
        self.btn_Reset.Bind(wx.EVT_BUTTON, self.OnReset)
        self.Radio_Min5.Bind(wx.EVT_RADIOBUTTON, self.min5)
        self.Radio_Min10.Bind(wx.EVT_RADIOBUTTON, self.min10)
        self.Radio_Min15.Bind(wx.EVT_RADIOBUTTON, self.min15)
        self.Radio_MinCustom.Bind(wx.EVT_RADIOBUTTON, self.mincustom)
        self.m_choice1.Bind(wx.EVT_CHOICE, self.layout)
        self.ChkBox_ACSnooze.Bind(wx.EVT_CHECKBOX, self.ACstime)

    def ACstime(self, event):

        if self.ChkBox_ACSnooze.Value:
            self.Choice_Snooze.Enable()

        else:
            self.Choice_Snooze.Disable()

    def layout(self, event):
        #    Layout

        x = self.m_choice1.GetSelection()
        print (x)
        # 0:CD 1:AC 2:SW
        if x == 0:
            hidelist = self.GroupSW + self.GroupAC
            showlist = self.GroupCD
            hide = [i.Hide() for i in hidelist]
            show = [i.Show() for i in showlist]

        if x == 1:
            hidelist = self.GroupSW + self.GroupCD
            showlist = self.GroupAC
            hide = [i.Hide() for i in hidelist]
            show = [i.Show() for i in showlist]

        if x == 2:
            hidelist = self.GroupCD + self.GroupAC
            showlist = self.GroupSW
            hide = [i.Hide() for i in hidelist]
            show = [i.Show() for i in showlist]

    def min5(self, event):
        self.Ctrl_CDCustom.SetLabel("00:05:00")
        self.Ctrl_CDCustom.SetEditable(False)

    def min10(self, event):
        self.Ctrl_CDCustom.SetLabel("00:10:00")
        self.Ctrl_CDCustom.SetEditable(False)

    def min15(self, event):
        self.Ctrl_CDCustom.SetLabel("00:15:00")
        self.Ctrl_CDCustom.SetEditable(False)

    def mincustom(self, event):
        self.Ctrl_CDCustom.SetEditable(True)

    def OnAboutDig(self, event):
        dlg = wx.MessageDialog(self, self.Msg, u"鬧鈴提醒", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    def OnAlarmMsgDig(self, event):
        dlg = wx.MessageDialog(self, self.Msg, u'鬧鈴提醒')
        dlg.SetOKCancelLabels(u"關閉鬧鐘", u"在等會兒")
        if dlg.ShowModal() == wx.ID_OK:
            self.OnStop(event)
        else:
            m5 = datetime.datetime.now() + datetime.timedelta(minutes=int(self.Stime))
            self.Ctrl_ACCustom.SetLabel(m5.strftime("%H:%M:%S"))
        dlg.Destroy()

    def OnBeepSetting(self, event):
        dlg = wx.FileDialog(self, u"聲音檔案路徑", wildcard="Wav files (*.wav)|*.wav")
        if dlg.ShowModal() == wx.ID_OK:
            self.Sound = wx.Sound(dlg.Path)

        dlg.Destroy()

    def OnMsgSetting(self, event):
        dlg = wx.TextEntryDialog(self, u'設定鬧鈴提醒內容', u"設定")
        dlg.SetValue(self.Msg)

        if dlg.ShowModal() == wx.ID_OK:
            self.Msg = dlg.GetValue()
        dlg.Destroy()

    def OnPlay(self, event):
        print "OnPlay"
        x = self.m_choice1.GetSelection()
        self.m_choice1.Disable()

        [i.Hide() for i in [self.btn_Play, self.btn_Reset, self.btn_Pause]]
        [i.Show() for i in [self.btn_Stop]]

        if x == 0:
            print ("0")

            self.Ctrl_CDCustom.SetEditable(False)
            self.CDtime = self.Ctrl_CDCustom.Value
            h, m, s = self.Ctrl_CDCustom.Value.split(":")
            self.CDendtime = datetime.datetime.now() + datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))


            self.timeCD.Start(1000)

        if x == 1:
            print ("1")

            self.Ctrl_ACCustom.SetEditable(False)
            self.ACtime = self.Ctrl_ACCustom.Value
            self.timeAC.Start(1000)

        if x == 2:
            print ("2")
            [i.Show() for i in [self.btn_Reset, self.btn_Pause]]
            [i.Hide() for i in [self.btn_Play, self.btn_Stop]]
            self.SWtime = self.Label_Stopwatch.GetLabel()
            self.timeSW.Start(1000)

    def OnPause(self, event):
        self.Label_SWcontentlist.append(self.Label_Stopwatch.GetLabel())
        self.Label_SWcontentlist.reverse()
        self.Label_SWcontent.SetLabel("\n".join(self.Label_SWcontentlist))
        self.Label_SWcontentlist.reverse()

    def OnStop(self, event):
        print "OnStop"
        [i.Hide() for i in [self.btn_Stop, ]]
        [i.Show() for i in [self.btn_Play, self.btn_Reset]]

        self.m_choice1.Enable()

        x = self.m_choice1.GetSelection()
        if x == 0:
            self.timeCD.Stop()

        if x == 1:
            self.Ctrl_ACCustom.SetBackgroundColour("255,255,255")
            self.Ctrl_ACCustom.SetEditable(True)
            self.timeAC.Stop()
        if x == 2:
            self.timeSW.Stop()

    def OnReset(self, event):
        x = self.m_choice1.GetSelection()

        if x == 0:
            self.Ctrl_CDCustom.SetEditable(True)
            self.Radio_MinCustom.SetValue(True)
            self.Ctrl_CDCustom.SetValue(self.CDtime)

        if x == 1:
            self.Ctrl_ACCustom.SetValue(self.ACtime)

        if x == 2:
            self.Label_Stopwatch.SetLabel("00:00:00")
            self.OnStop(event)

    def _OnRefresh(self, event):

        '''
        系統時間
        '''

        NowTime = time.strftime("%Y/%m/%d %H:%M:%S")
        self.Label_Nowtime.SetLabel(NowTime)

    def _OnCD(self, event):

        diff = self.CDendtime - datetime.datetime.now()

        if diff.total_seconds() <= 0:
            self.Ctrl_CDCustom.SetValue(self.CDtime)
            h, m, s = self.CDtime.split(":")
            self.CDendtime = self.CDendtime + datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s))
            self.Sound.Play()

            if not self.ChkBox_CDRepeat.Value: self.OnStop(event)
            if self.ChkBox_CDAlart.Value: self.OnAboutDig(event)
        else:

            self.Ctrl_CDCustom.SetValue((str(diff)).split(".")[0])

    def _OnSW(self, event):

        h, m, s = self.Label_Stopwatch.GetLabel().split(":")
        end = datetime.timedelta(hours=int(h), minutes=int(m), seconds=int(s)) + datetime.timedelta(seconds=1)
        self.Label_Stopwatch.SetLabel(str(end))

    def _OnAC(self, event):

        CustomACtext = self.Ctrl_ACCustom.Value
        label_nowtime = self.Label_Nowtime.GetLabelText().split(" ")[1]

        if CustomACtext == label_nowtime:
            self.Sound.Play()
            if self.ChkBox_ACSnooze.Value:
                self.Stime = self.Choice_Snooze.GetString(self.Choice_Snooze.GetSelection())
                self.OnAlarmMsgDig(event)
            else:
                self.OnAboutDig(event)
                self.OnStop(event)

    def createTimer(self):
        # 現在時間
        self.timer1 = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self._OnRefresh, self.timer1)
        self.timer1.Start(1000)

        # timeAC 鬧鐘功能
        self.timeAC = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self._OnAC, self.timeAC)

        # timeCD 倒計時功能
        self.timeCD = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self._OnCD, self.timeCD)

        # timeSW 碼表
        self.timeSW = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self._OnSW, self.timeSW)


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame1().Show()
    app.MainLoop()

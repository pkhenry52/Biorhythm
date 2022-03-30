
import wx
import os
import webbrowser

import wx.adv
from wx.adv import CalendarCtrl

from datetime import date
import matplotlib.dates
import matplotlib.pyplot as plt
from numpy import array, sin, pi

from matplotlib.backends.backend_wxagg import \
    FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wx import \
    NavigationToolbar2Wx as NavigationToolbar
from matplotlib.figure import Figure


class InputForm(wx.Frame):
    '''The main entery form which contains the grid and the
    plot area for the biorhythm chart'''
    def __init__(self):

        super().__init__(None, wx.ID_ANY,
                         title='Biorhythm Chart',
                         size=(1300, 840))

        # create the form level sizer
        Main_Sizer = wx.BoxSizer(wx.HORIZONTAL)

        # add the sizer for the left side widgets
        sizerL = wx.BoxSizer(wx.VERTICAL)

        gbs = wx.GridBagSizer(10, 15)

        self.lblname = wx.StaticText(self, label="  Your name:")
        self.editname = wx.TextCtrl(self, value=" ", size=(140, 35))

        self.lblDOB = wx.StaticText(self, label="  Date of Birth: *")
        self.editDOB = wx.StaticText(self, label='')
        self.calDOB = wx.Button(self, id=101, size=(45, 35))
        self.calstart = wx.Button(self, id=102, size=(45, 35))
        self.calinter = wx.Button(self, id=103, size=(45, 35))
        if os.path.isfile(os.getcwd() + os.sep + 'Biorhythm' +
                          os.sep + 'btnCal.ico'):
            bmp = wx.Bitmap(os.getcwd() + os.sep + 'btnCal.ico')
            self.calDOB.SetBitmap(bmp)
            self.calstart.SetBitmap(bmp)
            self.calinter.SetBitmap(bmp)
        else:
            btnlbl = 'Calendar'
            self.calDOB.SetLabel(btnlbl)
            self.calstart.SetLabel(btnlbl)
            self.calinter.SetLabel(btnlbl)

        self.Bind(wx.EVT_BUTTON, self.OnCal, self.calDOB)
        self.Bind(wx.EVT_BUTTON, self.OnCal, self.calstart)
        self.Bind(wx.EVT_BUTTON, self.OnCal, self.calinter)

        self.lblstart = wx.StaticText(self, label="  Plot Start Date:  ")
        yy, mm, dd = [int(i) for i in str(date.today()).split('-')]
        # set default start date to present day
        todaydate = str(dd) + '/' + str(mm) + '/' + str(yy)
        self.editstart = wx.StaticText(self, label=todaydate)

        self.lblspan = wx.StaticText(self, label="  Days in Plot:")
        # Set a default value of 29 days
        self.editspan = wx.TextCtrl(self, value="29", size=(140, 35))

        self.lblinter = wx.StaticText(self, label="  Date of Interest:  ")
        self.editinter = wx.StaticText(self, label=todaydate)

        gbs.Add(self.lblname, pos=(0, 0), flag=wx.EXPAND)
        gbs.Add(self.editname, pos=(0, 1), flag=wx.EXPAND)

        gbs.Add(self.lblDOB, pos=(1, 0), flag=wx.EXPAND)
        gbs.Add(self.editDOB, pos=(1, 1), flag=wx.EXPAND)
        gbs.Add(self.calDOB, pos=(1, 2), flag=wx.EXPAND)

        gbs.Add(self.lblstart, pos=(2, 0), flag=wx.EXPAND)
        gbs.Add(self.editstart, pos=(2, 1), flag=wx.EXPAND)
        gbs.Add(self.calstart, pos=(2, 2), flag=wx.EXPAND)

        gbs.Add(self.lblspan, pos=(3, 0), flag=wx.EXPAND)
        gbs.Add(self.editspan, pos=(3, 1), flag=wx.EXPAND)

        gbs.Add(self.lblinter, pos=(4, 0), flag=wx.EXPAND)
        gbs.Add(self.editinter, pos=(4, 1), flag=wx.EXPAND)
        gbs.Add(self.calinter, pos=(4, 2), flag=wx.EXPAND)        

        # set up the check boxs for the charts to be ploted
        hdr1 = wx.StaticText(self, id=wx.ID_ANY, label='Primary\nCurves')
        hdr2 = wx.StaticText(self, id=wx.ID_ANY, label='Seconary\nCurves')
        self.cb1 = wx.CheckBox(self, label='Physical')
        self.cb2 = wx.CheckBox(self, label='Emotional')
        self.cb3 = wx.CheckBox(self, label='Intellegence')
        self.cb4 = wx.CheckBox(self, label='Intuitive')
        self.cb5 = wx.CheckBox(self, label='Awareness')
        self.cb6 = wx.CheckBox(self, label='Wisdom')
        self.cb7 = wx.CheckBox(self, label='Passion')
        # set the primary charts checkboxs
        self.cb1.SetValue(True)
        self.cb2.SetValue(True)
        self.cb3.SetValue(True)
        gbs.Add(hdr1, pos=(5, 0), flag=wx.EXPAND)
        gbs.Add(hdr2, pos=(5, 1), flag=wx.EXPAND)
        gbs.Add(self.cb1, pos=(6, 0), flag=wx.EXPAND)
        gbs.Add(self.cb2, pos=(7, 0), flag=wx.EXPAND)
        gbs.Add(self.cb3, pos=(8, 0), flag=wx.EXPAND)
        gbs.Add(self.cb4, pos=(6, 1), flag=wx.EXPAND)
        gbs.Add(self.cb5, pos=(7, 1), flag=wx.EXPAND)
        gbs.Add(self.cb6, pos=(8, 1), flag=wx.EXPAND)
        gbs.Add(self.cb7, pos=(9, 1), flag=wx.EXPAND)

#        btnsizer = wx.BoxSizer(wx.HORIZONTAL)
        # add button to plot curves
        self.primary = wx.Button(self, id=wx.ID_ANY,
                                 label="Plot Selected\nCurves")
        # add button to open document explaining BIORHYTHM charts
        biodoc = wx.Button(self, id=wx.ID_ANY, label='Review\nDocumentation')
        xit = wx.Button(self, id=wx.ID_ANY, label="Exit")
        samples = wx.Button(self, id=wx.ID_ANY, label='Sample\nInterpretations')

#        btnsizer.Add(self.primary, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
#        btnsizer.Add(biodoc, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)
#        btnsizer.Add(xit, 0, wx.ALL | wx.ALIGN_CENTER, 5)

        self.Bind(wx.EVT_BUTTON, self.OnExit, xit)
        self.Bind(wx.EVT_BUTTON, self.OnPrimary, self.primary)
        self.Bind(wx.EVT_BUTTON, self.OnView, biodoc)
        self.Bind(wx.EVT_BUTTON, self.OnSamples, samples)

        gbs.Add(self.primary, pos=(10, 0), flag=wx.EXPAND)
        gbs.Add(biodoc, pos=(10, 1), flag=wx.EXPAND)
        gbs.Add(xit, pos=(10, 2), flag=wx.EXPAND)
        gbs.Add(samples, pos=(11, 1), flag=wx.EXPAND)

        sizerL.Add(15, 15)
        sizerL.Add(gbs, 1, wx.ALIGN_CENTER)
#        sizerL.Add(btnsizer, 1, wx.ALIGN_CENTER, wx.EXPAND)

        sizerR = wx.BoxSizer(wx.VERTICAL)
        # add the draw panel
        self.figure = Figure()
        self.axes = self.figure.add_subplot(111)
        self.canvas = FigureCanvas(self, -1, self.figure)
        self.ax = self.canvas.figure.axes[0]
        self.add_toolbar()

        sizerR.Add(self.canvas, 1, wx.EXPAND)
        sizerR.Add(self.toolbar)

        Main_Sizer.Add(sizerL, 0, wx.EXPAND)
        Main_Sizer.Add((10, 10))
        Main_Sizer.Add(sizerR, 1, wx.EXPAND)
        self.SetSizer(Main_Sizer)

        self.Center()
        self.Show(True)
        self.Maximize(True)

    def OnCal(self, evt):
        btn_id = str(evt.GetId())
        if btn_id == '101':
            ttl = 'D.O.B.'
        elif btn_id == '102':
            ttl = 'Plot Start Date'
        else:
            ttl = 'Date of Interest'

        dlg = MyCalendar(self, ttl, btn_id)
        dlg.ShowModal()

    def add_toolbar(self):
        self.toolbar = NavigationToolbar(self.canvas)
        self.toolbar.Realize()
        self.toolbar.update()

    def OnPrimary(self, evt):
        # clear any previuos plot and then calculate new curves
        self.axes.clear()

        # get DOB from editDOB
        if self.editDOB.GetLabel() == '':
            wx.MessageBox('A Date of Birth is needed!',
                          'Info', wx.OK | wx.ICON_INFORMATION)
            return
        else:
            dd, mm, yy = [int(i) for i in self.editDOB.GetLabel().split('/')]
            t0 = date(yy, mm, dd).toordinal()

        # get plot start date from editstart
        dd, mm, yy = [int(i) for i in self.editstart.GetLabel().split('/')]
        t1 = date(yy, mm, dd).toordinal()

        # calculate range date using editspan
        if self.editspan.GetValue() == '':
            self.editspan.SetValue('29')
            wx.MessageBox('Plot span has defaulted to 29 days!',
                          'Info', wx.OK | wx.ICON_INFORMATION)

        # set the span of days for the curves
        plot_span = int(self.editspan.GetValue())
        t = array(range(t1-2, t1 + plot_span))

        # list of names to be included in plot legend
        lgnd = []

        # get date of interest from editinter
        dd, mm, yy = [int(i) for i in self.editinter.GetLabel().split('/')]
        t4 = date(yy, mm, dd)
        if t4.toordinal() < t1 or t4.toordinal() > t1 + int(self.editspan.GetValue()):
            wx.MessageBox('Date of Interest is outside plot envelope', 'Info', wx.OK | wx.ICON_INFORMATION)
        else:
            # plot a vertical line at the date of interest
            lgnd.append('Date of\nInterest')
            self.ax.axvline(t4, color='magenta', linestyle='--', linewidth=2)

        # the y coordinates for the various curves
        # [physical, emotional, intellectual, intuitive, awareness]
        # curves for wisdom and passion are calculated from primary curves
        # passion from physical + emotional
        # wisdom from emotional + intellectual
        y = (sin(2*pi*(t-t0)/23), sin(2*pi*(t-t0)/28),
             sin(2*pi*(t-t0)/33), sin(2*pi*(t-t0)/38),
             sin(2*pi*(t-t0)/48))

        # converting ordinals to date format
        label = []
        for p in t:
            label.append(date.fromordinal(p))

        # value calculated for average of primary curves
        avg_prim = 0
        if self.cb1.GetValue():
            self.ax.plot(label, y[0], color="blue", linewidth=3, alpha=.7)
            avg_prim = y[0]
            lgnd.append('Physical')
        if self.cb2.GetValue():
            self.ax.plot(label, y[1], color="red", linewidth=3, alpha=.7)
            avg_prim = avg_prim + y[1]
            lgnd.append('Emotional')
        if self.cb3.GetValue():
            self.ax.plot(label, y[2], color="green", linewidth=3, alpha=.7)
            avg_prim = avg_prim + y[3]
            lgnd.append('Intellectual')

        # determine how many primary curves there are in the average
        cbsum = (int(self.cb1.GetValue() == 1) +
                 int(self.cb2.GetValue() == 1) +
                 int(self.cb3.GetValue() == 1))
        # if 2 of the primaries are ploted, plot the average
        # note the average curve may overlay the passion or wisdom curve
        if cbsum > 1:
            avg_prim = avg_prim / cbsum
            self.ax.plot(label, avg_prim, linewidth=2,
                         linestyle="dashed", color="black")
            lgnd.append('Average\nPrimaries')
        # plot the intuitive curve
        if self.cb4.GetValue():
            self.ax.plot(label, y[3], linewidth=2,
                         linestyle="dotted", color="orange")
            lgnd.append('Intuitive')
        # plot the awareness curve
        if self.cb5.GetValue():
            self.ax.plot(label, y[4], linewidth=2,
                         linestyle="dotted", color="yellow")
            lgnd.append('Awareness')
        # plot the wisdom curve
        if self.cb6.GetValue():
            self.ax.plot(label, .5*(y[1]+y[2]), linewidth=2,
                         linestyle='dotted', color='blue', alpha=.65)
            lgnd.append('Wisdom')
        # plot the passion curve
        if self.cb7.GetValue():
            self.ax.plot(label, .5*(y[0]+y[1]), linewidth=2,
                         linestyle='dotted', color='blue', alpha=.65)
            lgnd.append('Passion')

        # formatting the dates on the x axis
        self.ax.legend(lgnd)
        self.ax.xaxis.set_major_formatter(
            matplotlib.dates.DateFormatter('%d/%b')
            )
        self.ax.axhline(0, color="black", linewidth=1.4)
        self.ax.grid(True, linestyle="-", alpha=.3)
        plt.xlim((t[0], t[-1]))
        self.ax.set(title=(self.editname.GetValue() + ' DOB ' +
                           self.editDOB.GetLabel()))

        self.canvas.draw()

    def OnView(self, evt):
        import webbrowser
        html_path = ''
        filename = ''

        filename = (os.getcwd() + os.sep + 'Biorhythm' + os.sep + 'BiorhythmsChart.pdf')
        self.OpenWeb(filename)

    def OnSamples(self, evt):
        import webbrowser
        html_path = ''
        filename = ''

        filename = (os.getcwd() + os.sep + 'Biorhythm' + os.sep + 'BioSmpl.pdf')
        self.OpenWeb(filename)

    def OnExit(self, evt):
        self.Destroy()

    def OpenWeb(self, filename):
        # if default location does not work then open directory finder
        if os.path.isfile(filename) is False:
            dlg = wx.FileDialog(self, "Open XYZ file", wildcard="PDF files (*.pdf)|*.pdf",
                                style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

            if dlg.ShowModal() == wx.ID_CANCEL:
                return     # the user changed their mind

            # Proceed loading the file chosen by the user
            filename = dlg.GetPath()

        html_path = 'file:' + os.sep*2 + filename
        
        if html_path == '':
            wx.MessageBox('Problem Locating Biorhythm Examples File', 'Error', wx.OK)
        else:
            brwsrs = ['firefox', 'safari', 'chrome', 'opera',
                      'netscape', 'google-chrome', 'lynx',
                      'mozilla', 'galeon', 'chromium',
                      'chromium-browser', 'windows-default',
                      'w3m', 'no browser']
            for brwsr in brwsrs:
                if brwsr == 'no browser':
                    wx.MessageBox('Problem Locating Web Browser',
                                  'Error', wx.OK)
                else:
                    try:
                        webbrowser.get(using=brwsr).open(html_path, new=2)
                        break
                    except Exception:
                        pass


class MyCalendar(wx.Dialog):
    def __init__(self, parent, ttl, btn_id):

        super(MyCalendar, self).__init__(parent, title=ttl, size=(220, 250))
        panel = wx.Panel(self)
        self.title = ttl
        self.parent = parent
        self.btn_id = str(btn_id)

        calsizer = wx.BoxSizer(wx.VERTICAL)
        self.caldate = CalendarCtrl(
            panel,
            id=wx.ID_ANY,
            date=wx.DateTime().Today(),
            style=wx.adv.CAL_SEQUENTIAL_MONTH_SELECTION
            )

        # set an initial calander start date to Jan 1 1975
        if self.btn_id == '101':
            self.caldate.SetDate(wx.DateTime.FromDMY(1, 0, 1975))

        self.btn = wx.Button(panel, label="OK", size=(100, 35))
        calsizer.Add(self.caldate, 0, wx.EXPAND)
        calsizer.Add((10, 20))
        calsizer.Add(self.btn, 0, wx.ALIGN_CENTER)
        panel.SetSizerAndFit(calsizer)

        self.Bind(wx.EVT_BUTTON, self.OnOK, self.btn)

    def OnOK(self, evt):
        seldate = self.caldate.GetDate()

        day = seldate.GetDay()
        mth = seldate.GetMonth() + 1
        yr = seldate.GetYear()
        datestr = str(day) + '/' + str(mth) + '/' + str(yr)

        # set the corresponding adte labels to the selected calender date
        if self.btn_id == '101':
            self.parent.editDOB.SetLabel(datestr)
        elif self.btn_id == '102':
            self.parent.editstart.SetLabel(datestr)
        elif self.btn_id == '103':
            self.parent.editinter.SetLabel(datestr)
        self.Close()


# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frm = InputForm()
    app.MainLoop()

import wx
from wx import aui

from meerk40t.gui.icons import (
    icons8_down_50,
    icons8_down_left_50,
    icons8_down_right_50,
    icons8_home_filled_50,
    icons8_left_50,
    icons8_lock_50,
    icons8_padlock_50,
    icons8_right_50,
    icons8_up_50,
    icons8_up_left_50,
    icons8_up_right_50,
)

_ = wx.GetTranslation

MILS_IN_MM = 39.3701


def register_panel(window, context):
    panel = Jog(window, wx.ID_ANY, context=context)
    pane = (
        aui.AuiPaneInfo()
        .Right()
        .MinSize(174, 230)
        .FloatingSize(174, 230)
        .MaxSize(300, 300)
        .Caption(_("Jog"))
        .Name("jog")
        .CaptionVisible(not context.pane_lock)
    )
    pane.dock_proportion = 230
    pane.control = panel
    pane.submenu = _("Navigation")

    window.on_pane_add(pane)
    context.register("pane/jog", pane)


class Jog(wx.Panel):
    def __init__(self, *args, context=None, **kwds):
        # begin wxGlade: Jog.__init__
        kwds["style"] = kwds.get("style", 0) | wx.TAB_TRAVERSAL

        wx.Panel.__init__(self, *args, **kwds)
        self.context = context
        context.setting(float, "navigate_jog", 394.0)
        self.button_navigate_up_left = wx.BitmapButton(
            self, wx.ID_ANY, icons8_up_left_50.GetBitmap()
        )
        self.button_navigate_up = wx.BitmapButton(
            self, wx.ID_ANY, icons8_up_50.GetBitmap()
        )
        self.button_navigate_up_right = wx.BitmapButton(
            self, wx.ID_ANY, icons8_up_right_50.GetBitmap()
        )
        self.button_navigate_left = wx.BitmapButton(
            self, wx.ID_ANY, icons8_left_50.GetBitmap()
        )
        self.button_navigate_home = wx.BitmapButton(
            self, wx.ID_ANY, icons8_home_filled_50.GetBitmap()
        )
        self.button_navigate_right = wx.BitmapButton(
            self, wx.ID_ANY, icons8_right_50.GetBitmap()
        )
        self.button_navigate_down_left = wx.BitmapButton(
            self, wx.ID_ANY, icons8_down_left_50.GetBitmap()
        )
        self.button_navigate_down = wx.BitmapButton(
            self, wx.ID_ANY, icons8_down_50.GetBitmap()
        )
        self.button_navigate_down_right = wx.BitmapButton(
            self, wx.ID_ANY, icons8_down_right_50.GetBitmap()
        )
        self.button_navigate_unlock = wx.BitmapButton(
            self, wx.ID_ANY, icons8_padlock_50.GetBitmap()
        )
        self.button_navigate_lock = wx.BitmapButton(
            self, wx.ID_ANY, icons8_lock_50.GetBitmap()
        )
        self.__set_properties()
        self.__do_layout()

        self.Bind(
            wx.EVT_BUTTON, self.on_button_navigate_ul, self.button_navigate_up_left
        )
        self.Bind(wx.EVT_BUTTON, self.on_button_navigate_u, self.button_navigate_up)
        self.Bind(
            wx.EVT_BUTTON, self.on_button_navigate_ur, self.button_navigate_up_right
        )
        self.Bind(wx.EVT_BUTTON, self.on_button_navigate_l, self.button_navigate_left)
        self.Bind(
            wx.EVT_BUTTON, self.on_button_navigate_home, self.button_navigate_home
        )
        self.Bind(wx.EVT_BUTTON, self.on_button_navigate_r, self.button_navigate_right)
        self.Bind(
            wx.EVT_BUTTON, self.on_button_navigate_dl, self.button_navigate_down_left
        )
        self.Bind(wx.EVT_BUTTON, self.on_button_navigate_d, self.button_navigate_down)
        self.Bind(
            wx.EVT_BUTTON, self.on_button_navigate_dr, self.button_navigate_down_right
        )
        self.Bind(
            wx.EVT_BUTTON, self.on_button_navigate_unlock, self.button_navigate_unlock
        )
        self.Bind(
            wx.EVT_BUTTON, self.on_button_navigate_lock, self.button_navigate_lock
        )
        # end wxGlade

    def __set_properties(self):
        # begin wxGlade: Jog.__set_properties
        self.button_navigate_up_left.SetToolTip(
            _("Move laser diagonally in the up and left direction")
        )
        self.button_navigate_up_left.SetSize(self.button_navigate_up_left.GetBestSize())
        self.button_navigate_up.SetToolTip(_("Move laser in the up direction"))
        self.button_navigate_up.SetSize(self.button_navigate_up.GetBestSize())
        self.button_navigate_up_right.SetToolTip(
            _("Move laser diagonally in the up and right direction")
        )
        self.button_navigate_up_right.SetSize(
            self.button_navigate_up_right.GetBestSize()
        )
        self.button_navigate_left.SetToolTip(_("Move laser in the left direction"))
        self.button_navigate_left.SetSize(self.button_navigate_left.GetBestSize())
        self.button_navigate_home.SetSize(self.button_navigate_home.GetBestSize())
        self.button_navigate_right.SetToolTip(_("Move laser in the right direction"))
        self.button_navigate_right.SetSize(self.button_navigate_right.GetBestSize())
        self.button_navigate_down_left.SetToolTip(
            _("Move laser diagonally in the down and left direction")
        )
        self.button_navigate_down_left.SetSize(
            self.button_navigate_down_left.GetBestSize()
        )
        self.button_navigate_down.SetToolTip(_("Move laser in the down direction"))
        self.button_navigate_down.SetSize(self.button_navigate_down.GetBestSize())
        self.button_navigate_down_right.SetToolTip(
            _("Move laser diagonally in the down and right direction")
        )
        self.button_navigate_down_right.SetSize(
            self.button_navigate_down_right.GetBestSize()
        )
        self.button_navigate_unlock.SetToolTip(_("Unlock the laser rail"))
        self.button_navigate_unlock.SetSize(self.button_navigate_unlock.GetBestSize())
        self.button_navigate_lock.SetToolTip(_("Lock the laser rail"))
        self.button_navigate_lock.SetSize(self.button_navigate_lock.GetBestSize())
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: Jog.__do_layout
        navigation_sizer = wx.FlexGridSizer(4, 3, 0, 0)
        navigation_sizer.Add(self.button_navigate_up_left, 0, 0, 0)
        navigation_sizer.Add(self.button_navigate_up, 0, 0, 0)
        navigation_sizer.Add(self.button_navigate_up_right, 0, 0, 0)
        navigation_sizer.Add(self.button_navigate_left, 0, 0, 0)
        navigation_sizer.Add(self.button_navigate_home, 0, 0, 0)
        navigation_sizer.Add(self.button_navigate_right, 0, 0, 0)
        navigation_sizer.Add(self.button_navigate_down_left, 0, 0, 0)
        navigation_sizer.Add(self.button_navigate_down, 0, 0, 0)
        navigation_sizer.Add(self.button_navigate_down_right, 0, 0, 0)
        navigation_sizer.Add(self.button_navigate_unlock, 0, 0, 0)
        navigation_sizer.Add((0, 0), 0, 0, 0)
        navigation_sizer.Add(self.button_navigate_lock, 0, 0, 0)
        self.SetSizer(navigation_sizer)
        navigation_sizer.Fit(self)
        self.Layout()
        # end wxGlade

    def on_button_navigate_home(
        self, event=None
    ):  # wxGlade: Navigation.<event_handler>
        self.context("home\n")

    def on_button_navigate_ul(self, event=None):  # wxGlade: Navigation.<event_handler>
        dx = -self.context.navigate_jog
        dy = -self.context.navigate_jog
        self.context("move_relative %d %d\n" % (dx, dy))

    def on_button_navigate_u(self, event=None):  # wxGlade: Navigation.<event_handler>
        dx = 0
        dy = -self.context.navigate_jog
        self.context("move_relative %d %d\n" % (dx, dy))

    def on_button_navigate_ur(self, event=None):  # wxGlade: Navigation.<event_handler>
        dx = self.context.navigate_jog
        dy = -self.context.navigate_jog
        self.context("move_relative %d %d\n" % (dx, dy))

    def on_button_navigate_l(self, event=None):  # wxGlade: Navigation.<event_handler>
        dx = -self.context.navigate_jog
        dy = 0
        self.context("move_relative %d %d\n" % (dx, dy))

    def on_button_navigate_r(self, event=None):  # wxGlade: Navigation.<event_handler>
        dx = self.context.navigate_jog
        dy = 0
        self.context("move_relative %d %d\n" % (dx, dy))

    def on_button_navigate_dl(self, event=None):  # wxGlade: Navigation.<event_handler>
        dx = -self.context.navigate_jog
        dy = self.context.navigate_jog
        self.context("move_relative %d %d\n" % (dx, dy))

    def on_button_navigate_d(self, event=None):  # wxGlade: Navigation.<event_handler>
        dx = 0
        dy = self.context.navigate_jog
        self.context("move_relative %d %d\n" % (dx, dy))

    def on_button_navigate_dr(self, event=None):  # wxGlade: Navigation.<event_handler>
        dx = self.context.navigate_jog
        dy = self.context.navigate_jog
        self.context("move_relative %d %d\n" % (dx, dy))

    def on_button_navigate_unlock(
        self, event=None
    ):  # wxGlade: Navigation.<event_handler>
        self.context("unlock\n")

    def on_button_navigate_lock(
        self, event=None
    ):  # wxGlade: Navigation.<event_handler>
        self.context("lock\n")

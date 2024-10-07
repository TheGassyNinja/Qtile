# Void Qtile

import os
import subprocess
from libqtile import bar, layout, qtile, widget, hook 
from libqtile.utils import send_notification
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy

@hook.subscribe.startup_once
def autostart():
    home = os.path.expanduser('~/.config/qtile/autostart.sh')
    subprocess.Popen([home])

def send_notification(title, message):
    subprocess.run(["notify-send", "-u", "low", title, message])

@hook.subscribe.layout_change
def layout_change(layout, group):
    send_notification(
        "Layout Change",
        f"{layout.name}"
    )


colors = []
cache='/home/thegassyninja/.cache/wal/colors'
def load_colors(cache):
    with open(cache, 'r') as file:
        for i in range(8):
            colors.append(file.readline().strip())
    colors.append('#ffffff')
    lazy.reload()
load_colors(cache)


mod = "mod4"
terminal = "kitty"
terminal2 = "kitty --config /home/thegassyninja/.config/kitty/kitty-clear.conf --class CLEAR"
floaterm = "tdrop -am -w 80% -h 65% -x 10% -y 13% -n 0 kitty --config /home/thegassyninja/.config/kitty/kitty-clear.conf --class SPOTIFY"
floaterm2 = "tdrop -am -w 37% -h 20% -x 2% -y 58% -n 0 kitty --config /home/thegassyninja/.config/kitty/kitty-clear.conf --class SPOTIFY"
scrnshot = "/home/thegassyninja/.config/qtile/Scripts/screenshot"

keys = [
        Key([], "Print", lazy.spawn(scrnshot), desc="Take a screenshot"),
        Key([mod], "KP_End", lazy.spawn(floaterm), desc="Launch Floaterm(Tdrop)"),
        Key([mod], "KP_Down", lazy.spawn(floaterm2), desc="Launch Floaterm(Tdrop)"),
        Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
        Key([mod, "shift"], "Return", lazy.spawn(terminal2), desc="Launch terminal"),
        Key([mod], "c", lazy.window.kill(), desc="Kill focused window"),
        Key([mod], "r", lazy.spawn("rofi -show drun")),
        Key([mod], "b", lazy.hide_show_bar(), desc="Toggle bar"),
    
    # Switch between windows
    Key([mod], "h", lazy.layout.left(), desc="Move focus to left"),
    Key([mod], "l", lazy.layout.right(), desc="Move focus to right"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "space", lazy.layout.next(), desc="Move window focus to other window"),
    
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),
    
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left"),
    Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right"),
    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes"),
    
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
]

groups = [Group(i) for i in "123456789"]
for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layouts = [
    layout.Columns(border_focus=colors[3],
                     border_unfocus=colors[6],
                        margin=5, border_width=8,
                                 border_on_single=0),
    layout.Max(),
]

widget_defaults = dict(
    font="Hack Nerd Font NF",
    fontsize=22,
    padding=0,
    background=colors[0],
)
extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.TextBox(text='', fontsize=34,
                                  background=colors[0], foreground=colors[6]),
                widget.Memory(format='RAM: {MemPercent}% ',
                                  background=colors[6], foreground=colors[0]), 
                widget.TextBox(text='',
                                fontsize=34,
                                  background=colors[0], foreground=colors[6]),
                
                widget.Spacer(length=bar.STRETCH,),
                widget.GroupBox(highlight_method='line',
                                    spacing=5, active=colors[5]),
                widget.Spacer(length=bar.STRETCH,
                                     background=colors[0],),
                
                widget.GenPollText(update_interval=1,
                                    func=lambda: subprocess.check_output(["/home/thegassyninja/.config/qtile/Scripts/check-share.sh"]).decode(),
                                    background=colors[0], foreground=colors[1], fontsize=30),
                
                widget.Spacer(length=20,),
                
                widget.TextBox(text='',
                                fontsize=34,
                                  background=colors[0], foreground=colors[5]),
                widget.CPU(format='CPU: {load_percent}%',
                            background=colors[5], foreground=colors[8]),
                widget.TextBox(text='',
                                fontsize=34,
                                  background=colors[0], foreground=colors[5]),

            ],
            36,
            opacity=0.70,
            margin=[4, 480, 4, 480],
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = False
cursor_warp = False
floating_layout = layout.Floating(border_focus=colors[3],
                                   border_unfocus=colors[1],
                                                 border_width=0,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="FLOATERM"),  # Tdrop (Local Term) 
        Match(wm_class="SPOTIFY"),  # Spotify Tdrop (SSH-Term)
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

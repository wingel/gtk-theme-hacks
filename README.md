# Adwaita fix and general CSS stripping tool

This project contains Gtk3 Adwaita themes that disable "backdrop"
which makes widgets in a Gtk3 application fade to a disabled
appearance when the window is inactive.

On the way to fixing this I asked ChatGPT to create a generic tool
which can strip selectors from a CSS file.  It might be useful for
somebody.

## Background

Gtk3 has support for something called "backdrop" which is used to
theme inactive windows.  In the Gtk3 Adwaita theme this will make all
widgets in an inactive windows slowly fade to a disabled appearance,
something that (and apparently may others) find incredibly annoying.
Otherwise I kind of like Adwaita, it might not be that pretty, but
it's very functional and mostly just works.

I'm using Xfce4 on my desktop becaause it is also simple, fast and
does its thing without getting in the way.  I have a perfectly good
title bar that shows if a windows is active or not and I don't need
the widgets in the window to look disabled.  Having to watch an
animation every time i activate/deactivate a windows is just not my
thing.

## Quick Fix

If you just want an Adwaita theme without backdrop fading, here's what
to do.  I have tested this on Debian 12 with Xfce4.

If you want to call it something else than "Adwaita-fixed", just use a
different name and remember to edit index.theme acordingly.

First, make a copy the Adwaita theme from the system:

```
mkdir -p ~/.themes
rm -rf ~/.themes/Adwaita-fixed
cp -r /usr/share/themes/Adwaita ~/.themes/Adwaita-fixed
```

Install a description of the fixed theme:

```
cp -r Adwaita-fixed/index.theme ~/.themes/Adwaita-fixed
```

Copy one of the fixed themes, either the normal (light) one:

```
cp Adwaita-fixed/gtk-contained.stripped.css ~/.themes/Adwaita-fixed/gtk-3.0/gtk.css
```

or the dark one:

```
cp Adwaita-fixed/gtk-contained-dark.striped.css ~/.themes/Adwaita-fixed/gtk-3.0/gtk.css
```

Open Xfce4 Settings and find the settings for "Appearance".  There
should now be an "Adwaita-fixed" theme available in the "Style" tab.
Select it and you should hopefully have a theme without backdrop
functionality.  You might have to restart some applications for the
theme to take effect.

# More informatin

## Discussion

For a discussion and complaints about backdrop, see:

https://forum.xfce.org/viewtopic.php?id=13140

## Other themes

It should be possible to disable backdrop in other themes too, as long
as you have the "gtk-contained.css" file for it.  Here's how I
recreated the file for the Gtk3 Adwaita theme.

Gtk3 is trying to make it hard to modify their themes.  But it is
still possible to do it.  This page provided invaluable guidance:

https://www.dedoimedo.com/computers/gnome-40-edit-theme.html

Based on the page I arrived at this.

Clone out the Gtk reposistory and check out the source for your Gtk
version.  For Debian 12 this is Gtk 3.24.  Getting the version exacly
right is probably not that important.

```
git clone https://gitlab.gnome.org/GNOME/gtk.git
cd gtk
git checkout gtk-3-24
```

Find the CSS files for the theme you want to modify and copy them to
your directory.

```
cd gtk/theme/Adwaita
cp gtk-contained.css gtk-contained-dark.css /path/to/your/directory
```

Then run the following script to strip out the backdrop selector.  I'm
telling the tool to keep selectors related to "titlebar" and
"headerbar" so that applications that use Gtk3 client side decorations
will hopefully still work:

Next, install the tinycss2 Python module.  (It's probably better to
use a virtual environment such as uv, but this document is long enough
as it is.)

If you are using uv to manage a virtual environment, run:

```
uv run css-strip.py \
    --remove backdrop \
    --keep titlebar --keep headerbar \
    gtk-contained.css gtk-contained-dark.css
```

Or if you just want to make things as easy for yourself as possible,
install required Python dependencies with pip:

```
pip3 install --break-system-packages tinycss2
```

and then run:

```
python3 css-strip.py \
    --remove backdrop \
    --keep titlebar --keep headerbar \
    gtk-contained.css gtk-contained-dark.css
```

This will produce files with the specified selectors stripped out:

```
gtk-contained-dark.stripped.css
gtk-contained.stripped.css
```

The tool will also produce /normalized/ files which ideally should be
identical to the original ones.  It turns out that they were not.  So
this was just a sanity check so that I could test the new files and
make sure the tool doesn't break anything.

```
gtk-contained-dark.normalized.css
gtk-contained.normalized.css
```


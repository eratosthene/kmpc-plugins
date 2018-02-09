#######
Plugins
#######

***********
kivypiewifi
***********

A simple GUI plugin to scan for wifi access points and set them on a KivyPie
box. Hit Scan, choose a network, hit Connect, type in the pre-shared key, hit
OK. It will write the chosen values to /boot/interfaces. Uses ``iwconfig`` to scan
for networks. Needs sudo access, so make sure your user can run password-less
sudo commands.

*******
osxwifi
*******

A simple GUI plugin to scan for wifi access points and set them on a Mac. Hit
Scan, choose a network, hit Connect, type in the pre-shared key, hit OK. Uses
``airport`` to scan for networks and ``networksetup`` to connect. Only tested
on macOS Sierra, you may need to adjust the location of ``airport`` for older
macOS versions.

*******
manager
*******

A script plugin that just runs ``kmpcmanager``. Allows you to manage your
synclist directly from your car.


from functools import partial
from subprocess import check_output,call
import re
import os

import kivy
kivy.require('1.10.0')

from kivy.logger import Logger

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from kivy.factory import Factory
from kivy.properties import ObjectProperty

from kmpc.sync import Subproc
from twisted.internet.defer import Deferred

class PSKPopup(Popup):
    plugin=ObjectProperty(None)

class osxwifiPluginContent(BoxLayout):

    def scan(self):
        from twisted.internet import reactor
        self.aps=[]
        self.ids.connectbutton.disabled=True
        cmdline=["/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport","-s"]
        pp=Subproc(self.scan_line)
        pp.deferred=Deferred()
        pp.deferred.addCallback(self.build_ap_list)
        reactor.spawnProcess(pp,cmdline[0],cmdline,{'PATH':os.environ['PATH']})

    def scan_line(self,line):
        match=re.match(r'\s*(.*)\s..:..:..:..:..:..',line)
        if match:
            self.aps.append(str(match.group(1)))

    def build_ap_list(self,r):
        Logger.debug("build_ap_list: "+format(self.aps))
        self.ids.apbox.clear_widgets()
        fb=None
        for ap in self.aps:
            b=ToggleButton(text='Connect to "'+ap+'"',size_hint_y=None,height='48sp',group='ap',allow_no_selection=False)
            if not fb: fb=b
            b.bind(on_press=partial(self.set_ap,ap))
            self.ids.apbox.add_widget(b)
        if fb: self.ids.sv.scroll_to(fb)

    def set_ap(self,ap,instance):
        self.connect_to=ap
        self.ids.connectbutton.disabled=False

    def connect(self):
        Logger.debug("wifi: getting psk for "+self.connect_to)
        pskPopup=Factory.PSKPopup(plugin=self)
        pskPopup.open()

    def connect2(self,psk):
        cmdline="networksetup -setairportnetwork `networksetup -listallhardwareports|grep -A1 'Wi-Fi'|tail -n 1|cut -d' ' -f 2` "+self.connect_to+" "+psk
        Logger.debug("connect2: "+cmdline)
        call(cmdline,shell=True)

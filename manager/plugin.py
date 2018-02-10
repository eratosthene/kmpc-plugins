from pkg_resources import resource_filename
import os

import kivy
kivy.require('1.10.0')

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder

from kmpc.managerinterface import ManagerInterface

class managerPluginContent(ManagerInterface):

    def __init__(self,**kwargs):
        Builder.load_file(resource_filename('kmpc',os.path.join('resources/kv','manager.kv')))
        ManagerInterface.__init__(self,App.get_running_app().config,**kwargs)

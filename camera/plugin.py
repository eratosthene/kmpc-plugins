import cv2
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.properties import ObjectProperty, BooleanProperty


class KivyCamera(Image):

    capture=ObjectProperty(None)
    mirror=BooleanProperty(False)

    def __init__(self, **kwargs):
        Image.__init__(self, **kwargs)
        if kwargs.get('mirror'):
            self.mirror=True

    def start(self, fps=30):
        if not self.capture:
            self.capture = cv2.VideoCapture(0)
            self.capture.set(cv2.CAP_PROP_FRAME_WIDTH,800)
            self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT,448)
        Clock.schedule_interval(self.update, 1.0 / fps)

    def stop(self):
        Clock.unschedule_interval(self.update)
        self.capture = None

    def update(self, dt):
        return_value, frame = self.capture.read()
        if return_value:
            texture = self.texture
            w, h = frame.shape[1], frame.shape[0]
            if not texture or texture.width != w or texture.height != h:
                self.texture = texture = Texture.create(size=(w, h))
                texture.flip_vertical()
                if self.mirror:
                    texture.flip_horizontal()
            texture.blit_buffer(frame.tobytes(), colorfmt='bgr')
            self.canvas.ask_update()


class cameraPluginContent(BoxLayout):
    def __init__(self,**kwargs):
        BoxLayout.__init__(self, **kwargs)
        self.ids.camera.start()

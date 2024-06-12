from kivy.app import App
from kivy.lang import Builder


kv = Builder.load_string(

    """
ScreenManager:
    Screen:
        name: 'first'
        on_enter: app.update('first')
        Label:
            id: lbl_1
            pos_hint: {'center_x': .5, 'center_y': .5}
            text: 'first 1'
        Button:
            size_hint: None, None
            size: dp(100), dp(35)
            pos_hint: {'center_x': .5, 'center_y': .1}
            text: 'go to second'
            on_release:
                app.update('first')
                
    Screen:
        name: 'second'
        on_enter: app.update('second')
        Label:
            id: lbl_2
            pos_hint: {'center_x': .5, 'center_y': .5}
        Button:
            size_hint: None, None
            size: dp(100), dp(35)
            pos_hint: {'center_x': .5, 'center_y': .1}
            text: 'go to first'
            on_release:
                root.transition.direction = 'left'
                root.current = 'first'
    """
)


class MyApp(App):

    first = 1
    second = 0

    def build(self):
        return kv

    def update(self, screen):
        self.first += 1
        self.root.ids.lbl_1.text = f'{screen} {self.first}'


MyApp().run()
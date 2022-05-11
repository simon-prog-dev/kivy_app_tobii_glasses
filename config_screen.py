from kivy.config import Config

if __name__ == "__main__":

    Config.set('graphics', 'fullscreen', '0')   # 'fake', 'auto'
    Config.set('graphics', 'window_state', 'visble')   # ‘visible’, ‘hidden’, ‘maximized’
    Config.write()


import view
from kivymd.app import MDApp


class MyApp(MDApp):  

    def build(self):  
        self.load_kv("view_container.kv") 
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "BlueGray"
        return view.Container() 
        

if __name__ == "__main__":  
    MyApp().run()
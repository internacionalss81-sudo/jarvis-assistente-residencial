import urllib.request
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

class CasaInteligenteApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Campo para o IP do ESP32
        self.ip_input = TextInput(text="192.168.0.100", multiline=False, size_hint=(1, 0.2))
        self.layout.add_widget(self.ip_input)

        # Rótulo de status
        self.label_status = Label(text="Conectar ao ESP32", size_hint=(1, 0.2))
        self.layout.add_widget(self.label_status)

        # Botões de controle
        btn_sala = Button(text="Luz Sala", size_hint=(1, 0.3))
        btn_sala.bind(on_press=lambda x: self.enviar_comando("/sala"))
        self.layout.add_widget(btn_sala)

        btn_quarto = Button(text="Luz Quarto", size_hint=(1, 0.3))
        btn_quarto.bind(on_press=lambda x: self.enviar_comando("/quarto"))
        self.layout.add_widget(btn_quarto)

        btn_porta = Button(text="Abrir Porta", size_hint=(1, 0.3))
        btn_porta.bind(on_press=lambda x: self.enviar_comando("/destravar"))
        self.layout.add_widget(btn_porta)

        return self.layout

    def enviar_comando(self, rota):
        ip = self.ip_input.text
        url = f"http://{ip}{rota}"
        try:
            urllib.request.urlopen(url, timeout=2)
            self.label_status.text = f"Comando {rota} enviado!"
        except Exception as e:
            self.label_status.text = "Erro ao conectar!"

if __name__ == '__main__':
    CasaInteligenteApp().run()
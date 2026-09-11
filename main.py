import urllib.request
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.utils import platform

class CasaInteligenteApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)
        
        # Campo para o IP do ESP32
        self.ip_input = TextInput(text="192.168.0.100", multiline=False, size_hint=(1, 0.15))
        self.layout.add_widget(self.ip_input)

        # Status
        self.label_status = Label(text="Aguardando comando...", size_hint=(1, 0.15))
        self.layout.add_widget(self.label_status)

        # Botão de Voz
        btn_voz = Button(text="🎤 Falar Comando (Voz)", size_hint=(1, 0.25), background_color=(0.2, 0.6, 1, 1))
        btn_voz.bind(on_press=self.ouvir_comando)
        self.layout.add_widget(btn_voz)

        # Botões Manuais
        btn_sala = Button(text="Luz Sala", size_hint=(1, 0.15))
        btn_sala.bind(on_press=lambda x: self.enviar_comando("/sala"))
        self.layout.add_widget(btn_sala)

        btn_quarto = Button(text="Luz Quarto", size_hint=(1, 0.15))
        btn_quarto.bind(on_press=lambda x: self.enviar_comando("/quarto"))
        self.layout.add_widget(btn_quarto)

        btn_porta = Button(text="Abrir Porta", size_hint=(1, 0.15))
        btn_porta.bind(on_press=lambda x: self.enviar_comando("/destravar"))
        self.layout.add_widget(btn_porta)

        return self.layout

    def ouvir_comando(self, instance):
        if platform == 'android':
            try:
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                Intent = autoclass('android.content.Intent')
                RecognizerIntent = autoclass('android.speech.RecognizerIntent')

                intent = Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH)
                intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL, RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
                intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, "pt-BR")
                
                # Dispara o reconhecedor de voz do Android
                PythonActivity.mActivity.startActivityForResult(intent, 1001)
                self.label_status.text = "Ouvindo..."
            except Exception as e:
                self.label_status.text = f"Erro no microfone: {e}"
        else:
            self.label_status.text = "Comando de voz disponível apenas no Android"

    def processar_texto_voz(self, texto):
        texto = texto.lower()
        if "sala" in texto:
            self.enviar_comando("/sala")
        elif "quarto" in texto:
            self.enviar_comando("/quarto")
        elif "porta" in texto or "abrir" in texto or "destravar" in texto:
            self.enviar_comando("/destravar")
        else:
            self.label_status.text = f"Comando não reconhecido: '{texto}'"

    def enviar_comando(self, rota):
        ip = self.ip_input.text
        url = f"http://{ip}{rota}"
        try:
            urllib.request.urlopen(url, timeout=2)
            self.label_status.text = f"Comando {rota} enviado!"
        except Exception:
            self.label_status.text = "Erro ao conectar no ESP32!"

if __name__ == '__main__':
    CasaInteligenteApp().run()
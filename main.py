import threading
import time
import requests
from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.video import Video

# Configuração da Janela (Simulação PC)
Window.size = (380, 720)
Window.clearcolor = (0, 0, 0, 1)

# IP DO SEU ESP32
ESP32_IP = "http://192.168.1.221"
PIN_ACESSO = "23121478"


class RoundedButton(Button):

    def __init__(
        self,
        bg_color=(0.15, 0.15, 0.15, 1),
        text_color=(1, 1, 1, 1),
        border_color=None,
        radius=[12],
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.background_normal = ""
        self.background_color = (0, 0, 0, 0)
        self.custom_bg = bg_color
        self.custom_text_color = text_color
        self.border_color = border_color
        self.radius = radius
        self.color = text_color
        self.bold = True

        self.bind(pos=self._update_canvas, size=self._update_canvas)

    def _update_canvas(self, *args):
        self.canvas.before.clear()
        with self.canvas.before:
            if self.border_color:
                Color(*self.border_color)
                RoundedRectangle(
                    pos=(self.pos[0] - 2, self.pos[1] - 2),
                    size=(self.size[0] + 4, self.size[1] + 4),
                    radius=self.radius,
                )
            Color(*self.custom_bg)
            RoundedRectangle(pos=self.pos, size=self.size, radius=self.radius)


class CasaInteligenteApp(App):

    def build(self):
        self.icon = "icone.png"

        self.logado = False
        self.session = requests.Session()

        scroll = ScrollView()
        main_layout = BoxLayout(
            orientation="vertical",
            padding=[20, 10, 20, 20],
            spacing=12,
            size_hint_y=None,
        )
        main_layout.bind(minimum_height=main_layout.setter("height"))

        # 1. RELÓGIO DIGITAL
        self.lbl_clock = Label(
            text="00:00:00",
            font_size="32sp",
            bold=True,
            color=(1, 0.5, 0, 1),
            size_hint_y=None,
            height=45,
        )
        main_layout.add_widget(self.lbl_clock)
        Clock.schedule_interval(self.update_clock, 1)

        # 2. CARD DE TEMPERATURA E UMIDADE
        card_temp = BoxLayout(
            orientation="vertical",
            padding=10,
            spacing=2,
            size_hint_y=None,
            height=110,
        )
        with card_temp.canvas.before:
            Color(0.12, 0.12, 0.12, 1)
            self.rect_card = RoundedRectangle(
                pos=card_temp.pos, size=card_temp.size, radius=[15]
            )
        card_temp.bind(
            pos=lambda inst, val: setattr(self.rect_card, "pos", val),
            size=lambda inst, val: setattr(self.rect_card, "size", val),
        )

        self.lbl_temp = Label(
            text="--°C",
            font_size="30sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=40,
        )
        self.lbl_umid = Label(
            text="UMIDADE: --%",
            font_size="13sp",
            bold=True,
            color=(0, 0.8, 0.3, 1),
            size_hint_y=None,
            height=25,
        )
        self.lbl_status = Label(
            text="Conectando...",
            font_size="12sp",
            color=(1, 0.5, 0, 1),
            size_hint_y=None,
            height=20,
        )

        card_temp.add_widget(self.lbl_temp)
        card_temp.add_widget(self.lbl_umid)
        card_temp.add_widget(self.lbl_status)
        main_layout.add_widget(card_temp)

        # 3. STREAM DA CÂMERA YOOSEE (192.168.1.49) - Protegido contra falhas de DLL no PC
        lbl_cam_titulo = Label(
            text="CÂMERA YOOSEE (AO VIVO)",
            font_size="12sp",
            bold=True,
            color=(1, 0.5, 0, 1),
            size_hint_y=None,
            height=20,
        )
        main_layout.add_widget(lbl_cam_titulo)

        try:
            self.cam_stream = Video(
                source="rtsp://admin:23121478@192.168.1.49:554/onvif1",
                state="play",
                options={"eos": "loop"},
                size_hint_y=None,
                height=200,
            )
            main_layout.add_widget(self.cam_stream)
        except Exception as e:
            print("Player de vídeo indisponível neste ambiente:", e)
            lbl_erro_cam = Label(
                text="[Vídeo indisponível no PC]",
                font_size="12sp",
                color=(0.7, 0.7, 0.7, 1),
                size_hint_y=None,
                height=40,
            )
            main_layout.add_widget(lbl_erro_cam)

        # 4. GRADE DE BOTÕES (Luzes, Ventilador e TV)
        grid = GridLayout(cols=2, spacing=10, size_hint_y=None, height=130)

        self.btn_sala = RoundedButton(
            text="SALA",
            bg_color=(0.15, 0.15, 0.15, 1),
            text_color=(1, 1, 1, 1),
        )
        self.btn_sala.bind(on_press=lambda x: self.enviar_comando("/sala"))

        self.btn_quarto = RoundedButton(
            text="QUARTO",
            bg_color=(0.15, 0.15, 0.15, 1),
            text_color=(1, 1, 1, 1),
        )
        self.btn_quarto.bind(on_press=lambda x: self.enviar_comando("/quarto"))

        self.btn_vent = RoundedButton(
            text="VENTILADOR",
            bg_color=(0.15, 0.15, 0.15, 1),
            text_color=(1, 1, 1, 1),
        )
        self.btn_vent.bind(on_press=lambda x: self.enviar_comando("/vent"))

        self.btn_tv = RoundedButton(
            text="TV (IR)",
            bg_color=(0.15, 0.15, 0.15, 1),
            text_color=(1, 1, 1, 1),
        )
        self.btn_tv.bind(
            on_press=lambda x: self.enviar_comando_pulso(
                "/ir_tv", self.btn_tv, 0.5
            )
        )

        grid.add_widget(self.btn_sala)
        grid.add_widget(self.btn_quarto)
        grid.add_widget(self.btn_vent)
        grid.add_widget(self.btn_tv)
        main_layout.add_widget(grid)

        # 5. BOTÃO GARAGEM
        self.btn_garagem = RoundedButton(
            text="GARAGEM",
            bg_color=(0.15, 0.15, 0.15, 1),
            text_color=(1, 1, 1, 1),
            size_hint_y=None,
            height=50,
        )
        self.btn_garagem.bind(
            on_press=lambda x: self.enviar_comando_pulso(
                "/garagem", self.btn_garagem, 0.8
            )
        )
        main_layout.add_widget(self.btn_garagem)

        # 6. BOTÃO MODO NOITE
        self.btn_noite = RoundedButton(
            text="🌙  MODO NOITE",
            bg_color=(0.1, 0.1, 0.1, 1),
            text_color=(1, 0.5, 0, 1),
            size_hint_y=None,
            height=50,
        )
        self.btn_noite.bind(on_press=lambda x: self.enviar_comando("/noite"))
        main_layout.add_widget(self.btn_noite)

        # 7. BOTÃO FALAR COM JAVA
        self.btn_java = RoundedButton(
            text="🎙️  FALAR COM JAVA",
            bg_color=(1, 0.6, 0, 1),
            text_color=(0, 0, 0, 1),
            size_hint_y=None,
            height=55,
        )
        main_layout.add_widget(self.btn_java)

        # 8. BOTÃO ABRIR PORTA
        self.btn_porta = RoundedButton(
            text="ABRIR PORTA",
            bg_color=(0, 0, 0, 1),
            text_color=(0, 0.9, 0.3, 1),
            border_color=(0, 0.9, 0.3, 1),
            size_hint_y=None,
            height=50,
        )
        self.btn_porta.bind(
            on_press=lambda x: self.enviar_comando_pulso(
                "/destravar", self.btn_porta, 1.5, cor_pulso=(0, 0.9, 0.3, 1)
            )
        )
        main_layout.add_widget(self.btn_porta)

        scroll.add_widget(main_layout)

        threading.Thread(target=self.conectar_e_atualizar, daemon=True).start()

        return scroll

    def update_clock(self, dt):
        self.lbl_clock.text = time.strftime("%H:%M:%S")

    def conectar_e_atualizar(self):
        while True:
            if not self.logado:
                try:
                    r = self.session.get(
                        f"{ESP32_IP}/login?senha={PIN_ACESSO}", timeout=3
                    )
                    if r.status_code == 200:
                        self.logado = True
                        Clock.schedule_once(
                            lambda dt: setattr(
                                self.lbl_status, "text", "Conectado"
                            )
                        )
                    else:
                        Clock.schedule_once(
                            lambda dt: setattr(
                                self.lbl_status, "text", "Erro de PIN"
                            )
                        )
                except Exception:
                    Clock.schedule_once(
                        lambda dt: setattr(
                            self.lbl_status, "text", "ESP32 Desconectado"
                        )
                    )
                    time.sleep(3)
                    continue

            try:
                res = self.session.get(f"{ESP32_IP}/status", timeout=2)
                if res.status_code == 200:
                    dados = dict(
                        x.split(":")
                        for x in res.text.split("|")
                        if ":" in x
                    )
                    Clock.schedule_once(
                        lambda dt: self.atualizar_interface(dados)
                    )
            except Exception:
                self.logado = False

            time.sleep(2)

    def atualizar_interface(self, dados):
        self.lbl_temp.text = f"{dados.get('Temp', '--')}°C"
        self.lbl_umid.text = f"UMIDADE: {dados.get('Umid', '--')}%"

        self.definir_cor_botao(self.btn_sala, dados.get("Sala") == "ON")
        self.definir_cor_botao(self.btn_quarto, dados.get("Quarto") == "ON")
        self.definir_cor_botao(self.btn_vent, dados.get("Vent") == "ON")

    def definir_cor_botao(self, btn, ativo):
        if ativo:
            btn.custom_bg = (1, 0.6, 0, 1)
            btn.color = (0, 0, 0, 1)
        else:
            btn.custom_bg = (0.15, 0.15, 0.15, 1)
            btn.color = (1, 1, 1, 1)
        btn._update_canvas()

    def enviar_comando(self, rota):
        def requisitar():
            try:
                self.session.get(f"{ESP32_IP}{rota}", timeout=2)
            except Exception as e:
                print(f"Erro ao enviar comando {rota}: {e}")

        threading.Thread(target=requisitar, daemon=True).start()

    def enviar_comando_pulso(
        self, rota, btn, tempo_segundos, cor_pulso=(1, 0.6, 0, 1)
    ):
        cor_original_bg = btn.custom_bg
        cor_original_txt = btn.color

        btn.custom_bg = cor_pulso
        btn.color = (0, 0, 0, 1)
        btn._update_canvas()

        def restaurar_botao(dt):
            btn.custom_bg = cor_original_bg
            btn.color = cor_original_txt
            btn._update_canvas()

        Clock.schedule_once(restaurar_botao, tempo_segundos)
        self.enviar_comando(rota)


if __name__ == "__main__":
    CasaInteligenteApp().run()
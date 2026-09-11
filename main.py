from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
import time

# Configuração da janela (simulando tela de celular no PC)
Window.size = (380, 680)
Window.clearcolor = (0, 0, 0, 1)  # Fundo preto puro


class RoundedButton(Button):
    """Botão personalizado com bordas arredondadas e troca de cores"""

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
        # Container principal com rolagem para não cortar os botões em telas menores
        scroll = ScrollView()
        main_layout = BoxLayout(
            orientation="vertical",
            padding=[20, 10, 20, 20],
            spacing=12,
            size_hint_y=None,
        )
        main_layout.bind(
            minimum_height=main_layout.setter("height")
        )

        # 1. RELÓGIO DIGITAL (Topo)
        self.lbl_clock = Label(
            text="00:00:00",
            font_size="32sp",
            bold=True,
            color=(1, 0.5, 0, 1),  # Laranja brilhante
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

        lbl_temp = Label(
            text="28.5°C",
            font_size="30sp",
            bold=True,
            color=(1, 1, 1, 1),
            size_hint_y=None,
            height=40,
        )
        lbl_umid = Label(
            text="UMIDADE: 68.0%",
            font_size="13sp",
            bold=True,
            color=(0, 0.8, 0.3, 1),  # Verde
            size_hint_y=None,
            height=25,
        )
        lbl_status = Label(
            text="Pronto",
            font_size="12sp",
            color=(1, 0.5, 0, 1),  # Laranja
            size_hint_y=None,
            height=20,
        )

        card_temp.add_widget(lbl_temp)
        card_temp.add_widget(lbl_umid)
        card_temp.add_widget(lbl_status)
        main_layout.add_widget(card_temp)

        # 3. GRADE DE BOTÕES (SALA, QUARTO, VENTILADOR, TV IR)
        grid = GridLayout(cols=2, spacing=10, size_hint_y=None, height=130)

        self.btn_sala = RoundedButton(
            text="SALA",
            bg_color=(0.15, 0.15, 0.15, 1),
            text_color=(1, 1, 1, 1),
        )
        self.btn_sala.bind(
            on_press=lambda x: self.toggle_btn(
                self.btn_sala, (1, 0.6, 0, 1), (0, 0, 0, 1)
            )
        )

        self.btn_quarto = RoundedButton(
            text="QUARTO",
            bg_color=(1, 0.6, 0, 1),  # Ativo por padrão (Laranja)
            text_color=(0, 0, 0, 1),
        )
        self.btn_quarto.bind(
            on_press=lambda x: self.toggle_btn(
                self.btn_quarto, (1, 0.6, 0, 1), (0, 0, 0, 1)
            )
        )

        self.btn_vent = RoundedButton(
            text="VENTILADOR",
            bg_color=(1, 0.6, 0, 1),  # Ativo por padrão (Laranja)
            text_color=(0, 0, 0, 1),
        )
        self.btn_vent.bind(
            on_press=lambda x: self.toggle_btn(
                self.btn_vent, (1, 0.6, 0, 1), (0, 0, 0, 1)
            )
        )

        self.btn_tv = RoundedButton(
            text="TV (IR)",
            bg_color=(0.15, 0.15, 0.15, 1),
            text_color=(1, 1, 1, 1),
        )
        self.btn_tv.bind(
            on_press=lambda x: self.toggle_btn(
                self.btn_tv, (1, 0.6, 0, 1), (0, 0, 0, 1)
            )
        )

        grid.add_widget(self.btn_sala)
        grid.add_widget(self.btn_quarto)
        grid.add_widget(self.btn_vent)
        grid.add_widget(self.btn_tv)
        main_layout.add_widget(grid)

        # 4. BOTÃO GARAGEM
        self.btn_garagem = RoundedButton(
            text="GARAGEM",
            bg_color=(0.15, 0.15, 0.15, 1),
            text_color=(1, 1, 1, 1),
            size_hint_y=None,
            height=50,
        )
        self.btn_garagem.bind(
            on_press=lambda x: self.toggle_btn(
                self.btn_garagem, (1, 0.6, 0, 1), (0, 0, 0, 1)
            )
        )
        main_layout.add_widget(self.btn_garagem)

        # 5. BOTÃO MODO NOITE
        self.btn_noite = RoundedButton(
            text="🌙  MODO NOITE",
            bg_color=(0.1, 0.1, 0.1, 1),
            text_color=(1, 0.5, 0, 1),
            size_hint_y=None,
            height=50,
        )
        main_layout.add_widget(self.btn_noite)

        # 6. BOTÃO FALAR COM JAVA
        self.btn_java = RoundedButton(
            text="🎙️  FALAR COM JAVA",
            bg_color=(1, 0.6, 0, 1),
            text_color=(0, 0, 0, 1),
            size_hint_y=None,
            height=55,
        )
        main_layout.add_widget(self.btn_java)

        # 7. BOTÃO ABRIR PORTA
        self.btn_porta = RoundedButton(
            text="ABRIR PORTA",
            bg_color=(0, 0, 0, 1),
            text_color=(0, 0.9, 0.3, 1),
            border_color=(0, 0.9, 0.3, 1),  # Borda verde
            size_hint_y=None,
            height=50,
        )
        main_layout.add_widget(self.btn_porta)

        scroll.add_widget(main_layout)
        return scroll

    def update_clock(self, dt):
        self.lbl_clock.text = time.strftime("%H:%M:%S")

    def toggle_btn(self, btn, active_bg, active_text):
        if btn.custom_bg == active_bg:
            btn.custom_bg = (0.15, 0.15, 0.15, 1)
            btn.color = (1, 1, 1, 1)
        else:
            btn.custom_bg = active_bg
            btn.color = active_text
        btn._update_canvas()


if __name__ == "__main__":
    CasaInteligenteApp().run()
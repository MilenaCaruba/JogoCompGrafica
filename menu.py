"""
menu.py — Tela de menu principal do jogo.

Exibe título, botões Jogar / Sair e (opcionalmente) o resultado da partida anterior.
"""

from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import DirectFrame, DirectButton
from panda3d.core import TextNode


class Menu:
    """
    Painel de menu principal com botões Jogar e Sair.
    Pode exibir o resultado da última partida.
    """

    def __init__(self, base, on_start, on_quit):
        self.base     = base
        self._on_start = on_start
        self._on_quit  = on_quit

        # ── Frame de fundo que cobre a tela inteira ───────────────────────
        self._frame = DirectFrame(
            frameColor=(0.05, 0.07, 0.18, 1.0),
            frameSize=(-2, 2, -1.2, 1.2),
            pos=(0, 0, 0),
        )

        # ── Título ─────────────────────────────────────────────────────────
        OnscreenText(
            text="COLETOR 3D",
            pos=(0, 0.62),
            scale=0.20,
            fg=(1.0, 0.85, 0.0, 1),
            shadow=(0, 0, 0, 1),
            shadowOffset=(0.006, 0.006),
            align=TextNode.ACenter,
            parent=self._frame,
        )

        OnscreenText(
            text="Trabalho de Computacao Grafica",
            pos=(0, 0.42),
            scale=0.055,
            fg=(0.65, 0.75, 1.0, 1),
            align=TextNode.ACenter,
            parent=self._frame,
        )

        # ── Separador decorativo ───────────────────────────────────────────
        OnscreenText(
            text="─" * 36,
            pos=(0, 0.30),
            scale=0.045,
            fg=(0.3, 0.4, 0.6, 1),
            align=TextNode.ACenter,
            parent=self._frame,
        )

        # ── Instruções ─────────────────────────────────────────────────────
        OnscreenText(
            text="Colete todos os 15 objetos espalhados pelo mapa!\n"
                 "W / S  —  mover      A / D  —  girar      Mouse  —  olhar",
            pos=(0, 0.14),
            scale=0.055,
            fg=(0.80, 0.80, 0.80, 1),
            align=TextNode.ACenter,
            parent=self._frame,
        )

        # ── Botão JOGAR ─────────────────────────────────────────────────────
        DirectButton(
            text="  JOGAR  ",
            scale=0.10,
            pos=(0, 0, -0.12),
            frameSize=(-3.2, 3.2, -0.7, 1.0),
            frameColor=[
                (0.15, 0.55, 0.15, 1),   # normal
                (0.22, 0.75, 0.22, 1),   # hover
                (0.10, 0.38, 0.10, 1),   # pressed
                (0.08, 0.25, 0.08, 1),   # disabled
            ],
            text_fg=(1, 1, 1, 1),
            text_shadow=(0, 0, 0, 0.8),
            relief=1,
            command=on_start,
            parent=self._frame,
        )

        # ── Botão SAIR ──────────────────────────────────────────────────────
        DirectButton(
            text="  SAIR  ",
            scale=0.085,
            pos=(0, 0, -0.35),
            frameSize=(-3.2, 3.2, -0.7, 1.0),
            frameColor=[
                (0.50, 0.10, 0.10, 1),
                (0.70, 0.18, 0.18, 1),
                (0.35, 0.06, 0.06, 1),
                (0.25, 0.04, 0.04, 1),
            ],
            text_fg=(1, 1, 1, 1),
            text_shadow=(0, 0, 0, 0.8),
            relief=1,
            command=on_quit,
            parent=self._frame,
        )

        # ── Área de resultado da última partida (oculta inicialmente) ───────
        self._result_text = OnscreenText(
            text="",
            pos=(0, -0.60),
            scale=0.055,
            fg=(0.6, 1.0, 0.6, 1),
            shadow=(0, 0, 0, 0.7),
            align=TextNode.ACenter,
            mayChange=True,
            parent=self._frame,
        )

    # ─────────────────────────────────────────────────────────────────────────
    def show(self, last_score: int = None, last_time: float = None):
        """Exibe o menu. Se informados, mostra o resultado da última partida."""
        if last_score is not None:
            self._result_text.setText(
                f"Ultima partida:  {last_score} pontos  em  {last_time:.1f}s"
            )
        else:
            self._result_text.setText("")
        self._frame.show()

    def hide(self):
        self._frame.hide()

    def destroy(self):
        self._frame.destroy()

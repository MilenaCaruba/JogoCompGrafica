"""
hud.py — Interface gráfica sobreposta (HUD).

Exibe:
  - Pontuação atual
  - Itens restantes
  - Cronômetro
  - Tela de vitória ao concluir a coleta
"""

from direct.gui.OnscreenText import OnscreenText
from direct.gui.DirectGui import DirectFrame, DirectLabel, DirectButton
from panda3d.core import TextNode, Vec4


class HUD:
    """
    Gerencia todos os elementos de texto e UI na tela.
    """

    def __init__(self, base):
        self.base         = base
        self.score        = 0
        self.elapsed_time = 0.0

        # ── Painel superior esquerdo ─────────────────────────────────────
        self._score_text = OnscreenText(
            text="Pontos: 0",
            pos=(-1.55, 0.88),
            scale=0.07,
            fg=(1, 1, 0.2, 1),
            shadow=(0, 0, 0, 0.8),
            shadowOffset=(0.003, 0.003),
            align=TextNode.ALeft,
            mayChange=True,
        )

        self._items_text = OnscreenText(
            text="Itens: 0 / 0",
            pos=(-1.55, 0.78),
            scale=0.06,
            fg=(0.9, 0.9, 0.9, 1),
            shadow=(0, 0, 0, 0.8),
            shadowOffset=(0.003, 0.003),
            align=TextNode.ALeft,
            mayChange=True,
        )

        self._timer_text = OnscreenText(
            text="Tempo: 0s",
            pos=(-1.55, 0.68),
            scale=0.06,
            fg=(0.7, 1.0, 1.0, 1),
            shadow=(0, 0, 0, 0.8),
            shadowOffset=(0.003, 0.003),
            align=TextNode.ALeft,
            mayChange=True,
        )

        # ── Mira central ─────────────────────────────────────────────────
        self._crosshair = OnscreenText(
            text="+",
            pos=(0, 0),
            scale=0.05,
            fg=(1, 1, 1, 0.8),
            shadow=(0, 0, 0, 0.5),
            align=TextNode.ACenter,
        )

        # ── Dicas de controle ─────────────────────────────────────────────
        self._help_text = OnscreenText(
            text="WASD: mover  |  Mouse: girar  |  ESC: sair",
            pos=(0, -0.92),
            scale=0.045,
            fg=(0.7, 0.7, 0.7, 0.8),
            shadow=(0, 0, 0, 0.6),
            align=TextNode.ACenter,
        )

        # ── Tela de vitória (inicialmente oculta) ─────────────────────────
        self._victory_frame = None

    # ────────────────────────────────────────────────────────────────────────
    def update(self, dt: float):
        """Atualiza cronômetro e textos a cada frame."""
        self.elapsed_time += dt

        total     = self.base.collectible_manager.total()
        remaining = self.base.collectible_manager.remaining()
        collected = total - remaining

        self._score_text.setText(f"Pontos: {self.score}")
        self._items_text.setText(f"Itens: {collected} / {total}")
        self._timer_text.setText(f"Tempo: {self.elapsed_time:.1f}s")

    def add_score(self, points: int):
        self.score += points

    def destroy(self):
        """Remove todos os elementos do HUD da tela."""
        self._score_text.removeNode()
        self._items_text.removeNode()
        self._timer_text.removeNode()
        self._crosshair.removeNode()
        self._help_text.removeNode()
        if self._victory_frame:
            self._victory_frame.destroy()
            self._victory_frame = None

    # ────────────────────────────────────────────────────────────────────────
    # Tela de vitória
    # ────────────────────────────────────────────────────────────────────────
    def show_victory(self, final_score: int, final_time: float,
                     on_restart=None, on_menu=None):
        """Exibe painel de vitoria com botoes de acao."""

        self._victory_frame = DirectFrame(
            frameColor=(0, 0, 0, 0.75),
            frameSize=(-0.85, 0.85, -0.62, 0.62),
            pos=(0, 0, 0),
        )

        OnscreenText(
            text="VOCE VENCEU!",
            pos=(0, 0.40),
            scale=0.13,
            fg=(1.0, 0.85, 0.0, 1),
            shadow=(0, 0, 0, 1),
            shadowOffset=(0.005, 0.005),
            align=TextNode.ACenter,
            parent=self._victory_frame,
        )

        OnscreenText(
            text=f"Pontuacao final:  {final_score} pontos",
            pos=(0, 0.18),
            scale=0.075,
            fg=(1, 1, 1, 1),
            align=TextNode.ACenter,
            parent=self._victory_frame,
        )

        OnscreenText(
            text=f"Tempo:  {final_time:.1f} segundos",
            pos=(0, 0.04),
            scale=0.065,
            fg=(0.7, 1.0, 1.0, 1),
            align=TextNode.ACenter,
            parent=self._victory_frame,
        )

        # Botao Jogar Novamente
        if on_restart:
            DirectButton(
                text="  Jogar Novamente  ",
                scale=0.075,
                pos=(-0.28, 0, -0.22),
                frameSize=(-3.5, 3.5, -0.75, 1.0),
                frameColor=[
                    (0.15, 0.50, 0.15, 1),
                    (0.22, 0.70, 0.22, 1),
                    (0.10, 0.35, 0.10, 1),
                    (0.08, 0.25, 0.08, 1),
                ],
                text_fg=(1, 1, 1, 1),
                relief=1,
                command=on_restart,
                parent=self._victory_frame,
            )

        # Botao Menu Principal
        if on_menu:
            DirectButton(
                text="  Menu Principal  ",
                scale=0.075,
                pos=(0.30, 0, -0.22),
                frameSize=(-3.5, 3.5, -0.75, 1.0),
                frameColor=[
                    (0.15, 0.25, 0.55, 1),
                    (0.22, 0.38, 0.75, 1),
                    (0.10, 0.18, 0.38, 1),
                    (0.08, 0.12, 0.28, 1),
                ],
                text_fg=(1, 1, 1, 1),
                relief=1,
                command=on_menu,
                parent=self._victory_frame,
            )

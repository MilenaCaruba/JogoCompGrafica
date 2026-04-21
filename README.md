# Coletor 3D — Trabalho de Computação Gráfica

Jogo 3D de coleta em primeira pessoa desenvolvido com **Python + Panda3D**.

---

## Estrutura do projeto

```
trabalho_compgrafica/
├── main.py           # Ponto de entrada — máquina de estados Menu / Jogo
├── menu.py           # Tela de menu principal com botões e resultado anterior
├── player.py         # Controlador FPS (câmera, WASD, mouse center-warp)
├── collectibles.py   # Geometria procedural, animação e sistema de coleta
├── scene.py          # Cenário 3D (laje, paredes, árvores, plataformas, skybox)
├── hud.py            # HUD (pontos, timer, tela de vitória com botões)
├── requirements.txt  # Dependência: panda3d>=1.10.13
├── .gitignore
└── README.md
```

---

## Dependências

| Pacote  | Versão mínima | Uso |
|---------|---------------|-----|
| panda3d | 1.10.13 | Engine 3D (render, input, colisão, GUI, áudio) |

Python recomendado: **3.9 – 3.11**

---

## Instalação e execução

### 1. Clonar o repositório

```bash
git clone https://github.com/inoa-rfschuinki/JogoCompGrafica.git
cd JogoCompGrafica
```

### 2. (Opcional) Criar ambiente virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Executar

```bash
python main.py
```

---

## Fluxo do jogo

```
┌─────────────┐   Jogar    ┌─────────────┐   Todos coletados   ┌──────────────┐
│  Menu       │ ─────────► │  Partida    │ ──────────────────► │  Vitória     │
│  Principal  │            │  em curso   │                     │  (painel)    │
└─────────────┘            └─────────────┘                     └──────┬───────┘
       ▲                          │ ESC                               │
       └──────────────────────────┘        Menu Principal ◄───────────┘
                                                    ou
                                           Jogar Novamente ──► (nova partida)
```

---

## Controles

| Tecla / Dispositivo | Ação |
|---------------------|------|
| **W** | Mover para frente |
| **S** | Mover para trás |
| **A** | Girar à esquerda |
| **D** | Girar à direita |
| **Mouse** | Controlar câmera (yaw + pitch) |
| **ESC** (durante o jogo) | Voltar ao menu principal |
| **ESC** (no menu) | Fechar o jogo |

---

## Objetivo

Colete todos os **15 objetos** espalhados pelo mapa no menor tempo possível.  
Ao coletar o último item a tela de vitória exibe pontuação, tempo e dois botões:
- **Jogar Novamente** — inicia uma nova partida imediatamente
- **Menu Principal** — volta ao menu (exibe resultado da última partida)

---

## Conceitos de Computação Gráfica demonstrados

| Conceito | Onde é aplicado |
|----------|-----------------|
| **Geometria procedural** | `collectibles.py` (esfera UV subdividida, cubo com normais por face) e `scene.py` (laje, caixas, árvores) |
| **Normais de superfície** | Calculadas manualmente em todas as primitivas para iluminação correta |
| **Material Phong** (difuso + especular + ambiente) | Todos os objetos via `panda3d.core.Material` |
| **Iluminação** (ambiente + direcional "sol" + contraluz) | `main.py → _setup_lighting()` com 3 luzes |
| **Grafo de cena hierárquico** | NodePath pai/filho: `render → scene_root`, `pivot → camera`, `root → geom + col_np` |
| **Transformações T/R por frame** | `player.py` (translação + heading/pitch), coletáveis (rotação + bob) |
| **Animação senoidal (bob)** | `collectibles.py` — oscilação vertical via `sin(elapsed * speed + phase)` |
| **Colisão esférica** | `CollisionSphere` + `CollisionTraverser` + `CollisionHandlerEvent` + tags `cid` |
| **Câmera FPS (center-warp)** | `player.py` — separação heading (pivot Z) / pitch (câmera X), warp ao centro |
| **Lente perspectiva** | `camLens.setFov(75)`, `setNear(0.1)`, `setFar(1000)` |
| **Skybox** | Cubo invertido 400u com `setLightOff()` + `setColor()` + bin "background" |
| **HUD 2D sobreposto** | `OnscreenText`, `DirectFrame`, `DirectButton` em coordenadas normalizadas |
| **Máquina de estados** | `main.py` — estados MENU / JOGO com criação e destruição limpa de subsistemas |
| **Anti-aliasing** | `render.setAntialias(AntialiasAttrib.MAuto)` |

---

## Descrição técnica dos arquivos

### `main.py`
Classe `Game` (herda `ShowBase`). Implementa uma **máquina de estados** com dois modos:
- **Menu**: menu visível, cena 3D inexistente, mouse livre
- **Jogo**: cena construída, HUD ativo, mouse capturado  

Gerencia o ciclo completo de vida dos subsistemas (`_start_game` / `_cleanup_game` / `_go_to_menu`).

### `menu.py`
Classe `Menu`. Painel de tela cheia com título, instruções e botões **Jogar** / **Sair**. Exibe o resultado da última partida ao retornar do jogo.

### `player.py`
Classe `Player`. Usa um nó **pivot** para desacoplar rotação horizontal (heading, eixo Z) da inclinação vertical da câmera (pitch, eixo X). O controle de mouse usa **center-warp**: lê o delta em relação ao centro da janela e reposiciona o cursor a cada frame. Limite de pitch ±80°. Velocidade de movimento: 10 u/s; rotação por teclado: 90°/s.

### `collectibles.py`
Funções `_make_sphere_geom` (esfera UV, 12×16 subdivisões) e `_make_cube_geom` (cubo com normais por face) constroem geometria via `GeomVertexData` + `GeomTriangles`. Cada `Collectible` recebe uma **tag `cid`** no nó de colisão para identificação inequívoca no evento. `CollectibleManager` gerencia 15 itens em posições fixas.

### `scene.py`
`_make_box` gera caixas com normais por face. A classe `Scene` constrói: **laje de chão** sólida (evita ver o vazio sob o FOV), **4 paredes** limite, **16 árvores** (tronco + copa), **6 plataformas** decorativas e **skybox** (cubo 400u invertido com `setLightOff`).

### `hud.py`
`OnscreenText` para pontuação, contagem de itens e cronômetro. `DirectButton` na tela de vitória para "Jogar Novamente" e "Menu Principal". Método `destroy()` remove todos os nós da cena ao encerrar a partida.

# Coletor 3D — Trabalho de Computação Gráfica

Jogo 3D de coleta em primeira pessoa desenvolvido com **Python + Panda3D**.

---

## Estrutura do projeto

```
trabalho_compgrafica/
├── main.py           # Ponto de entrada — classe Game (loop principal)
├── player.py         # Controlador do jogador (câmera FPS + colisão)
├── collectibles.py   # Sistema de objetos coletáveis (geometria + animação)
├── scene.py          # Cenário 3D (chão, paredes, decorações, céu)
├── hud.py            # Interface HUD (pontos, timer, tela de vitória)
├── requirements.txt  # Dependência: panda3d
└── README.md         # Este arquivo
```

---

## Dependências

| Pacote   | Versão mínima | Uso                          |
|----------|---------------|------------------------------|
| panda3d  | 1.10.13       | Engine 3D completa (render, input, colisão, GUI) |

Python recomendado: **3.9 – 3.11**

---

## Instalação passo a passo

### 1. Criar e ativar ambiente virtual (opcional, mas recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Executar o jogo

```bash
python main.py
```

---

## Controles

| Tecla / Dispositivo | Ação                        |
|---------------------|-----------------------------|
| **W**               | Mover para frente           |
| **S**               | Mover para trás             |
| **A**               | Girar à esquerda            |
| **D**               | Girar à direita             |
| **Mouse**           | Controlar câmera (pitch/yaw) |
| **ESC**             | Sair do jogo                |

---

## Objetivo

Colete todos os **15 objetos** espalhados pelo mapa.  
Ao coletar o último item, uma tela de vitória exibe sua pontuação e tempo.

---

## Conceitos de Computação Gráfica demonstrados

| Conceito                        | Onde é aplicado                                  |
|---------------------------------|--------------------------------------------------|
| Geometria procedural            | `collectibles.py`, `scene.py` (esfera UV, cubo, plano com grid) |
| Normais de superfície           | Calculadas manualmente para iluminação Phong     |
| Material Phong (difuso + especular + ambiente) | Todos os objetos via `panda3d.core.Material` |
| Iluminação (ambiente + direcional + contraluz) | `main.py` — `_setup_lighting()`      |
| Grafo de cena hierárquico       | NodePath pai/filho (pivot → câmera, root → geom) |
| Transformações (T, R, S)        | `player.py` (translação/rotação), animação de coletáveis |
| Animação por interpolação       | Bob senoidal (`sin`) e rotação contínua nos coletáveis |
| Colisão esférica                | `CollisionSphere` + `CollisionTraverser` + `CollisionHandlerEvent` |
| Câmera de primeira pessoa       | Separação heading/pitch via nó pivot             |
| HUD / Texto 2D sobreposto       | `OnscreenText`, `DirectFrame` em coordenadas normalizadas |
| Skybox                          | Cubo grande com `setLightOff()` para cor constante |
| Anti-aliasing                   | `render.setAntialias(AntialiasAttrib.MAuto)`     |

---

## Descrição técnica dos arquivos

### `main.py`
Classe `Game` (herda `ShowBase`). Inicializa todos os subsistemas, configura iluminação, registra eventos de colisão e executa o task `_update` a cada frame.

### `player.py`
Classe `Player`. Usa um nó *pivot* para separar a rotação horizontal (heading, eixo Z) da inclinação vertical da câmera (pitch, eixo X). Lê entradas de teclado e mouse a cada frame, calculando deslocamento no plano XY e limitando o jogador ao mapa.

### `collectibles.py`
Funções `_make_sphere_geom` e `_make_cube_geom` constroem geometria via `GeomVertexData` + `GeomTriangles`. A classe `Collectible` anima cada item (rotação + bob senoidal). `CollectibleManager` instancia todos os itens e detecta coletas via nome do nó de colisão.

### `scene.py`
Função `_make_plane` gera chão com subdivisions para iluminação suave. `_make_box` cria caixas com normais por face. A classe `Scene` monta chão, paredes, árvores (tronco + copa), plataformas e skybox.

### `hud.py`
Usa `OnscreenText` e `DirectFrame` do Panda3D para exibir pontuação, contagem de itens, cronômetro e tela de vitória.

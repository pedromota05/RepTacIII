# Guia de Correções e Implementações (Questões A e B)

---

## Questão A: Consertar o preenchimento dos tiles na grid principal

Ocorriam três problemas simultâneos que quebravam o correto posicionamento e seleção das peças:
1. Posição ignorava a movimentação da câmera (âncora).
2. Mouse e renderização lidavam com escalas/resoluções diferentes.
3. Peças invisíveis duplicadas causavam seleções incorretas na paleta.

Abaixo estão os trechos e soluções aplicadas em cada arquivo para sanar o problema:

### 1. Correção do Posição no Mapa (`editor.py`)
Quando você clicava para adicionar um novo *tile* na grid, a peça era enviada para a posição visual da janela, e não a posição real do grande mapa de nível. O código antigo tentava salvar o *tile* diretamente nessas posições (`self.grid.level.tiles[lin][col]`).

**O que foi alterado em `editor.py`:**
```diff
-                                self.grid.level.tiles[lin][col] = self.pallet.select
-                                left = (col + self.grid.anchor[0]) * TILE_SIZE
-                                top = (lin + self.grid.anchor[1]) * TILE_SIZE
-                                self.grid.level.tiles[lin][col].rect.topleft = (left, top)

+                                map_col = col + self.grid.anchor[0]
+                                map_lin = lin + self.grid.anchor[1]
+
+                                # nova instância para não compartilhar o mesmo rect entre células
+                                placed = Tile(*self.tile_map.codes[self.pallet.select.id])
+                                left = map_col * TILE_SIZE
+                                top = map_lin * TILE_SIZE
+
+                                placed.rect.topleft = (left, top)
+                                self.grid.level.tiles[map_lin][map_col] = placed
```

### 2. Normalização do Mouse e Resolução (`editor.py`, `grid.py` e `pallet.py`)
O jogo lia a posição do clique do mouse usando o tamanho absoluto do seu monitor no Windows (`display.size`). No entanto, o motor `OpenGL` desenhava os elementos baseado numa escala interna (`WIDTH` e `HEIGHT`). O clique do mouse ocorria num local físico enquanto os tiles lógicos habitavam outro local proporcional. 

**O que foi alterado na leitura do clique em `editor.py`:**
Adicionamos a normalização com `WIDTH` e `HEIGHT` para que o *collidepoint* corresponda 100% à tela escalada.
```diff
             # mouse
             if event.type == pygame.MOUSEBUTTONDOWN:
                 x,y = pygame.mouse.get_pos()
+                x = (x / display.size[0]) * WIDTH
+                y = (y / display.size[1]) * HEIGHT
```

**O que foi alterado no tamanho lógico em `grid.py` e `pallet.py`:**
Em vez de desenhar dependendo do tamanho bruto do computador, fixamos no tamanho da constante lógica.

`grid.py`:
```diff
-        self.size = (display.size[0]*0.7, display.size[1]*0.8)
+        self.size = (WIDTH*0.7, HEIGHT*0.8)
...
-        self.rect.topleft = (display.size[0]*0.1, display.size[1]*0.1)      
+        self.rect.topleft = (WIDTH*0.1, HEIGHT*0.1)      
```

`pallet.py`:
```diff
-        self.size = (display.size[0]*0.1, display.size[1]*0.8)
+        self.size = (WIDTH*0.1, HEIGHT*0.8)
...
-        self.rect.topleft = (display.size[0]*0.9, display.size[1]*0.1)         
+        self.rect.topleft = (WIDTH*0.9, HEIGHT*0.1)         
```


### 3. Remoção de Tiles Duplicados na Paleta (`pallet.py`)
Sempre que a Paleta movia, a função `update_tiles` colocava todos os tiles de novo na lista visual, gerando centenas de blocos sobrepostos na memória que roubavam o clique incorretamente.

**O que foi alterado em `pallet.py`:**
```diff
     def clear(self):
         self.image.fill("black")
+        self.tiles.clear()
```

---

## Questão B: Adicione mais três tiles novos na paleta

Para disponibilizar 3 novos itens pra você utilizar na arquitetura, recortamos mais três coordenadas adjacentes aos itens já existentes e incluímos na base de IDs da classe.

**O que foi alterado em `tiles.py`:**
Adicionamos 3 novas extrações (`subsurface`) a partir da imagem nativa e as mapeamos aos ids *5, 6* e *7* na lista `codes`:

```diff
         self.floor2 = self.map_items.subsurface((768,448,TILE_CROP,TILE_CROP))
         self.brick1 = self.map_items.subsurface((320,144,TILE_CROP,TILE_CROP))
         self.brick2 = self.map_items.subsurface((832,400,TILE_CROP,TILE_CROP))
+        
+        # novos tiles adicionados (Questão B)
+        self.floor3 = self.map_items.subsurface((16,208,TILE_CROP,TILE_CROP))
+        self.brick3 = self.map_items.subsurface((336,144,TILE_CROP,TILE_CROP))
+        self.block1 = self.map_items.subsurface((32,208,TILE_CROP,TILE_CROP))
       
         # object codes
         self.codes = [            
             None,   # code by index - 0 draw nothing
             (1, self.floor1, "floor1"),     # id, surface, description
             (2, self.floor2, "floor2"),
             (3, self.brick1, "brick1"),
-            (4, self.brick2, "brick2")
+            (4, self.brick2, "brick2"),
+            (5, self.floor3, "floor3"),
+            (6, self.brick3, "brick3"),
+            (7, self.block1, "block1")
         ]
```

---

## Questão C: Botão de Salvar Nível

Foi implementado um sistema que varre os tiles renderizados no momento e os consolida em uma nova matriz esparsa, gravando em seguida sobre o arquivo binário original da fase (npz).

**O que foi alterado em `levels.py`:**
Criamos a rotina `save(self)` e removemos o código de debug `self.create_first_map()` que deletava as edições da fase assim que o arquivo era aberto.

```diff
     def load(self, tile_map):        
         # debug
-        self.create_first_map()
+        # self.create_first_map()
         
...

+    def save(self):
+        dense_matrix = np.zeros((TILE_MAP_LEVEL1[1], TILE_MAP_LEVEL1[0]), dtype=int)
+        for lin in range(TILE_MAP_LEVEL1[1]):
+            for col in range(TILE_MAP_LEVEL1[0]):
+                tile = self.tiles[lin][col]
+                if tile is not None:
+                    dense_matrix[lin,col] = tile.id
+        sparse_matrix = sp.csr_array(dense_matrix)
+        sp.save_npz(FILE_LV1, sparse_matrix)
+        print("Level saved to file!")
```

**O que foi alterado em `info.py` e `editor.py`:**
Renderizamos dinamicamente um botão "SAVE" posicionado no canto inferior esquerdo e injetamos a intercepção do clique no laço de eventos.

Em `info.py` (Criação visual do botão):
```diff
+        save_text = "[ SAVE ]"
+        self.image_save_btn = self.font2.render(save_text, True, pygame.Color("white"), pygame.Color("blue")).convert_alpha()
+        self.image_save_btn = pygame.transform.smoothscale_by(self.image_save_btn, 1/(SCALE*4))
+        self.rect_save_btn = self.image_save_btn.get_rect()
+        self.rect_save_btn.topleft = (0, HEIGHT - self.rect_save_btn.h)
+        self.texture_id_save_btn = utils.surface_to_texture(self.image_save_btn)
...
+        x, y, w, h = self.rect_save_btn.x, self.rect_save_btn.y, self.rect_save_btn.w, self.rect_save_btn.h
+        utils.draw_textured_quad(self.texture_id_save_btn, x, y, w, h)
```

Em `editor.py` (Lógica de Click):
```diff
             # mouse
             if event.type == pygame.MOUSEBUTTONDOWN:
                 x,y = pygame.mouse.get_pos()
                 x = (x / display.size[0]) * WIDTH
                 y = (y / display.size[1]) * HEIGHT
+                if self.info.rect_save_btn.collidepoint(x, y):
+                    self.grid.level.save()
```

---

## Questão D: Informações sobre a Paleta na Tela

Para disponibilizar informações sobre a paleta em tempo real na parte superior direita da tela, atualizamos a classe `Info` para receber uma referência da paleta.

**O que foi alterado em `editor.py`:**
A inicialização e a atualização foram reorganizadas para incluir a paleta no `info`.
```diff
-            self.grid = Grid(self.level1)
-            self.info = Info(self.grid)
-            self.pallet = Pallet(self.tile_map)
+            self.grid = Grid(self.level1)
+            self.pallet = Pallet(self.tile_map)
+            self.info = Info(self.grid, self.pallet)

...

-        self.info.update(dt, self.grid)
+        self.info.update(dt, self.grid, self.pallet)
```

**O que foi alterado em `info.py`:**
Adicionamos o texto, alinhando a posição usando a largura lógica do jogo no canto superior direito (`topright = (WIDTH, 0)`).

```diff
-from ..constants import SCALE, TILE_MAP_LEVEL1
+from ..constants import SCALE, TILE_MAP_LEVEL1, WIDTH
...
+from .pallet import Pallet
...
-    def __init__(self, grid:Grid): 
+    def __init__(self, grid:Grid, pallet:Pallet): 
...
+        pallet_text = f"Paleta: {len(pallet.tiles)} tiles | Sel: {pallet.select.id if pallet.select else 'None'}"
+        self.image_pallet = self.font2.render(pallet_text, True, pygame.Color("green"))
+        self.image_pallet = pygame.transform.smoothscale_by(self.image_pallet, 1/(SCALE*4))
+        self.rect_pallet = self.image_pallet.get_rect()
+        self.rect_pallet.topright = (WIDTH, 0)
+        self.texture_id_pallet = utils.surface_to_texture(self.image_pallet)
...
-    def update(self, dt:float, grid:Grid):
+    def update(self, dt:float, grid:Grid, pallet:Pallet):
...
+            pallet_text = f"Paleta: {len(pallet.tiles)} tiles | Sel: {pallet.select.id if pallet.select else 'None'}"
+            ...
+            self.texture_id_pallet = utils.update_texture(self.texture_id_pallet, self.image_pallet)
...
+        x, y, w, h = self.rect_pallet.x, self.rect_pallet.y, self.rect_pallet.w, self.rect_pallet.h
+        utils.draw_textured_quad(self.texture_id_pallet, x, y, w, h)
```

---

## Questão E: Remover tile com o clique direito

O evento `MOUSEBUTTONDOWN` informa qual botão foi pressionado em `event.button`: **1** = esquerdo, **2** = meio (scroll), **3** = direito. O clique esquerdo continua preenchendo, e o direito passa a apagar o tile, gravando `None` na posição real do mapa (considerando a âncora, igual à Questão A).

> Atenção: usar `event.button == 2` faz a remoção funcionar apenas com o botão do meio — o clique direito é o `3`.

**O que foi alterado em `editor.py`:**
```diff
              if event.type == pygame.MOUSEBUTTONDOWN:
-                 x,y = pygame.mouse.get_pos()
-                 ...
+                 if event.button == 1:
+                     x,y = pygame.mouse.get_pos()
+                     ...   # (lógica de salvar, selecionar na paleta e preencher a grid)
+                 elif event.button == 3:
+                     x, y = pygame.mouse.get_pos()
+                     x = (x / display.size[0]) * WIDTH
+                     y = (y / display.size[1]) * HEIGHT
+
+                     if self.grid.rect.collidepoint(x, y):
+                         for tile in self.grid.tiles:
+                             if tile.rect.collidepoint(x, y):
+                                 col, lin = tile.desc.split(",")
+                                 col = int(col)
+                                 lin = int(lin)
+
+                                 map_col = col + self.grid.anchor[0]
+                                 map_lin = lin + self.grid.anchor[1]
+
+                                 # Remove o tile
+                                 self.grid.level.tiles[map_lin][map_col] = None
+                                 self.notify_fill.event()
+                                 break
```

Como o `save()` da Questão C só grava tiles diferentes de `None`, as posições removidas são salvas como `0` (vazio) no arquivo.

---

## Questão F: Botões de navegação nos quatro lados da grid

Criamos um componente novo com quatro botões de seta posicionados ao redor da grid (acima, abaixo, à esquerda e à direita). As setas são desenhadas com `pygame.draw.polygon`, para não depender de a fonte ter os caracteres de seta. Segurar o clique esquerdo sobre um botão move a grid continuamente, igual às setas do teclado.

**Arquivo novo `navigation.py`:**
Cada botão guarda seu `rect` (posicionado relativo ao `grid.rect`), sua textura e a direção `(dx, dy)` de movimento.
```diff
+BTN_SIZE = 48
+BTN_GAP = 8
+
+class NavButtons():
+    def __init__(self, grid:Grid):
+        r = grid.rect
+        self.directions = {
+            "up":    (0, -1),
+            "down":  (0, 1),
+            "left":  (-1, 0),
+            "right": (1, 0),
+        }
+        ...
+        for name in self.directions:
+            rect = pygame.Rect(0, 0, BTN_SIZE, BTN_SIZE)
+            if name == "up":
+                rect.midbottom = (r.centerx, r.top - BTN_GAP)
+            elif name == "down":
+                rect.midtop = (r.centerx, r.bottom + BTN_GAP)
+            elif name == "left":
+                rect.midright = (r.left - BTN_GAP, r.centery)
+            elif name == "right":
+                rect.midleft = (r.right + BTN_GAP, r.centery)
+            self.rects[name] = rect
+            self.textures[name] = utils.surface_to_texture(self.make_arrow(name))
+
+    def make_arrow(self, name:str) -> pygame.Surface:
+        ...   # fundo azul com borda branca + triângulo branco apontando para a direção
+        pygame.draw.polygon(surf, "white", points)
+        return surf
+
+    def collide(self, x, y):
+        """Retorna (dx, dy) do botão sob o ponto (x, y), ou None."""
+        for name, rect in self.rects.items():
+            if rect.collidepoint(x, y):
+                return self.directions[name]
+        return None
+
+    def draw(self):
+        for name, rect in self.rects.items():
+            utils.draw_textured_quad(self.textures[name], rect.x, rect.y, rect.w, rect.h)
```

**O que foi alterado em `editor.py`:**
A lógica de movimento, que estava repetida para cada seta do teclado, foi centralizada em `move_anchor(dx, dy)`, que limita a âncora às bordas do mapa. Teclado e botões passam a usar o mesmo método.
```diff
+from .navigation import NavButtons
...
             self.info = Info(self.grid, self.pallet)
+            self.nav = NavButtons(self.grid)
...
         keys = pygame.key.get_pressed()
         if keys[pygame.K_LEFT]:
-            if self.grid.anchor[0] > 0:
-                self.grid.anchor[0] -= 1
-                self.notify_anchor.event()
+            self.move_anchor(-1, 0)
         if keys[pygame.K_RIGHT]:
-            max = TILE_MAP_LEVEL1[0] - self.grid.x_tiles
-            if self.grid.anchor[0] < max:
-                self.grid.anchor[0] += 1
-                self.notify_anchor.event()
+            self.move_anchor(1, 0)
         if keys[pygame.K_UP]:
-            ...
+            self.move_anchor(0, -1)
         if keys[pygame.K_DOWN]:
-            ...
+            self.move_anchor(0, 1)
+
+        # botões de navegação - segurar o botão esquerdo move continuamente
+        if pygame.mouse.get_pressed()[0]:
+            x,y = pygame.mouse.get_pos()
+            x = (x / display.size[0]) * WIDTH
+            y = (y / display.size[1]) * HEIGHT
+            direction = self.nav.collide(x, y)
+            if direction:
+                self.move_anchor(*direction)
+
+    def move_anchor(self, dx:int, dy:int):
+        """Move a âncora da grid respeitando os limites do mapa"""
+        max_x = TILE_MAP_LEVEL1[0] - self.grid.x_tiles
+        max_y = TILE_MAP_LEVEL1[1] - self.grid.y_tiles
+        new_x = min(max(self.grid.anchor[0] + dx, 0), max_x)
+        new_y = min(max(self.grid.anchor[1] + dy, 0), max_y)
+        if [new_x, new_y] != self.grid.anchor:
+            self.grid.anchor[0] = new_x
+            self.grid.anchor[1] = new_y
+            self.notify_anchor.event()
...
         self.pallet.draw()
+        self.nav.draw()
```

import pygame
from ..utils import utils
from .grid import Grid

BTN_SIZE = 48
BTN_GAP = 8


class NavButtons():
    """Botões de navegação (setas) posicionados nos quatro lados da grid."""
    def __init__(self, grid:Grid):
        r = grid.rect
        # direção -> (dx, dy) de movimento da âncora
        self.directions = {
            "up":    (0, -1),
            "down":  (0, 1),
            "left":  (-1, 0),
            "right": (1, 0),
        }
        self.rects:dict[str, pygame.Rect] = {}
        self.textures:dict[str, int] = {}

        for name in self.directions:
            rect = pygame.Rect(0, 0, BTN_SIZE, BTN_SIZE)
            if name == "up":
                rect.midbottom = (r.centerx, r.top - BTN_GAP)
            elif name == "down":
                rect.midtop = (r.centerx, r.bottom + BTN_GAP)
            elif name == "left":
                rect.midright = (r.left - BTN_GAP, r.centery)
            elif name == "right":
                rect.midleft = (r.right + BTN_GAP, r.centery)
            self.rects[name] = rect
            self.textures[name] = utils.surface_to_texture(self.make_arrow(name))


    def make_arrow(self, name:str) -> pygame.Surface:
        s = BTN_SIZE
        surf = pygame.Surface((s, s), pygame.SRCALPHA).convert_alpha()
        surf.fill((0, 0, 0, 0))
        pygame.draw.rect(surf, "blue", (0, 0, s, s), border_radius=8)
        pygame.draw.rect(surf, "white", (0, 0, s, s), 2, border_radius=8)
        m = s // 4      # margem
        c = s // 2      # centro
        points = {
            "up":    [(c, m), (s - m, s - m), (m, s - m)],
            "down":  [(m, m), (s - m, m), (c, s - m)],
            "left":  [(m, c), (s - m, m), (s - m, s - m)],
            "right": [(m, m), (s - m, c), (m, s - m)],
        }[name]
        pygame.draw.polygon(surf, "white", points)
        return surf


    def collide(self, x, y):
        """Retorna (dx, dy) do botão sob o ponto (x, y), ou None."""
        for name, rect in self.rects.items():
            if rect.collidepoint(x, y):
                return self.directions[name]
        return None


    def draw(self):
        for name, rect in self.rects.items():
            utils.draw_textured_quad(self.textures[name], rect.x, rect.y, rect.w, rect.h)

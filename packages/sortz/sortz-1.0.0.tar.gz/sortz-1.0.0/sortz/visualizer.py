import pygame
from random import randint
from .sorters import bubble_sort

class Visualizer:
    """
    Pygame based GUI for visualizing sorting algorithms.
    """

    def __init__(self, sorter, fps):
        """
        Initialize the GUI.

        Parameters
        ----------
        sorter : generator
            A generator which sorts a single item in an array per iteration.
        fps : int
            The framerate of the visualizer
        """

        self._init_pygame()
        self.fps = fps
        self.screen = pygame.display.set_mode((800, 600))
        self.colors = {
            'black' : (0, 0, 0),
            'white' : (255, 255, 255),
            'red' : (255, 0, 0),
        }
        self.clock = pygame.time.Clock()
        font = pygame.font.Font(None, 12)
        self.display = {
        'font' : font,
        'line1' : font.render("", True, self.colors['red'], None),
        'line2' : font.render("", True, self.colors['red'], None),
        'line3' : font.render("", True, self.colors['red'], None),
        }
        self.is_sorted = False
        self.paused = False

        # Create list of bars as (Surface, Rect) tuples
        self.bars = []
        for _ in range(100):
            surf = pygame.Surface((8, randint(10, 600)))
            rect = surf.get_rect()
            self.bars.append((surf, rect))
        
        # Color screen and rectangles
        self.screen.fill(self.colors['black'])
        for surf, _ in self.bars:
            surf.fill(self.colors['white'])

        # Set initial position of bars on screen
        self.xcoords = []
        screen_height = self.screen.get_rect().height
        for i, (surf, rect) in enumerate(self.bars):
            rect.bottom = screen_height
            rect.left = 8 * i
            self.xcoords.append(8 * i)

        # Initialize the sorter generator
        self.sorter = sorter(self.bars)

    def main_loop(self):
        while True:
            self._handle_input()
            self._update()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Sorting Visualizer")

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.paused = not self.paused
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.fps = self.fps + 1 if self.fps < 120 else 120
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self.fps = self.fps - 1 if self.fps > 1 else 1

    def _update(self):
        # Sort and update position if needed
        if not self.is_sorted and not self.paused:
            self.is_sorted = next(self.sorter)

            for (_, rect), xcoord in zip(self.bars, self.xcoords):
                rect.left = xcoord

        # Update display text
        self.display['line1'] = self.display['font'].render(f"Sorted: {self.is_sorted}",
                                                            True, self.colors['red'], None)
        self.display['line2'] = self.display['font'].render(f"FPS: {self.fps}",
                                                            True, self.colors['red'], None)
        self.display['line3'] = self.display['font'].render(f"Paused: {self.paused}",
                                                            True, self.colors['red'], None)

    def _draw(self):
        # Draw rects
        self.screen.fill(self.colors['black'])
        for surf, rect in self.bars:
            self.screen.blit(surf, rect)

        # Draw display
        self.screen.blit(self.display['line1'], (0, 0))
        self.screen.blit(self.display['line2'], (0, 8))
        self.screen.blit(self.display['line3'], (0, 16))

        # Maintain framerate
        self.clock.tick(self.fps)

        pygame.display.flip()

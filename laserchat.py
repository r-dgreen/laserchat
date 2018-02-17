import pygame
from itertools import product
from random import randrange


class LaserChat:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Laser Chat")
        #self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN | pygame.DOUBLEBUF)
        self.screen = pygame.display.set_mode((1366, 768), pygame.DOUBLEBUF)
        self.h_slices = 80
        self.v_slices = 45
        self.screen_width, self.screen_height = self.screen.get_size()
        self.x_multiplier = self.screen_width // self.h_slices
        self.y_multiplier = self.screen_height // self.v_slices
        
        self.entry_text_font = pygame.font.SysFont('mono', 20, bold=True)        
        self.text_colors = [(255,0,0), (255,128,0), (255,255,0), (128,255,0), (0,255,0), (0,255,128), (0,255,255), (0,128,255), (0,0,255), (128,0,255), (255,0,255), (255,0,128)]
        self.entry_text_index = randrange(0, len(self.text_colors))
        self.entry_text = ''
        self.chatbox_text = ''

        self.to_font = pygame.font.SysFont('mono', 20, bold=True)        
        self.to = 1
        
        self.background = pygame.Surface((self.screen_width, self.screen_height)).convert()
        self.background.fill((64,64,64))
        self.grid = self.generate_grid()
        self.populate_background()


        
        self.clock = pygame.time.Clock()
        
    def generate_grid(self):
        """Split the grid into the given number of sections for coord snapping"""
        grid = self.background
        left_pad = (self.screen_width % (self.x_multiplier * self.h_slices)) // 2
        top_pad = (self.screen_height % (self.y_multiplier * self.v_slices)) // 2
        x_pos = [(self.x_multiplier * x) + left_pad for x in range(self.h_slices)]
        y_pos = [(self.y_multiplier * y) + top_pad for y in range(self.v_slices)]
        coords = [[(x, y) for y in y_pos] for x in x_pos]
        return coords

    def draw_backgrid(self, surface=None):
        if not surface:
            surface = self.background
        self.draw_shape((0,0), (self.h_slices, self.v_slices), (0,0,0), surface=None)
        for col in range(1, 80):
            pygame.draw.line(surface, (col, 16, 16), self.grid[col][1], self.grid[col][44])
        for row in range(1,45):
            pygame.draw.line(surface, (row, 16, 16), self.grid[1][row], self.grid[79][row])
    
    def draw_horizontal_pipe(self, surface=None):
        self.draw_shape((0,23), (80, 2), (64,64,196), surface=surface)
        self.draw_shape((0,23), (80, 1), (80,80,196), surface=surface)    
        
    def draw_lower_pipe(self, surface=None):
        self.draw_shape((38,20), (2, 21), (64,64,196), surface=surface)
        self.draw_shape((39,20), (1, 21), (80,80,196), surface=surface)
        
    def draw_router(self, surface=None):
        self.draw_shape((30,18), (18,12), (8,8,196), surface=surface)
        self.draw_shape((30,27), (18,6), (8,8,196), type='ellipse', surface=surface)
        self.draw_shape((32,21), (14,8), (8,8,16), surface=surface)
        self.draw_shape((32,27), (14,4), (8,8,16), type='ellipse', surface=surface)
        self.draw_shape((31,19), (16,4), (8,8,196), type='ellipse', surface=surface)
        self.draw_shape((30,15), (18,6), (64,64,255), type='ellipse', surface=surface)

    def draw_upper_pipe(self, surface=None):
        self.draw_shape((36,17), (6, 1), (32,32,196), type='ellipse', surface=surface)        
        self.draw_shape((38,6), (2, 12), (64,64,196), surface=surface)
        self.draw_shape((39,6), (1, 12), (80,80,196), surface=surface)
    
    def draw_entry_box(self, surface=None):
        self.draw_shape((0,41), (80, 4), (32,32,32), surface=surface)
        self.draw_shape((1,42), (78, 2), (8,8,8), surface=surface)
        self.draw_shape((0,40), (80, 1), (128,128,128), surface=surface)
        
    def draw_chat_box(self,surface=None):
        self.draw_shape((0,0), (80, 10), (128,128,128), surface=surface)
        self.draw_shape((1,1), (78, 8), (64,64,64), surface=surface)
        self.draw_shape((0,10), (80, 1), (32,32,32), surface=surface)
        
    def draw_hud(self, surface=None):
        self.draw_shape((0,35), (6,5), (128,128,128), surface=surface)
        self.draw_shape((1,36), (4,4), (32,32,32), surface=surface)
        self.draw_shape((2,37), (2,2), self.text_colors[self.entry_text_index], surface=surface)    
        self.draw_poly([(2,37), (3,36), (4,37)], (128,128,128), surface=surface)
        self.draw_poly([(2,39), (3,40), (4,39)], (128,128,128), surface=surface)        
        self.draw_shape((1,36), (1,4), (16,16,16), surface=surface)
        self.draw_shape((4,36), (1,4), (16,16,16), surface=surface)
        
        self.draw_shape((74,35), (6,5), (128,128,128), surface=surface)
        self.draw_shape((75,36), (4,4), (32,32,32), surface=surface)
        self.draw_poly([(75,38), (76,37), (76,39)], (128,128,128), surface=surface)
        self.draw_poly([(79,38), (78,37), (78,39)], (128,128,128), surface=surface)
        self.draw_shape((76,37), (2,2), (8,8,8), surface=surface)
        self.draw_shape((75,36), (4,1), (16,16,16), surface=surface)
        self.draw_shape((75,39), (4,1), (16,16,16), surface=surface)

    
    def populate_background(self):
        self.draw_backgrid()
        self.draw_horizontal_pipe()
        self.draw_lower_pipe()
        self.draw_router()
        self.draw_upper_pipe()
        self.draw_entry_box()
        self.draw_chat_box()
        self.draw_hud()
        
    def draw_poly(self, coords, color, surface=None):
        if not surface:
            surface = self.background
        coord_list = [self.grid[coord[0]][coord[1]] for coord in coords]
        pygame.draw.polygon(surface, color, coord_list)
        
    def draw_shape(self, coords, size, color, type='box', surface=None):
        if not surface:
            surface = self.background
        x, y = self.grid[coords[0]][coords[1]]        
        w = size[0] * self.x_multiplier
        h = size[1] * self.y_multiplier

        if type == 'box':
            pygame.draw.rect(surface, color, (x, y, w, h))
        elif type == 'ellipse':
            pygame.draw.ellipse(surface, color, (x, y, w, h))

    def draw_entry_text(self, text, coords):
        x, y = self.grid[coords[0]][coords[1]] 
        y += self.y_multiplier // 2
        surface = self.entry_text_font.render(text, True, self.text_colors[self.entry_text_index])
        self.screen.blit(surface, (x, y))
        
    def draw_to_text(self):
        x, y = self.grid[76][37] 
        y += (self.y_multiplier // 2) - 1
        x += (self.x_multiplier // 2) - 3
        surface = self.to_font.render('{:02}'.format(self.to), True, (255,255,255))
        self.screen.blit(surface, (x, y))
            
    def scroll_letter_up(self, letter='X', delay=0, color=(255,255,255)):
        x, y = self.grid[38][40]
        end_y = self.grid[40][32][1]
        x += (self.x_multiplier // 2) + 3
        while delay > 0:
            delay -= 1
            yield True
        while y > end_y:
            surface = self.entry_text_font.render(letter, True, color)
            self.screen.blit(surface, (x, y))
            y -= 1 
            yield True
        yield False
            
    def run(self):
        running = True
        slu = False
        lower_pipe_scrolls = []
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key == pygame.K_RETURN:
                        lower_pipe_scrolls += [self.scroll_letter_up(letter=letter, delay=delay * 18, color=self.text_colors[self.entry_text_index]) for delay, letter in enumerate(self.entry_text)]
                        self.entry_text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        self.entry_text = self.entry_text[:-1]
                    elif event.key == pygame.K_UP:
                        self.entry_text_index += 1
                        if self.entry_text_index > 11:
                            self.entry_text_index = 0
                        self.draw_hud()
                    elif event.key == pygame.K_DOWN:
                        self.entry_text_index -= 1
                        if self.entry_text_index < 0:
                            self.entry_text_index = 11
                        self.draw_hud()
                    elif event.key == pygame.K_LEFT and self.to > 1:
                        self.to-=1
                    elif event.key == pygame.K_RIGHT and self.to < 20:
                        self.to+=1
                    else: 
                        self.entry_text += event.unicode
                        
            if lower_pipe_scrolls:
                for index, generator in enumerate(lower_pipe_scrolls):
                    iterations_remain = generator.send(None)
                    if not iterations_remain:
                        lower_pipe_scrolls.pop(index)

                        
            self.draw_router(surface=self.screen)
            self.draw_entry_box(surface=self.screen)
            self.draw_upper_pipe(surface=self.screen)
            self.draw_chat_box(surface=self.screen)
            self.draw_to_text()
            
            self.draw_entry_text('|> {}'.format(self.entry_text), (1,42))
            pygame.display.flip()
            self.screen.blit(self.background, (0, 0))
            self.clock.tick(300)
        pygame.quit()            


if __name__ == '__main__':
    LaserChat().run()
import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
import threading
import time
#from pygame.locals import *

class Game:

    
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, WINDOW_HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)#HOLD DOWN KEY TO MOVE
        self.load_data()
        self.right_hand_thread = threading.Thread(target=self.rhrule_thread, args=())
        self.rand_thread = threading.Thread(target=self.rand_thread,args=())
        self.left_hand_thread = threading.Thread(target=self.lhrule_thread, args=())
        self.rec_thread = threading.Thread(target=self.rec_thread, args=())
        self.rh_steps = 0
        self.player_steps = 0
        self.rando_steps = 0
        self.lhrule_steps = 0
        self.font = pg.font.Font('freesansbold.ttf', 20)
        #self.font = pg.font.SysFont("monospace", 32)
        
        
    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
        with open(path.join(game_folder, 'new_map.txt'), 'rt') as f:
            for line in f:
                self.map_data.append(line)
        pass

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        #self.teles = pg.sprite.Group()
        self.teles =[]
        self.maze = []
        #spawn location
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                elif tile == 'p':
                    filler(self, col, row)
                elif tile == '@':
                    start(self, col, row)
                    x = col
                    y = row
                elif tile == 'e':
                    end(self, col, row)
                    self.endx = col
                    self.endy = row
        self.player = Player(self, x, y)
        self.rhrule = RightHandRule(self, x, y)
        self.rando = RandomMover(self, x, y)
        self.lhrule = LeftHandRule(self, x ,y)
        self.rec = Recursive(self, x, y)

            
    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        self.right_hand_thread.start()
        self.rand_thread.start()
        self.left_hand_thread.start()
        self.rec_thread.start()
        
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
                

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        pg.display.flip()

        
        self.player_text = self.font.render("Player Steps: {0}".format(self.player_steps), 1, YELLOW)
        self.rh_text = self.font.render("RH Rule Steps: {0}".format(self.rh_steps), 1, BLUE)
        self.rando_text = self.font.render("Random Rule Steps: {0}".format(self.rando_steps), 1, LIGHTBLUE)
        self.lh_text = self.font.render("LH Rule Steps: {0}".format(self.lhrule_steps), 1, PINK)
        self.screen.blit(self.player_text, (50, 805))
        self.screen.blit(self.rh_text, (50, 830))
        self.screen.blit(self.rando_text, (240, 805))
        self.screen.blit(self.lh_text, (240, 830))
        
        pg.display.update()

    def rhrule_thread(self):
        while self.rhrule.x != self.endx or self.rhrule.y != self.endy:
            self.rh_steps = self.rh_steps + 1
            time.sleep(.1)
            self.rhrule.determine_move()

    def rand_thread(self):
        while self.rando.x != self.endx or self.rando.y != self.endy:
            self.rando_steps = self.rando_steps + 1
            time.sleep(.1)
            self.rando.determine_move()

    def lhrule_thread(self):
        while self.lhrule.x != self.endx or self.lhrule.y != self.endy:
            self.lhrule_steps = self.lhrule_steps + 1
            time.sleep(.1)
            self.lhrule.determine_move()

    def rec_thread(self):
        self.rec.start()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:#CONTROL S MOVEMENT
                #   ADJUST PLAYER STEP TO ONLY CHANGE ON MOVE AND NOT ON EVENT
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if not (self.player.x == self.endx and self.player.y == self.endy):
                    if event.key == pg.K_LEFT:
                        self.player.move(dx=-1)
                        self.player_steps = self.player_steps + 1
                    if event.key == pg.K_RIGHT:
                        self.player.move(dx=1)
                        self.player_steps = self.player_steps + 1
                    if event.key == pg.K_UP:
                        self.player.move(dy=-1)
                        self.player_steps = self.player_steps + 1
                    if event.key == pg.K_DOWN:
                        self.player.move(dy=1)
                        self.player_steps = self.player_steps + 1
        
    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass

    

    
# create the game object
g = Game()
g.show_start_screen()

while True:
    g.new()
    g.run()
    g.show_go_screen()

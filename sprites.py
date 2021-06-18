import pygame as pg
import random
from settings import *

class RandomMover(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(LIGHTBLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def move(self, dx = 0, dy = 0):
        self.x += dx
        self.y += dy

    def determine_move(self):
        horiz_or_vert = random.randint(1,2)

        if(horiz_or_vert == 1):
            stepx = random.randrange(-1,2,2)
            if not self.collide_with_walls(dx = stepx, dy = 0):
                self.move(dx = stepx, dy = 0)
                
        if(horiz_or_vert == 2):
            stepy = random.randrange(-1, 2, 2)
            if not self.collide_with_walls(dx = 0, dy = stepy):
                self.move(dx = 0, dy = stepy)
        
    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            print(wall.x)
            print(wall.y)
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
            return False
        
    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
        
        
    



class RightHandRule(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.currx = 1
        self.curry = 0

    def move(self, dx=0, dy=0):
        self.x += dx
        self.y += dy

    def determine_move(self):

        if self.currx == 1:
            if not self.collide(dx = 0, dy = 1):
                #moving right, checking down
                
                self.currx = 0
                self.curry = 1
                self.move(dx = 0, dy = 1)
                
            elif not self.collide(dx = 1, dy = 0):
                self.move(dx = 1, dy = 0)
                
            elif not self.collide(dx = 0, dy = -1):
                self.currx = 0
                self.curry = -1
                self.move(dx = 0, dy = -1)
                
            else:
                self.currx = -1
                self.move(dx = -1, dy = 0)
                
                
                
        elif self.currx == -1:
            if not self.collide(dx = 0, dy = -1):
                #moving left, checking up
                
                self.currx = 0
                self.curry = -1
                self.move(dy = -1)
                
            elif not self.collide(dx = -1, dy = 0):
                self.move(dx = -1)

            elif not self.collide(dx = 0, dy = 1):
                self.currx = 0
                self.curry = 1
                self.move(dx = 0, dy = 1)
            else:
                self.currx = 1
                self.move(dx = 1, dy = 0)

                
                          
        elif self.curry == 1:
            if not self.collide(dx = -1, dy = 0):
                #moving down, checking left
                
                self.currx = -1
                self.curry = 0
                self.move(dx = -1)
                
            elif not self.collide(dx = 0, dy = 1):
                self.move(dy = 1)

            elif not self.collide(dx = 1, dy = 0):
                self.currx = 1
                self.curry = 0
                self.move(dx = 1, dy = 0)

            else:
                self.curry = -1
                self.move(dx = 0, dy = -1)

        elif self.curry == -1:
            if not self.collide(dx = 1, dy = 0):
                #moving up, checking right
                
                self.currx = 1
                self.curry = 0
                self.move(dx = 1)
                
            elif not self.collide(dx = 0, dy = -1):
                self.move(dy = -1)

            elif not self.collide(dx = -1, dy = 0):
                self.currx = -1
                self.curry = 0
                self.move(dx = -1, dy = 0)

            else:
                self.curry = 1
                self.move(dx = 0, dy = 1)
        


    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

    def collide(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y

    def move(self, dx=0, dy=0):
        if not self.collide_with_walls(dx, dy):
            self.x += dx
            self.y += dy

    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class filler(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(LIGHTGREY)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        
class start(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        
class end(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        

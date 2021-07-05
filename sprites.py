import pygame as pg
import random
from settings import *
import time
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
        self.currx = 1
        self.curry = 0

    def move(self, dx = 0, dy = 0):
        self.x += dx
        self.y += dy

    def collide(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

    def determine_move(self):
        if self.currx == 0:
            if ((not self.collide(dx = -1, dy = 0)) or (not self.collide(dx = 1, dy = 0))):
                self.pick_random_move()
        if self.curry == 0:
            if ((not self.collide(dx = 0, dy = -1)) or (not self.collide(dx = 0, dy = 1))):
                 self.pick_random_move()
                                                                                                  
        if not self.collide(dx = self.currx, dy = self.curry):
            self.move(dx = self.currx, dy = self.curry)
        else:
            self.pick_random_move()

    def pick_random_move(self):
        self.next_move = random.randint(1, 4)
        if self.next_move == 1:
            self.curry = 0
            self.currx = 1
        elif self.next_move == 2:
            self.curry = 0
            self.currx = -1
        elif self.next_move == 3:
            self.currx = 0
            self.curry = 1
        elif self.next_move == 4:
            self.currx = 0
            self.curry = -1
        
    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

class Recursive(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.currx = 1
        self.curry = 0
        self.rec_jumps =[[x],[y]]

    def start(self):
        self.rec_solver(1, 0)

    def isJunction(self, funcX, funcY):
        if funcX == 0:
            if ((not self.collide(dx = -1, dy = 0)) or (not self.collide(dx = 1, dy = 0))):
                return True
            else:
                return False
        if funcY == 0:
            if ((not self.collide(dx = 0, dy = -1)) or (not self.collide(dx = 0, dy = 1))):
                 return True
            else:
                return False

    def rec_solver(self, dirX, dirY):
        time.sleep(.5)
        print("rec")
        print("Current X: " + str(self.x))
        print("Current Y: " + str(self.y))
        if self.isJunction(dirX, dirY):

            print(self.rec_jumps)
            self.rec_jumps[0].append(self.x)
            self.rec_jumps[1].append(self.y)
            print(self.rec_jumps)
            
            #SPLIT UPWARDS <- call rec
            if not self.collide(dx = 0, dy = -1):
                print("a1")
                self.move(dx = 0, dy = -1)
                self.rec_solver(0, -1)
            else:
                print("b1")
                self.x = self.rec_jumps[0].pop()
                self.y = self.rec_jumps[1].pop()
            self.update()

            #SPLIT RIGHT <- call rec
            if not self.collide(dx = 1, dy = 0):
                print("a2")
                self.move(dx = 1, dy = 0)
                self.rec_solver(1, 0)
            else:
                print("b2")
                self.x = self.rec_jumps[0].pop()
                self.y = self.rec_jumps[1].pop()
            self.update()

            #SPLIT DOWNWARDS <- call rec
            if not self.collide(dx = 0, dy = 1):
                print("a3")
                self.move(dx = 0, dy = 1)
                self.rec_solver(0, 1)
            else:
                print("b3")
                self.x = self.rec_jumps[0].pop()
                self.y = self.rec_jumps[1].pop()
            self.update()

            #SPLIT LEFT <- call rec
            if not self.collide(dx = -1, dy = 0):
                print("a4")
                self.move(dx = -1, dy = 0)
                self.rec_solver(-1, 0)
            else:
                print("b4")
                self.x = self.rec_jumps[0].pop()
                self.y = self.rec_jumps[1].pop()
            self.update()
                

            
        else:
            self.currx = dirX
            self.curry = dirY
            if not self.collide(dx = self.currx, dy = self.curry):
                self.move(dx = self.currx, dy = self.curry)
                self.rec_solver(self.currx, self.curry)


    def collide(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

    def move(self, dx = 0, dy = 0):
        self.x += dx
        self.y += dy
        self.update()

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE
    
    
        
        

class LeftHandRule(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(PINK)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.currx = 1
        self.curry = 0

    def move(self, dx = 0, dy = 0):
        self.x += dx
        self.y += dy

    def update(self):
        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

    def collide(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False

    def determine_move(self):

        #moving right, checking up
        if self.currx == 1:
            if not self.collide(dx = 0, dy = -1):
                
                self.currx = 0
                self.curry = -1
                self.move(dx = self.currx, dy = self.curry)

            elif not self.collide(dx = 1, dy = 0):
                
                self.currx = 1
                self.curry = 0
                self.move(dx = self.currx, dy = self.curry)

            elif not self.collide(dx = 0, dy = 1):
                self.currx = 0
                self.curry = 1
                self.move(dx = self.currx, dy = self.curry)

            else:
                self.currx = -1
                self.curry = 0
                self.move(dx = self.currx, dy = self.curry)

        #moving left, checking down
        if self.currx == -1:
            if not self.collide(dx = 0, dy = 1):
                
                self.currx = 0
                self.curry = 1
                self.move(dx = self.currx, dy = self.curry)

            elif not self.collide(dx = -1, dy = 0):
                
                self.currx = -1
                self.curry = 0
                self.move(dx = self.currx, dy = self.curry)

            elif not self.collide(dx = 0, dy = -1):
                self.currx = 0
                self.curry = -1
                self.move(dx = self.currx, dy = self.curry)

            else:
                self.currx = 1
                self.curry = 0
                self.move(dx = self.currx, dy = self.curry)
        
        #moving up, checking left
        if self.curry == -1:
            if not self.collide(dx = -1, dy = 0):
                
                self.currx = -1
                self.curry = 0
                self.move(dx = self.currx, dy = self.curry)

            elif not self.collide(dx = 0, dy = -1):
                
                self.currx = 0
                self.curry = -1
                self.move(dx = self.currx, dy = self.curry)

            elif not self.collide(dx = 1, dy = 0):
                self.currx = 1
                self.curry = 0
                self.move(dx = self.currx, dy = self.curry)

            else:
                self.currx = 0
                self.curry = 1
                self.move(dx = self.currx, dy = self.curry)
                
        #moving down, checking right
        if self.curry == 1:
            if not self.collide(dx = 1, dy = 0):
                
                self.currx = 1
                self.curry = 0
                self.move(dx = self.currx, dy = self.curry)

            elif not self.collide(dx = 0, dy = 1):
                
                self.currx = 0
                self.curry = 1
                self.move(dx = self.currx, dy = self.curry)

            elif not self.collide(dx = -1, dy = 0):
                self.currx = -1
                self.curry = 0
                self.move(dx = self.currx, dy = self.curry)

            else:
                self.currx = 0
                self.curry = -1
                self.move(dx = self.currx, dy = self.curry)

    



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
        


import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)

class Wall(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, color):

        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Player(pygame.sprite.Sprite):

    change_x = 0
    change_y = 0

    def __init__(self, x, y):

        super().__init__()
        self.image = pygame.Surface([15, 15])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def changeSpeed(self, x, y):

        self.change_x += x
        self.change_y += y

    def move(self, walls):

        self.rect.x += self.change_x
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)

        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right
        
        self.rect.y += self.change_y
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)

        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom

class Room(object):

    wall_list = None
    enemy_sprites = None 

    def __init__(self):

        self.wall_list = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

    def addWallList(self, walls):
        
        for item in walls:
            wall = Wall(item[0], item[1], item[2], item[3], item[4])
            self.wall_list.add(wall)

class Room1(Room):

    def __init__(self):

        super().__init__()
        walls = [
            [0,0,20,250, WHITE],
            [0,350,20,250, WHITE],
            [780,0,20,250,WHITE],
            [780,350,20,250,WHITE],
            [20,0,760,20,WHITE],
            [20,580,760,20,WHITE],
            [390,50,20,500,BLUE]
        ]

        self.addWallList(walls)

class Room2(Room):

    def __init__(self):

        super().__init__()
        walls = [
            [0,0,20,250,RED],
            [0,350,20,250,RED],
            [780,0,20,250,RED],
            [780,350,20,250,RED],
            [20,0,760,20,RED],
            [20,580,760,20,RED],
            [190,50,20,500,GREEN]
        ]

        self.addWallList(walls)

class Room3(Room):

    def __init__(self):

        super().__init__()
        walls = [
            [0,0,20,250,PURPLE],
            [0,350,20,250,PURPLE],
            [780,0,20,250,PURPLE],
            [780,350,20,250,PURPLE],
            [20,0,760,20,PURPLE],
            [20,580,760,20,PURPLE]
        ]

        self.addWallList(walls)

        for x in range(100,800,100):
            for y in range(50,451,300):
                wall = Wall(x,y,20,200,RED)
                self.wall_list.add(wall)

        for x in range(150,700,100):
            wall = Wall(x,200,20,200,WHITE)
            self.wall_list.add(wall)

def main():
    pygame.init()
    screen = pygame.display.set_mode([800, 600])
    pygame.display.set_caption('Maze Runner')
    player = Player(50,50)
    movingSprites = pygame.sprite.Group()
    movingSprites.add(player)
    rooms = []
    room = Room1()
    rooms.append(room)
    room = Room2()
    rooms.append(room)
    room = Room3()
    rooms.append(room)
    current_room_no = 0
    current_room = rooms[current_room_no]
    clock = pygame.time.Clock()
    done = False 

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.changeSpeed(-5,0)
                if event.key == pygame.K_RIGHT:
                    player.changeSpeed(5,0)
                if event.key == pygame.K_UP:
                    player.changeSpeed(0,-5)
                if event.key == pygame.K_DOWN:
                    player.changeSpeed(0,5)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    player.changeSpeed(5,0)
                if event.key == pygame.K_RIGHT:
                    player.changeSpeed(-5,0)
                if event.key == pygame.K_UP:
                    player.changeSpeed(0,5)
                if event.key == pygame.K_DOWN:
                    player.changeSpeed(0,-5)

        player.move(current_room.wall_list)

        if player.rect.x < -15:
            if current_room_no == 0:
                current_room_no = 2
            elif current_room_no == 2:
                current_room_no = 1
            else:
                current_room_no = 0
            
            current_room = rooms[current_room_no]
            player.rect.x = 790

        if player.rect.x > 801:
            if current_room_no == 0:
                current_room_no = 1
            elif current_room_no == 1:
                current_room_no = 2
            else:
                current_room_no = 0
            
            current_room = rooms[current_room_no]
            player.rect.x = 0
        
        screen.fill(BLACK)
        movingSprites.draw(screen)
        current_room.wall_list.draw(screen)
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

main()

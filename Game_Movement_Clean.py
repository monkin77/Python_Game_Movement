import pygame
import random
import math
pygame.init

win_width = 500
win_height = 480

win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Game Movement")

# Loading images
walkRight = [pygame.image.load('R1.png'), pygame.image.load('R2.png'), pygame.image.load('R3.png'), pygame.image.load('R4.png'), pygame.image.load('R5.png'), pygame.image.load('R6.png'), pygame.image.load('R7.png'), pygame.image.load('R8.png'), pygame.image.load('R9.png')]

walkLeft = [pygame.image.load('L1.png'), pygame.image.load('L2.png'), pygame.image.load('L3.png'), pygame.image.load('L4.png'), pygame.image.load('L5.png'), pygame.image.load('L6.png'), pygame.image.load('L7.png'), pygame.image.load('L8.png'), pygame.image.load('L9.png')]


bg = pygame.image.load('bg.jpg') # Background

char = pygame.image.load('standing.png') # character not moving or jumping

clock = pygame.time.Clock()

class Object(object): #Used to make simple objects
    pass

class spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as message:
            print ('Unable to load spritesheet image:')
            raise SystemExit
    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates" 
        return [self.image_at(rect, colorkey) for rect in rects]
    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)
    
goblin_animation = Object()
setattr(goblin_animation, 'walkRight', [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')])
setattr(goblin_animation, 'walkLeft', [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')])


bat_ss = spritesheet('rat and bat spritesheet calciumtrice.png')
bat_animation = Object()
bat_coordinates = []
for x in range(10):
    bat_coordinates.append((x*32, 160,32,32))
setattr(bat_animation, 'walkRight', bat_ss.images_at(bat_coordinates, colorkey=(255,255,255)))


rat_ss = spritesheet('rat and bat spritesheet calciumtrice.png')
rat_animation = Object()
rat_coordinates = []
for x in range(10):
    rat_coordinates.append((x*32, 96,32,32))
setattr(rat_animation, 'walkRight', rat_ss.images_at(rat_coordinates, colorkey=(255,255,255)))

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5
        self.left = False
        self.right = False
        self.walkCount = 0
        self.isJump = False
        self.jumpCount = 10
        self.standing = True

    def draw(self, win):
        if self.walkCount + 1 >= 27:    #27
            self.walkCount = 0
        if not(self.standing):
            if self.left:
                win.blit(walkLeft[self.walkCount// 3], (self.x,self.y))
                self.walkCount += 1 
            elif self.right:
                win.blit(walkRight[self.walkCount// 3], (self.x,self.y))  # "//" divides and removes the remainder
                self.walkCount += 1
        else:                           #if standing
            if self.right:
                win.blit(walkRight[0], (self.x, self.y))        # Leaves the player looking right
            elif self.left:
                win.blit(walkLeft[0], (self.x, self.y))
            else:
                win.blit(char, (self.x, self.y))    


class projectile(object):
    def __init__ (self, x , y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing= facing # facing is either 1 or -1 to determine if the bullet goes left or right
        self.vel = 8 * facing
    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)

class enemy(object):
    def __init__(self, images, x, y, width, height):
        self.images = images
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.walkCount = 0

    def draw(self, win):
        self.move()
        if(self.vel > 0):
            win.blit(self.images.walkRight[self.walkCount])
        elif(self.vel < 0):
            win.blit(self.images.walkLeft[self.walkCount])
        self.walkCount = (self.walkCount + 1) % len(self.images.walkRight)

    def move(self, x, y):
        return

class enemy_ground(enemy):

    def __init__(self, images, x, y, width, height, end):
        super(enemy_ground, self).__init__(images, x, y, width, height)
        self.height = height
        self.end = end
        self.path = [self.x, self.end]
        self.vel = 3
    
    def draw(self, win):
        self.move()
        if self.walkCount >= 33:        #33
            self.walkCount = 0
        if self.vel > 0:
            win.blit(self.images.walkRight[self.walkCount // 3], (self.x,self.y))
            self.walkCount += 1
        else:
            win.blit(self.images.walkLeft[self.walkCount //3], (self.x, self.y))
            self.walkCount += 1

        pass
    def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel
            else:
                self.vel = self.vel * -1
                self.walkCount = 0


        pass

class goblin(enemy_ground):
    #goblin_animation.walkRight = [pygame.image.load('R1E.png'), pygame.image.load('R2E.png'), pygame.image.load('R3E.png'), pygame.image.load('R4E.png'), pygame.image.load('R5E.png'), pygame.image.load('R6E.png'), pygame.image.load('R7E.png'), pygame.image.load('R8E.png'), pygame.image.load('R9E.png'), pygame.image.load('R10E.png'), pygame.image.load('R11E.png')]
    #goblin_animation.walkLeft = [pygame.image.load('L1E.png'), pygame.image.load('L2E.png'), pygame.image.load('L3E.png'), pygame.image.load('L4E.png'), pygame.image.load('L5E.png'), pygame.image.load('L6E.png'), pygame.image.load('L7E.png'), pygame.image.load('L8E.png'), pygame.image.load('L9E.png'), pygame.image.load('L10E.png'), pygame.image.load('L11E.png')]

    
    def __init__(self, x, y, end):
        super(goblin, self).__init__(goblin_animation, x, y, 64, 64, end)
        self.end = end

class rat(enemy_ground):

    def __init(self, x, y, end):
        super(rat, self).__init__(rat_animation, x, y, 64, 64, end)
        self.end = end

class enemy_flying(enemy):
    def __init__(self, images, to_attack, x , witdh, height):
        super(enemy_flying, self).__init__(images, x, 10, width, height)
        self.speed = 5
        self.x = random.randint(0, win_width)
        self.goal_x = random.randint(0, win_width)
        self.attacking = 1
        self.to_attack = to_attack
        self.walkCount = 0

    def draw(self, win):
        self.move(self.to_attack.x, self.to_attack.y +10)
##        print(self.x, self.y)
##        print(self.attacking)
        win.blit(self.images.walkRight[self.walkCount % 10], (self.x, self.y))
        self.walkCount = (self.walkCount + 1) % 10

    def move(self, x, y): #x and y of the player
        if self.attacking:
            if self.y > (y - 10):
                self.attacking = False
                self.goal_x = random.randint(0, win_width)
            else:
                vel = self.get_vel(self.x, self.y, x, y)
                self.x = self.x + vel[0]
                self.y = self.y + vel[1]      
        else:
            if self.y < 10:
                self.attacking = True
            else:
                vel = self.get_vel(self.x, self.y, self.goal_x, 10)
                self.x = self.x + 2 * vel[0]
                self.y = self.y + 2 * vel[1]
                

    def get_vel(self, x1, y1, x2, y2):
        angle = math.atan2(y2-y1, x2-x1)
        x_vel = math.cos(angle) * self.speed
        y_vel = math.sin(angle) * self.speed
        return [x_vel, y_vel]

class bat(enemy_flying):

    def __init__(self, to_attack):
        super(bat, self).__init__(bat_animation, to_attack, x, 32, 32)

def redrawGameWindow():
    global walkCount        #defines the variable in the whole code
    win.blit(bg, (0,0))
    man.draw(win)          # Player
    goblin1.draw(win)
    bat1.draw(win)
    for bullet in bullets:
        bullet.draw(win) 

    pygame.display.update()

#Main Loop
man = player(300, 410, 64, 64)  # Character Specs (x,y,width,height)
goblin1 = goblin(100, 410, 450)
#goblin = enemy(100, 410, 64, 64, 450)
bat1 = bat(man)
bullets =  []
run = True

while run:
    clock.tick(27)  #27

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for bullet in bullets:
        if bullet.x < 500 and bullet.x > 0:
            bullet.x += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))  # remove the bullet  

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        if man.left: 
            facing = -1
        else:
            facing = 1
        if len(bullets) < 50:
            bullets.append(projectile(round(man.x + man.width // 2), round(man.y + man.height // 2), 6, (0,0,0), facing))

    if keys[pygame.K_LEFT] and man.x >= man.vel:
        man.x -= man.vel
        man.left = True
        man.right = False
        man.standing = False
    elif keys[pygame.K_RIGHT] and man.x < 500 - man.width - man.vel:
        man.x += man.vel
        man.left = False
        man.right = True
        man.standing = False
    else: 
        man.standing = True 
        man.walkCount = 0

    if not(man.isJump):
                    #   if keys[pygame.K_UP] and y > 0:            
                    #       y -= vel
                    #   if keys[pygame.K_DOWN] and y < 440:
                    #       y += vel
        if keys[pygame.K_UP]:
            man.isJump = True
            man.right = False
            man.left = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -10:
            neg = 1
            if man.jumpCount < 0:
                neg = -1 
            man.y -= (man.jumpCount ** 2) * 0.5* neg
            man.jumpCount -= 1
        else:
            man.isJump = False
            man.jumpCount = 10
    redrawGameWindow()


pygame.quit()







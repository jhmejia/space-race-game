import pygame
import random
import time

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
    K_w,
    K_s,
)

pygame.init()


# Constants (You can change these to make the game easier or harder! Try it out!)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SIZE_OF_SHIP = 20
MAX_VEL = 2
ACCERLATION = 0.01
WIDTH_OF_STARS = 20
HEIGHT_OF_STARS = 2
MAX_SPEED_OF_STARS = 2
MIN_SPEED_OF_STARS = 0.5
DISABILITY_PENALTY_TIME = 200 # Frames you are disabled after hitting a star
DISABILITY_PENALTY_POINTS = 0 # Points you lose when you hit a star
NUM_STARS = 20
GAME_TIME = 60 # Game time in seconds



# Variables

velocity_ship1 = 0
velocity_ship2 = 0

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


# Make 2 ships

ship1 = pygame.image.load("spaceship.png")
ship1 = pygame.transform.scale(ship1, (SIZE_OF_SHIP, SIZE_OF_SHIP))
ship1_x = SCREEN_WIDTH * 0.2 - SIZE_OF_SHIP/2
ship1_y = SCREEN_HEIGHT * 0.8

ship2 = pygame.image.load("spaceship.png")
ship2 = pygame.transform.scale(ship2, (SIZE_OF_SHIP, SIZE_OF_SHIP))
ship2_x = SCREEN_WIDTH * 0.8 - SIZE_OF_SHIP/2
ship2_y = SCREEN_HEIGHT * 0.8

# Make 2 scores

isDisabledShip1 = False
isDisabledShip2 = False

disabilityTime1 = 0
disabilityTime2 = 0


score1 = 0
score2 = 0

myFont = pygame.font.SysFont("monospace", 15)



# Make stars

class Star:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def move(self):
        self.x += self.speed

        # If the star goes off the screen, move it to the other side
        if self.x > SCREEN_WIDTH:
            self.x = 0
        if self.x < 0:
            self.x = SCREEN_WIDTH

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, WIDTH_OF_STARS, HEIGHT_OF_STARS))
        pygame.draw.ellipse(screen, (255, 255, 255), (self.x, self.y, WIDTH_OF_STARS, HEIGHT_OF_STARS))

# Add 10 stars to the screen at random positions

stars = []
for i in range(NUM_STARS):
    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(SCREEN_HEIGHT*.02, int(SCREEN_HEIGHT*0.75))

    speed = random.choice((-1, 1)) * round(random.uniform(MIN_SPEED_OF_STARS, MAX_SPEED_OF_STARS), 2)

    stars.append(Star(x, y, speed))





def flip_ship(ship, direction):
    ship1 = pygame.image.load("spaceship.png")
    ship1 = pygame.transform.scale(ship1, (SIZE_OF_SHIP, SIZE_OF_SHIP))

    if direction == "up":
        ship = pygame.transform.flip(ship1, False, True)
    if direction == "down":
        ship = pygame.transform.flip(ship1, False, False)
    return ship


    
def add_score(ship):
    print ("Ship " + str(ship) + " scored a point!")
    if ship == 1:
        global score1
        score1 += 1
    if ship == 2:
        global score2
        score2 += 1

def add_velocity(direction, velocity):
    if direction == "down" and velocity < MAX_VEL:
        velocity += ACCERLATION
    if direction == "down" and velocity < MAX_VEL and velocity < 0:
        velocity += ACCERLATION * 3
    if direction == "up" and velocity > -MAX_VEL:
        velocity -= ACCERLATION
    if direction == "up" and velocity > -MAX_VEL and velocity > 0:
        velocity -= ACCERLATION * 3
    return velocity


def check_point(ship1_y, ship2_y):
    if ship1_y <= 0:
        ship1_y = SCREEN_HEIGHT - SIZE_OF_SHIP
        add_score(1)
    if ship1_y >= SCREEN_HEIGHT - SIZE_OF_SHIP:
        ship1_y = SCREEN_HEIGHT - SIZE_OF_SHIP
    if ship2_y <= 0:
        ship2_y = SCREEN_HEIGHT - SIZE_OF_SHIP
        add_score(2)
    if ship2_y >= SCREEN_HEIGHT - SIZE_OF_SHIP:
        ship2_y = SCREEN_HEIGHT - SIZE_OF_SHIP
    return ship1_y, ship2_y





    



def update(keys, ship1_y, ship2_y, velocity_ship1, velocity_ship2, isShip1Disabled, isShip2Disabled):
    if (not isDisabledShip1):
        if keys[K_w]:
            velocity_ship1 = add_velocity("up", velocity_ship1)
            ship1_y += velocity_ship1
        
        if keys[K_s]:
            velocity_ship1 = add_velocity("down", velocity_ship1)
            ship1_y += velocity_ship1

        if not keys[K_w] and not keys[K_s]:
            if velocity_ship1 > .1:
                velocity_ship1 -= ACCERLATION * 2
                ship1_y += velocity_ship1
            if velocity_ship1 < -.1:
                velocity_ship1 += ACCERLATION * 2
                ship1_y += velocity_ship1
            if velocity_ship1 < .1 and velocity_ship1 > -.1:
                velocity_ship1 = 0
        
    if (not isDisabledShip2):

        if keys[K_UP]:
            velocity_ship2 = add_velocity("up",   velocity_ship2)
            ship2_y += velocity_ship2
            
        if keys[K_DOWN]:
            velocity_ship2 = add_velocity("down", velocity_ship2)
            ship2_y += velocity_ship2

        if not keys[K_UP] and not keys[K_DOWN]:
            if velocity_ship2 > .1:
                velocity_ship2 -= ACCERLATION * 2
                ship2_y += velocity_ship2
            if velocity_ship2 < -.1:
                velocity_ship2 += ACCERLATION * 2
                ship2_y += velocity_ship2
            if velocity_ship2 < .1 and velocity_ship2 > -.1:
                velocity_ship2 = 0
    
        
    
    
    
    ship1_y, ship2_y = check_point(ship1_y, ship2_y)

   

    return ship1_y, ship2_y, velocity_ship1, velocity_ship2


game_start_time = time.time()


###### Main Running Function ######



def get_game_state():
    game_state = [ship1_y, ship2_y, velocity_ship1, velocity_ship2, isDisabledShip1, isDisabledShip2, disabilityTime1, disabilityTime2, score1, score2, stars]
    time_left  = time.time() - game_start_time
    keys_pressed = pygame.key.get_pressed()
    game_state.append(keys_pressed)
    game_state.append(time_left)
    return game_state


running = True


while running:

    if time.time() - game_start_time > GAME_TIME:
        running = False
        print("Game Over!")
        print("Player 1 Score: " + str(score1))
        print("Player 2 Score: " + str(score2))
        if score1 > score2:
            print("Player 1 Wins!")
        if score2 > score1:
            print("Player 2 Wins!")
        if score1 == score2:
            print("Tie Game!")
    

    screen.fill((0, 0, 0))

    pressed_keys = pygame.key.get_pressed()

    if isDisabledShip1:
        disabilityTime1 += 1
        pygame.draw.rect(screen, (255, 0, 0), (ship1_x, ship1_y + SIZE_OF_SHIP, SIZE_OF_SHIP, HEIGHT_OF_STARS))
        if disabilityTime1 > DISABILITY_PENALTY_TIME:
            isDisabledShip1 = False
            disabilityTime1 = 0
    if isDisabledShip2:
        disabilityTime2 += 1
        pygame.draw.rect(screen, (255, 0, 0), (ship2_x, ship2_y + SIZE_OF_SHIP, SIZE_OF_SHIP, HEIGHT_OF_STARS))
        if disabilityTime2 > DISABILITY_PENALTY_TIME:
            isDisabledShip2 = False
            disabilityTime2 = 0


    ship1_y, ship2_y, velocity_ship1, velocity_ship2 = update(pressed_keys, ship1_y, ship2_y, velocity_ship1, velocity_ship2, isDisabledShip1, isDisabledShip2)

    for event in pygame.event.get():

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False

    
    # Draw all the stars
    for star in stars:

        star.draw()
        star.move()

        # Check collision with ship

        if star.x < ship1_x + SIZE_OF_SHIP and star.x > ship1_x and star.y < ship1_y + SIZE_OF_SHIP and star.y > ship1_y:
            isDisabledShip1 = True
            ship1_y = SCREEN_HEIGHT * 0.9
            velocity_ship1 = 0
            score1 -= DISABILITY_PENALTY_POINTS
            print ("Ship 1 is disabled!")
            

        if star.x < ship2_x + SIZE_OF_SHIP and star.x > ship2_x and star.y < ship2_y + SIZE_OF_SHIP and star.y > ship2_y:
            isDisabledShip2 = True
            velocity_ship2 = 0
            ship2_y = SCREEN_HEIGHT * 0.9
            score2 -= DISABILITY_PENALTY_POINTS
            print ("Ship 2 is disabled!")
        



    if velocity_ship1 >= .5:
        ship1 = flip_ship(ship1, "up")
    if velocity_ship2 >= .5:
        ship2 = flip_ship(ship2, "up")
    if velocity_ship1 <= 0:
        ship1 = flip_ship(ship1, "down")
    if velocity_ship2 <= 0:
        ship2 = flip_ship(ship2, "down")




    screen.blit(ship1, (ship1_x, ship1_y))
    screen.blit(ship2, (ship2_x, ship2_y))

    score1display = myFont.render("Score 1: " + str(score1), 1, (255,255,0))
    score2display = myFont.render("Score 2: " + str(score2), 1, (255,255,0))
    timer_display = myFont.render("Time: " + str(int(GAME_TIME - (time.time() - game_start_time))), 1, (255,255,0))
    
    screen.blit(score1display, (SCREEN_WIDTH * 0.2 - score1display.get_width()/2, 0))
    screen.blit(score2display, (SCREEN_WIDTH * 0.8 - score2display.get_width()/2, 0))
    screen.blit(timer_display, (SCREEN_WIDTH * 0.5 - timer_display.get_width()/2, 0))

    pygame.display.update()
    pygame.display.flip()

pygame.quit()






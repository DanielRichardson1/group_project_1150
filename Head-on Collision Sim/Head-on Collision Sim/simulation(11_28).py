import pygame
import time

global_deacceleration = -15  # global deacceleration value of a car in fps given dry, stable conditions
DSRC_length = 984.252  # in feet avg DSRC reliable communication length
HUMAN_length = 300  # in feet avg distance human can anticipate a crash


# Note: every unit is in terms of feet/seconds,
# the x & y positions represent the front of each car
# This simulation is to prove:
# V2V communication extends and enhances currently available crash avoidance systems

# We are testing V2V's preventative ability in head-on vehicle collision

class Car:  # car object that has position, velcity, and acceleration
    def __init__(self, x, acceleration, velocity, direction, brakeDistance):
        self.x = x  # Position on road (We are sticking to 1-D for now b/c head-on collisions are essentially 1-D)
        self.acceleration = acceleration  # This will mainly be intialized at zero and then changed to -15 for de-acceleration power of brakes, b/c the average driver is not constantly accelerating
        self.velocity = velocity  # Current velocity of the car (unsigned)
        self.direction = direction  # direction of car (1 = left to right, -1 = right to left)
        self.brakeDistance = brakeDistance  # Distance the car will start braking from

    def brake(self):
        self.acceleration = -15

    def update(self, time):  # included time so we can choose accuracy vs processing power balance
        if self.velocity > 0:
            self.velocity += self.acceleration * time
        else:
            self.velocity = 0
        self.x += self.velocity * self.direction * time

    def getX(self):
        return self.x

    def getV(self):
        return self.velocity

    def getBrakeDistance(self):
        return self.brakeDistance


# THESE ARE OUR MAIN 2 OBJECTS WHICH WE WILL TEST WITH DIFFERENT VALUES FOR VELOCITY AND BRAKE DISTANCE
# multiply a num by 1.467 to convert from mph to fps
carLeft = Car(x=60, acceleration=0, velocity=90*1.467, direction=1, brakeDistance=DSRC_length)
carRight = Car(x=1140, acceleration=0, velocity=85*1.467, direction=-1, brakeDistance=DSRC_length)

t = 0  # time counter in seconds

# initialize pygame
pygame.init()

# Screen Definintion
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 200
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption("Car Simulation")

#car1 = pygame.Rect((0,160,60,40))
#car2 = pygame.Rect((1200,160,60,40))
xLeft = 0
xRight = 1140

# Images
bg = pygame.image.load("bg.png")
bg = bg.convert()
bc = pygame.image.load("bluecarimagelowres.png")
rc = pygame.image.load("redcarimagelowres.png")
explosion = pygame.image.load("explosion30x30.png")

# Stop Watch
clock = pygame.time.Clock()
font1 = pygame.freetype.SysFont(None, 34)
font1.origin = True
font2 = pygame.freetype.SysFont(None, 20)
font2.origin = True

# Loop for Game
run = True
while run:
    #clock.tick(60) # limits game to 60 fps
    # Refresh the screen
    screen.blit(bg,(0,0))

    # ACTUAL SIMULATION START -------------------------------------------------------
    # check if it's time to brake
    if carRight.getX() - carLeft.getX() <= carLeft.getBrakeDistance():
        carLeft.brake()
    if carRight.getX() - carLeft.getX() <= carRight.getBrakeDistance():
        carRight.brake()

    # update each car position/velocity 1 ms at a time
    carLeft.update(.001)
    carRight.update(.001)
    # increment time counter by 1 ms
    t += .001
    pygame.time.delay(1)

    # Display Timer
    ticks = t*1000
    millis = int(ticks) % 1000
    seconds = int(ticks / 1000 % 60)
    out = '{seconds:02d}:{millis}'.format(millis=millis, seconds=seconds)
    font1.render_to(screen, (0, 30), out, pygame.Color('dodgerblue'))
    print("time: ", t)
    print()

    # Display cars
    # (coords in pygame apply to top-left, but we want front of car)
    screen.blit(rc, (xLeft, 160))
    screen.blit(bc,(xRight, 160))
    if not (xLeft >= xRight - 60): # If Statement so that collision looks right on display
        xLeft = carLeft.getX() - 60
        xRight = carRight.getX()

    # check for crash
    if (carLeft.getX() >= carRight.getX()):
        screen.blit(explosion,(xRight-15,160))
        print("CRASH")
        crashmsg = 'Cars Crashed! Velocity of the red car: {v1} mph & Velocity of the blue car: {v2} mph'.format(v1=round(carLeft.getV()*0.681818,2), v2=round(carRight.getV()*0.681818,2))
        font2.render_to(screen, (100, 100), crashmsg, pygame.Color('red'))
        pygame.display.update()
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

    # check for safely stopped
    if (carLeft.getV() == 0 and carRight.getV() == 0):
        print("SAFELY STOPPED")
        safemsg = 'Cars Stopped Safely with a distance of {d} feet!'.format(d = round(carRight.getX()-carLeft.getX(),2))
        font2.render_to(screen, (100, 100), safemsg, pygame.Color('green'))
        pygame.display.update()
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

    # ACTUAL SIMULATION END -------------------------------------------------------
    # Check for Game Exit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Update the screen
    pygame.display.update()
#Exit Game
pygame.quit()

# Notes:
# 1 pixel = 1 ft
# Cars are shown at about 4x their normal size for visual purposes, but this does not effect simulation results
# 175 fps is max velocity we need to test (as DSRC will fail against a still object)
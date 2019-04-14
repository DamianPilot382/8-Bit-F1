#-------------------------------------------------------------------------------
# Name:        8-Bit Formula 1 (Originally Grip)
# Author:      Stuart Laxton (Formulafied by Damian Ugalde)
# Created:     2012-04-13, 2019-04-13
#-------------------------------------------------------------------------------
from __future__ import division
import pygame, sys, time, random, math
from pygame.locals import *

# set up pygame
pygame.init()
mainClock = pygame.time.Clock()

# set up the window
WINDOWWIDTH = 1000
WINDOWHEIGHT = 600
windowSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT),0,32)
pygame.display.set_caption('8-bit Formula 1')

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255,255,255)
GREEN = (0, 160, 0)
LGREEN = (86, 119, 61)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
LBLUE = (0, 200, 255)
BROWN = (139,69,19)
DGREY = (25,25,25)

# set up variables
moveLeft = False
moveRight = False
moveUp = False
moveDown = False
MOVESPEED = 25
carSettings = [16,0,12,20,2,60,2,120]# 0-Max Speed, 1-Current Count, 2-Acceleration rate, 3-Braking Rate, 4-Free Wheel, 5-Gear Change,6-Turn Speed,7-Max Boost
movespeed = [0,0,2,0]#0-Current movespeed, 1-Max movespeed, 2-Rotation speed, 3-Turn Speed Multiply
position = [650,250,0,0,0,0]# 0-1 Track position, 2-3 Background position, 4-5 Previous position
rotRect = (100,50)
degree = 0# Player rotation angle
radians = 0
moveRadians = 0
timer = [0,0,10000,0,0,0,0,False]# 0-Current Lap ,1-Last Lap ,2-Best lap ,3-Section 1 ,4-Section 2 ,5-Section 3,6-Time Dif, 7-Timer running
drawTrack = [1,'laps1.txt','laps2.txt','laps3.txt','laps4.txt','laps5.txt','laps6.txt','laps7.txt','laps8.txt','laps9.txt']#0-Track selector, 1-4 LapRecord file names
cheatCheck = [0,False,False,False,0,30,'         ',WHITE]# 0-Cheat Check ,1-Finish Line Check ,2-Section 1 Check ,3-Section 2 Check, 4-Grass Counter, 5-Grass Limit, 6-Time Dif Output, 7-Lap Text Colour
fps = [0,60,10,60,0]# 0-On/Off, 1-Set Point, 2-Actual FPS, 3-Lowest Recorded, 4-Highest Recorded
playerSettings = [WINDOWWIDTH/2-50,WINDOWHEIGHT/2,0,0]# 0-Player Horizontal, 1-Player Vertical, 2-Rotation position (x5 for degrees)
lap = [0,0,0,0,0]#0-Lap Time, 1-Sector 1, 2-Sector 2, 3-Sector 3, 4-Valid/Invalid
lapCount = 0
curser = [40, 190, 50, 50]# Start position for the curser on the menu
option = [0]
carImage = pygame.image.load('graphics/bike1.png').convert_alpha()
limit = [1,-1950+WINDOWWIDTH,-1450+WINDOWHEIGHT,1750,1350,0,-5]
skiding = [False,0] # Skiding, Counter
skids = []
skidPosition = []
oldFrontPosition = [0,0]
oldRearPosition = [0,0]
dirty = []
dirtPosition = 0
frontWheel = [0,0]
rearWheel = [0,0]
validLap = True

trackImage11 = pygame.image.load('graphics/b-1-1.png').convert_alpha()
trackImage21 = pygame.image.load('graphics/b-2-1.png').convert_alpha()
trackImage31 = pygame.image.load('graphics/b-3-1.png').convert_alpha()
trackImage41 = pygame.image.load('graphics/b-4-1.png').convert_alpha()
trackImage5 = pygame.image.load('graphics/st-v-3.png').convert_alpha()
trackImage51 = pygame.image.load('graphics/st-v-3-k1.png').convert_alpha()
trackImage52 = pygame.image.load('graphics/st-v-3-k2.png').convert_alpha()
trackImage53 = pygame.image.load('graphics/st-v-3-k3.png').convert_alpha()
trackImage54 = pygame.image.load('graphics/st-v-3-k4.png').convert_alpha()
trackImage6 = pygame.image.load('graphics/st-h-3.png').convert_alpha()
trackImage61 = pygame.image.load('graphics/st-h-3-k1.png').convert_alpha()
trackImage62 = pygame.image.load('graphics/st-h-3-k2.png').convert_alpha()
trackImage63 = pygame.image.load('graphics/st-h-3-k3.png').convert_alpha()
trackImage64 = pygame.image.load('graphics/st-h-3-k4.png').convert_alpha()
trackImage12 = pygame.image.load('graphics/b-1-2.png').convert_alpha()
trackImage22 = pygame.image.load('graphics/b-2-2.png').convert_alpha()
trackImage32 = pygame.image.load('graphics/b-3-2.png').convert_alpha()
trackImage42 = pygame.image.load('graphics/b-4-2.png').convert_alpha()
trackImage13 = pygame.image.load('graphics/b-1-3.png').convert_alpha()
trackImage23 = pygame.image.load('graphics/b-2-3.png').convert_alpha()
trackImage33 = pygame.image.load('graphics/b-3-3.png').convert_alpha()
trackImage43 = pygame.image.load('graphics/b-4-3.png').convert_alpha()
trackImage14 = pygame.image.load('graphics/b-1-4.png').convert_alpha()
trackImage24 = pygame.image.load('graphics/b-2-4.png').convert_alpha()
trackImage34 = pygame.image.load('graphics/b-3-4.png').convert_alpha()
trackImage44 = pygame.image.load('graphics/b-4-4.png').convert_alpha()

# set up the fonts
smallFont = pygame.font.SysFont(None, 20)
guessFont = pygame.font.SysFont(None, 36)

def setDisplay(w,h):
    playerSettings[0] = WINDOWWIDTH/2-50
    playerSettings[1] = WINDOWHEIGHT/2
    windowSurface = pygame.display.set_mode((w, h),0,32)
    pygame.display.set_caption('8-Bit Formula 1')

def framerate():
    mainClock.tick(fps[1])
    fps[2]=int(mainClock.get_fps())
    if fps[0]==1:
        if fps[2]<fps[3]:
            fps[3]=fps[2]
        if fps[2]>fps[4]:
            fps[4]=fps[2]

# Opening menu
def menu():
    # run the menu loop
    moveUp = False
    moveDown = False
    moveLeft = False
    moveRight = False
    global position
    global timer
    global lapCount
    global cheatCheck
    global lap
    global limit
    global carImage
    global playerImage
    global skids
    global dirty
    global validLap

    position = [(WINDOWWIDTH/2)+50,(WINDOWHEIGHT/2)-50,0,0,0,0]
    playerImager = pygame.image.load('graphics/bike1-1.png').convert_alpha()
    carImage = pygame.image.load('graphics/bike1.png').convert_alpha()
    playerImage = [5,playerImager,playerImager,playerImager,playerImager,playerImager,playerImager,playerImager,playerImager,playerImager]
    skids = []
    dirty = []
    fps[3] = 60
    playerSettings[2]=0
    timer = [0,0,10000,0,0,0,0,False]
    cheatCheck = [0,False,False,False,0,25,'         ',RED]
    lap = [0,0,0,0,0,0]
    lapCount = 0
    option[0]=2
    validLap = True

    framerate()
    # draw the window onto the screen
    pygame.display.update()

def scrollLimits(drawTrack):
    global WINDOWWIDTH
    global WINDOWHEIGHT
    position = [(WINDOWWIDTH/2)+50,(WINDOWHEIGHT/2)-50,0,0,0,0]
    if drawTrack[0] == 1:
        limit = [1,-1950+WINDOWWIDTH,-1450+WINDOWHEIGHT,1750,1350,0,-5]
    elif drawTrack[0] == 2:
        limit = [1,-1300+WINDOWWIDTH,-1450+WINDOWHEIGHT,1850,1350,0,-5]
    elif drawTrack[0] == 3:
        limit = [1,-1750+WINDOWWIDTH,-1950+WINDOWHEIGHT,1350,150,0,-5]
    elif drawTrack[0] == 4:
        limit = [1,-3350+WINDOWWIDTH,-2350+WINDOWHEIGHT,750,150,0,-5]
    elif drawTrack[0] == 5:
        limit = [1,-1950+WINDOWWIDTH,-2350+WINDOWHEIGHT,1350,150,0,-5]
    elif drawTrack[0] == 6:
        limit = [1,-1500+WINDOWWIDTH,-2850+WINDOWHEIGHT,1850,150,0,-5]
    elif drawTrack[0] == 7:
        limit = [1,-2250+WINDOWWIDTH,-1550+WINDOWHEIGHT,1550,1450,0,-5]
    elif drawTrack[0] == 8:
        limit = [1,-4150+WINDOWWIDTH,-2150+WINDOWHEIGHT,1250,900,0,-5]
    else:
        limit = [1,-1800+WINDOWWIDTH,-3150+WINDOWHEIGHT,1250,600,0,-5]
    return position, limit

def moveTrack():
    windowSurface.blit(trackImage62,(position[0]-1000,position[1]-115))
    windowSurface.blit(trackImage6,(position[0]-700,position[1]-100))
    windowSurface.blit(trackImage6,(position[0]-400,position[1]-100))
    windowSurface.blit(trackImage6,(position[0]-100,position[1]-100))
    windowSurface.blit(trackImage6,(position[0],position[1]-100))
    windowSurface.blit(trackImage64,(position[0]+300,position[1]-100))
    windowSurface.blit(trackImage41,(position[0]+600,position[1]-100))
    windowSurface.blit(trackImage31,(position[0]+600,position[1]+300))
    windowSurface.blit(trackImage63,(position[0]+300,position[1]+385))
    windowSurface.blit(trackImage6,(position[0],position[1]+400))
    windowSurface.blit(trackImage6,(position[0]-300,position[1]+400))
    windowSurface.blit(trackImage61,(position[0]-600,position[1]+400))
    windowSurface.blit(trackImage12,(position[0]-1100,position[1]+400))
    windowSurface.blit(trackImage22,(position[0]-1100,position[1]+900))
    windowSurface.blit(trackImage62,(position[0]-600,position[1]+1085))
    windowSurface.blit(trackImage6,(position[0]-300,position[1]+1100))
    windowSurface.blit(trackImage6,(position[0],position[1]+1100))
    windowSurface.blit(trackImage6,(position[0]+300,position[1]+1100))
    windowSurface.blit(trackImage6,(position[0]+600,position[1]+1100))
    windowSurface.blit(trackImage63,(position[0]+900,position[1]+1085))
    windowSurface.blit(trackImage34,(position[0]+1200,position[1]+700))
    windowSurface.blit(trackImage53,(position[0]+1585,position[1]+400))
    windowSurface.blit(trackImage54,(position[0]+1585,position[1]+100))
    windowSurface.blit(trackImage41,(position[0]+1500,position[1]-300))
    windowSurface.blit(trackImage21,(position[0]+1100,position[1]-400))
    windowSurface.blit(trackImage44,(position[0]+700,position[1]-1100))
    windowSurface.blit(trackImage11,(position[0]+300,position[1]-1100))
    windowSurface.blit(trackImage31,(position[0]+200,position[1]-700))
    windowSurface.blit(trackImage63,(position[0]-100,position[1]-615))
    windowSurface.blit(trackImage62,(position[0]-100,position[1]-615))
    windowSurface.blit(trackImage22,(position[0]-600,position[1]-800))
    windowSurface.blit(trackImage41,(position[0]-700,position[1]-1200))
    windowSurface.blit(trackImage64,(position[0]-1000,position[1]-1200))
    windowSurface.blit(trackImage61,(position[0]-1000,position[1]-1200))
    windowSurface.blit(trackImage14,(position[0]-1700,position[1]-1200))
    windowSurface.blit(trackImage24,(position[0]-1700,position[1]-500))
    # Timing Lines
    finishLine = pygame.draw.rect(windowSurface, WHITE,(position[0]+50,position[1]-100, 1,300))
    section1 = pygame.draw.rect(windowSurface, WHITE,(position[0],position[1]+1100, 1,300))
    section2 = pygame.draw.rect(windowSurface, WHITE,(position[0]-700,position[1]-1200, 1,300))
    return finishLine, section1, section2

def rotation(image,imageNo,where,degree):
    # Calculate rotated graphics & centre position
    surf =  pygame.Surface((100,50))
    rotatedImage = pygame.transform.rotate(image[imageNo],degree)
    blittedRect = windowSurface.blit(surf, where)
    oldCenter = blittedRect.center
    rotatedSurf =  pygame.transform.rotate(surf, degree)
    rotRect = rotatedSurf.get_rect()
    rotRect.center = oldCenter
    return rotatedImage, rotRect, oldCenter

def skidmarks(skid,colour):
    global position
    originalH = (position[0]-skid[2])+WINDOWWIDTH/2
    originalV = (position[1]-skid[3])+(WINDOWHEIGHT/2)+18
    newH = (position[0]-skid[0])+WINDOWWIDTH/2
    newV = (position[1]-skid[1])+(WINDOWHEIGHT/2)+18
    if originalH >= -50 and originalH <= WINDOWWIDTH+50 and originalV >= -50 and originalV<= WINDOWHEIGHT+50:
        pygame.draw.line(windowSurface, colour,(originalH,originalV),(newH,newV),4)

def recordSkid(skidCount,resolution,location,wheels):
    if skidCount < 1:
        oldRearPosition[0] = rearWheel[0]
        oldRearPosition[1] = rearWheel[1]
        if wheels == 2:
            oldFrontPosition[0] = frontWheel[0]
            oldFrontPosition[1] = frontWheel[1]
        skidCount = resolution
        return skidCount
    elif skidCount > 1:
        skidCount -= 1
        return skidCount
    else:
        skidRear = [rearWheel[0],rearWheel[1],oldRearPosition[0],oldRearPosition[1]]
        location.append(skidRear)
        oldRearPosition[0] = rearWheel[0]
        oldRearPosition[1] = rearWheel[1]
        if wheels == 2:
            skidFront = [frontWheel[0],frontWheel[1],oldFrontPosition[0],oldFrontPosition[1]]
            location.append(skidFront)
            oldFrontPosition[0] = frontWheel[0]
            oldFrontPosition[1] = frontWheel[1]
        skidCount = resolution
        return skidCount

# run the game loop
setDisplay(WINDOWWIDTH,WINDOWHEIGHT)
shadowImager = pygame.image.load('graphics/shadow1.png').convert_alpha()
shadowImage = [5,shadowImager,shadowImager,shadowImager,shadowImager,shadowImager,shadowImager,shadowImager,shadowImager,shadowImager]
menu()

while option[0]==2:
    # check for the QUIT event
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            # change the keyboard variables
            if event.key == K_LEFT or event.key == ord('a'):
                moveRight = False
                moveLeft = True
            if event.key == K_RIGHT or event.key == ord('d'):
                moveLeft = False
                moveRight = True
            if event.key == ord('w'):
                moveDown = False
                moveUp = True
            if event.key == ord('s'):
                moveDown = True

        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                moveUp = False
                movespeed = [0,0,2,0]
                option[0]=0
                position,limit = scrollLimits(drawTrack)
                menu()
            if event.key == K_LEFT or event.key == ord('a'):
                moveLeft = False
            if event.key == K_RIGHT or event.key == ord('d'):
                moveRight = False
            if event.key == ord('w'):
                moveUp = False
            if event.key == ord('s'):
                moveDown = False

    # Get rotated graphics
    where = playerSettings[0], playerSettings[1]
    playerRotatedImage, rotRect, oldCenter = rotation(playerImage,playerImage[0], where,degree)
    whereShadow = playerSettings[0]-10, playerSettings[1]-5
    shadowRotatedImage, srotRect, soldCenter = rotation(shadowImage,playerImage[0], whereShadow,degree)

    # Fill the background green
    windowSurface.fill(LGREEN)

    # draw the track onto the surface
    finishLine, section1, section2 = moveTrack()

    # Check the background colour
    colour = windowSurface.get_at((oldCenter))# centre colour
    if colour[0] >= 88 and colour[0] <= 91 or colour[0] == 165 or colour[0] == 255:
        dirtPosition = 0
    else:
        movespeed[2] = 3
        if playerImage[0]<3:
            playerImage[0] +=1
        if playerImage[0]>7:
            playerImage[0] -= 1
        if movespeed[0] >4:
            carSettings[1] -= carSettings[3]*2
            cheatCheck[4]+=1
        if movespeed[0] >1:
            dirtPosition = recordSkid(dirtPosition,6,dirty,2)
            validLap = False

    for skid in skids:
    # draw lines for braking skids
        skidmarks(skid,DGREY)

    for dirt in dirty:
    # draw line on grass for dirt tracks
        skidmarks(dirt,BROWN)

    # draw the player onto the surface
    windowSurface.blit(shadowRotatedImage,srotRect)
    windowSurface.blit(playerRotatedImage,rotRect)

    # Calculate player direction rotation
    degree = -5 * playerSettings[2]
    radians = -degree * (3.142/180)

    if skiding[0] == False:
        moveDegree = degree
        moveRadians = radians
        movespeed[2] = 2
        playerSettings[3] = playerSettings[2]
    else:
        moveDegree = -5 * playerSettings[3]
        moveRadians = -moveDegree * (3.142/180)

    position[0]-=(movespeed[0]*((math.cos(moveRadians))))
    position[1]-=(movespeed[0]*((math.sin(moveRadians))))
    frontWheel[0]=position[0]-(30*((math.cos(radians))))
    frontWheel[1]=position[1]-(30*((math.sin(radians))))
    rearWheel[0]=position[0]+(30*(math.cos(radians)))
    rearWheel[1]=position[1]+(30*(math.sin(radians)))

    position[2]-=(movespeed[0]*((math.cos(moveRadians))))
    position[3]-=(movespeed[0]*((math.sin(moveRadians))))

    if moveLeft:    # Turn Left
        if movespeed[0] > 0:
            carSettings[6]-=1
            if carSettings[6]==0:
                playerSettings[2] -= 1
                carSettings[6] = movespeed[2]
                if playerImage[0] > 1:
                    playerImage[0] -=1
                if playerSettings[2] < 0:
                    playerSettings[2]=71

    if moveRight:
        if movespeed[0] > 0:
            carSettings[6]-=1
            if carSettings[6]==0:
                playerSettings[2] += 1
                carSettings[6] = movespeed[2]
                if playerImage[0] < 9:
                    playerImage[0] +=1
                if playerSettings[2]>71:
                    playerSettings[2]=0

    if moveRight == False and moveLeft == False:
        if playerImage[0]<5:
            playerImage[0] +=1
        elif playerImage[0]>5:
            playerImage[0] -= 1

    # check if the player has crossed the section 1 line.
    if rotRect.colliderect(section1):
        if cheatCheck[2] == False:
            cheatCheck[0] = 1
            timer[3] = timer[0]
            timer[4] = 0
            timer[5] = 0
            cheatCheck[2] = True
    else:
        cheatCheck[2] = False

    # check if the player has crossed the section 2 line.
    if rotRect.colliderect(section2):
        if cheatCheck[3] == False:
            cheatCheck[0] += 10
            timer[4] = timer[0]-timer[3]
            cheatCheck[3] = True
    else:
        cheatCheck[3] = False

    # check if the player has crossed the finish line.
    if rotRect.colliderect(finishLine):

        timer[7] = True
        if cheatCheck[1] == False:
            if cheatCheck[4] >0:
                cheatCheck[0] +=100
                #LAP INVALID, Above statement is a dummy.
            if cheatCheck[0]==111:
                cheatCheck[0]=0
                if timer[0] < timer[2] and timer[0] > 0:
                    timer[2] = timer[0]
                timer[1] = timer[0]
                lap[4]='Valid'
                validLap = False
            else:
                lap[4]='Invalid'
                validLap = True
            lap[0]=timer[0]
            lap[1]=timer[3]
            lap[2]=timer[4]
            lap[3]=timer[5]
            lap = [0,0,0,0,0,0,WHITE,WHITE,WHITE,WHITE]
            timer[0]=0
            cheatCheck[4]=0
            lapCount += 1
            cheatCheck[1] = True
            cheatCheck[7] = WHITE
    else:
        cheatCheck[1]=False
        if timer[7]:
            timer[0]+=1


    # move the player
    if moveDown:    # Braking
        carSettings[1] -= carSettings[3]
        if movespeed[0] > 14:
            skiding[0]=True
            if dirtPosition == 0:
                skiding[1] = recordSkid(skiding[1],4,skids,2)
        elif skiding[1] > 0:
            skiding[1] -= 1
        else:
            skiding[0] = False
    else:
        skiding[0] = False
        skiding[1] = 0

    if moveUp:    # Accelerate
        carSettings[1] += carSettings[2]
    else:
        carSettings[1] -= carSettings[4]

    movespeed[1] = carSettings[0]

    if carSettings[1] >= carSettings[5] and movespeed[0] < movespeed[1]:# Change up gear
        movespeed[0] +=1
        carSettings[1] = 0
    elif carSettings[1] >= carSettings[5] and movespeed[0] >= movespeed[1]:# Accelerate Limiter
        carSettings[1] = carSettings[5]
    elif carSettings[1] < 0 and movespeed[0] == 0: # Braking limiter
        carSettings[1]=0
        movespeed[0]=0
    elif carSettings[1] <0:# Change down gears
        movespeed[0] -=1
        carSettings[1]=carSettings[5]

    if movespeed[0] > movespeed[1]:
        carSettings[1] -= carSettings[3]

    pygame.draw.rect(windowSurface, BLACK,(WINDOWWIDTH-100,WINDOWHEIGHT-50, 50,((-carSettings[0]-1)*carSettings[5]/6)),2)
    pygame.draw.rect(windowSurface, BLUE,(WINDOWWIDTH-98,(WINDOWHEIGHT-51), 47,(-movespeed[0]*carSettings[5]-carSettings[1])/6))

    if moveUp:
        pygame.draw.circle(windowSurface, GREEN, (WINDOWWIDTH-200, WINDOWHEIGHT-75), 19, 0)
    pygame.draw.circle(windowSurface, BLACK, (WINDOWWIDTH-200, WINDOWHEIGHT-75), 20, 1)
    if moveDown:
        pygame.draw.circle(windowSurface, RED, (WINDOWWIDTH-250, WINDOWHEIGHT-75), 19, 0)
    pygame.draw.circle(windowSurface, BLACK, (WINDOWWIDTH-250, WINDOWHEIGHT-75), 20, 1)

    if moveRight:
        pygame.draw.circle(windowSurface, LBLUE, (WINDOWWIDTH-300, WINDOWHEIGHT-75), 19, 0)
    pygame.draw.circle(windowSurface, BLACK, (WINDOWWIDTH-300, WINDOWHEIGHT-75), 20, 1)

    if moveLeft:
        pygame.draw.circle(windowSurface, LBLUE, (WINDOWWIDTH-350, WINDOWHEIGHT-75), 19, 0)
    pygame.draw.circle(windowSurface, BLACK, (WINDOWWIDTH-350, WINDOWHEIGHT-75), 20, 1)

    speedText = smallFont.render('Speed', True, WHITE,)
    windowSurface.blit(speedText, (WINDOWWIDTH-96,WINDOWHEIGHT-64))

    gasText = smallFont.render('Gas', True, WHITE,)
    windowSurface.blit(gasText, (WINDOWWIDTH-212, WINDOWHEIGHT-110))

    brakeText = smallFont.render('Brake', True, WHITE,)
    windowSurface.blit(brakeText, (WINDOWWIDTH-267, WINDOWHEIGHT-110))

    rightText = smallFont.render('-->', True, WHITE,)
    windowSurface.blit(rightText, (WINDOWWIDTH-307, WINDOWHEIGHT-110))

    leftText = smallFont.render('<--', True, WHITE,)
    windowSurface.blit(leftText, (WINDOWWIDTH-359, WINDOWHEIGHT-110))

    lapLabelColor = WHITE
    if not validLap:
        lapLabelColor = RED
    last = guessFont.render("%.2f" %(round(timer[0]/60,2)), True, lapLabelColor,)
    windowSurface.blit(last, (WINDOWWIDTH/2-25,20))

    # draw the window onto the screen
    framerate()
    pygame.display.update()
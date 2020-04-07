import pygame
import playerControl
import machineControl
import classes
import pygame.locals
import math

gamemodeChosen = False
while not gamemodeChosen:
    GAMEMODE = "usr"#input("enter the gamemode(ai/usr):")
    if GAMEMODE=="ai":
        gamemodeChosen = True
    elif GAMEMODE=="usr":
        gamemodeChosen = True
    else:
        print("command not recognised")

pygame.init()

display_width = 1440
display_height = 720

black = (0,0,0)
darkGrey = (192,192,192)
white = (255,255,255)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Mark's race simulator")

clock = pygame.time.Clock()

def getControls(carStatus, gamemode):
    if gamemode=="ai":
        return machineControl.getControls(carStatus)
    return playerControl.getControls(CONTROLS)

def updateCarView(car, track):
    turnAmount = car.move(CONTROLS, track)
    msg = ("({},{})")
    print(msg.format(turnAmount.x,turnAmount.y))
    message_display(msg.format(turnAmount.x,turnAmount.y))
    gameDisplay.blit(car.img, (car.pos.x,car.pos.y))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    bigfont = pygame.font.Font('freesansbold.ttf',60)
    TextSurf, TextRect = text_objects(text, bigfont)
    TextRect.center = ((display_width*11/12),(display_height*11/12))
    gameDisplay.blit(TextSurf, TextRect)


def drawMap(map):
    track = map.nodes
    prevSection = track[len(track)-1]
    for trackSection in track:
         a = (display_width*trackSection[1][0],display_height*trackSection[1][1])
         b = (display_width*trackSection[0][0],display_height*trackSection[0][1])
         c = (display_width*prevSection[0][0],display_height*prevSection[0][1])
         d = (display_width*prevSection[1][0],display_height*prevSection[1][1])
         pygame.draw.polygon(gameDisplay,darkGrey,(a,b,c,d))
         prevSection = trackSection

dummyTrack =  classes.Map(
                    (0.45,0.8),
                    (
                        (#across1
                            (1/6,1/6),#coordinate1
                            (1/3,1/3)#coordinate2
                        ),
                        (#across2
                            (5/6,1/6),
                            (2/3,1/3)
                        ),
                        (#across3
                            (5/6,5/6),
                            (2/3,2/3)
                        ),
                        (#across4
                            (1/6,5/6),
                            (1/3,2/3)
                        )
                    )                
                )
                
TRACK = dummyTrack
CAR = classes.Car()
STARTPOS = (display_width*0.45, display_height*0.8)
CAR.pos.x = STARTPOS[0]
CAR.pos.y = STARTPOS[1]
CAR.posMax.x = display_width
CAR.posMax.y = display_height


CONTROLS = classes.Control()

FRAMERATE = 60      #frames per second
CONTINUE = True
HANDLER_LOOKUP = dict()

'''
    newHandler:
    adds an event-handler relationship to the HANDLER_LOOKUP dict, and returns a tuple for removal purposes
    '''
def newHandler(event_type, handler):
    if event_type not in HANDLER_LOOKUP.keys():
        HANDLER_LOOKUP[event_type] = set()
    HANDLER_LOOKUP[event_type].add(handler)
    return (event_type, handler)
def removeHandler(handlerID):
    try:
        event_name = handlerID[0]
        handler = handlerID[1]
        HANDLER_LOOKUP[event_name].remove(handler)
        return True
    except KeyError:
        return False

def quitEventloop(event):
    global CONTINUE
    CONTINUE = False
def quitGame(event):
    dummy = ""
    if event.key == pygame.locals.K_ESCAPE:
        quitEventloop(dummy)

'''
    event listeners
    '''
newHandler(pygame.QUIT, quitEventloop)
newHandler(pygame.KEYDOWN,quitGame)


while CONTINUE:
    #-----------EVENT LOOP------------
    for event in pygame.event.get():
        handlers = set()
        if event.type in HANDLER_LOOKUP.keys():
            handlers = HANDLER_LOOKUP[event.type]
            if handlers is None:
                continue
            for handler in handlers:
                handler(event)
    
    status = True
    
    CONTROLS = getControls(status, GAMEMODE)

    gameDisplay.fill(white)
    drawMap(dummyTrack)
    updateCarView(CAR, TRACK)
    pygame.display.update()

    clock.tick( FRAMERATE )

pygame.quit()
quit()
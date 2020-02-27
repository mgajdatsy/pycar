import pygame
import classes
import pygame.locals
import math

def getControls(control: classes.Control):
    keys = pygame.key.get_pressed()
    control.steer   /= 2
    control.gas     /= 2
    if keys[pygame.locals.K_UP]:
        control.gas += 0.2
    if keys[pygame.locals.K_DOWN]:
        control.gas -= 0.2
    if keys[pygame.locals.K_LEFT]:
        control.steer += 0.5
    if keys[pygame.locals.K_RIGHT]:
        control.steer -= 0.5
    return control
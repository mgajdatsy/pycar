import pygame
import classes
import math

def getControls(status):
    control = classes.Control()
    control.steer   = 0
    control.gas     = 0
    return control

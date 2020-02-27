import pygame
import math
import json

class Vector:
    def __init__(self, x = 0, y = 0 ):
        self.x = x
        self.y = y
    
    x: float
    y: float

    def getLength(self):
        return self.dotProduct(self)
    
    def getAngle(self):
        return math.atan2(self.y, self.x)
    
    def getNormal(self):
        return Vector( self.x / self.getLength(), self.y / self.getLength())

    def dotProduct(self, other):
        return math.sqrt(self.x*other.x + self.y*other.y)

    def getDistanceFromSection(self,segment):
        y = segment.end.y-segment.start.y
        x = segment.end.x-segment.start.x
        normal = Vector(y, -x)
        return math.sqrt( self.dotProduct(normal)-normal.getLength() )

class Line:
    def __init__(self, a=0, b=0, c=0):
        self.a = a
        self.b = b
        self.c = c
    
    a: float
    b: float
    c: float

    def isVertical(self):
        if self.b == 0:
            return True
        else: return False
    
    def isHorizontal(self):
        if self.a == 0:
            return True
        else: return False

    def isParallelWith(self, other):
        if self.isHorizontal() != other.isHorizontal():
            return False
        elif self.isHorizontal() and other.isHorizontal():
            return True
        else:
            if (self.b / self.a) == (other.b / other.a):
                return True
            else: return False

    def intersectWithLine(self, other):
        intersection = Vector(0,0)
        if not self.isHorizontal():
            pass
            

class Section:
    def __init__(self, startPoint = Vector(),  endPoint = Vector()):
        self.start = startPoint
        self.end = endPoint
    
    start: Vector
    end: Vector

    def line(self):
        a = self.start.y-self.end.y
        b = self.end.x-self.start.x
        c = -b*self.start.y - a*self.start.x
        return Line(a,b,c)

class Car:
    def __init__(self):
        self.steer = 0
        self.speed = 0
        self.pos = Vector()
        self.posMax = Vector()
        self.facing = 0
        self.facingInRadians = (self.facing/180)*math.pi
        
    steer: float
    speed: float
    pos: Vector
    posMax: Vector
    facing: float
    facingInRadians: float
    originalImg = pygame.image.load("assets/pickups/grey2.png")
    img=originalImg        

    def move(self, control, track):
        self.speed *= 0.97
        self.speed += control.gas
        self.facing += control.steer*self.speed*0.9
        if self.facing > 360:
            self.facing -= 360
        if self.facing < 0:
            self.facing += 360
        self.pos.x += math.cos(self.facingInRadians)*self.speed*1.2
        self.pos.y -= math.sin(self.facingInRadians)*self.speed*1.2
        self.facingInRadians = (self.facing/180)*math.pi
        if self.pos.x > self.posMax.x:
            self.pos.x -= self.posMax.x
        if self.pos.y > self.posMax.y:
            self.pos.y -= self.posMax.y
        if self.pos.x < 0:
            self.pos.x += self.posMax.x
        if self.pos.y < 0:
            self.pos.y += self.posMax.y
           
    def updateFacing(self):
        self.img = pygame.transform.rotate(self.originalImg, self.facing)
    
class Control:
    def __init__(self):
        self.steer = 0
        self.gas = 0

    steer:  float
    gas:    float

class Map:
    nodes: list
    startPos: Vector

    def __init__(self, start, node_list):
        self.startPos=start
        self.nodes = node_list
    
    def open(self, url):
        mapfile = open(url)
        data = json.load(mapfile)
        self.startPos = data[0]
        self.nodes = data[1]
        mapfile.close()

    def save(self, url):
        pass
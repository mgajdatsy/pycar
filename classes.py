import pygame
import math
import json

class Vector:
    def __init__(self, x = 0, y = 0 ):
        self.x = x
        self.y = y
    
    def __eq__(self, obj):
        return isinstance(obj, Vector) and self.x == obj.x and self.y == obj.y

    x: float
    y: float

    def getLength(self):
        return self.dotProduct(self)
    
    def getAngle(self):
        return math.atan2(self.y, self.x)
    
    def getNormal(self):
        return Vector( self.x / self.getLength(), self.y / self.getLength())


    def plus(self, other):
        return Vector(self.x + other.x, self.y + other.y)
    
    def minus(self, other):
        other = other.multiplyByScalar(-1)
        return self.add(other)

    def dotProduct(self, other):
        return math.sqrt(self.x*other.x + self.y*other.y)

    def multiplyByScalar(self, other: int):
        return Vector(self.x*other, self.y*other)

    def multiplyByComplex(self, other):
        x = self.x*other.x - self.y*other.y
        y = self.x*other.y + self.y*other.x
        return Vector(x,y)


    def getDistanceFromSection(self,segment):
        y = segment.end.y-segment.start.y
        x = segment.end.x-segment.start.x
        normal = Vector(y, -x)
        return math.sqrt( self.dotProduct(normal)-normal.getLength() )

def getVectorFromRadians(angle):
    x = math.cos(angle)
    y = math.sin(angle)
    return Vector(x,y)

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

    def isParallelCheck(self, other):
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
        if not self.isParallelWith(other):
            if abs(self.b) == abs(other.b):
                other.a*=2
                other.b*=2
                other.c*=2
            if not self.isHorizontal():
                intersection.y = ( ( self.a * other.c ) - ( other.a * self.c ) ) / (self.a * ( self.b + other.b ))
                intersection.x = ( self.c - self.b * intersection.y ) / self.a
                return intersection
            else:
                intersection.y = self.c / self.b
                intersection.x = ( other.c - other.b * intersection.y ) / other.a
                return intersection
        else:
            return None

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

    def containsPointInBox(self, point):
        if ((point.x < self.startPoint.x) == (point.x > self.endPoint.x)) and ((point.y < self.startPoint.y) == (point.y > self.endPoint.y)):
            return True
        return False

    def getIntersectWithSection(self, other):
        inters = self.line().intersectWithLine(other.line())
        if inters is not None:
            if self.containsPointInBox(inters) and other.containsPointInBox(inters):
                return inters
        return None

class Car:
    def __init__(self):
        self.steer = 0
        self.speed = 0
        self.pos = Vector()
        self.posMax = Vector()
        self.facingInComplex = Vector(1,0)
        self.width = 16
        self.length = 32
        
    def IGetColliderList(self):
        nodes = [] #0:lf, 1:lr, 2:rr, 3:rf
        nodes.append(Vector(self.length/2, self.width/2))
        nodes.append(Vector(-self.length/2, self.width/2))
        nodes.append(Vector(-self.length/2, -self.width/2))
        nodes.append(Vector(self.length/2, -self.width/2))
        for node in nodes:
            node = node.multiplyByComplex(self.facingInComplex)
            node = node.add(self.pos)
        edges = []
        prevNode = nodes[len(nodes)-1]
        for node in nodes:
            edges.append(Section(prevNode, node))
            prevNode = node
        return edges
        

    steer: float
    speed: float
    length: float
    width: float
    pos: Vector
    posMax: Vector

    facingInComplex: Vector
    def getFacing(self):
        return self.facingInComplex.getAngle()

    def getFacingInRadians(self):
        return (self.getFacing()/180)*math.pi

    originalImg = pygame.image.load("assets/pickups/grey2.png")
    img=originalImg        

    def move(self, control, track):
        self.speed *= 0.97
        self.speed += control.gas
        turn = getVectorFromRadians(control.steer*self.speed)
        self.facingInComplex = self.facingInComplex.multiplyByComplex(turn)
        self.pos.x += math.cos(self.getFacingInRadians())*self.speed*1.2
        self.pos.y -= math.sin(self.getFacingInRadians())*self.speed*1.2
        if self.pos.x > self.posMax.x:
            self.pos.x -= self.posMax.x
        if self.pos.y > self.posMax.y:
            self.pos.y -= self.posMax.y
        if self.pos.x < 0:
            self.pos.x += self.posMax.x
        if self.pos.y < 0:
            self.pos.y += self.posMax.y
        self.updateFacing()
        return turn
           
    def updateFacing(self):
        self.img = pygame.transform.rotate(self.originalImg, self.getFacing())
    
class Control:
    def __init__(self):
        self.steer = 0
        self.gas = 0

    steer:  float
    gas:    float

class Map:
    def __init__(self, start, node_list):
        self.startPos=start
        self.nodes = node_list
    
    def IGetColliderList(self):
        edges = []
        prevSection = self.nodes[len(self.nodes)-1]
        for trackSection in self.nodes:
            edges.append(Section(prevSection.startPoint, trackSection.startPoint))
            edges.append(Section(prevSection.endPoint, trackSection.endPoint))
            prevSection = trackSection
        return edges

    nodes: list
    startPos: Vector

    def open(self, url):
        mapfile = open(url)
        data = json.load(mapfile)
        self.startPos = data[0]
        self.nodes = data[1]
        mapfile.close()

    def save(self, url):
        pass

def doesCollide(obj1, obj2):
    for edge1 in obj1.getColliderList():
        for edge2 in obj2.getColliderList():
            if edge1.getIntersectWithSection(edge2) is None:
                pass
            else:
                return True
    return False
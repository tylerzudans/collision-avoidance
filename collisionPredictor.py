#Collision detector for python v1.0
#Author: Tyler V. Zudans

import matplotlib.pyplot as plt
import numpy as np

class box:#represents an on screen box such as a bounding box for an object or the camera's view
    def __init__(self,xmin,xmax,ymin,ymax):# points in pixels
        self.xmin=float(xmin)
        self.xmax=float(xmax)
        self.ymin=float(ymin)
        self.ymax=float(ymax)
        self.label= ""
    def x(self): # center of box x
        return((self.xmin+self.xmax)/2.0)
    def y(self): # center of box y
        return((self.ymin+self.ymax)/2.0)
    def w(self): #width of box
        return(self.xmax-self.xmin)
    def h(self):
        return(self.ymax-self.ymin)
    def get_lines(self):
        #plt.plot(plt.axvline(self.xmin, self.ymin, self.ymax, color='r'))#l
        lines =[
        plt.axvline(self.xmin, self.ymin, self.ymax, color='r',linewidth=10),#l
        plt.axvline(self.xmax, self.ymin, self.ymax, color='r',linewidth=2),#r
        plt.axhline(self.ymax,self.xmin,self.xmax, color='r',linewidth=2),#top
        plt.axhline(self.ymin,self.xmin,self.xmax, color='r',linewidth=2)#bot
        ]
        return lines
        #plt.show()
    def area(self):
        return(self.w()*self.h())
    def plot_box(self,c):
        #plt.plot(plt.axvline(self.xmin, self.ymin, self.ymax, color='r'))#l\
        l =2
        plt.plot([self.xmin, self.xmin],[self.ymax,self.ymin], color=c,linewidth=l),#l
        plt.plot([self.xmax, self.xmax],[self.ymax,self.ymin], color=c,linewidth=l),#r
        plt.plot([self.xmax, self.xmin],[self.ymax,self.ymax], color=c,linewidth=l),#t
        plt.plot([self.xmax, self.xmin],[self.ymin,self.ymin], color=c,linewidth=l),#b
        plt.plot([self.x()],[self.y()],'o',color = c)#c
        #plt.text(self.x()+o,self.y()+o,self.label,color = c)
    def plot_label(self):
        o = 10

        plt.text(self.x()+o,self.y()+o,self.label,bbox=dict(boxstyle="square",
                   ec=(0.3, 0.3, 0.3),#outline color
                   fc=(1., 1., 1.),
                   )
        )
    def contains(self,x,y):
        return(x>self.xmin and x<self.xmax and y<self.ymax and y> self.ymin)
class Threat:
    def __init__(self,box, time):# Represents the bounding box of a threat and its ETA
        self.box= box
        self.time = time

def detectThreat(frame1,frame2,camera,delT):#projects threat into future from current(f2) and past(f1) frames with elapsed time delT in the camera frame
    delX=frame2.x()-frame1.x()
    delY=frame2.y()-frame1.y()
    tf = delT
    if(delX!=0):
        tf=delT*(camera.x()-frame2.x())/(delX)
    def y(t):
        return frame2.y()+(delY)*t
    y_col = y(tf)
    x_col = camera.x()
    h_col = frame2.h()+(frame2.h()-frame1.h())*tf/delT
    w_col = frame2.w()+(frame2.w()-frame1.w())*tf/delT
    def yxht_to_box(y,x,h,w):
        h2 = h_col/2
        w2 = w_col/2
        return box(x-w2,x+w2,y-h2,y+h2)
    return Threat(yxht_to_box(y_col,x_col,h_col,w_col),tf)
def plot_collision(camera,boxes):
    for box in boxes:
        plt.plot([box.x()],[box.y()],'ro')
def plot_collision_boxes(camera,boxes):
    for box in boxes:
        #print box of random color
        color = np.random.rand(3,)
        plt.plot([box.x()],[box.y()],'o',color=color)
        box.plot_box(color)
    for box in boxes:
        box.plot_label()
        
    plt.plot(camera.x(),camera.y(),'k+')      
    plt.axis([camera.xmin, camera.xmax, camera.ymin, camera.ymax])
    plt.show()
def threatInfo(frame1,frame2,camera,delT,suppress_output = False,close = 0.1,soon = 5.0):
    #threshold for dangerous size as percentage of screen
    #now in parameters
    
    #threshold for how much time it must be from collision
    #now in parameters
    collision = detectThreat(frame1,frame2,camera,delT);
    
    
    
    #send warning if is a threat
    collision_true = collision.box.area()>camera.area()*close #object is large enough
    collision_true = collision_true and collision.time <soon #object will collide before "soon"
    collision_true = collision_true and collision.box.contains(camera.x(),camera.y()) #center of camera is in object
    collision_true = collision_true and collision.time > 0 #collsion is in future, not past
    
    
    if(collision_true):
        if(not suppress_output):
            #Create Labels
            frame1.label = "Seconds = -"+str(delT)
            frame2.label = "Seconds = 0"
            collision.box.label = "Seconds = +"+str(collision.time)
            
            #Display Danger
            plot_collision_boxes(camera,[frame1,frame2,collision.box])
            print("WARNING: Object approching from "+ getRelativeLocation(camera,collision.box)+", collision in ",collision.time," seconds")
        return True
    return False
    
def getRelativeLocation(camera,box):
    up = "below"
    right = "right"
    if(box.y()<camera.y()):
        up="above";
    if(box.x()<camera.x()):
        right = "left"
    return((up+" and to the "+right))

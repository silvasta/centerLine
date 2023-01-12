import numpy as np
import matplotlib.pyplot as plt
import math


class CircleLineAnnotator:

    def __init__(self, line, height=480, width=640):
        self.p1 = line[0]
        self.p2 = line[1]
        self.height = height
        self.width = width
        self.radius = max(height,width)

    def two_points_to_circle(self):
        dx = self.p2[0]-self.p1[0] #x2-x1
        dy = self.p2[1]-self.p1[1] #y2-y1
        dr = math.sqrt(dx**2+dy**2)
        D  = self.p1[0]*self.p2[1] - self.p2[0]*self.p1[1]  #x1*y2 - x2*y1

        xr1 = (D*dy+np.sign(dy)*dx*math.sqrt(self.radius**2*dr**2-D**2))/dr**2
        yr1 = (-D*dx+abs(dy)*math.sqrt(self.radius**2*dr**2-D**2))/dr**2

        xr2 = (D*dy-np.sign(dy)*dx*math.sqrt(self.radius**2*dr**2-D**2))/dr**2
        yr2 = (-D*dx-abs(dy)*math.sqrt(self.radius**2*dr**2-D**2))/dr**2

        #necessary ??
        self.pr1 = (xr1,yr1)
        self.pr2 = (xr2,yr2)
        # print(self.pr1)
        # print(self.pr2)
        
        # angle clockwise from y axis in range -pi to pi
        self.phi   = np.arctan2(xr1, yr1)
        self.theta = np.arctan2(xr2, yr2)
        # print(self.phi*180/math.pi)
        # print(self.theta*180/math.pi)
    
    def plot_on_circle(self):
        # plot circle
        circle = plt.Circle((0,0),self.radius, fc='lightgrey',ec="black")
        plt.gca().add_patch(circle)

        # plot rectangle
        rectangle = plt.Rectangle((-self.width/2,-self.height/2), self.width, self.height, fc='limegreen',ec="black")
        plt.gca().add_patch(rectangle)

        # plot lines
        line = plt.Line2D((self.pr1[0], self.pr2[0]), (self.pr1[1], self.pr2[1]), lw=1, color="red", linestyle='dashed')
        plt.gca().add_line(line)
        line_segment = plt.Line2D((self.p1[0], self.p2[0]), (self.p1[1], self.p2[1]), lw=3, color="white")
        plt.gca().add_line(line_segment)
        plt.gca().add_patch(plt.Circle(self.p1, 8, fc="yellow", ec="yellow"))
        plt.gca().add_patch(plt.Circle(self.p2, 8, fc="yellow", ec="yellow"))
        line_x = plt.Line2D((0, 0), (-750, 750), lw=1, color="grey", linestyle='dashdot')
        plt.gca().add_line(line_x)
        line_y = plt.Line2D((-750, 750), (0, 0), lw=1, color="grey", linestyle='dashdot')
        plt.gca().add_line(line_y)

        p1 = plt.Circle(self.pr1, 15, fc='None', ec="Blue")
        p2 = plt.Circle(self.pr2 ,15, fc='None', ec="Blue")
        plt.gca().add_patch(p1)
        plt.gca().add_patch(p2)

        plt.box(False)
        plt.axis(False)
        plt.axis("equal")
        #plt.grid()
        plt.show()

def main():
    x1 = -50
    y1 = -10
    x2 = 150
    y2 = 300

    line = [(x1,y1), (x2,y2)]

    circleAnnotation = CircleLineAnnotator(line)
    circleAnnotation.two_points_to_circle()
    circleAnnotation.plot_on_circle()




if __name__ == "__main__":
    main()

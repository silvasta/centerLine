import numpy as np
import matplotlib.pyplot as plt
import math

height = 480
width = 640

r = max(height,width)


x1 = 50
y1 = -150
x2 = 150
y2 = 150

dx = x2-x1
dy = y2-y1
dr = math.sqrt(dx**2+dy**2)
D = x1*y2 - x2*y1

xr1 = (D*dy+np.sign(dy)*dx*math.sqrt(r**2*dr**2-D**2))/dr**2
yr1 = (-D*dx+abs(dy)*math.sqrt(r**2*dr**2-D**2))/dr**2

xr2 = (D*dy-np.sign(dy)*dx*math.sqrt(r**2*dr**2-D**2))/dr**2
yr2 = (-D*dx-abs(dy)*math.sqrt(r**2*dr**2-D**2))/dr**2

print(xr1, yr1)

p1 = plt.Circle((xr1,yr1),20, fc='None',ec="Red")
p2 = plt.Circle((xr2,yr2),20, fc='None',ec="Red")
plt.gca().add_patch(p1)
plt.gca().add_patch(p2)

#plot circle
    # ts = np.linspace(0, 2*np.pi)
    # xs = [r*np.cos(t) for t in ts]
    # ys = [r*np.sin(t) for t in ts]
    # plt.plot(xs, ys, "r")
circle = plt.Circle((0,0),r, fc='None',ec="black")
plt.gca().add_patch(circle)

# plot rectangle
rectangle = plt.Rectangle((-width/2,-height/2), width, height, fc='None',ec="black")
plt.gca().add_patch(rectangle)

# plot lines
line = plt.Line2D((-150, 350), (-750, 750), lw=1, color="green")
plt.gca().add_line(line)
line_segment = plt.Line2D((50, 150), (-150, 150), lw=3, color="purple")
plt.gca().add_line(line_segment)
line_x = plt.Line2D((0, 0), (-750, 750), lw=1, color="grey")
plt.gca().add_line(line_x)
line_y = plt.Line2D((-750, 750), (0, 0), lw=1, color="grey")
plt.gca().add_line(line_y)


line_xr1 = plt.Line2D((xr1, xr1), (-750, 750) ,lw=1, color="grey")
plt.gca().add_line(line_xr1)
line_xr2 = plt.Line2D((xr2, xr2), (-750, 750) ,lw=1, color="grey")
plt.gca().add_line(line_xr2)

line_yr1 = plt.Line2D((-750, 750), (yr1, yr1), lw=1, color="grey")
plt.gca().add_line(line_yr1)
line_yr2 = plt.Line2D((-750, 750), (yr2, yr2), lw=1, color="grey")
plt.gca().add_line(line_yr2)



plt.box(True)
plt.axis(True)
plt.axis("equal")
#plt.grid()
plt.show()
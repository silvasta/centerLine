import numpy as np
import matplotlib.pyplot as plt
import math

height = 480
width = 640

A = (285,441)
B = (329,72)
p1 = plt.Circle(A,5, fc='None',ec="Red")
p2 = plt.Circle(B,5, fc='None',ec="Red")
line = plt.Line2D((A[0],B[0]),(A[1],B[1]), lw=1, color="green")
plt.gca().add_patch(p1)
plt.gca().add_patch(p2)
plt.gca().add_line(line)

circle = plt.Circle((-41,530),40, fc='None',ec="black")
plt.gca().add_patch(circle)

circle = plt.Circle((305,-169),473, fc='None',ec="black")
plt.gca().add_patch(circle)


circle = plt.Circle((301,303),2, fc='None',ec="blue")
plt.gca().add_patch(circle)

circle = plt.Circle((-194,-52),61, fc='None',ec="black")
plt.gca().add_patch(circle)

circle = plt.Circle((475,-13),45, fc='None',ec="black")
plt.gca().add_patch(circle)

circle = plt.Circle((625,-124),37, fc='None',ec="black")
plt.gca().add_patch(circle)


circle = plt.Circle((329,72),2, fc='None',ec="blue")
plt.gca().add_patch(circle)






rectangle = plt.Rectangle((0,0), width, height, fc='None',ec="black")
plt.gca().add_patch(rectangle)

plt.box(True)
plt.axis(True)
plt.axis("equal")
#plt.grid()
plt.show()

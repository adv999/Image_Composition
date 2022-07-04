import cv2
from PIL import Image, ImageFilter
import numpy as np
import math
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def get_line_value(endPoints,w,h):
    thirds_line=np.zeros((4,4))
    thirds_line[0]=[0, 1/3*h, w, 1/3*h]
    thirds_line[1]=[0, 2/3*h, w, 2/3*h]
    thirds_line[2]=[1/3*w, 0, 1/3*w, h]
    thirds_line[3]=[2/3*w, 0, 2/3*w, h]

    thirds_center=np.zeros((4,2))
    thirds_center[0]=[0.5*w, 1/3*h]
    thirds_center[1]=[0.5*w, 2/3*h]
    thirds_center[2]=[1/3*w, 0.5*h]
    thirds_center[3]=[2/3*w, 0.5*h]

    sigma_line=0.17
    line_idx=0

    len=math.sqrt((thirds_line[0][2]-thirds_line[0][0])**2 + (thirds_line[0][3]-thirds_line[0][1])**2)
    d1=(((thirds_line[0][3]-thirds_line[0][1]) * endPoints[0][0] - (thirds_line[0][2]-thirds_line[0][0])*endPoints[0][1] + thirds_line[0][2]*thirds_line[0][1] - thirds_line[0][0]*thirds_line[0][3]))/len
    d2=(((thirds_line[0][3]-thirds_line[0][1]) * endPoints[1][0] - (thirds_line[0][2]-thirds_line[0][0])*endPoints[1][1] + thirds_line[0][2]*thirds_line[0][1] - thirds_line[0][0]*thirds_line[0][3]))/len

    if(d1*d2>=0):
        temp=abs(d1+d2)/2
    else:
        temp=(d1*d1+d2*d2)/2/abs(d1-d2)
    

    for i in range (1,4):
        len=math.sqrt((thirds_line[i][2]-thirds_line[i][0])**2 + (thirds_line[i][3]-thirds_line[i][1])**2)
        d1=(((thirds_line[i][3]-thirds_line[i][1]) * endPoints[0][0] - (thirds_line[i][2]-thirds_line[i][0])*endPoints[0][1] + thirds_line[i][2]*thirds_line[i][1] - thirds_line[i][0]*thirds_line[i][3]))/len
        d2=(((thirds_line[i][3]-thirds_line[i][1]) * endPoints[1][0] - (thirds_line[i][2]-thirds_line[i][0])*endPoints[1][1] + thirds_line[i][2]*thirds_line[i][1] - thirds_line[i][0]*thirds_line[i][3]))/len

        if(d1*d2>=0):
            line_distance=abs(d1+d2)/2
        else:
            line_distance=(d1*d1+d2*d2)/2/abs(d1-d2)
        
        if line_distance<temp:
            temp=line_distance
            line_idx=i
    
    x1=endPoints[0][0]
    y1=endPoints[0][1]
    x2=endPoints[1][0]
    y2=endPoints[1][1]

    k = abs((y2-y1) / (x2-x1))
    image_center_x = 0.5 * w
    image_center_y = 0.5 * h

    targetPoint=np.zeros((1,2))

    if line_idx==0 or line_idx==1:
        tanTheta = h/w
        tanTheta1 = 1/4 * tanTheta
        tanTheta2 = 3/4 * tanTheta
        if k<tanTheta:
            targetPoint=[thirds_center[line_idx]]
            line_info=0
        else:
            targetPoint=[[image_center_x, image_center_y]]
            line_info=2
            if (x2-x1)==0:
                line_info=1
        
        dist=abs(targetPoint[0][1]-(y1+y2)*0.5)/w + abs(targetPoint[0][0]-(x1+x2)*0.5)/h
        line_value=math.exp(-dist*dist/2/sigma_line**2)
    
    elif line_idx==2 or line_idx==3:
        k = 1/k
        tanTheta = w/h
        tanTheta1 = 1/4 * tanTheta
        tanTheta2 = 3/4 * tanTheta
        if (k < tanTheta1) or ((x2-x1) == 0):
            targetPoint = [thirds_center[line_idx]];
            line_info=1
        else:
            targetPoint=[[image_center_x, image_center_y]]
            line_info=3
        
        dist=abs(targetPoint[0][0]-(x1+x2)*0.5)/w + abs(targetPoint[0][1]-(y1+y2)*0.5)/h
        line_value=math.exp(-dist*dist/2/sigma_line**2)
    

    return [line_value,line_info]

# print(get_line_value([[2,3],[1,2]],3,4))



    
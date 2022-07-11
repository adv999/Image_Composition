import cv2
from PIL import Image, ImageFilter
from cv2 import projectPoints
import numpy as np
import math
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def get_end_points(im):
   
    # cv2.imshow("Original Image",im)

    # im=cv2.GaussianBlur(im,(5,5),cv2.BORDER_DEFAULT)    #Apply gaussian filter

    # cv2.imshow("Gaussian filter image",im)

    gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)    #Finding gray image
    
    # cv2.imshow("Gray Scale Image",gray)

    edges=cv2.Canny(gray,50,150,apertureSize=3)    #applying edge detection method
    # cv2.imshow("Gray Scale Image",edges)  

    lines=cv2.HoughLines(edges,1,np.pi/180,100)

    lines1=cv2.HoughLinesP(edges,1,np.pi/180,threshold=100,minLineLength=5,maxLineGap=10)

    # print(lines)
    # print(type(lines))
    # print(lines.size)

    mxlen=0
    i=0

    points=[]

    for r_theta in lines:

        r,theta = r_theta[0]

        a = np.cos(theta)

        b = np.sin(theta)
        
        x0 = a*r
        
        y0 = b*r
        
        x1 = int(x0 + 1000*(-b))

        y1 = int(y0 + 1000*(a))
    
        x2 = int(x0 - 1000*(-b))
        
        y2 = int(y0 - 1000*(a))

        points.append([x1,y1,x2,y2])

        len=math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))

        
        # cv2.line(im,(x1,y1),(x2,y2),(0,0,255),1)
        if mxlen<len:
            mxlen=len
            xylong=points 

    # print(points)
    # houghlinep meethod
    # for points in lines1:
    #   # Extracted points nested in the list
    #     x1,y1,x2,y2=points[0]
    #     # Draw the lines joing the points
    #     # On the original image
    #     cv2.line(im,(x1,y1),(x2,y2),(0,255,0),2) 

    # # print(points) 
    # # im=cv2.resize(im,(im.shape[1],im.shape[0]))
    # cv2.imshow("Detected lines",im)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    length_lines=np.shape(lines)[0]

    # print(length_lines,np.shape(lines),np.shape(linesrt))
    
    a=np.zeros((length_lines,1))

    b=np.zeros((length_lines,1))

    for i in range (length_lines):
        a[i]=lines[i][0][0]
        b[i]=lines[i][0][1]

    mean_a=a.mean(axis=0)   

    mean_b=b.mean(axis=0)

    # print(mean_a,mean_b)

    a=a-mean_a[0]
    b=b-mean_b[0]

    std_a=a.std(axis=0)

    std_b=b.std(axis=0)

    if std_a[0]==0 or std_b[0]==0:
        return [[0,0],[0,0]]

    # print(std_a,std_b)

    a=a/std_a[0]
    b=b/std_b[0]

    if length_lines==0:
        return [[-1,-1],[-1,-1]]
    

    num_cluster=min(5,length_lines)

    c=np.zeros((length_lines,2))
    for i in range (length_lines):
        c[i][0]=a[i][0]
        c[i][1]=b[i][0]

    kmeans=KMeans(n_clusters=num_cluster,random_state=0).fit(c)

    idx=kmeans.labels_
    center=kmeans.cluster_centers_

    # print(idx,center)

    sum_line_length=np.zeros((num_cluster,1))



    for i in range (length_lines):
        x1=points[i][0]
        y1=points[i][1]
        x2=points[i][2]
        y2=points[i][3]
        sum_line_length[idx[i]][0]+=math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))

    mx=0
    ind=0
    i=0
    for d in sum_line_length:
        if d[0]>mx:
            mx=d
            ind=i
        i+=1
    
    ab=center[ind]*[std_a[0],std_b[0]]+[mean_a[0],mean_b[0]]

    rho=ab[0]
    theta=math.radians(ab[1])

    h,w,c=im.shape

    ips=[[1, int((rho-math.cos(theta))/math.sin(theta))],
            [w, int((rho-w*math.cos(theta))/math.sin(theta))],
            [int((rho-math.sin(theta))/math.cos(theta)),1],
            [int((rho-h*math.sin(theta))/math.cos(theta)),h]]
    
    j=0
    endpoints=np.zeros((2,2))
    for i in range (4):
        p=ips[i]
        if(p[0]>0 and p[0]<=w and p[1]>0 and p[1]<=h):
            endpoints[j]=p
            j+=1

    return endpoints
    

# im=cv2.imread("newpic.png")   
# endpoints=get_end_points(im)
# print(endpoints)



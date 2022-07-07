
import getline
import getlinevalue
import math
import cv2
from matplotlib import pyplot as plt

def score(im):
    threshold = 0.35
    num = 0
    num_good = 0
    num_bad = 0

    areaBound_small = 0.33
    areaBound_large = 0.69

    sigma_size = 0.33
    sigma_vb = 0.2
    sigma_point = 0.17

    m_EnSize = 0
    m_EnROT = 0
    m_EnVB = 0
    m_EnDiag = 0
    m_sumEn = 0

    m_wtSize = 0.2
    m_wtROT = 1
    m_wtVB = 0.3
    m_wtDiag = 1
    m_bDiag = 0

    m_wtROTPt = 0.4
    m_wtROTLn = 0.6

    x=im.shape
    print(x)
    height=x[0]
    width=x[1]
    c=x[2]

    # if c==1:
    #     im=cat(3,im,im,im)
    
    
    area_image = height * width
    balanceCenter_x = 0.5 * width
    balanceCenter_y = 0.5 * height

    endPoints=getline.get_end_points(im)

    line_value,line_info=getlinevalue.get_line_value(endPoints,width,height)

    #find salient objects

    saliency=cv2.saliency.StaticSaliencySpectralResidual_create()
    status,saliency_map=saliency.computeSaliency(im)
    saliencyMap = (saliency_map * 255).astype("uint8")
    # print(saliencyMap.shape)
    # cv2.imshow("Saliency map",saliency_map)
    
    
    ret,thresh=cv2.threshold(saliencyMap,89,255,0)
    # cv2.imshow("Saliency map",thresh)
    

    # contours,hierarchy=cv2.findContours(saliency_map,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    contours,hierarchy=cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    
    # finding pixel values
    pixel_value=[]
    for cnt in contours:
        s=0
        for i in range (len(cnt)):
            s+=saliencyMap[cnt[i][0][1]][cnt[i][0][0]]
        pixel_value.append(s)

    multi_ob=0

    temp_area_object=[]

    centroid_object_x=[]
    centroid_object_y=[]
    area_object=[]
    bounding_box=[]
    mean_salval=[]

    cx=[]
    cy=[]
    area_ob=[]
    bounding=[]
    for i in range (len(contours)):
        area_ob.append(cv2.contourArea(contours[i]))     #area
        m=cv2.moments(contours[i])                       #moments
        cx.append(int(m['m10']/m['m00']))                #centroid x
        cy.append(int(m['m01']/m['m00']))                #centroid y
        bounding.append(cv2.boundingRect(contours[i]))   #bounding box

    if len(contours)>1:

        for i in range (len(contours)):
            # finding area of contour[i]
            area=cv2.contourArea(contours[i])
            temp_area_object.append([area,i])

        temp_area_object.sort(reverse=True)

        # print(temp_area_object)

        ratio_objects=temp_area_object[1]/temp_area_object[0]

        if ratio_objects<0.15:
            area_object.append(temp_area_object[0][0])
            centroid_object_x.append(cx[temp_area_object[0][1]])
            centroid_object_y.append(cy[temp_area_object[0][1]])
            mean_salval.append(pixel_value[temp_area_object[0][1]]/temp_area_object[0][0])
            bounding_box.append(bounding[temp_area_object[0][1]])

        else:
            multi_ob=1
            for i in range (len(contours)):
                area_object.append(area_ob[i])
                centroid_object_x.append(cx[i])
                centroid_object_y.append(cy[i])
                mean_salval.append(pixel_value[i]/area_ob[i])
                bounding_box.append(bounding[i])

    else:
        area_object=area_ob
        bounding_box=bounding
        centroid_object_x=cx
        centroid_object_y=cy
        mean_salval.append(pixel_value[0]/area_ob[0])


    #Salient Region Size

    ratio_object_image=area_object[0]/area_image
    
    if (ratio_object_image <= areaBound_small):
        m_EnSize = math.sqrt((ratio_object_image-0.1)**2)
    elif (ratio_object_image <= areaBound_large) and (ratio_object_image > areaBound_small):
        m_EnSize = math.sqrt((ratio_object_image-0.56)**2)
    elif (ratio_object_image > areaBound_large):
        m_EnSize = math.sqrt((ratio_object_image-0.82)**2)
    
    m_EnSize=math.exp(-m_EnSize*m_EnSize/2/sigma_size**2)

    # Visual Balance

    x = 0
    y = 0
    d = 0
    weight = 0
    weightSum = 0

    if multi_ob==1:
        for i in range (len(contours)):
            weight = area_object(i) * mean_salval[i]
            x = x + weight * (centroid_object_x[i])
            y = y + weight * (centroid_object_y[i])
            weightSum = weightSum + weight
    else:
        weight = area_object[0] * mean_salval[0]
        x = x + weight * (centroid_object_x[0])
        y = y + weight * (centroid_object_y[0])
        weightSum = weightSum + weight
    
    x = x / weightSum - balanceCenter_x
    y = y / weightSum - balanceCenter_y
    x = x / width
    y = y / height
    d = abs(x) + abs(y)
    d = math.exp(-d*d/2/sigma_vb**2)
    m_EnVB = d
    
    # Rule of Thirds
    # Line based ROT 
    if line_info==0 or line_info==1:
        m_EnROTLn=line_value
    else:
        m_EnROTLn=0

    # Point based ROT

    dx = 0
    dy = 0
    dist = 0
    weight = 0
    weightSum = 0
    m_EnROTPt = 0

    ptx1 = 1/3 * width
    ptx2 = 2/3 * width
    pty1 = 1/3 * height
    pty2 = 2/3 * height

    if multi_ob==1:
        for i in range (len(contours)):
            weight = area_object[i] * mean_salval[i]
            dx = min(abs(centroid_object_x[i] - ptx1), abs(centroid_object_x[i] - ptx2))
            dy = min(abs(centroid_object_y[i] - pty1), abs(centroid_object_y[i] - pty2))
            weightSum = weightSum + weight
            dist = dx / width + dy / height
            dist = math.exp(-dist*dist/2/sigma_point**2)
            m_EnROTPt = m_EnROTPt + weight*dist
    else:
        weight = area_object[0] * mean_salval[0]
        dx = min(abs(centroid_object_x[0] - ptx1), abs(centroid_object_x[0] - ptx2))
        dy = min(abs(centroid_object_y[0] - pty1), abs(centroid_object_y[0] - pty2))
        weightSum = weightSum + weight
        dist = dx / width + dy / height
        dist = math.exp(-dist*dist/2/sigma_point**2)
        m_EnROTPt = m_EnROTPt + weight*dist


    m_EnROTPt = m_EnROTPt/weightSum
    xx = 0
    if (m_EnROTLn == 0) or (m_EnROTPt == 0):
        m_EnROT = m_EnROTLn + m_EnROTPt
    else:
        m_EnROT = 1 / (m_wtROTPt + m_wtROTLn) * (m_wtROTPt * m_EnROTPt + m_wtROTLn * m_EnROTLn)
        xx = m_EnROTPt

    # Diagonal Dominance

    if (line_info==2) or (line_info == 3):
        m_EnDiag = line_value
        m_bDiag = 1
    else:
        m_EnDiag = 0
        m_bDiag = 0

    # Final Composition Score 

    m_sumEn = (m_wtSize*m_EnSize + m_wtROT*m_EnROT + m_wtVB * m_EnVB + m_bDiag * m_wtDiag * m_EnDiag) / (m_wtSize + m_wtROT + m_wtVB + m_bDiag * m_wtDiag)

    if (m_sumEn > 0.78):
        Result = 'Good'
    elif (m_sumEn < 0.62):
        Result = 'Bad'
    else:
        Result = 'Not Bad'

    ROT_score = m_EnROT * m_wtROT
    VB_score = m_EnVB * m_wtVB
    Diag_score = m_bDiag * m_EnDiag * m_wtDiag
    Size_score = m_EnSize * m_wtSize
    Total_score = m_sumEn

    return [ROT_score,VB_score,Diag_score,Size_score,Total_score,Result]


# im=cv2.imread('newpic.png')
# score(im)

import getline
import getlinevalue
import math
import cv2
import gbvs

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

    height,width,c=im.shape

    if c==1:
        im=cat(3,im,im,im)
    
    area_image = height * width
    balanceCenter_x = 0.5 * width
    balanceCenter_y = 0.5 * height

    endPoints=getline.get_end_points(im)

    line_value,line_info=getlinevalue.get_line_value(endPoints,width,height)

    #find salient objects

    map=gbvs(im)
    print(map)
    

    # Visual Balance

    x = 0
    y = 0
    d = 0
    weight = 0
    weightSum = 0

    
    # Rule of Thirds
    # Line based ROT 
    if line_info==0 or line_info==1:
        m_EnRotLn=line_value
    else:
        m_EnRotLn=0

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

    if multi_obj==1:
        for i in range (np.shape(s)[0]):
            weight = area_object(i) * mean_salval(i)
            dx = min(abs(centroid_object_x(i) - ptx1), abs(centroid_object_x(i) - ptx2))
            dy = min(abs(centroid_object_y(i) - pty1), abs(centroid_object_y(i) - pty2))
            weightSum = weightSum + weight
            dist = dx / width + dy / height
            dist = math.exp(-dist*dist/2/sigma_point**2)
            m_EnROTPt = m_EnROTPt + weight*dist
    else:
        weight = area_object * mean_salval
        dx = min(abs(centroid_object_x - ptx1), abs(centroid_object_x - ptx2))
        dy = min(abs(centroid_object_y - pty1), abs(centroid_object_y - pty2))
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



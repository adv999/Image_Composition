
import cv2
from makeGBVSParams import get_parameters


def out_gbvs(img,param=0,prevMotionInfo=[]):
    
    # if ( strcmp(class(img),'char') == 1 ) img = imread(img); end
    # if ( strcmp(class(img),'uint8') == 1 ) img = double(img)/255; end
    
    dim=img.shape
    if(dim[0]<128 or dim[1]<128):
        print('GBVS Error: gbvs() meant to be used with images >= 128x128')
        return []

    if param==0:
        param=get_parameters()
    
    if param.useIttiKochInsteadOfGBVS==1:
        print('Note: Computing STANDARD Itti/Koch instead of Graph-Based Visual Saliency (GBVS)')
    
    
    # Step 1: Computing raw feature maps from image

    print('Computing Feature Maps')
         

    


im=cv2.imread("newpic.png")
out_gbvs(im)


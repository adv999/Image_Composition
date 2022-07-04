
import makeGBVSParams
import gbvs
import cv2

def ittikochmap(img):
    params = makeGBVSParams.get_parameters()

    params.useIttiKochInsteadOfGBVS = 1
    
    params.channels = 'CIO'
    params.verbose = 1
    params.unCenterBias = 0

    # uncomment the line below (ittiDeltaLevels = [2 3]) for more faithful implementation 
    # (however, known to give crappy results for small images i.e. < 640 in height or width )
    # % params.ittiDeltaLevels = [ 2 3 ]
    
    # if ( strcmp(class(img),'char') == 1 ) img = imread(img); end
    # if ( strcmp(class(img),'uint8') == 1 ) img = double(img)/255; end


    params.salmapmaxsize=round(max(img.shape)/8)
    

    return gbvs.out_gbvs(img,params)



# im=cv2.imread('51622.jpg')
# ittikochmap(im)
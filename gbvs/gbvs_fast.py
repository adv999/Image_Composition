
import makeGBVSParams
import gbvs
import cv2

# Use this instead of gbvs() if you want slightly less predictive maps
# computed in a fraction of the time.


def gbvs_Fast(im):
    params=makeGBVSParams.get_parameters()

    params.channels='DO'

    params.gaborangles=[0,90]

    params.levels=3

    params.verbose=0

    params.tol=0.003

    params.salmapmaxsize=24

    return gbvs.out_gbvs(im,params,0)

# im=cv2.imread("newpic.png")
# print(gbvs_Fast(im))

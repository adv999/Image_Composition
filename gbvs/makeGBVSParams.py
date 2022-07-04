
class Params:

    # General
    salmapmaxsize=0

    verbose=0

    verboseout=' '

    saveInputImage=0

    blurfrac=0 

    channels=0

    # Feature Channel Parameters
    colorWeight = 1     

    intensityWeight = 1  

    orientationWeight = 1

    contrastWeight = 1

    flickerWeight = 1

    motionWeight = 1

    dklcolorWeight = 1

    gaborangles=[]   

    contrastwidth=0.1

    flickerNewFrameWt=1

    motionAngles=[]

    #GBVS Parameters

    unCenterBias = 0          

    levels = []        

    multilevels = [];     

    sigma_frac_act = 0.15;      
    sigma_frac_norm = 0.06;     
    num_norm_iters = 1;         

    tol = .0001;         
                                    
    cyclic_type = 2;    

    #Parameters to use Itti/Koch or Simpler Saliency Algorithm

    useIttiKochInsteadOfGBVS = 0   
    activationType=1   

    normalizeType=1     

    normalizeTopChannelMaps=0   

    ittiCenterLevels=[]  
    ittiDeltaLevels=[]       
    ittiblurfrac=0.0       


def get_parameters():
    p=Params()

    #General

    p.salmapmaxsize=32      #size of output saliency maps
                            #dont set it too high
    
    p.verbose=0             #turn status messages on(1) / off(0)

    p.verboseout='screen'   #='screen' to echo messages on screen
                            #= = 'myfile.txt' to echo messages to file  

    p.saveInputImage=0      #save input image in output struct

    p.blurfrac=0.02         # final blur to apply to master saliency map

    #Feature Channel Parameters

    p.channels='DIO'
    # feature channels to use encoded as a string
    # C - Color
    # I - Intensity
    # O - Orientation
    # R - Contrast 
    # F - Flicker 
    # M - Motion 
    # D - DKL Color(Derrington Krauskpof Lennie) much better than C Channel 

    p.colorWeight = 1      # weights of feature channels (do not need to sum to 1). 
    p.intensityWeight = 1             
    p.orientationWeight = 1
    p.contrastWeight = 1
    p.flickerWeight = 1
    p.motionWeight = 1
    p.dklcolorWeight = 1

    p.gaborangles=[0,45,90,135]   #angles of gabor filters

    p.contrastwidth=0.1

    p.flickerNewFrameWt=1

    p.motionAngles=[0,45,90,135]


    
    #GBVS Parameters

    p.unCenterBias = 0          
    #  % turned off (0) by default. Attempts to undo some emergent
    #  % center bias in GBVS (by pointwise-multiplying final saliency map by 
    #  % an inverse-bias map).

    p.levels = [2, 3, 4]        
    #  % resolution of feature maps relative to original image (in 2^-(n-1) fractions)
    #  % (default [ 2 3 4]) .. maximum level 9 is allowed
    #  % these feature map levels will be used
    #  % if graph-based activation is used.
    #  % otherwise, the ittiCenter/Delta levels
    #  % are (see below)
    #  % minimum value allowed  = 2
    #  % maximum value allowed  = 9

    p.multilevels = [];     # [1 2] corresponds to 2 additional node lattices ,
                            # ... one at half and one at quarter size
                            # use [] for single-resolution version of algorithm.

    p.sigma_frac_act = 0.15;      # sigma parameter in activation step of GBVS (as a fraction of image width) - default .15
    p.sigma_frac_norm = 0.06;     # sigma parameter in normalizaiton step of GBVS (as a fraction of image width) - default .06
    p.num_norm_iters = 1;         # number of normalization iterations in GBVS - default 1

    p.tol = .0001;          # tol controls a stopping rule on the computation of the equilibrium distribution (principal eigenvector)
                            # the higher it is, the faster the algorithm runs, but the more approximate it becomes.
                            # it is used by algsrc/principalEigenvectorRaw.m - default .0001
                                    

    p.cyclic_type = 2;      # this should *not* be changed (non-cyclic boundary rules)

    
    
    #Parameters to use Itti/Koch or Simpler Saliency Algorithm

    p.useIttiKochInsteadOfGBVS = 0   #use value 0 for gbvs 
                                    # use value 1 for ittloch

    p.activationType=1    #use 1 for graph based activation
                          #use 2 for center surround activation
                          # type 2 only if useittikoch=1

    p.normalizeType=1     #1 = simplest & fastest. raises map values to a power before adding them together (default)
                          #2 = graph-based normalization scheme (no longer recommended)
                          #3 = normalization by (M-m)^2, where M = global maxima
                          # type 3 used if useittikoch=1                  

    p.normalizeTopChannelMaps=0   
    #this specifies whether to normalise the top-level feature map 
    #0 = dont do it
    #1 = do it

    p.ittiCenterLevels=[2,3]    #the c scale for center maps

    p.ittiDeltaLevels=[2]       #the 'delta' in s=c+delta levels for 'surround' scales

    p.ittiblurfrac=0.03        #apply final blur to master saliency map
    
    return p


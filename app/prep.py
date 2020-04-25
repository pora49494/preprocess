import sys
sys.path.insert(1, 'module')

from data import Data
from module.thres import find_thres
from module.lifespan import find_lifespan
# from module.coherent import find_coherent

if __name__ == "__main__" :
    task = sys.argv[1]
    Y = int(sys.argv[2])
    M = int(sys.argv[3])
    
    if task == 'thres' :
        find_thres( Data(Y, M, npts=True) )
    elif task == 'lifespan' :
        find_lifespan( Data(Y, M, npts=True) )
    # elif task == 'coherent' :
    #     find_coherent( data )
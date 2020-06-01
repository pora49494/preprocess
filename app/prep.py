import sys

from data import Data
from module.thres import find_thres
from module.lifespan import find_lifespan
from module.coherent import find_coherent
from module.proof import find_proof 
from module.source import find_source 
from module.peers import find_peers

if __name__ == "__main__" :
    task = sys.argv[1]
    Y = int(sys.argv[2])
    M = int(sys.argv[3])
    
    if task == 'thres' :
        find_thres( Data(Y, M, npts=True) )
    elif task == 'lifespan' :
        find_lifespan( Data(Y, M, npts=True) )
    elif task == 'coherent' :
        find_coherent( Data(Y, M, record=True, proof=True) )
    elif task == 'proof' :
        find_proof( Data(Y, M, npts=True) )
    elif task == 'source' :
        find_source( Data(Y, M, record=True) )
    elif task =='max-peer' :
        find_peers(Data(Y, M, npts=True))

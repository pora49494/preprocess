import sys

from data import Data
from module.thres import find_thres
from module.lifespan import find_lifespan
from module.coherent import find_coherent
from module.proof import find_proof 
from module.source import find_source 
from module.peers import find_peers
from module.corre import find_corre
from module.asn import find_asn
from module.bgp_update import find_bgp_update
from module.unique import find_unique

if __name__ == "__main__" :
    task = sys.argv[1]
    if len(sys.argv) == 4 :
        Y = int(sys.argv[2])
        M = int(sys.argv[3])
    elif len(sys.argv) == 3 :
        env = sys.argv[2] 
    
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
    elif task == 'max-peer' :
        find_peers(Data(Y, M, npts=True))
    elif task == 'corre' :
        find_corre(Data(Y,M,record=True))
    elif task == 'asn-info' :
        find_asn(env)
    elif task == 'bgp-update':
        find_bgp_update(env)
    elif task == 'unique':
        group_size = 3
        start_data = int(env)*group_size
        data = []
        for i in range(group_size):
            Y = (i+start_data)//12+2014
            M = 1+( (i+start_data) %12 )
            data.append( Data(Y, M, npts=True, proof=True) )
        find_unique( data, env)

        
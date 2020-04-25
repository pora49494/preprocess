from datetime import datetime
from data import Data
from collections import defaultdict
import sys

# def find_incoherent ( row, thres, processed_record ) :
    

if __name__ == "__main__" :
    Y = int(sys.argv[1])
    M = int(sys.argv[2])
    data = Data(Y, M)
    
    all_data = data.get_json_data()
    n = len(all_data)
    
    bgp_zombie = 0
    incoherent = 0
    incoherent_per_event = 0
    bgp_zombie_per_event = 0

    error = 0 

    for l in data.get_proof() :
        ts, prefix, proof, total_peers = l.strip().split("|")
        zombie = prefix+"|"+ts
    
        annouce = []
        asn_withdraw = set()

        bgp_zombie_per_event += 1
        count_incoherent = True

        for idx in range(n) :
            if zombie not in all_data[idx] :
                error += 1
                continue
            for peer in all_data[idx][zombie] :
                route = all_data[idx][zombie][peer]
                if route["status"] == "A" or route["status"] == "R" :
                    annouce.append( (peer, route["as_path"]) )
                    bgp_zombie += 1
                else :
                    asn_withdraw.add( str(route["peer_asn"]) )

        for peer, as_path in annouce :
            for asn in as_path.strip().split(" ") :
                if asn in asn_withdraw :
                    incoherent += 1
                    if count_incoherent :
                        incoherent_per_event += 1
                        count_incoherent = False
                    break

    print(bgp_zombie, incoherent, incoherent/bgp_zombie*100)   
    print(bgp_zombie_per_event, incoherent_per_event, incoherent_per_event/bgp_zombie_per_event*100)
    print(error)
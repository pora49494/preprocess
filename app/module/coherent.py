def find_coherent( data ) :
    
    all_data = data.get_data('record')
    n = len(all_data)
    
    bgp_zombie = 0
    incoherent = 0
    
    incoherent_proof = []

    for l in data.get_data('proof') :
        ts, prefix, proof, total_peers = l.strip().split("|")
        
        if int(total_peers) < 100 :
            continue

        zombie = prefix+"|"+ts

        annouce = []
        asn_withdraw = set()

        for p in range(n) :
            if zombie not in all_data[p] :
                continue
                
            for peer in all_data[p][zombie] :
                route = all_data[p][zombie][peer]
                if route["status"] == "A" or route["status"] == "R" :
                    annouce.append( (peer, route["as_path"], int(route['ts']) ) )
                    bgp_zombie += 1
                else :
                    asn_withdraw.add( str(route["peer_asn"]) )

        for peer, as_path, update_ts in annouce :
            incoherent_as_path = as_path.strip().split(" ")  
            incoherent_as_path_length = len(incoherent_as_path)
            is_incoherent = False

            for i in range(incoherent_as_path_length) :
                if incoherent_as_path[i] in asn_withdraw :
                    incoherent_as_path[i] = "!"+incoherent_as_path[i]
                    is_incoherent = True
        
            if is_incoherent :
                incoherent += 1
                incoherent_proof.append( f"{ts}|{prefix}|{peer}|{' '.join(incoherent_as_path)}|{update_ts}" )

    f = open(f"/result/{data.year}-{data.month}-incoherent-path.txt", "w") 
    f.write(f"{incoherent}/{bgp_zombie}\n")
    f.write("\n".join(incoherent_proof))
    f.close()
    
def find_coherent( data ) :
    
    all_data = data.get_data('record')
    n = len(all_data)
    
    bgp_zombie = 0
    incoherent = 0
    coherent = 0
    unknown = 0
    coherent_proof = []

    for l in data.get_data('proof') :
        ts, prefix, proof, total_peers = l.strip().split("|")
        
        if int(total_peers) < 100 :
            continue

        zombie = prefix+"|"+ts

        annouce = []
        asn_withdraw = set()
        asn_annouce = set()
        
        for p in range(n) :
            if zombie not in all_data[p] :
                continue
                
            for peer in all_data[p][zombie] :
                route = all_data[p][zombie][peer]
                if route["status"] == "A" or route["status"] == "R" :
                    annouce.append( (peer, route["as_path"], int(route['ts']) ) )
                    asn_annouce.add( str(route["peer_asn"]))
                    bgp_zombie += 1
                else :
                    asn_withdraw.add( str(route["peer_asn"]))

        for peer, as_path, update_ts in annouce :
            incoherent_as_path = as_path.strip().split(" ")  
            incoherent_as_path_length = len(incoherent_as_path)
            
            coherent_couter = 0
            incoherent_couter = 0
            
            for i in range(incoherent_as_path_length) :
                if incoherent_as_path[i] in asn_withdraw :
                    incoherent_couter += 1
                elif incoherent_as_path[i] in asn_annouce and i!=0 :
                    coherent_couter += 1
                    incoherent_as_path[i] = f"*{incoherent_as_path[i]}"
            
            if incoherent_couter > 0 :
                incoherent += 1
            elif incoherent_couter == 0 and coherent_couter > 0 :
                coherent += 1 
                coherent_proof.append( " ".join(incoherent_as_path) )
            else :
                unknown += 1
                
    f = open(f"/result/{data.year}-{data.month}-incoherent-path.txt", "w") 
    f.write(f"{incoherent}, {coherent}, {unknown}, {bgp_zombie}\n") 
    f.write("\n".join(coherent_proof))
    f.close()
    
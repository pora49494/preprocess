def find_unique(data_set, env):
    
    all_prefixes = set()
    zombie_prefixes = set()

    for data in data_set: 
        for l in data.get_data('proof') :
            _, prefix, _, _ = l.strip().split("|")
            prefix = prefix.strip()            
            all_prefixes.add( prefix )
            zombie_prefixes.add( prefix ) 
        
        for l in data.get_data('npts') : 
            temp = l.split(",")
            prefix = temp[0].strip()
            all_prefixes.add( prefix )
                

    v4_prefixes = 0
    v6_prefixes = 0
    v4_zombies = 0
    v6_zombies = 0
    
    for p in all_prefixes:
        if ":" in p :
            v6_prefixes += 1
        else :
            v4_prefixes += 1
    for p in zombie_prefixes:
        if ":" in p :
            v6_zombies += 1
        else :
            v4_zombies += 1
    
    f = open(f"/result/unique.txt", "a+")
    
    f.write(f"{env} {v4_zombies} {v4_prefixes} {v6_zombies} {v6_prefixes} {len(zombie_prefixes)} {len(all_prefixes)} \n")
    
    f.close()
    
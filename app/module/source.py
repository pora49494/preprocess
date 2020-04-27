from collections import defaultdict

def merge_record_by_zombie( all_records, rrc_records ) :
    for zombie in rrc_records :
        for peer in rrc_records[zombie] :
            if peer in all_records[zombie] :
                print(f"ALERT_DUPLICATED_PEER: {rrc_records[zombie][peer]} - {all_records[zombie][peer]}")
            all_records[zombie][peer] = rrc_records[zombie][peer]

def cal_zombie_score( z, n ) :
    if n == 0 and z == 0:
        return 0
    return (z-n)/(z+n)

def dfs(u, visited, check, adj) :
    if u is None :
        return
    if len(check) == 0 :
        return True
    
    for v in adj[u] :
        if v in check :
            check.remove(v)
        if v not in visited :
            visited.add(v)
            if dfs(v, visited, check, adj) :
                return True
    return False 

def find_source (data) : 
    all_records = defaultdict(dict)
    for rrc_record in data.get_data('record') :
        merge_record_by_zombie(all_records, rrc_record)
    
    zombie_source = []
    zombie_origin = defaultdict(int)
    for zombie in all_records :
        sources = find_source_helper( all_records[zombie] )
        for s in sources :
            zombie_origin[s] += 1 
        zombie_source.append( f"{zombie}|{' '.join(sources)}" )

    f = open(f"/result/{data.year}-{data.month}-zombie-source.txt", "w") 
    f.write("\n".join(zombie_source))
    f.close()

    f = open(f"/result/{data.year}-{data.month}-source-summary.txt", "w") 
    for asn in sorted(zombie_origin, key=lambda x: zombie_origin[x], reverse=True) :
        f.write( f"{asn} | {zombie_origin[asn]}\n" )
    f.close()

def find_source_helper ( record ) :
    edges_normal_path = defaultdict(int)
    edges_zombie_path = defaultdict(int)
    all_edges = set()
    adj = defaultdict(set)
    
    for peer in record :
        if 'as_path' not in record[peer] : continue
        as_path = record[peer]['as_path'].split(" ")
        v = as_path[0]
        edges = edges_normal_path if record[peer]['status'] == "W" else edges_zombie_path
            
        for u in as_path[1:] :
            if v == u :
                continue
            e = (u, v)
            edges[e] += 1
            all_edges.add(e)
            adj[u].add(v)
            v = u

    bad_peer = set()        
    for edge in all_edges :
        if cal_zombie_score( edges_zombie_path[edge], edges_normal_path[edge] ) > 0 :
            u, v = edge
            bad_peer.add(u) 

    source = []
    for u in bad_peer :
        check = bad_peer.copy()  
        visited = {u}
        check.remove(u)
        if dfs(u, visited, check, adj): 
            source.append(u)
    return source

from module.data import Data

def _find_stable (row) :
    n = len(row)
    prev = row[0]
    stable_for = 0
    stable = []
    st = None
    
    for i in range(1, n) : 
        if row[i] == prev :
            stable_for += 1
            if st is None :
                st = i
        else : 
            if stable_for >= 4 :
                stable.append( (st, i-1) )
            stable_for = 0
            st = None 
        prev = row[i]
    return stable

def _find_topology_depth (row, depth) :
    total_peers = max(row) 
    if total_peers < 100 :
        return 

    stable = _find_stable(row)
    if len(stable) == 0 :
        return 
    
    _, prev_end = stable[0]
    
    ok = total_peers*0.9
    for st, end in stable[1:] :
        if row[prev_end] >= ok :
            m = min(row[prev_end:st+1])
            if m != 0 :
                index = int( 100*m/total_peers )
                depth[index] += 1
        prev_end = end

def find_thres( data ) :
    depth_v4 = [0]*101
    depth_v6 = [0]*101

    lines = data.get_data('npts')
    for line in lines : 
        temp = line.split(",")
        prefix = temp[0]
        row = list(map(int, temp[1:]))
        depth = depth_v6 if ":" in prefix else depth_v4
        _find_topology_depth(row, depth)

    f = open(f"/result/{data.year}-{data.month}-thres.txt", "w")
    
    f.write(" ".join(list(map(str, depth_v4))) + "\n")
    f.write(" ".join(list(map(str, depth_v6))) + "\n")  

    f.close()
    
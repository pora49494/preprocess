import datetime

def dt2ts(dt): 
    return int((dt - datetime.datetime(1970, 1, 1)).total_seconds())

def find_proof ( data ) :
    _thres = 0.5
    ts_zombies = 6
    lines = data.get_data('npts')
    
    evidence = []
    start_ts = dt2ts(datetime.datetime(data.year, data.month, 10) )
            
    for line in lines : 
        temp = line.split(",")
        prefix = temp[0]
        row = list(map(int, temp[1:]))
        total_peers = max(row)
        
        if total_peers < 100 :
            continue
        
        thres = int(_thres * total_peers)
        
        i = 0
        n = len(row)
        while i < n-1 :
            if row[i] >= thres :
                j = 1
                while i+j < n and j < ts_zombies+1 and row[i+j] != 0 and row[i+j] < thres :
                    j += 1
                if j == ts_zombies+1 : 
                    record_ts = start_ts+900*(i+ts_zombies)
                    proof = " ".join(map(str, row[i:i+j]))
                    evidence.append(f"{record_ts}|{prefix}|{proof}|{total_peers}") 
                i += j 
            else :
                i += 1
 
    f = open(f"/result/{data.year}-{data.month}-zombies.txt", "w")
    f.write("\n".join(evidence))
    f.close()
    
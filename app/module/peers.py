def find_peers (data) :

    max_peers4 = [0]*1000
    max_peers6 = [0]*1000
    
    lines = data.get_data('npts')

    for line in lines : 
        temp = line.split(",")
        prefix = temp[0]
        row = list(map(int, temp[1:]))

        total_peers = max(row)
        if ":" in prefix :
            max_peers6[total_peers] += 1
        else :
            max_peers4[total_peers] += 1

    f = open(f"/result/{data.year}-{data.month}-max-peers.txt", "w")
    f.write(" ".join( list(map(str, max_peers4)) ) + "\n" )
    f.write(" ".join( list(map(str, max_peers6)) ) + "\n" )
    f.close()

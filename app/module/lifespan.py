def find_lifespan (data) :

    v4 = [ [0]*970 for _ in range(2)]
    v6 = [ [0]*970 for _ in range(2)]
    sparse = [ [], [] ]

    lines = data.get_data('npts')

    for line in lines : 
        temp = line.split(",")
        prefix = temp[0]
        row = list(map(int, temp[1:]))

        total_peers = max(row)
        if total_peers < 100 :
            continue
        
        if ":" in prefix :
            lifespan = v6 
            zombies = sparse[1]
        else :
            lifespan = v4
            zombies = sparse[0]
        
        thres = int(total_peers*0.5)
        
        n = len(row)
        i = 1
        
        while i < n :
            if row[i-1] >= thres and row[i] != 0 and row[i] < thres :
                j = i+1
                while j < n and row[j] != 0 and row[j] < thres :
                    j += 1
                
                if j < n and j-i > 6:
                    if row[j] == 0 :
                        lifespan[0][j-i-6] += 1
                        z = "{},{:.02f},D".format(j-i-6, 100*(sum(row[i+6:j])/(j-i-6))/total_peers )
                        zombies.append(z)
                    elif row[j] >= thres :
                        lifespan[1][j-i-6] += 1     
                        z = "{},{:.02f},R".format(j-i-6, 100*(sum(row[i+6:j])/(j-i-6))/total_peers )
                        zombies.append(z)
                                    
                i = j
            else :
                i += 1
                
    f = open(f"/result/{data.year}-{data.month}-zombie-lifespan-v4-heal-death.txt", "w")
    f.write(" ".join( list(map(str, v4[0])) ) + "\n" )
    f.write(" ".join( list(map(str, v4[1])) ) + "\n" )
    f.write("|".join( sparse[0] ) + "\n" )
    f.close()     

    f = open(f"/result/{data.year}-{data.month}-zombie-lifespan-v6-heal-death.txt", "w")
    f.write(" ".join( list(map(str, v6[0])) ) + "\n" )
    f.write(" ".join( list(map(str, v6[1])) ) + "\n" )
    f.write("|".join( sparse[1] ) + "\n" )
    f.close() 
import requests
        
def find_as_path_length(env) :
    f = open(f'/archive/_env-prefix/record-{env}', 'r')
    result = open(f'/result/path-length-{env}.txt', "a+")
    
    for _prefix in f.readlines() :
        prefix = _prefix.strip()
        netmask, subnet = prefix.split('/')
        res = [prefix] 
        try :

            for month in range(10,13) :
                as_path_length = 0 
                counter = 0
                
                url = f"https://stat.ripe.net/data/bgplay/data.json?endtime=2019-{month}-20T00%3A00%3A00&resource={netmask}%2F{subnet}&starttime=2019-{month}-10T00%3A00%3A00&unix_timestamps=TRUE"
                
                data = requests.get( url )
                data = data.json()
                for event in data['data']['events'] :
                    if event['type'] != "A" :
                        continue
                    prev = -1
                    counter += 1
                    for asn in event['attrs']['path'] :
                        if asn == prev :
                            continue
                        prev = asn 
                        as_path_length += 1
                if counter == 0 :
                    res.append("-1")
                else :
                    res.append(str(as_path_length/counter))
                
            result.write (",".join(res) + "\n")
            result.flush()

        except Exception as e:
            error = open(f'/result/error.txt', 'a+')
            error.write(f"{_prefix} {str(e)}\n")
            error.close()

    f.close()
    result.close()

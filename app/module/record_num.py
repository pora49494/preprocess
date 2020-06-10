import requests
        
def find_record_num(env) :
    f = open(f'/archive/_env-prefix/record-{env}', 'r')
    result = open(f'/result/record-num-{env}.txt', "a+")
    
    for _prefix in f.readlines() :
        prefix = _prefix.strip()
        netmask, subnet = prefix.split('/')
        res = [prefix] 
        try :
            for month in range(10,13) :
                url = f"https://stat.ripe.net/data/bgplay/data.json?endtime=2019-{month}-20T00%3A00%3A00&resource={netmask}%2F{subnet}&starttime=2019-{month}-10T00%3A00%3A00&unix_timestamps=TRUE"
                
                data = requests.get( url )
                data = data.json()
                change_number = len(data['data']['events'])
                res.append(str(change_number))
                
            result.write (",".join(res) + "\n")
        
        except Exception as e:
            error = open(f'/result/error.txt', 'a+')
            error.write(f"{_prefix} {str(e)}\n")
            error.close()

    f.close()
    result.close()

import requests
        
def find_asn(env) :
    f = open(f'/archive/_env/{env}', 'r')
    
    for _asn in f.readlines() :
        try :
            asn = _asn.strip()
            url_prefix = f"https://stat.ripe.net/data/announced-prefixes/data.json?resource=AS{asn}"
            url_path = f"https://stat.ripe.net/data/as-path-length/data.json?resource=AS{asn}&sort_by=geo"
            
            data = requests.get( url_prefix )
            prefix_num = len(data.json()['data']['prefixes']) 

            data = requests.get( url_path )
            avg = t = 0
            for ele in data.json()['data']['stats'] :
                avg += float(ele['stripped']['avg'])
                t += 1
            
            length = avg/t
            result = open(f'/result/asn-info-{env}.txt', "a+")
            result.write( f"{asn} {prefix_num} {length}\n")
            result.close()

        except Exception as e:
            missing = open(f'/result/missing.txt', 'a+')
            missing.write(f"{asn} {str(e)}\n")
            missing.close()

    f.close()
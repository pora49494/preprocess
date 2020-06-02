import json 
from collections import defaultdict, Counter

def build_new_asn_data() :
    return {
        'zombie' : 0,
        'normal' : 0,
        'total_length': 0,
        'count': 0
    } 

def poll_prefix_asn(poll_for_asn, average_path, record) :
    if "as_path" not in record :
        return 
    
    _as_path = record['as_path'].split(" ")
    as_path = []
    prev = ""

    for asn in _as_path :
        if asn==prev : 
            continue
        as_path.append(asn)
        prev = asn 

    if len(as_path) == 0: return 
    if "," in asn[-1] : return 
    if asn[0] == "{" : asn = asn[1:-1]
    average_path[0] += len(as_path)
    average_path[1] += 1
    poll_for_asn.append(asn)

def find_corre(data) :
    asn_summary = defaultdict( lambda : defaultdict (lambda : build_new_asn_data() ))
 
    all_data = data.get_data('record')   
    for i in range(len(all_data)) :
        route_collector = all_data[i]
        
        for zombie in route_collector :
            peers_data = route_collector[zombie]
            
            poll = []
            average_path = [0,0]
            zombie_counting = 0
            normal_counting = 0

            for peer in peers_data :
                record = peers_data[peer] 
                poll_prefix_asn(poll, average_path, record)
                if record['status'] == 'W' : 
                    normal_counting += 1
                else :
                    zombie_counting += 1
                
            if len(poll) == 0 : continue
            asn = Counter(poll).most_common(1)[0][0]
            asn_summary[asn][zombie]['zombie'] += zombie_counting
            asn_summary[asn][zombie]['normal'] += normal_counting
            asn_summary[asn][zombie]['total_length'] += average_path[0]
            asn_summary[asn][zombie]['count'] += average_path[1]

    remove_asn = []
    for asn in asn_summary : 
        remove_zombie = []
        for zombie in asn_summary[asn] :
            z = asn_summary[asn][zombie]['zombie']
            n = asn_summary[asn][zombie]['normal']
            if z+n < 100 :
                remove_zombie.append(zombie)
        for zombie in remove_zombie :
            del asn_summary[asn][zombie]

        if len(asn_summary[asn]) == 0 :
            remove_asn.append(asn)

    for asn in remove_asn :
        del asn_summary[asn]

    with open(f'/result/asn-summary-{data.year}-{data.month}.json', 'w') as outfile:
        json.dump(asn_summary, outfile)
    
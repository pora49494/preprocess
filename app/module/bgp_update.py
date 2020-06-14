import requests

def process_events(events):
    record_number = len(events)
    avg_as_path = 0
    
    as_path_length = 0
    counter = 0 
    
    for event in events:
        if event['type'] != "A":
            continue
        
        prev = -1
        counter += 1
        for asn in event['attrs']['path'] :
            if asn == prev :
                continue
            prev = asn 
            as_path_length += 1
                    
    if counter != 0 : 
        avg_as_path = as_path_length/counter
    
    return record_number, avg_as_path

def requests_data(prefix, year, _month):
    try:
        netmask, subnet = prefix.split('/')
        
        month = "{:02d}".format(_month)
        url = f"https://stat.ripe.net/data/bgplay/data.json?endtime={year}-{month}-20T00%3A00%3A00&resource={netmask}%2F{subnet}&starttime={year}-{month}-10T00%3A00%3A00&unix_timestamps=TRUE"
        data = requests.get( url )
        data = data.json()
        events = data['data']['events']
        return events

    except Exception as e:
        error = open(f'/result/error.txt', 'a+')
        error.write(f"{prefix} {str(e)}\n")
        error.close()
        return None 

def write_record(env, res_record, res_as_path):
    result_record = open(f'/result/record-num-{env}.txt', "a+")
    result_as_path = open(f'/result/path-length-{env}.txt', "a+")

    result_record.write (",".join(res_record) + "\n")
    result_as_path.write (",".join(res_as_path) + "\n")
        
    result_record.close()
    result_as_path.close()

def find_bgp_update(env) :
    f = open(f'/archive/_env-prefix/env-{env}', 'r')
    
    for _prefix in f.readlines() :
        prefix = _prefix.strip()
        res_record = [prefix] 
        res_as_path = [prefix] 
        
        for year in range(2018, 2020):
            for month in range(1,13):
                events = requests_data(prefix, year, month)
                if not events:
                    res_as_path.append("0")
                    res_record.append("0")
                else :
                    record_number, avg_as_path = process_events(events)
                    res_record.append(str(record_number))
                    res_as_path.append(str(avg_as_path))

        write_record( env, res_record, res_as_path )

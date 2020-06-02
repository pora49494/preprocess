Preprocessr
---
Help analyzing BGP data


### Add new module
- under `app/module/` adds new functions
- in `app/prep.py` import function and add it to main

### Data.py
- this is used as the data interfaces.
- Initialize it with the require type of data
- access it by `get_data('file_type')`

### Result data format (Over 100 peers)
#### thres
```
i   : 0   1 ....  n ...  100
Ai  : A0 A1 .... An ... A100
```
- value `Ai` refers number of time we find `min(Np(ts))` after change = `i`
- 1st line: IPv4
- 2nd line: IPv6


#### lifespan
```
i   : 0   1 ....  n ...  960
Ai  : A0 A1 .... An ... A960
```
- value `Ai` refers number of time we find `min(Np(ts))` after change = `i` 
- `i`'s maximum  is equal to 960 because we only analyze 10 day of data with 15 minutes interval.
- 1st line: death case
- 2nd line: recovery case

```
delta(i), avg(Np(ts), {R,D}
```
- 3rd line: all found events distribution

#### Path coherent
```
first line  : #incoherent_path / #BGP zombies
lines after : zombie ts | prefix | peer IP | AS_PATH* | record ts

1389742200|2.92.173.0/24|187.16.218.21|52888 1251 20080 !6762 3216 3216 8402|1389715193
```
- ASN in AS_PATH that is not coherent is shown by !ASN

#### Proof 
```
ts | prefix | proof | total_peers
```
- proof refers to the Np(ts) starting from drop, and end at ts+ts_withdrawal


#### Max-peer 
We want to find the number of prefix with lower peer count, to find how many percentage it occupies the total data.
```
# TO-DO
```

#### Correlationship
- For knowing better the characteristic of zombie AS
```json
{
    asn: {
        zombie: {
            #zombie: int,
            #normal: int1
        },
    }, 
}
```

#### Rank 
- for finding the basic information of investigated AS
    - there are 2 files: `info` and `missing`
    - run using environment value

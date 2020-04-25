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
WIP
```
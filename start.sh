cat "./env" | \
while read CMD 
do 
    YEAR_ENV="${CMD:0:4}"
    MONTH_ENV="${CMD:5:7}"
    TOPIC_HEADER="${YEAR_ENV}_${MONTH_ENV}"
    if [ ! -d result/"${1}" ]; then 
        mkdir result/"${1}"
    fi
    
    docker run -d --rm \
        --name "${TOPIC_HEADER}_${1}" \
        -v "${PWD}"/archive/:/archive \
        -v "${PWD}"/app:/app  \
        -v "${PWD}"/result/"${1}":/result \
        python:3.6-alpine3.9-request \
        python3 /app/prep.py ${1} ${YEAR_ENV} ${MONTH_ENV}
    
    while :
    do
        if [[ $(docker ps -qf "name=_${1}" | wc -l) -lt 6 ]]; then 
             break
        fi
        sleep 30
    done

done 

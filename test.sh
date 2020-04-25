docker run -it --rm \
    --name "test_find_thres" \
    -v "${PWD}"/archive/:/archive \
    -v "${PWD}"/app:/app  \
    -v "${PWD}"/result/test:/result \
    --workdir="/app/" \
    --entrypoint="/bin/sh" \
    python:3.6-alpine3.9

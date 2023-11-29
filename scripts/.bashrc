export XDG_CACHE_HOME=/data/.cache

function wait_port_available() {
    local port="$1"
    while true; do
        if nc -z localhost $port; then
            echo "$port start"
            break
        fi
        sleep 5
    done
    sleep 1
}


function is_gpu_available() {
    : ${memory_threshold:=2000}
    local index="$1"
    local memory_used=$(nvidia-smi --query-gpu=memory.used --id="$index" --format=csv,noheader,nounits)
    [ "$memory_used" -lt "$memory_threshold" ]
}

function find_gpu_available() {
    for gpu in 0 1 2 3 4 5 6 7; do
        if is_gpu_available "$gpu"; then
            echo "$gpu"
            break
        fi
    done
}

export -f wait_port_available
export -f is_gpu_available
export -f find_gpu_available

export OUT_ROOT=/data/outs
export DATA_ROOT=/data/dataset
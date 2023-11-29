source $LZY_HOME/environ.sh

function excute_tmux2() {
    local tasks=("$@")
    local i=0
    while ((i < ${#tasks[@]})); do
        gpu=$(find_gpu_available)
        if [ -n "$gpu" ]; then
            echo "Selected GPU: $gpu"
            echo "start Task: ${tasks[$i]} $gpu"
            
            tmux new -d -s "t-$i" "source $LZY_HOME/environ.sh;CUDA_VISIBLE_DEVICES=$gpu ${tasks[$i]}"
            sleep 200 # load model
            i=$((i + 1))
        else
            sleep 10
        fi
    done
}

function excute_tmux() {
    local tasks=("$@")
    local gpu=0
    local task_id=0
    local total_tasks=${#tasks[@]}
    # set -x # for debug
    while ((task_id < total_tasks)); do
        echo "$gpu"
        echo $(is_gpu_available "$gpu")
        if is_gpu_available "$gpu"; then
            
            if ! tmux has-session -t "tmux-$gpu" 2>/dev/null; then
                task=${tasks[$task_id]}
                echo "start: tmux-$gpu $task"
                
                # bash调bash的echo/print不会直接打出来，需要重定向
                # 使用双引号把字符串括起来，可以避免空格导致单词拆分

                tmux new-session -d -s tmux-$gpu bash -c \
                "source $LZY_HOME/environ.sh; \
                export CUDA_VISIBLE_DEVICES=$gpu; \
                source $LZY_HOME/time_wrapper.sh \"$task\";"
                
                ((task_id++))
            fi
        fi
        gpu=$(( (gpu+1) % 8 ))
        sleep 2
    done
}

function excute_debug() {
    local tasks=("$@")
    local gpu=0
    local task_id=0
    local total_tasks=${#tasks[@]}
    # set -x # for debug
    while ((task_id < total_tasks)); do
        gpu=$(( (gpu+1) % 8 ))
        if is_gpu_available "$gpu"; then
            if ! tmux has-session -t "tmux-$gpu" 2>/dev/null; then
                echo "start: CUDA_VISIBLE_DEVICES=$gpu ${tasks[$task_id]}"
                ((task_id++))
            fi
        fi
        sleep 2
    done
}

function excute_bash() {
    local tasks=("$@")
    local i=0
    set -x # for debug
    while ((i < ${#tasks[@]})); do
        task=${tasks[$i]}
        echo "start: $i $task"

        # need to set CUDA_VISIBLE_DEVICES in task
        bash -c \
        "source $LZY_HOME/environ.sh; \
        source $LZY_HOME/time_wrapper.sh \"$task\";"

        i=$((i + 1))
        sleep 1
    done
}

function echo_tasks() {
    local i=0
    for task in "$@"; do
        echo "$i: $task"
        ((i++))
    done
    echo ">>> total $i tasks"
}


function run_tasks_parallel(){
    local create_task="$1"
    tasks=()
    # Call the provided function
    "$create_task"
    echo_tasks "${tasks[@]}"
    sleep 5
    excute_tmux "${tasks[@]}"
}

function run_tasks_sequential(){
    local create_task="$1"
    tasks=()
    # Call the provided function
    "$create_task"
    echo_tasks "${tasks[@]}"
    sleep 5
    excute_bash "${tasks[@]}"
}

function run_tasks_debug(){
    local create_task="$1"
    tasks=()
    # Call the provided function
    "$create_task"
    echo_tasks "${tasks[@]}"
    sleep 5
    excute_debug "${tasks[@]}"
}



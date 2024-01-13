# huggingface-cli repo create qwen-bbq -y
# huggingface-cli repo create qwen-cnn -y
# huggingface-cli repo create qwen-guanaco -y
# 在setting里边手动make private
# huggingface-cli upload lu-vae/qwen-dolly /home/lzy/axolotl/src/outs/qwen-dolly/adapter_config.json adapter_config.json
# huggingface-cli upload lu-vae/qwen-dolly /home/lzy/axolotl/src/outs/qwen-dolly/adapter_model.bin adapter_model.bin
# huggingface-cli upload lu-vae/qwen-cnn /home/lzy/axolotl/src/outs/qwen-cnn-6w-32bit/adapter_config.json adapter_config.json
# huggingface-cli upload lu-vae/qwen-cnn /home/lzy/axolotl/src/outs/qwen-cnn-6w-32bit/adapter_model.bin adapter_model.bin
# huggingface-cli upload lu-vae/qwen-guanaco /home/lzy/axolotl/src/outs/qwen-guanaco/adapter_config.json adapter_config.json
# huggingface-cli upload lu-vae/qwen-guanaco /home/lzy/axolotl/src/outs/qwen-guanaco/adapter_model.bin adapter_model.bin
# huggingface-cli download
huggingface-cli upload --private lu-vae/qwen-sharegpt4 $OUT_ROOT/qwen-sharegpt4/adapter_model.bin adapter_model.bin 
huggingface-cli upload --private lu-vae/qwen-sharegpt4 $OUT_ROOT/qwen-sharegpt4/adapter_config.json adapter_config.json 

huggingface-cli upload --private lu-vae/qwen-chat2 /home/lzy/axolotl/src/outs/chat/three_class/qwen-chat4/adapter_model.bin adapter_model.bin
#  huggingface-cli repo create Miracle-Conversation --type dataset -y
#  huggingface-cli upload --repo-type dataset lu-vae/Miracle-Conversation dialogue_a.raw.jsonl


huggingface-cli repo create --private cciip-gpt-dataset --type dataset -y

huggingface-cli upload --repo-type dataset lu-vae/cciip-gpt-dataset cciip-gpt

huggingface-cli upload --private lu-vae/qwen-v1219 $OUT_ROOT/qwen-v1219


dir=/data/outs/qwen-v1226
huggingface-cli upload --private lu-vae/qwen-v1226 $dir/pytorch_model.bin pytorch_model.bin 
huggingface-cli upload --private lu-vae/qwen-v1226 $dir/config.json config.json
huggingface-cli upload --private lu-vae/qwen-v1226 $dir/generation_config.json generation_config.json
huggingface-cli upload --private lu-vae/qwen-v1226 $dir/qwen.tiktoken qwen.tiktoken
huggingface-cli upload --private lu-vae/qwen-v1226 $dir/special_tokens_map.json special_tokens_map.json
huggingface-cli upload --private lu-vae/qwen-v1226 $dir/tokenizer_config.json tokenizer_config.json
huggingface-cli upload --private lu-vae/qwen-v1226 $dir/checkpoint-3105 checkpoint-3105
huggingface-cli upload --private lu-vae/qwen-v1226 $dir/checkpoint-4657 checkpoint-4657
huggingface-cli upload --private lu-vae/qwen-v1226 $dir/checkpoint-6210 checkpoint-6210
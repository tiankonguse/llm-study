#  climb wall

```
conda create -n climb-wall python=3.11
conda activate climb-wall 

pip install -r requirements.txt

# 模型: --checkpoint /Users/tiankonguse-m3/project/github/segment-anything/checkpoint/sam_vit_h_4b8939.pth --model_type vit_h
# GPU/CPU: --device cpu
python app.py
```
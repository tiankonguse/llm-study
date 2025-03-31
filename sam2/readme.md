# sam2

```
conda create -n sam2 python=3.12
conda activate sam2 

# requires python>=3.10, torch>=2.5.1 torchvision>=0.20.1
pip install -e .
pip install opencv-python matplotlib


cd checkpoints
./download_ckpts.sh
cd ..
```
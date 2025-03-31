# segment-anything


## 思路


分为三个模块：预处理模块、定线模块、查线模块

预处理模块：识别图片，得到识别的所有图片的 mask(含坐标与颜色)，储存在一个json文件中，称为墙信息(图片、岩点、宽高、创建日期、岩馆、墙)。 
    mask 是一个图片
定线模块：加载图片与json，按顺序选择物体。支持动态删除、调序、插入等，设置难度级别、定线人的名称、线路名称、日期等，储存在json文件中，称为线路信息。
查线模块：加载墙信息和线路信息，支持查看所有岩点、爬线模式（仅仅显示5个点）



## segment-anything-webui 点击与box可用

Yet another SAM webui + CLIP
https://github.com/Kingfish404/segment-anything-webui

依赖 sam: https://github.com/facebookresearch/segment-anything
依赖 clip: https://github.com/openai/CLIP

### 总结

点击和box 使用都没问题，还可以得到 Segment 数据。  


### 安装


```bash
git clone https://github.com/Kingfish404/segment-anything-webui.git

cd segment-anything-webui
# python=3.12 存在冲突，需要使用低版本 3.11
conda create -n segment-anything-webui python=3.11
conda activate segment-anything-webui
conda install python=3.11 # 动态切换版本


pip install opencv-python 
pip install pycocotools
conda install matplotlib
conda install onnxruntime
conda install onnx
pip install git+https://github.com/facebookresearch/segment-anything.git

mkdir model
# download the model to `model/`
wget https://dl.fbaipublicfiles.com/segment_anything/sam_vit_b_01ec64.pth -O model/sam_vit_b_01ec64.pth
# https://dl.fbaipublicfiles.com/segment_anything/sam_vit_l_0b3195.pth
# https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth

# e.g. for CLIP
pip install torch
conda install torchvision
conda install ftfy
conda install regex
conda install tqdm
# pip install clip
# pip install git+https://github.com/openai/CLIP.git


# python server as backend
conda install numpy
conda install 'uvicorn[standard]' 
conda install fastapi
conda install pydantic
conda install python-multipart
conda install Pillow
conda install click
# or 
# cd scripts
# pip install -r requirements.txt

# webui frontend
npm i

python scripts/server.py   # webui backend
npm run dev                 # interactive webui frontend

#    ▲ Next.js 14.1.3
#    - Local:        http://localhost:3000

```

### POST /api/embedding

调用 `predictor.get_image_embedding()` 函数。  


### 数据格式

```
{
    "masks": [
        {
            "segmentation": "...",
            "stability_score": 0.9672289490699768,
            "bbox": [
                0,
                0,
                0,
                0
            ],
            "area": 2475
        }
    ],
    "points": [
        {
            "x": 6.842105263157895,
            "y": 442.10526315789474,
            "label": 1
        }
    ]
}
```


### 错误

Q: AssertionError: set_torch_image input must be BCHW with long side 1024.

A: 图片格式不对，需要修改代码，转换为 RGB 格式。

```
image_data = Image.open(io.BytesIO(file))
# image_array = np.array(image_data)  # 注释掉这行代码，增加 转换为 RGB 的代码
image_array = np.array(image_data.convert("RGB"))
```

## segment_anything_webui 不可用

https://github.com/5663015/segment_anything_webui

### 总结

手动修复安装依赖问题后，服务可以跑起来，但是运行错误。


### 依赖

```
gradio==3.41.2
numpy
opencv_python
Pillow
segment_anything
transformers
torch
torchvision
```



### 安装

```
git clone https://github.com/5663015/segment_anything_webui.git

cd segment_anything_webui
# python=3.12 存在冲突，需要使用低版本 3.11
conda create -n segment_anything_webui python=3.11
conda activate segment_anything_webui
conda install python=3.11 # 动态切换版本

pip install git+https://github.com/facebookresearch/segment-anything.git
pip install -r requirements.txt
```


### 错误 

Q: ERROR: No matching distribution found for numpy==1.21.5
A: 删除第三极版本依赖，例如 numpy==1.21

```
ERROR: Could not find a version that satisfies the requirement numpy==1.21.5 (from versions: 1.3.0, 1.4.1, 1.5.0, 1.5.1, 1.6.0, 1.6.1, 1.6.2, 1.7.0, 1.7.1, 1.7.2, 1.8.0, 1.8.1, 1.8.2, 1.9.0, 1.9.1, 1.9.2, 1.9.3, 1.10.0.post2, 1.10.1, 1.10.2, 1.10.4, 1.11.0, 1.11.1, 1.11.2, 1.11.3, 1.12.0, 1.12.1, 1.13.0, 1.13.1, 1.13.3, 1.14.0, 1.14.1, 1.14.2, 1.14.3, 1.14.4, 1.14.5, 1.14.6, 1.15.0, 1.15.1, 1.15.2, 1.15.3, 1.15.4, 1.16.0, 1.16.1, 1.16.2, 1.16.3, 1.16.4, 1.16.5, 1.16.6, 1.17.0, 1.17.1, 1.17.2, 1.17.3, 1.17.4, 1.17.5, 1.18.0, 1.18.1, 1.18.2, 1.18.3, 1.18.4, 1.18.5, 1.19.0, 1.19.1, 1.19.2, 1.19.3, 1.19.4, 1.19.5, 1.20.0, 1.20.1, 1.20.2, 1.20.3, 1.21.0, 1.21.1, 1.22.0, 1.22.1, 1.22.2, 1.22.3, 1.22.4, 1.23.0, 1.23.1, 1.23.2, 1.23.3, 1.23.4, 1.23.5, 1.24.0, 1.24.1, 1.24.2, 1.24.3, 1.24.4, 1.25.0, 1.25.1, 1.25.2, 1.26.0, 1.26.1, 1.26.2, 1.26.3, 1.26.4, 2.0.0, 2.0.1, 2.0.2, 2.1.0rc1, 2.1.0, 2.1.1, 2.1.2, 2.1.3, 2.2.0rc1, 2.2.0, 2.2.1, 2.2.2, 2.2.3, 2.2.4)
```

Q: ERROR: No matching distribution found for torch==1.13.1
A: 查找有的版本，进行替换，例如 torch==2.0


```
ERROR: Could not find a version that satisfies the requirement torch==1.13.1 (from versions: 2.0.0, 2.0.1, 2.1.0, 2.1.1, 2.1.2, 2.2.0, 2.2.1, 2.2.2, 2.3.0, 2.3.1, 2.4.0, 2.4.1, 2.5.0, 2.5.1, 2.6.0)
ERROR: No matching distribution found for torch==1.13.1
```



## ai_webui 自动识别所有物体

https://github.com/jasonaidm/ai_webui


### 总结

Segment Everything 使用的 fastsam 模型，做的比较好，可以识别所有物体。


### 安装


```bash
git clone https://github.com/jasonaidm/ai_webui.git
cd ai_webui

conda create -n aiwebui python=3.11
conda activate aiwebui

apt install ffmpeg -y 
pip install -r requirements.txt
```



## creeponsky-SAM-webui 只有点击识别

https://github.com/creeponsky/SAM-webui


### 总结


可以点击识别，也可以得到 mask。



### 安装

```
conda create -n sam-webui python=3.11
conda activate sam-webui

```

## derekray311511-SAM-webui 点击/box/自动识别都不错

颜色是随机的。

https://github.com/derekray311511/SAM-webui.git


```
conda create -n derekray311511-SAM-webui python=3.11
conda activate derekray311511-SAM-webui

pip install -e .
pip install opencv-python pycocotools matplotlib onnxruntime onnx flask flask_cors
pip install matplotlib  torch torchvision pycocotools onnx black isort

python app.py --model_type vit_h --checkpoint /Users/tiankonguse-m3/project/github/segment-anything/checkpoint/sam_vit_h_4b8939.pth --device cpu
vit_h /Users/tiankonguse-m3/project/github//segment-anything/checkpoint/sam_vit_h_4b8939.pth
vit_l /Users/tiankonguse-m3/project/github//segment-anything/demo/model/sam_vit_l_0b3195.pth
vit_b /Users/tiankonguse-m3/project/github//segment-anything/demo/model/sam_vit_b_01ec64.pth
```


## SegDrawer - 点击/box/一键全可用


https://github.com/lujiazho/SegDrawer.git


### 总结

```
conda create -n SegDrawer python=3.11
conda activate SegDrawer

pip install numpy
pip install matplotlib
pip install opencv-python pycocotools matplotlib onnxruntime onnx flask flask_cors
pip install matplotlib  torch torchvision pycocotools onnx black isort

python server.py
```

## segment-anything-webdemo - 点击demo


```
conda create -n segment-anything-webdemo python=3.11
conda activate segment-anything-webdemo

pip install -r requirements.txt

pip install matplotlib
pip install opencv-python pycocotools matplotlib onnxruntime onnx flask flask_cors
pip install matplotlib  torch torchvision pycocotools onnx black isort

python server.py
```
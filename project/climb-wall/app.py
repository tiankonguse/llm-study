from flask import Flask,render_template,request, jsonify
from flask_cors import CORS
import os
import cv2
import numpy as np
import torch
import torchvision
from collections import deque
import base64


from segment_anything import sam_model_registry, SamPredictor, SamAutomaticMaskGenerator

from arg_parse import parser

print("PyTorch version:", torch.__version__)
print("Torchvision version:", torchvision.__version__)
print("CUDA is available:", torch.cuda.is_available())

class Mode:
    def __init__(self) -> None:
        self.IAMGE = 1
        self.MASKS = 2
        self.CLEAR = 3
        self.P_POINT = 4
        self.N_POINT = 5
        self.BOXES = "box"
        self.INFERENCE = "inference"
        self.UNDO = 8
        self.COLOR_MASKS = 9

MODE = Mode()

class Web_App:
    def __init__(self, args):
        self.args = args
        self.app = Flask(__name__)
        CORS(self.app)
        self.loadModel()
        
        # Store the image globally on the server
        self.origin_image_rgba = None
        self.processed_img_rgba = None
        self.masked_img = None
        self.colorMasks = None
        self.imgSize = None
        self.imgIsSet = False           # To run self.predictor.set_image() or not

        self.mode = "box"           # p_point / n_point / box
        self.curr_view = "image"
        self.queue = deque(maxlen=1000)  # For undo list
        self.prev_inputs = deque(maxlen=500)

        self.points = []
        self.points_label = []
        self.boxes = []
        self.masks = []
        
        home_dir = os.path.expanduser("~")
        self.save_path = os.path.join(home_dir, "Downloads")
        
        self.route()
        
        
    def loadModel(self):
        # load model
        print("Loading model...", end="")
        device = args.device
        print(f"using {device}...", end="")
        sam = sam_model_registry[args.model_type](checkpoint=args.checkpoint)
        sam.to(device=device)

        self.predictor = SamPredictor(sam)
        print("Done")
    
    def route(self):
        self.app.route('/', methods=['GET'])(self.home)
        self.app.route('/upload_image', methods=['POST'])(self.upload_image)
        self.app.route('/button_click', methods=['POST'])(self.button_click)
        self.app.route('/box_receive', methods=['POST'])(self.box_receive)
    
    def home(self):
        return render_template('index.html', default_save_path=self.save_path)

    def upload_image(self):
        if 'image' not in request.files:
            return jsonify({'error': 'No image in the request'}), 400
        
        file = request.files['image']
        
        # file.read() 读取上传的文件内容，返回一个字节流
        # np.frombuffer 使用NumPy将字节流转换为uint8类型的数组
        # cv2.imdecode 使用OpenCV解码图像数据
        # cv2.IMREAD_COLOR标志表示以彩色模式加载图像（3通道BGR格式）
        # image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_COLOR)
        image = cv2.imdecode(np.frombuffer(file.read(), np.uint8), cv2.IMREAD_UNCHANGED)
        
        print("image IMREAD_COLOR ", image.shape[-1])
        if image.shape[-1] == 3:  # 如果是RGB图像, 转换为RGBA
            image = cv2.cvtColor(image, cv2.COLOR_RGB2RGBA)
            print("image IMREAD_COLOR ", image.shape[-1])
        
        image_rgb = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)
        
        
        # Store the image globally
        self.sam_image_rgb = image_rgb # 用于 sam 查询物体，必须是 rgb 格式
        self.origin_image_rgba = image
        self.processed_img_rgba = image
        self.masked_img = np.zeros_like(image)
        self.colorMasks = np.zeros_like(image)
        self.imgSize = image.shape
        print("imgSize ", self.imgSize)
        print("sam_imageSize ",image_rgb.shape)
        
        # Reset inputs and masks and image ebedding
        self.imgIsSet = False
        self.reset_inputs()
        self.reset_masks()
        self.queue.clear()
        self.prev_inputs.clear()
        torch.cuda.empty_cache()
        
        self.init_predictor()

        return "Uploaded image, successfully initialized"
    
    def init_predictor(self):
        # Image is set ?
        if self.imgIsSet == False:
            self.predictor.set_image(self.sam_image_rgb, image_format="RGB")
            self.imgIsSet = True
            print("Image set!")
        
    def button_click(self):
        if self.processed_img_rgba is None:
            return jsonify({'error': 'No image available for processing'}), 400

        data = request.get_json()
        button_id = data['button_id']
        image_type = data['image_type']
        print(f"Button {button_id} clicked， image_type {image_type}")

        # Info
        info = {
            'event': 'button_click',
            'data': button_id,
            'image_type': image_type,
        }

        # Process and return the image
        return self.process_image(self.processed_img_rgba, info)
    
    
    def box_receive(self):
        if self.processed_img_rgba is None:
            return jsonify({'error': 'No image available for processing'}), 400

        data = request.get_json()
        self.boxes.append(np.array([
            data['x1'], data['y1'],
            data['x2'], data['y2']
        ], dtype=np.float32))

        # Add command to queue list
        self.queue.append("box")

        return "server received boxes"
    
    def process_image(self, image, info):
        processed_image = image
        image_type = info["image_type"]
        
        if info['event'] == 'button_click':
            id = info['data']
            if (id == MODE.BOXES):
                self.mode = "box"
            elif (id == MODE.INFERENCE):
                print("INFERENCE")
                points = np.array(self.points)
                labels = np.array(self.points_label)
                boxes = np.array(self.boxes)
                print(f"Points shape {points.shape}", points)
                print(f"Labels shape {labels.shape}", labels)
                print(f"Boxes shape {boxes.shape}", boxes)
                prev_masks_len = len(self.masks)
                print(f"len masks {prev_masks_len}")
                processed_image, self.masked_img = self.inference(self.origin_image_rgba, points, labels, boxes)
                curr_masks_len = len(self.masks)
                self.get_colored_masks_image()
                self.processed_img_rgba = processed_image
                self.prev_inputs.append({
                    "points": self.points,
                    "labels": self.points_label,
                    "boxes": self.boxes
                })
                self.reset_inputs()
                self.queue.append(f"inference-{curr_masks_len - prev_masks_len}")
        
        if (image_type == "png"):
            _, buffer = cv2.imencode('.png', processed_image)
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            return jsonify({'image': img_base64, 'image_type': image_type})
        else:
            _, buffer = cv2.imencode('.jpg', processed_image)
            img_base64 = base64.b64encode(buffer).decode('utf-8')
            return jsonify({'image': img_base64, 'image_type': image_type})
    
    
    def inference(self, image, points, labels, boxes) -> np.ndarray:
        points_len, lables_len, boxes_len = len(points), len(labels), len(boxes)
        
        print(f"points_len {points_len}; lables_len {lables_len}; boxes_len {boxes_len}; ")
        if (len(points) == len(labels) == 0):
            points = labels = None
        if (len(boxes) == 0):
            boxes = None
        
        self.init_predictor()
        
        if ((boxes_len == 1) or (points_len > 0 and boxes_len <= 1)):
            masks, scores, logits = self.predictor.predict(
                point_coords=points,
                point_labels=labels,
                box=boxes,
                multimask_output=True,
            )
            print(f"predict len(masks)={len(masks)}  len(scores)={len(scores)}  len(logits)={len(logits)} ")
            print(f"masks shape: {masks.shape}")  # 打印masks的维度 (3, 2013, 1125)
            print(f"scores shape: {scores.shape}")  # 打印scores的维度 (3,)
            print(f"logits shape: {logits.shape}")  # 打印logits的维度 (3, 256, 256)
            max_idx = np.argmax(scores)
            self.masks.append({
                "mask": masks[max_idx], # mask 不关心颜色，所以是一个W*H 二维矩阵，大小等于图片输出的大小
                "opt": "positive"
            })
        # Multiple Object
        elif (boxes_len > 1):
            boxes = torch.tensor(boxes, device=self.predictor.device)
            transformed_boxes = self.predictor.transform.apply_boxes_torch(boxes, image.shape[:2])
            masks, scores, logits = self.predictor.predict_torch(
                point_coords=None,
                point_labels=None,
                boxes=transformed_boxes,
                multimask_output=False,
            )
            masks = masks.detach().cpu().numpy()
            scores = scores.detach().cpu().numpy()
            max_idxs = np.argmax(scores, axis=1)
            print(f"output mask shape: {masks.shape}")  # (batch_size) x (num_predicted_masks_per_input) x H x W
            for i in range(masks.shape[0]):
                self.masks.append({
                    "mask": masks[i][max_idxs[i]],
                    "opt": "positive"
                })
        # Update masks image to show
        overlayImage, maskedImage = self.updateMaskImg(self.origin_image_rgba, self.masks)
        # overlayImage, maskedImage = self.updateMaskImg(overlayImage, maskedImage, [self.brushMask])

        return overlayImage, maskedImage


    def get_colored_masks_image(self):
        masks = self.masks
        # 创建一个与原始图像大小相同的黑色背景图像
        darkImg = np.zeros_like(self.origin_image_rgba)
        image = darkImg.copy()

        np.random.seed(0)
        if (len(masks) == 0):
            self.colorMasks = image
            return image
        for mask in masks:
            if mask['opt'] == "negative":
                image = self.clearMaskWithOriginImg(darkImg, image, mask['mask'])
            else:
                image = self.overlay_mask(image, mask['mask'], 1)

        self.colorMasks = image
        return image

    def updateMaskImg(self, image, masks):

        if (len(masks) == 0 or masks[0] is None):
            print(masks)
            return image, np.zeros_like(image)
        
        
        image = image * 1 # 创建新的对象
        image[:, :, 3] = image[:, :, 3] * 0.5 # 表示只操作RGBA图像的Alpha通道（第4个通道）
        image = image.astype(dtype=np.uint8) # 确保数据仍然是8位无符号整数格式
        # 创建一个与图像大小相同的空白mask
        union_mask = np.zeros_like(image)[:, :, 0]
        print(f"union_mask = {union_mask.shape}")
        np.random.seed(0)
        for i in range(len(masks)):
            image = self.overlay_mask(image, masks[i]['mask'], i)
            # union_mask = np.bitwise_or(union_mask, masks[i]['mask'])
            union_mask = np.bitwise_or(union_mask, masks[i]['mask'])
        
        # Cut out objects using union mask
        # 使用union_mask从原始图像中裁剪出目标区域
        # masked_image = self.origin_image_rgba * union_mask[:, :, np.newaxis]
        
        return image, union_mask


    # Function to overlay a mask on an image
    def overlay_mask(
        self, 
        image: np.ndarray, 
        mask: np.ndarray, 
        index: int, 
    ) -> np.ndarray:
        """ Draw mask on origin image

        parameters:
        image:  Origin image
        mask:   Mask that have same size as image
        color:  Mask's color in BGR
        alpha:  Transparent ratio from 0.0-1.0

        return:
        blended: masked image
        """
        # Blend the image and the mask using the alpha value
        # if random_color:
        #     color = np.random.random(3)
        # else:
        #     color = np.array([30/255, 144/255, 255/255])    # BGR
        # color = np.array([(0x5F)/255, (0x9E)/255, (0xE4)/255])    # BGR #5F9FE4
        # color = np.array([0x5F, 0x9E, 0xE4])    # BGR #5F9FE4  #E49E60
        # mask = mask.reshape(h, w, 1) * color.reshape(1, 1, -1)
        # mask = mask * 2
        # mask = mask.astype(dtype=np.uint8)
        # blended = cv2.add(image, mask)
        # blended = cv2.bitwise_or(image, mask)
        # 将匹配位置的透明度设置为 255（完全不透明）
        h, w = mask.shape[-2:]
        mask = mask.reshape(h, w, 1)
        self.IncreaseSaturationBrightness(image, mask, index)
        # self.AddNumText(image, mask, index)
        return image
    
    def IncreaseSaturationBrightness(self, image, mask, index):
        # Convert the image's RGB channels to HSV
        rgb = image[:, :, :3]
        hsv = cv2.cvtColor(rgb, cv2.COLOR_RGB2HSV)
        # Create a boolean mask for pixels where mask > 0
        mask_bool = mask[:, :, 0] > 0
        # Increase saturation and brightness in masked regions by a factor of 1.2
        hsv[mask_bool, 1] = np.clip(hsv[mask_bool, 1].astype(np.float32) * 1.2, 0, 255).astype(np.uint8)
        hsv[mask_bool, 2] = np.clip(hsv[mask_bool, 2].astype(np.float32) * 1.2, 0, 255).astype(np.uint8)
        # Convert back to RGB and update the image's RGB channels
        image[:, :, :3] = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
        # Set alpha to fully opaque in the masked areas
        image[:, :, 3] = np.where(mask[:, :, 0] > 0, 255, image[:, :, 3])
        
        # Convert the mask to a binary image for contour detection
        mask_uint8 = (mask[:, :, 0] * 255).astype(np.uint8)
        contours, _ = cv2.findContours(mask_uint8, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Highlight the boundaries of the mask using a bright magenta color
        cv2.drawContours(image, contours, -1, color=(255, 0, 255, 255), thickness=2)
    
    def AddNumText(self, image, mask, index):
        mask_uint8 = (mask[:, :, 0] * 255).astype(np.uint8)
        # Compute center of mass of the mask for placing the index text
        M = cv2.moments(mask_uint8)
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = w // 2, h // 2

        # Set text properties: odd index -> yellow, even index -> blue
        text = str(index)
        if index % 2 == 1:
            text_color = (0, 255, 255, 255)  # Yellow (BGR order with alpha)
        else:
            text_color = (255, 0, 0, 255)      # Blue (BGR order with alpha)
        border_color = (0, 0, 0, 255)          # Black border

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        thickness = 2

        # Draw border by drawing the text several times offset in different directions
        for dx in [-1, 1]:
            for dy in [-1, 1]:
                cv2.putText(image, text, (cX + dx, cY + dy), font, font_scale, border_color, thickness + 2, cv2.LINE_AA)

        # Draw the actual bold text
        cv2.putText(image, text, (cX, cY), font, font_scale, text_color, thickness, cv2.LINE_AA)
        return image
    
    
    def clearMaskWithOriginImg(self, originImage, image, mask):
        originImgPart = originImage * np.invert(mask)[:, :, np.newaxis]
        image = image * mask[:, :, np.newaxis]
        image = cv2.add(image, originImgPart)
        return image

    def reset_inputs(self):
        self.points = []
        self.points_label = []
        self.boxes = []
    
    def reset_masks(self):
        self.masks = []
        self.masked_img = np.zeros_like(self.origin_image_rgba)
        self.colorMasks = np.zeros_like(self.origin_image_rgba)
    
    def run(self, debug=True):
        self.app.run(debug=debug, port=8990)
        
if __name__ == '__main__':
    args = parser().parse_args()
    app = Web_App(args)
    app.run(debug=True)
# llm-study



## 文件格式

### .safetensors 文件

TensorFlow 2.x 中新增的文件格式，用于保存模型参数和优化器状态。
它采用的是 TensorFlow 的自定义序列化格式，不能直接用于其他框架。
可以使用 TensorFlow 的 tf.train.Checkpoint 类来加载和保存 .safetensors 文件。


### .ckpt 文件

TensorFlow 1.x 中用于保存模型参数和优化器状态的文件格式。
它采用的是 TensorFlow 的自定义序列化格式，不能直接用于其他框架。
可以使用 TensorFlow 的 tf.train.Saver 类来加载和保存 .ckpt 文件。
可以使用 TensorFlow 2.x 的 tf.compat.v1.train.Saver 类来加载和保存 .ckpt 文件。


### .gguf 文件

Google 的 GFST（Google Finite State Transducer）格式，用于保存语言模型。
它采用的是 Google 的自定义序列化格式，不能直接用于其他框架。
可以使用 Google 的 fstcompile 和 fstrain 工具来加载和保存 .gguf 文件。


### .pth 文件

PyTorch 中用于保存模型参数和优化器状态的文件格式。
它采用的是 PyTorch 的自定义序列化格式，不能直接用于其他框架。
可以使用 PyTorch 的 torch.save 函数来加载和保存 .pth 文件。

### .bin 文件


一种通用的二进制文件格式，可以用于保存模型参数和优化器状态。
它可以被多种框架所使用，例如 TensorFlow、PyTorch 和 ONNX 等。
可以使用 NumPy 或 PyTorch 等框架的函数来加载和保存 .bin 文件。

## 格式转换

### .ckpt 文件到 .pth 文件

可以使用 TensorFlow 2.x 的 tf.compat.v1.train.Saver 类来加载 .ckpt 文件，然后使用 PyTorch 的 torch.Tensor.cpu 函数将模型参数转换为 CPU 张量，最后使用 PyTorch 的 torch.save 函数保存为 .pth 文件。


### .pth 文件到 .ckpt 文件

可以使用 PyTorch 的 torch.load 函数加载 .pth 文件，然后使用 TensorFlow 2.x 的 tf.convert_to_tensor 函数将模型参数转换为 TensorFlow 张量，最后使用 TensorFlow 2.x 的 tf.train.Checkpoint 类保存为 .ckpt 文件。


### .ckpt 文件或 .pth 文件到 ONNX 模型

可以使用 TensorFlow 2.x 的 tf2onnx.convert 函数或 PyTorch 的 torch.onnx.export 函数将模型转换为 ONNX 模型，然后使用 ONNX 的 onnxruntime.InferenceSession 类加载和使用 ONNX 模型。


### ONNX 模型到 .pth 文件或 .ckpt 文件

可以使用 ONNX 的 onnxruntime.InferenceSession 类加载 ONNX 模型，然后使用 PyTorch 的 torch.Tensor 或 TensorFlow 2.x 的 tf.convert\_to\_tensor 函数将模型参数转换为 PyTorch 或 TensorFlow 张量，最后使用 PyTorch 的 torch.save 函数或 TensorFlow 2.x 的 tf.train.Checkpoint 类保存为 .pth 文件或 .ckpt 文件。


### .gguf 文件到 ONNX 模型


可以使用 Google 的 fst2onnx 工具将 .gguf 文件转换为 ONNX 模型，然后使用 ONNX 的 onnxruntime.InferenceSession 类加载和使用 ONNX 模型。


### ONNX 模型到 .gguf 文件

可以使用 ONNX 的 onnxruntime.InferenceSession 类加载 ONNX 模型，然后使用 Google 的 onnx2fst 工具将 ONNX 模型转换为 .gguf 文件。
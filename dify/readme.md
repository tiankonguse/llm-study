# dify



https://github.com/langgenius/dify  
https://docs.dify.ai/zh-hans/getting-started/install-self-hosted


Dify 是一个开源的 LLM 应用开发平台。其直观的界面结合了 AI 工作流、RAG 管道、Agent、模型管理、可观测性功能等，让您可以快速从原型到生产。
Dify is an open-source LLM app development platform.   
Dify's intuitive interface combines AI workflow, RAG pipeline, agent capabilities, model management, observability features and more, letting you quickly go from prototype to production.




```
git clone https://github.com/langgenius/dify.git
cd dify
cd docker
cp .env.example .env
docker compose up -d
```


运行后，可以在浏览器上访问 http://127.0.0.1/install 进入 Dify 控制台并开始初始化安装操作。



## 自定义配置

如果您需要自定义配置，请参考 .env.example 文件中的注释，并更新 .env 文件中对应的值。  
此外，您可能需要根据您的具体部署环境和需求对 docker-compose.yaml 文件本身进行调整，例如更改镜像版本、端口映射或卷挂载。完成任何更改后，请重新运行 docker-compose up -d。  
您可以在此处找到可用环境变量的完整列表: https://docs.dify.ai/getting-started/install-self-hosted/environments


## 在 Dify 中接入 Ollama

在 设置 > 模型供应商 > Ollama 中填入


- 模型类型(Model Type): LLM 或者 Text Embedding
- 模型名称(Model Name)：llama3.2
- 基础 URL(Base URL) ：
  * 若 Dify 为 docker 部署，建议填写局域网 IP 地址，如：http://host.docker.internal:11434
  * 若为本地源码部署，可填写 http://localhost:11434
- 模型类型(Completion mode)：对话(Chat)
- 模型上下文长度(Model context size)：4096
- 最大 token 上限(Upper bound for max tokens)：4096
- 是否支持 Vision(Vision support)：否
  * 当模型支持图片理解（多模态）勾选此项，如 llava
- 函数调用(Function call support): 是


## Connection refused

这个错误是因为 Docker 容器无法访问 Ollama 服务。   
localhost 通常指的是容器本身，而不是主机或其他容器。
要解决此问题，您需要把地址修改成 http://host.docker.internal:11434  

```
httpconnectionpool(host=127.0.0.1, port=11434): max retries exceeded with url:/cpi/chat (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7f8562812c20>: fail to establish a new connection:[Errno 111] Connection refused'))

httpconnectionpool(host=localhost, port=11434): max retries exceeded with url:/cpi/chat (Caused by NewConnectionError('<urllib3.connection.HTTPConnection object at 0x7f8562812c20>: fail to establish a new connection:[Errno 111] Connection refused'))

```




## 使用 Ollama 模型



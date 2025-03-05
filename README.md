# llm-study


## 下载模型

```bash
ollama run hf.co/lmstudio-community/DeepSeek-R1-Distill-Qwen-1.5B-GGUF:Q3_K_L
vllm serve "lmstudio-community/DeepSeek-R1-Distill-Qwen-1.5B-GGUF"
llama-cli -hf lmstudio-community/DeepSeek-R1-Distill-Qwen-1.5B-GGUF

cd ~/models
huggingface-cli download  lmstudio-community/DeepSeek-R1-Distill-Qwen-1.5B-GGUF --local-dir DeepSeek-R1-Distill-Qwen-1.5B-GGUF
```

参考文档:  

https://github.com/langchain-ai/rag-from-scratch

LLM 缺点: LLMs are trained on a large but fixed corpus of data, limiting their ability to reason about private or recent information.
之前的解决方案: Fine-tuning is one way to mitigate this, but is often not well-suited for facutal recall and can be costly.
RAG 解决方案: Retrieval augmented generation (RAG) has emerged as a popular and powerful mechanism to expand an LLM's knowledge base, using documents retrieved from an external data source to ground the LLM generation via in-context learning. 
材料的目的: These notebooks accompany a video playlist that builds up an understanding of RAG from scratch, starting with the basics of indexing, retrieval, and generation.

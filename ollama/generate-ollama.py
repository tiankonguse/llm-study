import shlex
import ollama
import json

models = ["llama3.2", "deepseek-r1:8b", "llava:latest", "gemma2:2b"]

# Iterate over prompts and generate responses
for model in models:
    response = ollama.generate(
        model=model,  # 模型名称
        prompt="你是谁?"  # 提示文本
    )

    response = response.response
    print(model, " Response:", response)
    print("\n")

# prompt: Who are you
# Response str: I'm an artificial intelligence model known as Llama. Llama stands for "Large Language Model Meta AI."

# prompt: What is your name
# Response str: I don't have a personal name, but I'm an AI designed to assist and communicate with users. You can think of me as a conversational AI or a chatbot. I'm here to help answer your questions, provide information, and engage in conversations to the best of my abilities. Is there something specific you'd like to talk about or ask?

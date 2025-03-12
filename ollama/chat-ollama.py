from ollama import chat

response = chat(
    model="llama3.2",
    messages=[
        {"role": "user", "content": "你是谁?"}
    ]
)
# 转化为 json 格式化打印 response

print(response.message.content)
# I'm an artificial intelligence model known as Llama. Llama stands for "Large Language Model Meta AI."

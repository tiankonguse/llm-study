from ollama import generate

prompt = '''def Sort(s: str) -> str:
    """ '''

suffix = """
    return result
"""

response = generate(
  model='qwen2.5-coder:0.5b',
  prompt=prompt,
  suffix=suffix,
  options={
    'num_predict': 128,
    'temperature': 0,
    'top_p': 0.9,
    'stop': ['<EOT>'],
  },
)

print(response['response'])
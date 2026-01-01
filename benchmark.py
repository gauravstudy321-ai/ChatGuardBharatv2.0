import time
from bytez import Bytez

# Your API Key
key = "97b4ac4794c9f45fa143d008a893cb21"
sdk = Bytez(key)

# Models to test
models = [
    "meta-llama/Meta-Llama-3-8B-Instruct",
    "google/gemini-1.5-flash", 
    "openai/gpt-4o-mini",
    "mistralai/Mistral-7B-Instruct-v0.2"
]

print(f"{'MODEL':<40} | {'LATENCY':<10} | {'STATUS'}")
print("-" * 65)

for model_id in models:
    try:
        start = time.time()
        client = sdk.model(model_id)
        client.run([{"role": "user", "content": "Hi"}])
        end = time.time()
        
        duration = (end - start) * 1000 # to ms
        print(f"{model_id:<40} | {duration:.0f}ms    | [OK]")
    except Exception as e:
        print(f"{model_id:<40} | ERROR      | [FAIL]")

print("-" * 65)

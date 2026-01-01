from bytez import Bytez

key = "97b4ac4794c9f45fa143d008a893cb21"
sdk = Bytez(key)

print("Testing Qwen/Qwen3Guard-Stream-4B...")
try:
    # choose Qwen3Guard-Stream-4B
    model = sdk.model("Qwen/Qwen3Guard-Stream-4B")

    # send input to model
    output, error = model.run("John Smith went to London to sip lapsang souchong")

    print({ "error": error, "output": output })
except Exception as e:
    print(f"CRITICAL ERROR: {e}")

from bytez import Bytez

key = "97b4ac4794c9f45fa143d008a893cb21"
sdk = Bytez(key)

print("Testing openai/gpt-4o-mini...")
try:
    # choose gpt-4o-mini
    model = sdk.model("openai/gpt-4o-mini")

    # send input to model
    output, error = model.run([
      {
        "role": "user",
        "content": "Hello"
      }
    ])

    print({ "error": error, "output": output })

except Exception as e:
    print(f"CRITICAL ERROR: {e}")

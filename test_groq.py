from groq import Groq
import os

print("Initialising Groq...")
try:
    # Attempt to use the code provided by the user
    client = Groq(api_key="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") 
    
    print("Sending request to Groq...")
    completion = client.chat.completions.create(
        model="openai/gpt-oss-120b", # Using user's requested model
        messages=[
          {
            "role": "user",
            "content": "Hello world"
          }
        ],
        temperature=1,
        max_completion_tokens=8192,
        top_p=1,
        reasoning_effort="medium",
        stream=True,
        stop=None
    )

    print("Response received:")
    for chunk in completion:
        print(chunk.choices[0].delta.content or "", end="")
        
except Exception as e:
    print(f"\nCRITICAL ERROR: {e}")

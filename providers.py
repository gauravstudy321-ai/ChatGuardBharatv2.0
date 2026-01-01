"""
Provider Integrations for External Chatbot Testing
===================================================
This module handles communication with different chatbot APIs.
Users provide their API keys, and we send jailbreaks to THEIR bots.
"""

import os
import requests


def call_openai(api_key, model, prompt, system_prompt=""):
    """
    Call OpenAI API with user's credentials.
    This tests THEIR chatbot configuration.
    """
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=1024
        )
        return response.choices[0].message.content, None
    except Exception as e:
        return None, str(e)


def call_anthropic(api_key, model, prompt, system_prompt=""):
    """
    Call Anthropic API with user's credentials.
    """
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        
        # Anthropic handles system prompts as a separate parameter
        kwargs = {
            "model": model,
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": prompt}]
        }
        if system_prompt:
            kwargs["system"] = system_prompt
            
        response = client.messages.create(**kwargs)
        return response.content[0].text, None
    except Exception as e:
        return None, str(e)


def call_groq(api_key, model, prompt, system_prompt=""):
    """
    Call Groq API with user's credentials.
    """
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=1024
        )
        return response.choices[0].message.content, None
    except Exception as e:
        return None, str(e)


def call_huggingface(api_key, model, prompt, system_prompt=""):
    """
    Call HuggingFace Inference API via Together AI router.
    Works with Qwen, Llama, Mistral, and other models on HF.
    
    api_key: HuggingFace token (hf_...)
    model: e.g. "Qwen/Qwen2.5-7B-Instruct:together"
    """
    try:
        from openai import OpenAI
        client = OpenAI(
            api_key=api_key,
            base_url="https://router.huggingface.co/v1"
        )
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0.7,
            max_tokens=1024
        )
        return response.choices[0].message.content, None
    except Exception as e:
        return None, str(e)


def call_custom_webhook(endpoint, prompt, system_prompt=""):
    """
    Call custom webhook endpoint.
    Expects JSON format: {"message": "...", "system": "..."}
    Returns: {"response": "..."}
    """
    try:
        payload = {"message": prompt}
        if system_prompt:
            payload["system"] = system_prompt
            
        response = requests.post(
            endpoint,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        return data.get("response", ""), None
    except Exception as e:
        return None, str(e)


# Provider metadata
PROVIDERS = {
    "OpenAI": {
        "models": ["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo", "gpt-4"],
        "function": call_openai,
        "requires_key": True
    },
    "Anthropic": {
        "models": ["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"],
        "function": call_anthropic,
        "requires_key": True
    },
    "Groq": {
        "models": ["llama-3.1-70b-versatile", "mixtral-8x7b-32768", "gemma2-9b-it"],
        "function": call_groq,
        "requires_key": True
    },
    "HuggingFace": {
        "models": ["Qwen/Qwen2.5-7B-Instruct:together", "meta-llama/Llama-3.1-8B-Instruct:together", "mistralai/Mistral-7B-Instruct-v0.3:together"],
        "function": call_huggingface,
        "requires_key": True
    },
    "Custom Webhook": {
        "models": ["N/A"],
        "function": call_custom_webhook,
        "requires_key": False  # Uses endpoint URL instead
    }
}


def test_external_chatbot(provider, api_key, model, prompt, system_prompt=""):
    """
    Main function to test external chatbot.
    
    Args:
        provider: Provider name (from PROVIDERS keys)
        api_key: User's API key
        model: Specific model name
        prompt: The jailbreak prompt to send
        system_prompt: Optional system instructions
    """
    if provider not in PROVIDERS:
        return None, f"Unknown provider: {provider}"
    
    func = PROVIDERS[provider]["function"]
    
    # Custom webhook has different signature (endpoint instead of api_key)
    if provider == "Custom Webhook":
        return func(api_key, prompt, system_prompt)
    else:
        return func(api_key, model, prompt, system_prompt)

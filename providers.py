"""
Provider Integrations for External Chatbot Testing
===================================================
This module handles communication with different chatbot APIs.
Users provide their API keys, and we send jailbreaks to THEIR bots.
"""

import os
import requests


def call_openai(api_key, model, prompt):
    """
    Call OpenAI API with user's credentials.
    This tests THEIR chatbot configuration.
    """
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1024
        )
        return response.choices[0].message.content, None
    except Exception as e:
        return None, str(e)


def call_anthropic(api_key, model, prompt):
    """
    Call Anthropic API with user's credentials.
    """
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)
        response = client.messages.create(
            model=model,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text, None
    except Exception as e:
        return None, str(e)


def call_groq(api_key, model, prompt):
    """
    Call Groq API with user's credentials.
    """
    try:
        from groq import Groq
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1024
        )
        return response.choices[0].message.content, None
    except Exception as e:
        return None, str(e)


def call_custom_webhook(endpoint, prompt):
    """
    Call custom webhook endpoint.
    Expects JSON format: {"message": "..."}
    Returns: {"response": "..."}
    """
    try:
        response = requests.post(
            endpoint,
            json={"message": prompt},
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
    "Custom Webhook": {
        "models": ["N/A"],
        "function": call_custom_webhook,
        "requires_key": False  # Uses endpoint URL instead
    }
}


def test_external_chatbot(provider, api_key, model, prompt):
    """
    Main function to test external chatbot.
    
    Args:
        provider: "OpenAI", "Anthropic", "Groq", or "Custom Webhook"
        api_key: User's API key (or endpoint URL for webhook)
        model: Model name
        prompt: Jailbreak prompt to send
        
    Returns:
        (response_text, error_message) tuple
    """
    if provider not in PROVIDERS:
        return None, f"Unknown provider: {provider}"
    
    provider_func = PROVIDERS[provider]["function"]
    
    if provider == "Custom Webhook":
        return provider_func(api_key, prompt)  # api_key is actually the endpoint
    else:
        return provider_func(api_key, model, prompt)

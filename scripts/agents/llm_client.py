"""
LLM Client - Unified interface for AI API calls

Supports: Google Gemini (primary), Anthropic Claude (fallback)

Configure via environment variables:
- GOOGLE_API_KEY (for Gemini)
- ANTHROPIC_API_KEY (for Claude)
"""

import os
from typing import Optional

# Try to import available clients
try:
    from google import genai
    from google.genai import types
    HAS_GEMINI = True
except ImportError:
    HAS_GEMINI = False

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False


def get_available_provider() -> str:
    """Determine which LLM provider is available."""
    if os.environ.get("GOOGLE_API_KEY") and HAS_GEMINI:
        return "gemini"
    elif os.environ.get("ANTHROPIC_API_KEY") and HAS_ANTHROPIC:
        return "anthropic"
    else:
        return "none"


def call_llm(
    system_prompt: str,
    user_prompt: str,
    max_tokens: int = 8000,  # Gemini 2.5 Pro needs more for thinking
    provider: Optional[str] = None
) -> str:
    """
    Make an LLM API call with fresh context.
    
    Args:
        system_prompt: Instructions for the model
        user_prompt: User input/question
        max_tokens: Maximum response length
        provider: Force specific provider ("gemini" or "anthropic")
    
    Returns:
        Model response text
    """
    if provider is None:
        provider = get_available_provider()
    
    if provider == "gemini":
        return _call_gemini(system_prompt, user_prompt, max_tokens)
    elif provider == "anthropic":
        return _call_anthropic(system_prompt, user_prompt, max_tokens)
    else:
        raise ValueError(
            "No LLM API available. Set GOOGLE_API_KEY or ANTHROPIC_API_KEY environment variable."
        )


def _call_gemini(system_prompt: str, user_prompt: str, max_tokens: int) -> str:
    """Call Google Gemini API using the new google-genai SDK."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set")
    
    # Create client with API key
    client = genai.Client(api_key=api_key)
    
    # Combine system prompt and user prompt
    # Gemini 2.0 handles system instructions differently
    full_prompt = f"{system_prompt}\n\n---\n\n{user_prompt}"
    
    # Use Gemini 2.5 Pro (best quality, requires paid tier)
    response = client.models.generate_content(
        model="gemini-2.5-pro",
        contents=full_prompt,
        config=types.GenerateContentConfig(
            max_output_tokens=max_tokens,
            temperature=0.7
        )
    )
    
    return response.text


def _call_anthropic(system_prompt: str, user_prompt: str, max_tokens: int) -> str:
    """Call Anthropic Claude API."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")
    
    client = anthropic.Anthropic(api_key=api_key)
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}]
    )
    
    return response.content[0].text


# Quick test
if __name__ == "__main__":
    provider = get_available_provider()
    print(f"Available provider: {provider}")
    
    if provider != "none":
        print("Testing LLM call...")
        response = call_llm(
            system_prompt="You are a helpful assistant. Be very concise.",
            user_prompt="Say exactly: Hello, pipeline!",
            max_tokens=500  # Gemini 2.5 Pro needs room for thinking
        )
        print(f"✅ Response: {response}")
    else:
        print("No API key found.")
        print("Set GOOGLE_API_KEY or ANTHROPIC_API_KEY environment variable.")
        print("\nTo test, run:")
        print("  export GOOGLE_API_KEY='your-key-here'")
        print("  python3 scripts/agents/llm_client.py")

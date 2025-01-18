import os
from typing import Optional, Dict, Any, List
from openai import OpenAI, AsyncOpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure OpenAI with API key
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

def chat_completion(
    messages: List[Dict[str, Any]], 
    model_name: str = "gpt-4o",
    temperature: float = 0.0,
    client: OpenAI = None,
    **kwargs: Dict[str, Any]
):
    """
    Synchronous chat completion
    """
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=1.0 if 'o1' in model_name else temperature,
            **kwargs
        )
        
        return response
    
    except Exception as e:
        print(f"Error in chat completion: {str(e)}")
        raise

async def achat_completion(
    messages: List[Dict[str, Any]], 
    model_name: str = "gpt-4o",
    temperature: float = 0.0,
    client: AsyncOpenAI = None,
    **kwargs: Dict[str, Any]
):
    """
    Asynchronous chat completion
    """
    try:
        response = await client.chat.completions.create(
            model=model_name,
            messages=messages,
            temperature=1.0 if 'o1' in model_name else temperature,
            **kwargs
        )

        return response
    except Exception as e:
        print(f"Error in async chat completion: {str(e)}")
        raise

def format_response(response) -> str:

    content = response.choices[0].message.content
    usage = response.usage.model_dump()
    
    return content, usage

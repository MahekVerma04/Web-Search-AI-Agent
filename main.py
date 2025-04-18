import requests
import json
from config import HEADERS, openrouter_api_key, your_serpapi_key

def search_web(query):
    url = "https://serpapi.com/search"
    params = {
        "q": query,
        "api_key": your_serpapi_key,  # Use your SerpAPI key here
        "engine": "google",
        "num": 5,
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        results = response.json()

        if "organic_results" in results:
            snippets = [result["snippet"] for result in results["organic_results"] if "snippet" in result]
            return snippets, None  # Return snippets and no error
        else:
            return [], "No organic results found."  # Return empty list if no results found
    except requests.exceptions.RequestException as e:
        return [], f"Error fetching results: {e}"  # Return error message

def summarize_with_openrouter(query, snippets):
    system_prompt = "You are a helpful assistant that summarizes web search results."
    joined_text = "\n".join(snippets)
    user_prompt = f"""A user searched: "{query}"
Here are the top web results:
{joined_text}

Summarize these results into a helpful answer."""

    payload = {
        "model": "openai/gpt-3.5-turbo",  # or you can use "mistralai/mistral-7b-instruct"
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions",
                                 headers=HEADERS, json=payload)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"], None  # Return summary and no error
    except requests.exceptions.RequestException as e:
        return None, f"Error summarizing: {e}"  # Return error message


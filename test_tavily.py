import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("TAVILY_API_KEY")
print(f"Testing API Key: {api_key}")

try:
    client = TavilyClient(api_key=api_key)
    response = client.search("Apple 10-K 2023", max_results=1)
    print("Success!")
    print(response)
except Exception as e:
    print(f"Error: {e}")

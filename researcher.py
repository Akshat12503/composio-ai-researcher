import os
import json
from dotenv import load_dotenv
from openai import OpenAI
from composio import Composio
from composio_openai import OpenAIProvider

# 1. Load environment variables
load_dotenv()

# 2. Initialize Gemini pretending to be OpenAI
llm_client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# 3. Initialize the new Composio Client with the OpenAI Provider
composio = Composio(provider=OpenAIProvider())

# 4. We request standard search and browsing toolkits
# (Composio will route these to the best available web tools)
tools = composio.tools.get(user_id="pg-test-66b4bafa-b8bb-44be-96f4-9f15ffce4fb2", toolkits=["tavily"]) 

SCHEMA_INSTRUCTIONS = """
You must output ONLY a valid JSON object matching this exact structure:
{
  "app_name": "Name of the app",
  "category": "The specified category",
  "one_line_description": "Clean description under 15 words.",
  "auth_methods": ["OAuth2" or "API Key" or "Basic" or "Token" or "Other"],
  "access_type": "Self-serve" or "Gated",
  "api_surface": "Brief architectural summary (REST/GraphQL/etc.)",
  "mcp_exists": "Yes" or "No",
  "buildability_verdict": "Ready" or "Blocked",
  "blockers": "Main blocker or 'None'",
  "evidence_url": "Direct developer documentation URL found"
}
"""

def research_single_app(app_name, hint_url, category):
    print(f"\n🕵️ Researching {app_name}...")
    
    prompt = f"""
    Research the developer API details for the app: '{app_name}'.
    Hint URL to start with: {hint_url}
    Belongs to Category: {category}
    
    Use your tools to search for and read their official developer/API documentation. 
    Determine the authentication method, whether a developer can get instant self-serve access, 
    and if any Model Context Protocol (MCP) servers exist for it.
    """
    
    # Phase 1: Ask the agent to search the web
    response = llm_client.chat.completions.create(
        model="gemini-3.1-flash-lite", 
        tools=tools,
        messages=[
            {"role": "system", "content": "You are a precise research agent. Use your tools to find the requested information."},
            {"role": "user", "content": prompt}
        ]
    )
    
    # Composio executes the search (Be sure your pg-test-... ID is pasted here!)
    tool_result = composio.provider.handle_tool_calls(response=response, user_id="pg-test-66b4bafa-b8bb-44be-96f4-9f15ffce4fb2")
    
    # Phase 2: Feed the search results back to the LLM for JSON extraction
    print("🧠 Extracting insights into schema...")
    extraction_prompt = f"""
    Here is the raw documentation data retrieved from the web:
    {tool_result}
    
    Analyze this data and extract the information. 
    {SCHEMA_INSTRUCTIONS}
    """
    
    final_response = llm_client.chat.completions.create(
        model="gemini-3.1-flash-lite", 
        messages=[
            {"role": "system", "content": "You are a precise data extractor. You only output valid raw JSON, with no markdown formatting or extra text."},
            {"role": "user", "content": extraction_prompt}
        ]
    )
    
    return final_response.choices[0].message.content

import pandas as pd
import time

# ... (keep your existing imports, setup, and research_single_app function exactly as they are) ...

def process_all_apps(csv_file):
    print(f"📂 Loading apps from {csv_file}...")
    df = pd.read_csv(csv_file)
    results = []
    
    for index, row in df.iterrows():
        app_name = row['App']
        hint_url = row['Website / hint']
        category = row['Category']
        
        try:
            # Run the agent
            result_json_str = research_single_app(app_name, hint_url, category)
            
            # Clean up the output in case the LLM wrapped it in markdown code blocks
            clean_str = result_json_str.strip().removeprefix("```json").removesuffix("```").strip()
            result_dict = json.loads(clean_str)
            
            results.append(result_dict)
            
            # Save incrementally to a JSON file after every single app
            with open("research_results.json", "w") as f:
                json.dump(results, f, indent=4)
                
            print(f"✅ Successfully saved data for {app_name}\n")
            
        except Exception as e:
            print(f"❌ Error researching {app_name}: {e}\n")
            
        # Pause for a few seconds to avoid hitting API rate limits
        time.sleep(3)

if __name__ == "__main__":
    print("🚀 Starting Batch Research Process...")
    # Make sure you have created apps.csv in your folder before running this!
    process_all_apps("apps.csv")
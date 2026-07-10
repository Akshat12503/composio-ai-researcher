Markdown
# AI Product Ops: API & MCP Surface Researcher

This repository contains an autonomous AI research agent built for the Composio AI Product Ops evaluation. It uses the Composio SDK, Tavily toolsets, and the Gemini 3.1 Flash-Lite model to discover, read, and extract authentication and architecture patterns from developer documentation across 100 enterprise applications.

## Live Deliverable
**View the interactive Case Study Dashboard here:** 
[Insert your GitHub Pages Link Here]

## How to Run the Research Agent

### 1. Prerequisites
Ensure you have Python 3.9+ installed. You will need API keys for Google Gemini and Tavily.

### 2. Installation
Clone the repository and install the required dependencies:
```bash
git clone [https://github.com/Akshat12503/composio-ai-researcher.git](https://github.com/Akshat12503/composio-ai-researcher.git)
cd composio-ai-researcher
python -m venv venv
# On Windows: .\venv\Scripts\activate
# On Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
3. Environment Setup
Create a .env file in the root directory and add your Google Gemini API key:

Code snippet
GEMINI_API_KEY=your_gemini_api_key_here
Link your Composio workspace to Tavily using the CLI:

Bash
composio add tavily
(Follow the prompts to paste your Tavily API key).

4. Execute the Pipeline
Run the main script to process the 100 apps defined in apps.csv:

Bash
python researcher.py
The script will autonomously research each app, extract the schema using LLM validation, and incrementally save the output to research_results.json.


### Final Push
Once you save that `README.md`, run your quick Git commands to push it up:
```powershell
git add README.md
git commit -m "Add instructions to README"
git push

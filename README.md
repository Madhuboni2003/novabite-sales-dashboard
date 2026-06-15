# 🍕 Novabite Executive Sales Dashboard & AI Chat Analyst
A full-stack business intelligence web application featuring a decoupled engineering architecture: an interactive React UI client workspace and a high-performance Python FastAPI analytical backend utilizing an SQLite database instance via OpenRouter.
## 🎯 **Evaluation Quick Link:** Don't have time for local environment setups? Watch the full interactive application walkthrough directly on our repository home page!
> 🎬 **[Click here to watch the project video demo](https://github.com/user-attachments/assets/8f067602-ace9-4d6d-9862-c99e733e9178)**
## 💻 Prerequisites & Machine Setup
Before deploying the servers locally, ensure your computer has the runtime engines installed:

1. **Python 3.10+** - Required to power the analytical database backend.
2. **Node.js (LTS Version 22+)** - Required to compile and serve the React development UI.
   * *Note:* If running `npm` commands throws a `command not found` error, download and install Node.js from the official [nodejs.org](https://nodejs.org/) dashboard before proceeding.
---
## 🚀 Step-by-Step Local Deployment Guide

Follow these sequential steps in your terminal application (Git Bash, Command Prompt, or Terminal) to stand up the project workspace.

### 📥 1. Clone the Code and Switch Branches
Open a terminal window on your machine and run the following configuration commands:

```bash
# Clone the complete project repository code safely
git clone [https://github.com/Madhuboni2003/novabite-sales-dashboard.git](https://github.com/Madhuboni2003/novabite-sales-dashboard.git)

# Move your terminal directory directly into the root folder
cd novabite-sales-dashboard

# Switch over to the active tracking development branch containing the final work
git checkout feat/llm-chat-agent
```
# 🐍 2. Set Up the Python FastAPI Backend Engine
To establish your data layer pipelines, keep your current terminal active and move into the backend repository folder:
```bash
# 1. Enter the backend directory
cd backend

# 2. Build a fresh, clean Python virtual environment partition
python -m venv venv

# 3. Activate the environment tracker
source venv/Scripts/activate  # For Windows (Git Bash)
# OR venv\Scripts\activate   # For Windows (Standard CMD)
# OR source venv/bin/activate # For Mac/Linux

# 4. Install all analytical, server, and AI dependencies
pip install -r requirements.txt

# 5. Populate and generate the local SQLite transaction database
python seed.py
```
(Verifying step 5: You will see a file named novabite.db pop up right next to your code scripts).

🔑 Configuration: Adding your OpenRouter Key
Open the backend/main.py file in your code editor. Locate the OpenAI client configuration block (around line 29) and update the api_key string to pass your active OpenRouter token safely:

```Python
client = OpenAI(
    base_url="[https://openrouter.ai/api/v1](https://openrouter.ai/api/v1)",
    api_key="your_actual_openrouter_token_here"
)
```
Launch the Analytical Server
With the database seeded and the key authorized, spin up your background system engine:
```Bash
uvicorn main:app --reload
```
Verification Check: The backend engine will actively listen for incoming data streams on http://127.0.0.1:8000/.
⚛️ 3. Set Up the React Frontend Workspace
Open a second, completely separate terminal window to host your visual interfaces concurrently. Run the following setup blocks:
```Bash
# 1. Navigate straight to the frontend client directory from the root folder
cd novabite-sales-dashboard/frontend

# 2. Extract and download all UI packages and charting modules
npm install

# 3. Start the high-speed Vite development web application server
npm run dev
```
Verification Check: The application portal interface will launch immediately on http://localhost:5173/.

🔍 Interacting With the Interface
Open your browser window to http://localhost:5173/ to audit the features:

📊 Executive Dashboard Tab: Automatically hydrates live operational metrics from your backend (total_net_revenue, profit margins, and performance targets) and graphs seasonal operational trend lines using responsive Recharts bars.

🤖 AI Chat Analyst Tab: Type any complex plain-English manager request (e.g., “Which sales rep closed the most units in 2025”) and click Ask Engine. The pipeline converts the prompt string into structural SQLite code on the fly, queries the database, and returns clear conversational answers onto the screen.

2. Which LLM I used and why?
We integrated OpenRouter as our unified API gateway to connect our backend to a high-performing open-source LLM (such as Meta-Llama 3 or a similar top-tier free-tier model available on the platform).

Here is exactly why we chose this specific stack:

Zero-Cost Scalability: Utilizing a free-tier model through OpenRouter allowed us to build and evaluate a robust, production-grade text-to-SQL pipeline completely free of charge, with zero upfront API token costs.

Unified API Architecture: OpenRouter provides a single, clean OpenAI-compatible connection interface. If we ever need to swap the underlying model to a larger provider in the future, we can change a single string parameter in our configuration without rewriting any backend pipeline logic.

Excellent Schema Understanding: The open-source model accessed through OpenRouter handles natural language translation tasks beautifully, processing database schemas and parsing tables into safe SQLite queries with high semantic accuracy.

## Prompt Engineering Strategy (`/api/chat`)

To ensure the AI model converts plain-English questions into valid, error-free SQLite statements every single time, we implemented a strict **System Prompt Instruction** pipeline. 

Instead of just sending the user's question directly to the LLM, the backend wraps it in a carefully structured context template before hitting the OpenRouter API.

### The 3 Core Components of Our Prompt

1. **Context & Database Schema Injection:** We explicitly feed the exact structure of our SQLite database tables, column names, and data types directly into the AI's memory. This prevents the model from hallucinating or guessing table names.
2. **Strict Output Guardrails (SQL Only):** We instruct the AI to return *only* the raw executable SQL query string. We strictly forbid it from wrapping the code in markdown formatting (like 
http://googleusercontent.com/immersive_entry_chip/0

### 🎯 Why This Approach Works
By anchoring the AI with explicit constraints and injecting the precise table structure up front, we eliminated runtime query crashes. The frontend receives a predictable, clean SQL string that it can immediately execute against our local database engine safely.

## What you would improve with more time
As I am using a free LLM model , it is comparatively slow so in future I would like to incorportae better LLM model to make tha Chat Agent faster.
<img width="1142" height="767" alt="image_2026-06-15_23-25-58" src="https://github.com/user-attachments/assets/d0f8224e-20f4-4b2e-b92d-d4ca9519be59" />
<img width="1087" height="602" alt="Screenshot 2026-06-15 232438" src="https://github.com/user-attachments/assets/463bc63d-c5eb-4a53-959b-bffbe039c50e" />
<img width="980" height="738" alt="Screenshot 2026-06-15 120520" src="https://github.com/user-attachments/assets/c7d4f8f5-423e-40d3-9042-1b8913b14545" />
<img width="1162" height="767" alt="Screenshot 2026-06-15 223350" src="https://github.com/user-attachments/assets/40fe3f48-cc9d-4bf6-87df-424f7728289f" />
<img width="1092" height="610" alt="image_2026-06-15_23-25-18" src="https://github.com/user-attachments/assets/98cd1f85-29b1-4154-93be-e926874f35eb" />
> 🎬 **[Click here to watch the project video demo](https://github.com/user-attachments/assets/8f067602-ace9-4d6d-9862-c99e733e9178)**









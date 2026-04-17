# 🛠️ MCP Toolbox Demo (Streamlit + GenAI Toolbox + LangChain)

This project demonstrates how to integrate **Google GenAI Toolbox (MCP)** with a **LangChain agent** and a **Streamlit UI** to securely query a local SQLite database using natural language.

---

## 🚀 What This Project Does

* Uses **GenAI Toolbox (MCP)** to expose SQL queries as secure tools
* Uses **LangChain Agent** to dynamically call those tools
* Uses **Streamlit** for an interactive UI
* Works on a **local SQLite database created from CSV**

---

## 📂 Project Structure

```
.
├── app.py                # Streamlit app
├── tools.yaml           # MCP Toolbox config
├── Bookstore.csv        # Source dataset
├── bookstore.db         # Generated SQLite DB
├── create_db.py         # Script to generate DB
├── .env                 # API key (not committed)
└── requirements.txt
```

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd <your-repo-folder>
```

---

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Set Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

---

## 🗄️ Step 5: Create SQLite Database

Run:

```bash
python create_db.py
```

This will:

* Read `Bookstore.csv`
* Create `bookstore.db`
* Store data in a table called `books`

---

## 🧠 Step 6: Setup GenAI Toolbox (MCP)

Clone and build the toolbox:

```bash
git clone https://github.com/googleapis/genai-toolbox.git
cd genai-toolbox
docker build -t genai-toolbox .
```

---

### ▶️ Run the Toolbox Container

From your **project root directory** (where `tools.yaml` exists):

```bash
docker run \
  -p 8080:8080 \
  -v $(pwd):/data \
  genai-toolbox \
  --config /data/tools.yaml \
  --address 0.0.0.0 \
  --port 8080
```

✅ This will:

* Start MCP Toolbox on `http://localhost:8080`
* Load tools from `tools.yaml`
* Connect to your SQLite DB

---

## 💻 Step 7: Run the Streamlit App

```bash
streamlit run app.py
```

---

## 💬 Example Queries

Try asking:

* "How many sci-fi books are there?"
* "Show me books related to Harry Potter"
* "Top rated books in the West region"
* "What is the average price by format?"

---

## 🧩 How It Works (Architecture)

```
User → Streamlit UI → LangChain Agent → MCP Toolbox → SQLite DB
```

* The agent **does not write SQL directly**
* It calls **predefined tools from MCP**
* Ensures **security + governance**

---

## 🔐 Why MCP Toolbox?

* Prevents unsafe SQL generation
* Enforces controlled access to data
* Makes LLMs **tool-driven instead of query-guessing**

---

## 🧠 Key Concepts Demonstrated

* Tool Calling Agents
* MCP (Model Context Protocol)
* Secure Data Access via Tools
* LLM Orchestration with LangChain

---

## 🛠️ Troubleshooting

### ❌ Toolbox not connecting?

* Ensure Docker is running
* Check port `8080` is free

### ❌ No tools loaded?

* Verify `tools.yaml` path is correct
* Ensure DB exists inside `/data`

### ❌ OpenAI error?

* Check `.env` file
* Validate API key

---

## ✨ Future Improvements

* Add authentication layer
* Expand toolset (joins, analytics)
* Deploy on cloud (EC2 + Docker)
* Add multi-agent workflows

---

## 🙌 Final Note

This project is a **minimal but powerful example** of how modern AI systems should interact with data:

👉 Not by guessing queries
👉 But by **calling governed tools**

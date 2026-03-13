# LangGraphWork

A small, local workspace assistant built on **LangGraph** + **LangChain** to interact with files and folders via a conversational, tool-enabled agent.

This project lets you chat with an agent that can execute file system operations (list, read, create, edit, delete files/folders) safely inside a controlled `workspace/` directory.

---

## 🚀 What This Project Does

- Runs a **chat loop** (`main.py`) where you enter prompts and the agent responds.
- Uses **LangGraph** workflow (in `graph.py`) to alternate between:
  - The **LLM decision node** (makes chat/plan decisions)
  - The **tools node** (runs file operations automatically)
- Provides a set of **safe file tools** under `tools/file_tools.py` that operate only inside `workspace/`.
- Uses `langchain-openai` and an OpenAI API key to power the agent.

---

## ✅ Key Components

### `main.py`
Runs a read-eval-print loop (REPL) for the assistant.
- Tracks message history.
- Limits memory to the last 10 messages (5 user + 5 assistant).
- Supports commands:
  - `exit` / `quit` → close session
  - `forget` → clear chat history

### `graph.py`
Defines the LangGraph workflow:
- `agent` node calls the LLM
- `tools` node runs tools via `ToolNode`
- Decision function (`should_continue`) loops until the agent provides a final response.

### `tools/file_tools.py`
Contains tools decorated with `@tool` (LangChain tools) to safely operate on `workspace/`:
- `list_files_recursive`
- `create_file`
- `create_folder`
- `read_file`
- `edit_file`
- `rename_file_or_folder`
- `move_file_or_folder`
- `delete_file`
- `delete_folder`

All tools enforce a sandbox by using `_safe_path()` to prevent directory traversal outside `workspace/`.

### `utils/helpers.py`
Returns a configured LLM (`gpt-4o-mini` by default).

### `workspace/`
A sandbox folder where files are read/created/edited. Example included: `dinozorlar.html`.

---

## 🧩 Setup & Installation

1. **Clone or open this workspace** in VS Code.
2. **Ensure you have Python 3.11+ installed.**
3. **Set your OpenAI API key** in your environment.

For Windows PowerShell:
```powershell
$env:OPENAI_API_KEY="your_api_key_here"
```

4. **Install dependencies** (use a venv if desired):
```powershell
python -m pip install -U langgraph langchain-openai
```

> ⚠️ This repo does not include a dependency lock file. If you wish, create a `requirements.txt` for your environment.

---

## ▶️ Running the Assistant

From the project root:
```powershell
python main.py
```

Type questions and requests in natural language. The agent can automatically run tools like:
- "List files in the workspace"
- "Read `workspace/dinozorlar.html`"
- "Create a new note called `workspace/notes.txt`"

---

## 🛠 Extending the Agent

### Add a new tool
1. Add a new `@tool` function to `tools/file_tools.py` (or another module).
2. Make sure it uses `_safe_path()` or otherwise enforces sandboxing.
3. The tool will be automatically picked up by `ALL_TOOLS`.

### Change the LLM
Update `utils/helpers.py` to configure a different model, temperature, or client.

---

## ⚠️ Notes / Safety

- All file operations are restricted to the `workspace/` directory (via `_safe_path`).
- The agent uses `gpt-4o-mini` by default; change it for another OpenAI model or provider.
- The project currently does **not** include any ACL/authentication layer.

---

## 📌 Troubleshooting

- If you see `ModuleNotFoundError: No module named 'langgraph'`, install the missing package. 
- If the agent fails to respond, ensure `OPENAI_API_KEY` is correctly set and valid.

---

## 📚 License
No license specified. Use as you wish.

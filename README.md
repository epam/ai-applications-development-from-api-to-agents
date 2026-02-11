<h1 align="center">
    AI Applications Development Course: From API To Agents
</h1>
<p align="center">
    <a href="https://dialx.ai/">
        <img src="https://dialx.ai/logo/dialx_logo.svg" alt="About DIALX">
    </a>
</p>
<h4 align="center">
    <a href="https://discord.gg/ukzj9U9tEe">
        <img src="https://img.shields.io/static/v1?label=DIALX%20Community%20on&message=Discord&color=blue&logo=Discord&style=flat-square" alt="Discord">
    </a>
</h4>

## About the Course

This is a **Python course** focused on building AI-powered applications by working directly with APIs. 
Instead of relying on tools like LangChain that abstract away the internals, we go straight to the API level. By the
end, when you do use frameworks, you'll understand exactly what's happening under the hood.

**What this course IS:**

- API-first approach to building AI applications
- 80% hands-on practice with real-world tasks, no "Hello World" exercises
- A challenging journey that mirrors actual AI application development work

**What this course is NOT:**

- Not an ML course: we won't dive into transformers, training, or how LLMs work internally
- Not a prompt engineering course: we expect you to already know how to write prompts and understand that different
  models behave differently with the same input


> ⚠️ This is not an easy course. You will be building the same things professional AI developers build daily.

> 💡 What you get from this course depends on you. We designed it as a practical reference you can return to and reuse in your daily work.

> 🤝 Need help along the way? Join the [DIALX Community on Discord](https://discord.com/invite/ukzj9U9tEe) — we have dedicated course support channels. After joining, add the role shown below to unlock them.

![info](need/to/fix)

## Branches Structure

- `main` - tasks with descriptions
- `main-detailed` - tasks with super detailed descriptions
- `completed` - completed tasks, useful when stuck

---

## Prerequisites

- **Python 3.11+**
- **IDE** (PyCharm, VS Code, or any preferred editor)
- **Postman** (for testing API calls)
- **Docker** with Docker Compose
- **API Keys** to work with different models (you will need to pay ~5-10$ credits):
  - **OpenAI API Key** (we will be primarily working with OpenAI models). [Generate it here](https://platform.openai.com/settings/organization/api-keys) and set up as environment variable with name `OPENAI_API_KEY`
  - **Anthropic API Key** [Generate it here](https://platform.claude.com/settings/keys) and set up as environment variable with name `ANTHROPIC_API_KEY`
  - **Gemini API Key** [Generate it here](https://aistudio.google.com/app/api-keys) and set up as environment variable with name `GEMINI_API_KEY`

---

## Getting Started

### 0. ⭐️ **Star the repository** - it will help us grow ⭐️

### 1. ⑃ Fork and clone the repository

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**macOS / Linux:**

```bash
source .venv/bin/activate
```

**Windows:**

```bash
.venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---


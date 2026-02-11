# Work with AI APIs

In this task, you will work with APIs from different AI vendors. The goal is to understand how to make calls to 
different models, how to parse responses, how to work with streaming, and how these features work under the hood in the 
libraries we commonly use.

---

## Prerequisites

**API Keys** to work with different models (you will need to pay ~5-10$ credits):
  - **OpenAI API Key** (we will be primarily working with OpenAI models). [Generate it here](https://platform.openai.com/settings/organization/api-keys) and set up as environment variable with name `OPENAI_API_KEY`
  - **Anthropic API Key** [Generate it here](https://platform.claude.com/settings/keys) and set up as environment variable with name `ANTHROPIC_API_KEY`
  - **Gemini API Key** [Generate it here](https://aistudio.google.com/app/api-keys) and set up as environment variable with name `GEMINI_API_KEY`

---

## Task:
1. [Import](https://learning.postman.com/docs/getting-started/importing-and-exporting/importing-data) in Postman [collection](dial-ai-course.postman_collection.json). It will be quite useful for the further tasks. In the collection present OPENAI_API_KEY, ANTHROPIC_API_KEY and GEMINI_API_KEY environment variables, [here you can find how to configure environment in Portman](https://learning.postman.com/docs/sending-requests/variables/managing-environments)
2. Open [base_app](base_app.py) and implement it according TODO
3. Open [base_client](base_client.py) and review it, this client holds
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
3. Open [base_client](base_client.py) and review it — this is the abstract base class all AI clients extend

### OpenAI Chat Completions
4. Open [openai/base](openai/base.py) and implement TODO — validate api_key and call super with Bearer-formatted key
5. Open [openai/chat/completions/client.py](openai/chat/completions/client.py) and implement all TODOs (SDK client)
6. Run [openai_chat_completions_app.py](openai/chat/completions/openai_chat_completions_app.py) with `openai_client` and test
7. Open [openai/chat/completions/custom_client.py](openai/chat/completions/custom_client.py) and implement all TODOs (raw HTTP client)
8. In [openai_chat_completions_app.py](openai/chat/completions/openai_chat_completions_app.py) switch to `openai_custom_client` and test

### OpenAI Responses API
9. Open [openai/responses/client.py](openai/responses/client.py) and implement all TODOs (SDK client)
10. Run [openai_responses_app.py](openai/responses/openai_responses_app.py) with `openai_client` and test
11. Open [openai/responses/custom_client.py](openai/responses/custom_client.py) and implement all TODOs (raw HTTP client)
12. In [openai_responses_app.py](openai/responses/openai_responses_app.py) switch to `openai_custom_client` and test

### Anthropic
13. Open [anthropic/client.py](anthropic/client.py) and implement all TODOs (SDK client)
14. Run [anthropic_app.py](anthropic/anthropic_app.py) with `anthropic_client` and test
15. Open [anthropic/custom_client.py](anthropic/custom_client.py) and implement all TODOs (raw HTTP client)
16. In [anthropic_app.py](anthropic/anthropic_app.py) switch to `anthropic_custom_client` and test

### Gemini
17. Open [gemini/client.py](gemini/client.py) and implement all TODOs (SDK client)
18. Run [gemini_app.py](gemini/gemini_app.py) with `gemini_client` and test
19. Open [gemini/custom_client.py](gemini/custom_client.py) and implement all TODOs (raw HTTP client)
20. In [gemini_app.py](gemini/gemini_app.py) switch to `gemini_custom_client` and test

---

On top of that, you can explore Grok, DeepSeek, QWEN, LLAMA, and other OpenAI-compatible models using the OpenAI client 😵‍💫

**Congratulations 🎉 It wasn't easy, but now you know that AI APIs are not magic — they are plain REST (with SSE for streaming)!**
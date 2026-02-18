from t2_llms_output_tuning._clients.openai_responses_client import OpenAIResponsesClient
from t2_llms_output_tuning._main import run

# Responses API differences from Chat Completions:
#  - "messages" -> "input", "system" message -> "instructions" param
#  - "max_tokens" -> "max_output_tokens"
#  - "response_format" -> "text" param with format object
#  - "stop" is not available in Responses API
#  - built-in conversation state via "store" + "previous_response_id"
#  - "truncation" strategy for long contexts

# TODO 1: temperature — controls randomness. Range: 0.0-2.0, default: 1.0
#  Query: "Give me a name for a coffee shop"
#  Try: temperature=0.0 vs temperature=2.0, compare outputs

# TODO 2: top_p — nucleus sampling. Range: 0.0-1.0, default: 1.0
#  Query: "List 5 alternative uses for a paperclip"
#  Try: top_p=0.1 vs top_p=0.9

# TODO 3: max_output_tokens — max tokens in response (was "max_tokens" in Chat Completions)
#  Query: "Explain quantum computing"
#  Try: max_output_tokens=50 vs max_output_tokens=2048

# TODO 4: text — structured output format (replaces "response_format" from Chat Completions)
#  Uses text={"format": {...}} instead of response_format={...}
#  Query: "List 3 programming languages with their year of creation"
#  Try: text={"format": {"type": "json_schema", "name": "languages", "strict": True, "schema": {"type": "object", "properties": {"languages": {"type": "array", "items": {"type": "object", "properties": {"name": {"type": "string"}, "year": {"type": "integer"}}, "required": ["name", "year"], "additionalProperties": False}}}, "required": ["languages"], "additionalProperties": False}}}

# TODO 5: truncation — controls how long contexts are handled. Default: "disabled"
#  "auto" = drops older input messages to fit context window
#  Try: truncation="auto"

# TODO 6: metadata — attach key-value pairs to a response for tracking/filtering. Not available in Chat Completions
#  Up to 16 key-value pairs, keys up to 64 chars, values up to 512 chars
#  Try: metadata={"project": "demo", "user": "student-1"}

# TODO 7: reasoning — extended thinking config (replaces "reasoning_effort" from Chat Completions)
#  ⚠️ Note: does NOT work with non-default temperature
#  Query: "How many r's are in the word strawberry?"
#  Try: reasoning={"effort": "high"} vs reasoning={"effort": "low"}

run(
    client=OpenAIResponsesClient('gpt-5.2'),
    print_request=True, # Switch to False if you do not want to see the request in console
    print_only_content=False, # Switch to True if you want to see only content from response

)
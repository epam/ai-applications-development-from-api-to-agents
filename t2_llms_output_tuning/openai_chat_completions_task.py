from t2_llms_output_tuning._clients.openai_chat_completions_client import OpenAIChatCompletionsClient
from t2_llms_output_tuning._main import run

# TODO 1: n — number of completions to generate per request. Default: 1
#  ⚠️ Note: NOT available in Responses API
#  Query: "Give me a name for a coffee shop"
#  Try: n=3 — returns 3 different completions in choices[]

# TODO 2: temperature — controls randomness. Range: 0.0-2.0, default: 1.0
#  Lower = more deterministic, higher = more creative
#  Query: "Why white is white?"
#  Try: temperature=0.0 vs temperature=2.0, compare outputs
#  ⚠️ Note: it is okay that after temperature=1.5 you get some odd characters in output 😅

# TODO 3: top_p — nucleus sampling, keeps tokens within cumulative probability. Range: 0.0-1.0, default: 1.0
#  Lower = fewer token choices, more focused output
#  Query: "List 5 alternative uses for a paperclip"
#  Try: top_p=0.1 vs top_p=0.9

# TODO 4: max_tokens — max number of tokens in the response. Default: model-dependent
#  ⚠️ Note: Will work for models like gpt-4o. For gpt-5+ - `max_completion_tokens`.
#  Query: "Explain quantum computing"
#  Try: max_tokens=50 vs max_tokens=2048

# TODO 5: stop — list of strings (up to 4) that stop generation when encountered
#  ⚠️ Note: Will work for models like gpt-4o
#  Query: "Count from 1 to 20, comma separated"
#  Try: stop=["5"] — generation stops before reaching 5

# TODO 6: response_format — enforce structured output format
#  "text" (default) or "json_schema" with a schema definition
#  Query: "List 3 programming languages with their year of creation"
#  Try: response_format={"type": "json_schema", "json_schema": {"name": "languages", "strict": True, "schema": {"type": "object", "properties": {"languages": {"type": "array", "items": {"type": "object", "properties": {"name": {"type": "string"}, "year": {"type": "integer"}}, "required": ["name", "year"], "additionalProperties": False}}}, "required": ["languages"], "additionalProperties": False}}}

# TODO 7: frequency_penalty — penalizes tokens based on how often they appeared so far. Range: -2.0 to 2.0, default: 0
#  ⚠️ Note: Will work for models like gpt-4o
#  Positive = reduces repetition, negative = encourages repetition
#  Query: "Write a paragraph about the ocean"
#  Try: frequency_penalty=0.0 vs frequency_penalty=1.5

# TODO 8: presence_penalty — penalizes tokens based on whether they appeared at all. Range: -2.0 to 2.0, default: 0
#  ⚠️ Note: Will work for models like gpt-4o
#  Positive = encourages new topics, negative = stays on topic
#  Query: "Write a paragraph about the ocean"
#  Try: presence_penalty=0.0 vs presence_penalty=1.5

# TODO 9: seed — attempts deterministic output. Same seed + same input = same output (best effort)
#  ⚠️ Note: Will work for models like gpt-4o
#  Query: "Give me a name for a coffee shop"
#  Try: seed=42 — run twice with the same seed and compare outputs

# TODO 10: reasoning_effort — controls how much thinking the model does. Values: "low", "medium", "high" (default)
#  Lower effort = faster, cheaper responses; higher = more thorough reasoning
#  ⚠️ Note: does NOT work with non-default temperature (must omit temperature or set to 1.0)
#  Query: "How many r's are in the word strawberry?"
#  Try: reasoning_effort="low" vs reasoning_effort="high"

run(
    client=OpenAIChatCompletionsClient(model_name='gpt-5.2'),
    print_request=True, # Switch to False if you do not want to see the request in console
    print_only_content=False, # Switch to True if you want to see only content from response


)

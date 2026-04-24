- ```brew install uv```
- ```uv init```: runs git init internally
- ```uv sync``` : it works with pyproject.toml  
    - it takes the python version defined in .python-version creates the venv
    - and install all the dependencies present in pyproject.toml
- ```git branch -m "main"``` : renaming branch from the existing name to main
- ```uv add langchain```    
- ```source .venv/bin/activate```
- ```uv add --dev ipykernel``` --->  after this run ```uv sync```
- ```uv add langchain```
- ```uv add langchain-openai``` 
- ```uv add langchain_openai```
- ```uv add langchain-core```

## Comparison Table

| Feature | Correct Format | Example Command/Code |
|---|---|---|
| Installation | Hyphenated (-) | uv add langchain-openai  |
| Importing | Underscored (_) | from langchain_openai import ChatOpenAI  |
## 💻  Project : Deploy Application as a Web Service with Render

server deploying an OpenAI chat model and a chain to tell a joke about a topic.

## 🛠️ Requirements : PYTHON Installation & Setup

### Python 3.10.0

`brew install pyenv`
`pyenv install 3.10.0`

switch to python 3.10.0

`pyenv local 3.10.0`

### 🌐 Create a virtual environment & activate the virtual environment :

**MacOS/Linux**:

```
python3 -m venv env
source env/bin/activate
```

**Windows**:

```
python -m venv env
.\env\Scripts\activate
```


### 🏗️ Installation:

#### Install Python 3.6 or higher

use pip3 on a Mac or Linux and pip on Windows

```
pip install -r requirements.txt
pip install langchain python-dotenv fastapi "langserve[all]" uvicorn sse_starlette
```

### Install [LangServe (server and client)](https://python.langchain.com/docs/langserve#installation)
`pip install "langserve[all]"`

### Install Server [uvicorn ASGI server](https://www.uvicorn.org/)
`pip install "uvicorn[standard]"`

### [Get an API key](https://platform.openai.com/account/api-keys)

### Set OpenAI API Key as an environment variable:

`export OPENAI_API_KEY='sk-brHeh...A39v5iXsM2'`

.env file:

```
OPENAI_API_KEY=sk-brHeh...A39v5iXsM2
```

### Start the server:
`uvicorn server:app --reload`

### Test the RESTAPI 

joke/invoke
```
curl --location --request POST 'http://localhost:8000/joke/invoke' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "input": {
            "topic": "cats"
        }
    }'

```
joke/batch

```
curl --location --request POST 'http://localhost:8000/joke/batch' \
    --header 'Content-Type: application/json' \
    --data-raw '{
        "inputs": [
            {"topic": "cats"},
            {"topic": "dogs"}
        ]
    }'
```

### Try the Playground & Docs :

`http://localhost:8000/joke/playground/`
`http://localhost:8000/openai/playground/`


### Display a [documentation](https://python.langchain.com/docs/langserve#docss)

`http://localhost:8000/docs`

### Deploy Live to [Render](https://docs.render.com/deploy-fastapi)

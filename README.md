# Vellum Python Library

[![pypi](https://img.shields.io/pypi/v/vellum-ai.svg)](https://pypi.python.org/pypi/vellum-ai)
![license badge](https://img.shields.io/github/license/vellum-ai/vellum-client-python)
[![fern shield](https://img.shields.io/badge/%F0%9F%8C%BF-SDK%20generated%20by%20Fern-brightgreen)](https://buildwithfern.com/?utm_source=vellum-ai/vellum-client-python/readme)

The Vellum Python SDK provides access to the Vellum API from python.


## API Docs
You can find Vellum's complete API docs at [docs.vellum.ai](https://docs.vellum.ai/api-reference/introduction/getting-started).

## Installation

```sh
pip install --upgrade vellum-ai
```

## Usage
Below is how you would invoke a deployed Prompt from the Vellum API. For a complete list of all APIs
that Vellum supports, check out our [API Reference](https://docs.vellum.ai/api-reference/introduction/getting-started).

```python
from vellum import (
    StringInputRequest,
)
from vellum.client import Vellum

client = Vellum(
    api_key="YOUR_API_KEY",
)

def execute() -> str:
    result = client.execute_prompt(
        prompt_deployment_name="<example-deployment-name>>",
        release_tag="LATEST",
        inputs=[
            StringInputRequest(
                name="input_a",
                type="STRING",
                value="Hello, world!",
            )
        ],
    )
    
    if result.state == "REJECTED":
        raise Exception(result.error.message)

    return result.outputs[0].value

if __name__ == "__main__":
    print(execute())
```

> [!TIP]
> You can set a system environment variable `VELLUM_API_KEY` to avoid writing your api key within your code. To do so, add `export VELLUM_API_KEY=<your-api-token>`
> to your ~/.zshrc or ~/.bashrc, open a new terminal, and then any code calling `vellum.Vellum()` will read this key.

## Async Client
This SDK has an async version. Here's how to use it:



```python
import asyncio

import vellum
from vellum.client import AsyncVellum

client = AsyncVellum(api_key="YOUR_API_KEY")

async def execute() -> str:
    result = await client.execute_prompt(
        prompt_deployment_name="<example-deployment-name>>",
        release_tag="LATEST",
        inputs=[
            vellum.StringInputRequest(
                name="input_a",
                value="Hello, world!",
            )
        ],
    )

    if result.state == "REJECTED":
        raise Exception(result.error.message)
    
    return result.outputs[0].value

if __name__ == "__main__":
    print(asyncio.run(execute()))
```

## Contributing

While we value open-source contributions to this SDK, most of this library is generated programmatically.

Please feel free to make contributions to any of the directories or files below:
```plaintext
examples/*
src/vellum/lib/*
tests/*
README.md
```

Any additions made to files beyond those directories and files above would have to be moved over to our generation code
(found in the separate [vellum-client-generator](https://github.com/vellum-ai/vellum-client-generator) repo),
otherwise they would be overwritten upon the next generated release. Feel free to open a PR as a proof of concept,
but know that we will not be able to merge it as-is. We suggest opening an issue first to discuss with us!

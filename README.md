# Powertools Autodoc Proposal

I had a discussion with [Heitor Lessa](https://twitter.com/heitor_lessa), the mad genius behind AWS Powertools, on GitHub (in [this issue](https://github.com/awslabs/aws-lambda-powertools-python/issues/1236#issuecomment-1156886330)) about auto-generating README docs with Powertools. Heitor, I know I promised this to you again recently at re:Invent - so here is me delivering on that promise :) The idea is that we would generate required Input arguments for a particular Lambda function based on Pydantic models that are used for [event_parser utility](https://awslabs.github.io/aws-lambda-powertools-python/2.3.0/utilities/parser/#parsing-events).

This would solve a pain point that I've encountered across multiple organizations, and especially with my current startup. Figuring out how to use someone else's Lambda function basically requires either (1) good examples by the author, or (2) reading the code. And if you are forced to use option 2, hopefully you aren't bad at reading the language of the Lambda function you are trying to call, or else you will waste a lot of time! This is a productivity killer, and I think Powertools can help everyone do it better.

I created a way of doing this that we use inside our startup, for Python based Lambda functions. There are lots of ways it can be improved, and I don't particularly like it. But it does auto-document Pydantic models and pump it into a README. I mentioned this to Heitor and promised to share my code with him so he could get a better picture of what "bad but functional" looks like.

I also shared my idea of [what amazing would look like](#what-amazing-would-look-like), to give you a picture of my hopes and dreams for how Lambda Powertools could solve this problem.

# Demo of our existing tool

Remember - it's not [what amazing would look like](#what-amazing-would-look-like), it's what "bad but functional" looks like.

It leverages the [jsonschema2md2](https://github.com/sbrunner/jsonschema2md2) project, which is a more well-maintained fork of the original [jsonschema2md](https://github.com/RalfG/jsonschema2md) project.

## Installation

* First, set up the dependencies. This installs pydantic and jsonschema2md2.

```bash
# Install dependencies
make setup-dev
````

* Note the contents of the `lambda_function/models.py` file, where we define our Pydantic model. Consider that 

```python
from pydantic import BaseModel


class InputModel(BaseModel):
    first_name: str
    last_name: str
    email: str 
    age: int
    role: str
```

* Now, run the script:

```bash
# Run the script
python3 ./generate_schema.py
```

* Observe how it creates two files inside the `lambda_function` folder:
  1. `input_arguments.md` - the markdown file that contains the arguments
  2. `input_schema.json` - the JSON schema for the input arguments

Here's what it looks like:

<details><summary>input_arguments.md</summary>

# Lambda Function (Input)

## Definitions

- <a id="definitions/InputModel"></a>**`InputModel`** *(object)*
  - **`first_name`** *(string)*
  - **`last_name`** *(string)*
  - **`email`** *(string)*
  - **`age`** *(integer)*
  - **`role`** *(string)*

  Examples:
  ```json
  {
      "first_name": "Leroy",
      "last_name": "Jenkins",
      "age": 42,
      "email": "leroyjenkins42@gmail.com",
      "role": "Admin"
  }
  ```

</details>

<details><summary>input_schema.md</summary>

```json
{
    "title": "Lambda Function (Input)",
    "definitions": {
        "InputModel": {
            "title": "InputModel",
            "type": "object",
            "properties": {
                "first_name": {
                    "title": "First Name",
                    "type": "string"
                },
                "last_name": {
                    "title": "Last Name",
                    "type": "string"
                },
                "email": {
                    "title": "Email",
                    "type": "string"
                },
                "age": {
                    "title": "Age",
                    "type": "integer"
                },
                "role": {
                    "title": "Role",
                    "type": "string"
                }
            },
            "required": [
                "first_name",
                "last_name",
                "email",
                "age",
                "role"
            ]
        }
    }
}
```

</details>

# What amazing would look like

Imagine a case where I use the Event Parser function with Powertools and my Pydantic Model, and it would generate:
1. An `input_arguments.md` file in the same directory
2. An `input_schema.json` file in the same directory

For example:

```python
from aws_lambda_powertools.utilities.parser import event_parser, BaseModel
from aws_lambda_powertools.utilities.typing import LambdaContext
from pydantic import Field
from typing import List, Optional

import json

example_1 = {
    "first_name": "Leroy",
    "last_name": "Jenkins",
    "age": 42,
    "email": "leroyjenkins42@gmail.com",
    "role": "Admin"
}


class InputModel(BaseModel):
    first_name: str = Field(description="The person's first name", example="Leroy")
    last_name: str = Field(description="The person's last name", example="Jenkins")
    email: str = Field(description="The person's email address", example="leroyjenkins42@gmail.com")
    age: int = Field(description="The person's age", example=42)
    role: str = Field(description="The person's role", example="Admin", default="Admin", nullable=False)

    class Config:
        # If you use schema_extra.examples under Model Config, it will show up in the JSON Schema which gets passed down to the Markdown file
        schema_extra = {
            'examples': [
                example_1,
            ]
        }


@event_parser(model=InputModel)
def handler(event: InputModel, context: LambdaContext):
    print(event.id)
    print(event.description)
    print(event.items)

    order_items = [item for item in event.items]
    ...

handler(event=example_1, context=LambdaContext())
```

Then there could be a command like this that would generate the documentation in the same directory (or optionally in a different directory):

```bash
powertools-autodoc
```

The command would generate a README.md that looks like this:

<details><summary>Click to see README example</summary>

# Lambda Function Arguments

| Key          | Type   | Description                | Default | Required | Example                    |
|--------------|--------|----------------------------|---------|----------|----------------------------|
| `first_name` | string | The person's first name    |         | **True** | `Leroy`                    |
| `last_name`  | string | The person's last name     |         | **True** | `Jenkins`                  |
| `email`      | string | The person's email address |         | **True** | `leroyjenkins42@gmail.com` |
| `age`        | int    | The person's age           |         | False    | `42`                       |
| `role`       | string | The person's role          | `Admin` | **True** | `Admin`                    |


</details>

Notes:
* `Description` could be based on `description` if the `Field` type is used
* `Required` could be generated based on `nullable` in Pydantic
* `Default` could be generated based on `default` in Pydantic


## Including Examples in the Output

If you include `schema_extra.examples` under [Model Config](https://docs.pydantic.dev/usage/model_config/), when you generate the JSON Schema, it will show up in the JSON Schema examples. This is similar to how you can use [extend_schema_serializer in drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/customization.html#step-4-extend-schema-serializer) to include example payloads in the generated OpenAPI config. 

```python
from pydantic import BaseModel

example_1 = {
    "first_name": "Leroy",
    "last_name": "Jenkins",
    "age": 42,
    "email": "leroyjenkins42@gmail.com",
    "role": "Admin"
}


class InputModel(BaseModel):
    first_name: str
    last_name: str
    email: str
    age: int
    role: str

    class Config:
        # 
        schema_extra = {
            'examples': [
                example_1,
            ]
        }
```

When you use this, the generated JSON Schema now includes example payloads:

```json
{
    "title": "Lambda Function (Input)",
    "definitions": {
        "InputModel": {
            "title": "InputModel",
            "type": "object",
            "properties": { "//comment":  "truncated for brevity. See examples on the next line."},
            "examples": [
                {
                    "first_name": "Leroy",
                    "last_name": "Jenkins",
                    "age": 42,
                    "email": "leroyjenkins42@gmail.com",
                    "role": "Admin"
                }
            ]
        }
    }
}
```

# Wrapping it up

I know that was a lot of information! I hope this helps, and I'm happy to answer any questions about this proposal. Feel free to tag me on the 


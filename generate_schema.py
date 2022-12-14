#!/usr/bin/env python
import os
import json

from pydantic.schema import schema
import jsonschema2md2

from lambda_function.models import InputModel


def generate_json_schema(model, input_or_output: str, title: str, directory: str):
    """Generate JSON schema from Pydantic model."""
    # Generate JSONSchema file from Pydantic model
    top_level_schema = schema([model], title=title)
    schema_file = os.path.join(directory, f"{input_or_output}_schema.json")
    md_file = os.path.join(directory, f"{input_or_output}_arguments.md")
    if os.path.exists(schema_file):
        os.remove(schema_file)

    # Write the JSON Schema file to the destination directory
    with open(schema_file, "w") as f:
        json.dump(top_level_schema, f, indent=4)

    # Create the Markdown lines from the JSON Schema using jsonschema2md2
    parser = jsonschema2md2.Parser(
        examples_as_yaml=False,
        show_examples="all",
    )
    with open(schema_file, "r") as json_file:
        md_lines = parser.parse_schema(json.load(json_file))
    print(''.join(md_lines))

    # Write the Markdown file that specifies the Lambda function arguments to arguments.md
    if os.path.exists(md_file):
        os.remove(md_file)
    with open(md_file, "w") as f:
        f.write(''.join(md_lines))


def main():
    # If you want to add on more input models, you have to copy/paste the code below and specify the new model and the new directory.
    generate_json_schema(
        model=InputModel,
        input_or_output="input",
        title="Lambda Function (Input)",
        directory=os.path.join(os.path.dirname(__file__), "lambda_function")
    )


if __name__ == '__main__':
    main()

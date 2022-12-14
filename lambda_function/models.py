from pydantic import BaseModel, Field

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

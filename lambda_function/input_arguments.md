# Lambda Function (Input)

## Definitions

- <a id="definitions/InputModel"></a>**`InputModel`** *(object)*
  - **`first_name`** *(string)*: The person's first name.
  - **`last_name`** *(string)*: The person's last name.
  - **`email`** *(string)*: The person's email address.
  - **`age`** *(integer)*: The person's age.
  - **`role`** *(string)*: The person's role. Default: `"Admin"`.

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


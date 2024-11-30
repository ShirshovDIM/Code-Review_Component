import requests
import json


def get_evrazgpt_response(user_prompt: str, 
                          system_context = "answer in english", 
                          max_tokens=1024, 
                          temperature=.3, 
                          return_json=False) -> str:
    url = "http://84.201.152.196:8020/v1/completions"
    headers = {
        "Authorization": "Df5OqALNrsio9ynQYqZgOoO5erPJrL2n",  # Replace with your actual API key
        "Content-Type": "application/json"
    }

    # Define the payload
    payload = {
        "model": "mistral-nemo-instruct-2407",
        "messages": [
            {
                "role": "system",
                "content": system_context 
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        "max_tokens": max_tokens,
        "temperature": temperature
    }



    response = requests.post(url, headers=headers, data=json.dumps(payload))
    content = response.json()["choices"][0]["message"]["content"]

    print(f"Status Code: {response.status_code}")

    if return_json: 
        with open('responce.json', 'w') as file :
            json.dump(response.json(), file) 

    return response.json()

print(get_evrazgpt_response("""You answer binary: 0 if the issue is false, 1 otherwise. No additional info needed. Do not explain anything. 
Analyze python code.  According to structure of class define whether this object matches adapter patterns or not. Source_code: class GetInfo: def init(self, obj, adapted_methods): self.obj = obj self.dict.update(adapted_methods) def getattr**(self, attr): return getattr(self.obj, attr) def original_dict(self): return self.obj.dict
""", "You answer binary: 0 if the issue is false, 1 otherwise. No additional info needed. Do not explain anything", ))

# print(get_evrazgpt_response("""convert the SQL DDL (data definition language) below in the set of sqlalchemy objects:

# -- Addresses Table
# CREATE TABLE addresses (
#     id BIGINT PRIMARY KEY,
#     first_name VARCHAR(100) NOT NULL,
#     last_name VARCHAR(100) NOT NULL,
#     city VARCHAR(100) NOT NULL,
#     country VARCHAR(100) NOT NULL,
#     zip_code VARCHAR(20) NOT NULL,
#     street_address VARCHAR(255) NOT NULL,
#     phone_number VARCHAR(20),
#     user_id BIGINT REFERENCES users(id),
#     created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
#     updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
# );

# -- Categories Table
# CREATE TABLE categories (
#     id BIGINT PRIMARY KEY,
#     name VARCHAR(100) NOT NULL,
#     slug VARCHAR(100) UNIQUE NOT NULL,
#     description TEXT,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );

# -- Comments Table
# CREATE TABLE comments (
#     id BIGINT PRIMARY KEY,
#     content TEXT NOT NULL,
#     user_id BIGINT REFERENCES users(id),
#     product_id BIGINT REFERENCES products(id),
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );

# -- File Uploads Table
# CREATE TABLE file_uploads (
#     id BIGINT PRIMARY KEY,
#     type VARCHAR(50),
#     file_path VARCHAR(255) NOT NULL,
#     file_name VARCHAR(100) NOT NULL,
#     file_size BIGINT NOT NULL,
#     original_name VARCHAR(255),
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     tag_id BIGINT REFERENCES tags(id),
#     product_id BIGINT REFERENCES products(id),
#     category_id BIGINT REFERENCES categories(id)
# );

# -- Orders Table
# CREATE TABLE orders (
#     id BIGINT PRIMARY KEY,
#     order_status VARCHAR(50) NOT NULL,
#     tracking_number VARCHAR(100),
#     address_id BIGINT REFERENCES addresses(id),
#     user_id BIGINT REFERENCES users(id),
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );

# -- Order Items Table
# CREATE TABLE order_items (
#     id BIGINT PRIMARY KEY,
#     order_id BIGINT REFERENCES orders(id),
#     product_id BIGINT REFERENCES products(id),
#     price DECIMAL(10, 2) NOT NULL,
#     quantity SMALLINT NOT NULL,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );

# -- Products Table
# CREATE TABLE products (
#     id BIGINT PRIMARY KEY,
#     name VARCHAR(100) NOT NULL,
#     slug VARCHAR(100) UNIQUE NOT NULL,
#     description TEXT NOT NULL,
#     price DECIMAL(10, 2) NOT NULL,
#     stock INT NOT NULL,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     publish_on TIMESTAMP
# );

# -- Roles Table
# CREATE TABLE roles (
#     id BIGINT PRIMARY KEY,
#     name VARCHAR(50) NOT NULL,
#     description VARCHAR(255),
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );

# -- User Roles Table
# CREATE TABLE user_roles (
#     user_id BIGINT REFERENCES users(id),
#     role_id BIGINT REFERENCES roles(id),
#     PRIMARY KEY (user_id, role_id)
# );

# -- Tags Table
# CREATE TABLE tags (
#     id BIGINT PRIMARY KEY,
#     name VARCHAR(100) NOT NULL,
#     slug VARCHAR(100) UNIQUE NOT NULL,
#     description TEXT,
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );

# -- Users Table
# CREATE TABLE users (
#     id BIGINT PRIMARY KEY,
#     username VARCHAR(50) UNIQUE NOT NULL,
#     email VARCHAR(100) UNIQUE NOT NULL,
#     password VARCHAR(255) NOT NULL,
#     first_name VARCHAR(100),
#     last_name VARCHAR(100),
#     created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );""",
# system_context="""assume that you are proficient Python coder. You have string expertise in SQLAlchemy python library. You can only code. Do not explain anything""" ,
# return_json = True))
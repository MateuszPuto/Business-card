from fastapi import FastAPI, Request
# We remove 'Request' from the import and use Pydantic/Dict for body parsing
# from fastapi import Request 
from json import dumps, loads
# We will use Dict[str, Any] for the Pydantic-like body structure
from typing import Dict, Any 
import os
from fastapi.middleware.cors import CORSMiddleware


# 1. INITIALIZE THE APP ONLY ONCE
app = FastAPI()

# Define origins that are allowed to access your API
# NOTE: The client side is likely running on http://localhost:8080 or similar. 
# We add both the backend port (8000) and a common frontend port (8080)
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://localhost:8080", # Ensure your frontend address is listed here
    "http://0.0.0.0:8000",
]

# 2. ADD MIDDLEWARE CORRECTLY
app.add_middleware(
    CORSMiddleware,
    # FIX: Pass the list directly (not a list containing the list)
    allow_origins=origins, 
    allow_credentials=True,
    # OPTIONS must be included here to handle the preflight request
    allow_methods=["OPTIONS", "POST", "GET"], 
    allow_headers=["*"], 
)


FILE_PATH = "data_log.json"

# Function to save new data, overwriting the file
def overwrite_json_file(data: dict):
    """Writes a Python dictionary to the specified file path, overwriting existing content."""
    # Open the file in 'w' (write) mode. 
    with open(FILE_PATH, 'w') as f:
        # Use dumps() to convert the Python dictionary to a formatted JSON string
        f.write(dumps(data, indent=4)) 

# The endpoint now expects a JSON body directly, letting FastAPI handle parsing errors.
# FastAPI will automatically return a 422 (Unprocessable Entity) or a 400 if the body is invalid, 
# which is generally cleaner than catching generic exceptions.
@app.post("/submit")
@app.post("/submit/")
async def save_json_to_file(data: Dict[str, Any]):
    try:
        # 1. FastAPI has already parsed the body into the 'data' dictionary for us.
        
        # Log keys for successful debugging
        print(f">>> Data Received Successfully! Keys: {data.keys()}")
        
        # 2. Call the function to overwrite the file
        overwrite_json_file(data)
        
        # 3. Return a success response
        return {"message": "JSON data successfully **overwritten** to file.", 
                "received_data_domain": data.get('domain', 'N/A')}
        
    except Exception as e:
        # This catch block is now mainly for file writing errors, not parsing errors.
        print(f"Error processing request: {e}")
        # When using automatic body parsing, FastAPI handles the 400/422 status codes for parsing errors.
        # This return path is mostly for internal server errors (500).
        return {"message": f"Internal Server Error: Could not save data. Details: {e}"}, 500

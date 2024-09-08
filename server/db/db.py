import os
# from dotenv import load_dotenv
from supabase import create_client, Client
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
import uuid
import logging
from datetime import datetime, UTC
import json

# Load environment variables
# load_dotenv()

# Initialize Supabase client
url: str = os.environ["SUPABASE_URL"]
key: str = os.environ["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# Define the script collection
script_collection = supabase.table("scripts")

# Add logging near the top of the file
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Define the Script model
class Script(BaseModel):
    script_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    name: str
    user_id: str
    author: str = "AI Generated"
    description: str = ""
    script: str
    recording_base64: str
    version: str = "1.0"
    input_json_schema: str
    output_json_schema: str


# Function to create a new script
def create_script(
    name: str,
    script: str,
    user_id: str,
    recording_base64: str,
    input_json_schema: str,
    output_json_schema: str,
    description: str = "",
    author: str = "AI Generated",
    version: str = "1.0",
) -> Script:
    script_data = Script(
        name=name,
        script=script,
        user_id=user_id,
        description=description,
        author=author,
        version=version,
        recording_base64=recording_base64,
        input_json_schema=input_json_schema,
        output_json_schema=output_json_schema,
    )
    try:
        logger.info(
            f"Attempting to insert script with id: {script_data.script_id} and name {script_data.name}"
        )
        # Convert the model to a dictionary and format the datetime
        insert_data = script_data.model_dump()
        insert_data["created_at"] = insert_data["created_at"].isoformat()
        result = script_collection.insert(insert_data).execute()
        return Script(**result.data[0])
    except Exception as e:
        logger.error(f"Error inserting script: {str(e)}")
        raise


# Function to get all scripts
def get_all_scripts():
    return script_collection.select("*").execute()


# Function to get a specific script by id
def get_script_by_id(script_id: str) -> Optional[Script]:
    result = script_collection.select("*").eq("script_id", script_id).single().execute()
    if result.data:
        return Script(**result.data)
    return None


# Function to update a script
def update_script(
    script_id: str,
    user_id: str,
    script: Optional[str] = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
    author: Optional[str] = None,
    version: Optional[str] = None,
) -> Optional[Script]:
    update_data = {"user_id": user_id}
    if script is not None:
        update_data["script"] = script
    if name is not None:
        update_data["name"] = name
    if description is not None:
        update_data["description"] = description
    if author is not None:
        update_data["author"] = author
    if version is not None:
        update_data["version"] = version

    result = script_collection.update(update_data).eq("script_id", script_id).execute()
    return Script(**result.data[0]) if result.data else None


# Function to delete a script
def delete_script(script_id: str):
    return script_collection.delete().eq("script_id", script_id).execute()

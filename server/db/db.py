import os
from dotenv import load_dotenv
from supabase import create_client, Client
from typing import Optional

# Load environment variables
load_dotenv()

# Initialize Supabase client
url: str = os.environ["SUPABASE_URL"]
key: str = os.environ["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# Define the script collection
script_collection = supabase.table("scripts")


# Function to create a new script
def create_script(
    name: str,
    content: str,
    language: str,
    description: str = "",
    author: str = "AI Generated",
    display_name: str = "",
    version: str = "1.0",
):
    return script_collection.insert(
        {
            "name": name,
            "content": content,
            "language": language,
            "description": description,
            "author": author,
            "display_name": display_name or name.replace("_", " ").title(),
            "version": version,
        }
    ).execute()


# Function to get all scripts
def get_all_scripts():
    return script_collection.select("*").execute()


# Function to get a specific script by name
def get_script_by_name(name: str):
    return script_collection.select("*").eq("name", name).single().execute()


# Function to update a script
def update_script(
    name: str,
    content: Optional[str] = None,
    language: Optional[str] = None,
    description: Optional[str] = None,
    author: Optional[str] = None,
    display_name: Optional[str] = None,
    version: Optional[str] = None,
):
    update_data = {}
    if content is not None:
        update_data["content"] = content
    if language is not None:
        update_data["language"] = language
    if description is not None:
        update_data["description"] = description
    if author is not None:
        update_data["author"] = author
    if display_name is not None:
        update_data["display_name"] = display_name
    if version is not None:
        update_data["version"] = version

    return script_collection.update(update_data).eq("name", name).execute()


# Function to delete a script
def delete_script(name: str):
    return script_collection.delete().eq("name", name).execute()

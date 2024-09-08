import datetime
import smtplib

def get_current_weather(location: str, unit: str = 'metric') -> dict:
    """
    Simulates retrieving current weather (returns sample data).
    """
    print(f"Fetching current weather for {location} in {unit} units...")
    # Simulated weather data
    return {
        'temperature': 20 if unit == 'metric' else 68,  # °C or °F
        'feels_like': 18 if unit == 'metric' else 64,
        'condition': 'Partly Cloudy',
        'humidity': 60,
        'wind_speed': 5
    }

def set_timer(duration: int) -> str:
    """
    Sets a timer for the specified duration in seconds (simulated for now).
    """
    print(f"Timer set for {duration} seconds!")
    # In a real implementation, you would use time.sleep(duration) or a scheduling library
    return "Timer set successfully!" 

def get_news(query: str, count: int = 5) -> list:
    """
    Simulates retrieving news (returns sample data).
    """
    print(f"Searching for news about '{query}' (up to {count} articles)...")
    # Simulated news data
    return [
        {
            'title': f"News Article {i+1} about {query}",
            'description': f"This is a brief description of the news article {i+1} related to {query}.",
            'url': f"https://www.example.com/news/{i+1}",
            'publishedAt': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')
        } for i in range(count)
    ]

def translate_text(text: str, target_language: str) -> str:
    """
    Simulates translation (returns the original text for now).
    """
    print(f"Translating '{text}' to {target_language}...")
    # In a real implementation, you would use a translation API or library
    return text  # Placeholder - replace with actual translation

def get_directions(origin: str, destination: str, mode: str = 'driving') -> dict:
    """
    Simulates getting directions (returns sample data).
    """
    print(f"Getting directions from {origin} to {destination} by {mode}...")
    # Simulated directions data
    return {
        'summary': f"Directions from {origin} to {destination}",
        'distance': '10 miles',
        'duration': '20 minutes',
        'steps': [
            'Start at {origin}',
            'Head north on Main Street',
            'Turn right onto Elm Street',
            'Arrive at {destination}'
        ]
    }

def set_reminder(datetime_str: str, message: str) -> str:
    """
    Sets a reminder for the given date and time with the specified message (simulated for now)
    """
    try:
        datetime_obj = datetime.datetime.fromisoformat(datetime_str)
        now = datetime.datetime.now()
        if datetime_obj <= now:
            return "Reminder date/time is in the past. Please provide a future date/time."

        time_diff = datetime_obj - now
        seconds_diff = time_diff.total_seconds()

        print(f"Reminder set for {datetime_str} with message: '{message}'")
        # In a real implementation, you would use a scheduling library or platform-specific reminder functionality
        # For now, we'll just simulate it with a print statement after the specified time
        # threading.Timer(seconds_diff, lambda: print(f"Reminder: {message}")).start() 

        return "Reminder set successfully!"
    except ValueError:
        return "Invalid datetime format. Please use ISO 8601 format (e.g., '2024-09-10T15:30:00')"

def search_web(query: str) -> list:
    """
    Simulates web search (returns sample data).
    """
    print(f"Searching the web for '{query}'...")
    # Simulated search results
    return [
        {
            'title': f"Search Result {i+1} for {query}",
            'description': f"This is a brief description of search result {i+1} for the query '{query}'.",
            'url': f"https://www.example.com/search?q={query}&result={i+1}"
        } for i in range(3)  # Return 3 sample results
    ]
    

functions = [
    {
        "name": "get_current_weather",
        "description": "Get the current weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA"
                },
                "unit": {
                    "type": "string",
                    "enum": ["metric", "imperial"],
                    "description": "The unit system to use for temperature"
                }
            },
            "required": ["location"]
        }
    },
    {
        "name": "get_forecast",
        "description": "Get a weather forecast for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA"
                },
                "days": {
                    "type": "integer",
                    "description": "Number of days to forecast",
                    "minimum": 1,
                    "maximum": 10
                },
                "unit": {
                    "type": "string",
                    "enum": ["metric", "imperial"],
                    "description": "The unit system to use for temperature"
                }
            },
            "required": ["location"]
        }
    },
    {
        "name": "set_timer",
        "description": "Set a timer for a specified duration",
        "parameters": {
            "type": "object",
            "properties": {
                "duration": {
                    "type": "integer",
                    "description": "Duration of the timer in seconds"
                }
            },
            "required": ["duration"]
        }
    },
    {
        "name": "get_news",
        "description": "Get news articles based on a query",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query for news articles"
                },
                "count": {
                    "type": "integer",
                    "description": "Number of articles to retrieve",
                    "minimum": 1,
                    "maximum": 10
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "translate_text",
        "description": "Translate text to a target language",
        "parameters": {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "The text to translate"
                },
                "target_language": {
                    "type": "string",
                    "description": "The target language code (e.g., 'es' for Spanish)"
                }
            },
            "required": ["text", "target_language"]
        }
    },
    {
        "name": "get_directions",
        "description": "Get directions between two locations",
        "parameters": {
            "type": "object",
            "properties": {
                "origin": {
                    "type": "string",
                    "description": "Starting location"
                },
                "destination": {
                    "type": "string",
                    "description": "Ending location"
                },
                "mode": {
                    "type": "string",
                    "enum": ["driving", "walking", "bicycling", "transit"],
                    "description": "Mode of transportation"
                }
            },
            "required": ["origin", "destination"]
        }
    },
    {
        "name": "set_reminder",
        "description": "Set a reminder for a specific date and time",
        "parameters": {
            "type": "object",
            "properties": {
                "datetime_str": {
                    "type": "string",
                    "description": "Date and time for the reminder (ISO 8601 format)"
                },
                "message": {
                    "type": "string",
                    "description": "Reminder message"
                }
            },
            "required": ["datetime_str", "message"]
        }
    },
    {
        "name": "search_web",
        "description": "Perform a web search",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query"
                }
            },
            "required": ["query"]
        }
    }
]

    
import requests
from database import execute
import bcrypt

API_KEY = "001bc2b7c45f61072f64bb7164a656ae"

def get_weather_by_coordinates(lat: float, lon: float) -> dict:
    """Fetches weather data by coordinates from the OpenWeatherMap API."""
    params = {"lat": lat, "lon": lon, "appid": API_KEY, "units": "metric"}
    url = "https://api.openweathermap.org/data/2.5/weather"
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise error for non-200 response
    return response.json()

def get_weather_by_name(city_name: str) -> dict:
    """Fetches weather data by city name from the OpenWeatherMap API."""
    params = {"q": city_name, "appid": API_KEY, "units": "metric"}
    url = "https://api.openweathermap.org/data/2.5/weather"
    response = requests.get(url, params=params)
    response.raise_for_status()  # Raise error for non-200 response
    return response.json()

def print_weather(data: dict) -> None:
    """Prints weather data in a readable format."""
    print(
        f'City: {data["name"]}\nMax Temperature: {data["main"]["temp_max"]}°C\nMin Temperature: {data["main"]["temp_min"]}°C\nWind Speed: {data["wind"]["speed"]} m/s\n'
    )

def login(username: str, password: str) -> bool:
    """Logs in the user with the provided credentials."""
    stmt = """
    SELECT * FROM users WHERE username = ?;
    """
    user_data = execute(stmt, (username,), fetchone=True)
    if not user_data or not bcrypt.checkpw(password.encode('utf-8'), user_data["password"]):
        print("Wrong credentials!!!")
        return False
    return user_data["user_id"]

def register(username: str, password: str) -> None:
    """Registers a new user."""
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    stmt = """
    INSERT INTO users (username, password) VALUES (?, ?);
    """
    execute(stmt, (username, hashed_password), is_commitable=True)
    print("Registration successful!")

while True:
    print("""Hello!
          \nChoose:
          \n1. Log in
          \n2. Register
          \n3. Exit
          """)
    user_input = input("Choose: ")
    if user_input == "1":
        username = input("Enter username: ")
        password = input("Enter password: ")
        user_id, hashed_password = login(username, password)
        if user_id is not None:
            while True:
                print(f"Hello, {username}!\nChoose an option:\n1. Search by coordinates\n2. Search by name\n3. View search history\n4. Logout")
                user_input = input("Choose: ")
                if user_input == "1":
                    lat = float(input("Enter latitude: "))
                    lon = float(input("Enter longitude: "))
                    weather_data = get_weather_by_coordinates(lat, lon)
                    print_weather(weather_data)
                    # Store search history
                    execute("INSERT INTO user_history (user_id, request) VALUES (?, ?);", (user_id, f"Coordinates: {lat}, {lon}"), is_commitable=True)
                elif user_input == "2":
                    city_name = input("Enter city name: ")
                    weather_data = get_weather_by_name(city_name)
                    print_weather(weather_data)
                    # Store search history
                    execute("INSERT INTO user_history (user_id, request) VALUES (?, ?);", (user_id, f"City: {city_name}"), is_commitable=True)
                elif user_input == "3":
                    # Retrieve and print search history
                    history = execute("SELECT request FROM user_history WHERE user_id = ?;", (user_id,), fetchall=True)
                    print("Search History:")
                    for item in history:
                        print(item["request"])
                elif user_input == "4":
                    break
                else:
                    print("Invalid input!")
    elif user_input == "2":
        username = input("Enter username: ")
        password = input("Enter password: ")
        register(username, password)
    elif user_input == "3":
        print("Exiting...")
        break
    else:
        print("Invalid input!")

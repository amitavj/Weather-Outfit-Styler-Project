import requests


# ==========================================
# 1. FIND THE CITY
# ==========================================

def find_city(city):

    url = "https://geocoding-api.open-meteo.com/v1/search"

    parameters = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json",
        "countryCode": "CA"
    }

    response = requests.get(url, params=parameters)

    if response.status_code != 200:
        return None

    data = response.json()

    if "results" not in data:
        return None

    return data["results"][0]


# ==========================================
# 2. GET THE WEATHER
# ==========================================

def get_weather(latitude, longitude):

    url = "https://api.open-meteo.com/v1/forecast"

    parameters = {
        "latitude": latitude,
        "longitude": longitude,

        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_probability_max",
            "snowfall_sum"
        ],

        "hourly": [
            "wind_speed_10m"
        ],

        "temperature_unit": "celsius",
        "wind_speed_unit": "kmh",
        "forecast_days": 7,

        "timezone": "auto"
    }

    response = requests.get(url, params=parameters)

    if response.status_code != 200:
        return None

    return response.json()


# ==========================================
# 3. DECIDE WHAT TO WEAR
# ==========================================

def choose_outfit(high, low, rain, snow, wind):

    clothes = []
    reasons = []

    # -------------------------
    # TEMPERATURE
    # -------------------------

    if high <= -10:

        clothes.append("heavy winter coat")
        clothes.append("warm sweater")
        clothes.append("thermal pants")
        clothes.append("winter boots")
        clothes.append("gloves")
        clothes.append("hat")

        reasons.append("It is extremely cold.")

    elif high <= 0:

        clothes.append("winter coat")
        clothes.append("hoodie or sweater")
        clothes.append("warm pants")
        clothes.append("winter boots")

        reasons.append("It is below freezing.")

    elif high <= 8:

        clothes.append("winter jacket")
        clothes.append("hoodie")
        clothes.append("pants")
        clothes.append("closed-toe shoes")

        reasons.append("It is chilly.")

    elif high <= 15:

        clothes.append("light jacket or hoodie")
        clothes.append("long pants")
        clothes.append("closed-toe shoes")

        reasons.append("The temperature is cool.")

    elif high <= 20:

        clothes.append("hoodie or light sweater")
        clothes.append("pants")
        clothes.append("sneakers")

        reasons.append("The temperature is mild.")

    elif high <= 25:

        clothes.append("t-shirt")
        clothes.append("pants or shorts")
        clothes.append("sneakers")

        reasons.append("The temperature is comfortable.")

    elif high <= 30:

        clothes.append("t-shirt")
        clothes.append("shorts")
        clothes.append("sneakers")

        reasons.append("It is warm.")

    else:

        clothes.append("light t-shirt")
        clothes.append("shorts")
        clothes.append("breathable shoes")

        reasons.append("It is very hot.")


    # -------------------------
    # RAIN
    # -------------------------

    if rain >= 60:

        clothes.append("raincoat")

        reasons.append("There is a high chance of rain.")

    elif rain >= 30:

        clothes.append("water-resistant jacket")

        reasons.append("There is a moderate chance of rain.")


    # -------------------------
    # SNOW
    # -------------------------

    if snow > 0:

        clothes.append("winter boots")

        if "winter coat" not in clothes:
            clothes.append("warm coat")

        reasons.append("Snow is expected.")


    # -------------------------
    # WIND
    # -------------------------

    if wind >= 30:

        clothes.append("wind-resistant outer layer")

        reasons.append("It will be quite windy.")

    elif wind >= 20 and high <= 15:

        clothes.append("windbreaker")

        reasons.append("The wind will make the cool temperature feel colder.")


    return clothes, reasons


# ==========================================
# 4. MAIN PROGRAM
# ==========================================

print("======================================")
print("       ONTARIO OUTFIT AI")
print("======================================")

city = input("\nEnter your Ontario city: ")

location = find_city(city)

if location is None:

    print("\nSorry, I couldn't find that city.")
    print("Try something like Toronto, Brampton, Ottawa, Hamilton, or Mississauga.")

else:

    latitude = location["latitude"]
    longitude = location["longitude"]
    city_name = location["name"]

    print("\nGetting weather for", city_name + "...")

    weather = get_weather(latitude, longitude)

    if weather is None:

        print("Sorry, I couldn't get the weather.")

    else:

        dates = weather["daily"]["time"]

        high_temps = weather["daily"]["temperature_2m_max"]
        low_temps = weather["daily"]["temperature_2m_min"]
        rain_chances = weather["daily"]["precipitation_probability_max"]
        snowfall = weather["daily"]["snowfall_sum"]

        wind_speeds = weather["hourly"]["wind_speed_10m"]


        print("\n")
        print("======================================")
        print("       YOUR 7-DAY OUTFIT PLAN")
        print("======================================")


        for day in range(7):

            date = dates[day]

            high = high_temps[day]
            low = low_temps[day]
            rain = rain_chances[day]
            snow = snowfall[day]

            # Get the average wind for that day
            start = day * 24
            end = start + 24

            daily_winds = wind_speeds[start:end]

            wind = sum(daily_winds) / len(daily_winds)


            clothes, reasons = choose_outfit(
                high,
                low,
                rain,
                snow,
                wind
            )


            print("\n--------------------------------------")
            print("DATE:", date)
            print("--------------------------------------")

            print("High:", round(high), "°C")
            print("Low:", round(low), "°C")
            print("Rain chance:", rain, "%")
            print("Snow:", round(snow, 1), "cm")
            print("Average wind:", round(wind), "km/h")

            print("\nAI RECOMMENDS:")

            for item in clothes:
                print("  ✓", item)

            print("\nWHY:")

            for reason in reasons:
                print("  →", reason)


print("\n")
print("======================================")
print("        HAVE A GOOD DAY!")
print("======================================")
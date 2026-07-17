import requests

# Overpass API
OVERPASS_URL = "https://overpass-api.de/api/interpreter"


def find_autism_hospitals(location):
    """
    Search autism-specific hospitals near a location.
    If none are found, return nearby hospitals.
    """

    # -----------------------------
    # Step 1: Convert location to latitude & longitude
    # -----------------------------
    geo_url = "https://nominatim.openstreetmap.org/search"

    geo_params = {
        "q": location,
        "format": "json",
        "limit": 1
    }

    headers = {
        "User-Agent": "AutismPredictionSystem/1.0"
    }

    try:
        geo_response = requests.get(
            geo_url,
            params=geo_params,
            headers=headers,
            timeout=20
        )

        geo_response.raise_for_status()
        geo_data = geo_response.json()

    except requests.exceptions.RequestException as e:
        print("Geocoding Error:", e)
        return [], False

    except ValueError:
        print("Invalid response from Nominatim.")
        return [], False

    if not geo_data:
        return [], False

    lat = geo_data[0]["lat"]
    lon = geo_data[0]["lon"]

    # -----------------------------
    # Step 2: Search nearby hospitals
    # -----------------------------
    query = f"""
    [out:json];
    (
      node(around:15000,{lat},{lon})["amenity"="hospital"];
      way(around:15000,{lat},{lon})["amenity"="hospital"];
      relation(around:15000,{lat},{lon})["amenity"="hospital"];
    );
    out center tags;
    """

    try:
        response = requests.post(
            OVERPASS_URL,
            data=query,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        try:
            data = response.json()

        except ValueError:
            print("Overpass returned invalid JSON.")
            print(response.text[:500])
            return [], False

    except requests.exceptions.RequestException as e:
        print("Overpass API Error:", e)
        return [], False

    # -----------------------------
    # Autism-related keywords
    # -----------------------------
    AUTISM_KEYWORDS = [
        "autism",
        "asd",
        "child development",
        "developmental",
        "development center",
        "development centre",
        "behavioral",
        "behavioural",
        "speech therapy",
        "occupational therapy",
        "special child",
        "neurology",
        "neuro",
        "pediatric",
        "paediatric"
    ]

    hospitals = []

    # -----------------------------
    # Step 3: Search autism-specific hospitals
    # -----------------------------
    for place in data.get("elements", []):

        tags = place.get("tags", {})
        name = tags.get("name", "")

        if not name:
            continue

        if not any(keyword in name.lower() for keyword in AUTISM_KEYWORDS):
            continue

        address = ", ".join(filter(None, [
            tags.get("addr:street"),
            tags.get("addr:city"),
            tags.get("addr:state")
        ]))

        if "lat" in place:
            place_lat = place["lat"]
            place_lon = place["lon"]
        else:
            center = place.get("center", {})
            place_lat = center.get("lat")
            place_lon = center.get("lon")

        hospitals.append({
            "name": name,
            "address": address or "Address not available",
            "map": f"https://www.openstreetmap.org/?mlat={place_lat}&mlon={place_lon}#map=17/{place_lat}/{place_lon}"
        })

    # -----------------------------
    # Step 4: If none found,
    # show all nearby hospitals
    # -----------------------------
    fallback = False

    if not hospitals:

        fallback = True

        for place in data.get("elements", []):

            tags = place.get("tags", {})
            name = tags.get("name", "")

            if not name:
                continue

            address = ", ".join(filter(None, [
                tags.get("addr:street"),
                tags.get("addr:city"),
                tags.get("addr:state")
            ]))

            if "lat" in place:
                place_lat = place["lat"]
                place_lon = place["lon"]
            else:
                center = place.get("center", {})
                place_lat = center.get("lat")
                place_lon = center.get("lon")

            hospitals.append({
                "name": name,
                "address": address or "Address not available",
                "map": f"https://www.openstreetmap.org/?mlat={place_lat}&mlon={place_lon}#map=17/{place_lat}/{place_lon}"
            })

    # -----------------------------
    # Remove duplicate hospitals
    # -----------------------------
    unique_hospitals = []
    seen = set()

    for hospital in hospitals:

        key = hospital["name"].strip().lower()

        if key not in seen:
            seen.add(key)
            unique_hospitals.append(hospital)

    # -----------------------------
    # Return first 10 hospitals
    # -----------------------------
    return unique_hospitals[:10], fallback
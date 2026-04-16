import os
from datetime import datetime
from flask import Flask, jsonify, render_template
from dotenv import load_dotenv
from azure.cosmos import CosmosClient

load_dotenv()

app = Flask(__name__)

COSMOS_ENDPOINT = os.getenv("COSMOS_ENDPOINT")
COSMOS_KEY = os.getenv("COSMOS_KEY")
COSMOS_DATABASE = os.getenv("COSMOS_DATABASE", "CanalDB")
COSMOS_CONTAINER = os.getenv("COSMOS_CONTAINER", "SensorData")

client = CosmosClient(COSMOS_ENDPOINT, credential=COSMOS_KEY)
database = client.get_database_client(COSMOS_DATABASE)
container = database.get_container_client(COSMOS_CONTAINER)

LOCATIONS = ["Dow's Lake", "Fifth Avenue", "NAC"]


def safe_status_class(status: str) -> str:
    status = (status or "").lower()
    if status == "safe":
        return "safe"
    if status == "caution":
        return "caution"
    return "unsafe"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/dashboard")
def dashboard_data():
    query = """
    SELECT * FROM c
    ORDER BY c.windowEnd DESC
    """

    items = list(
        container.query_items(
            query=query,
            enable_cross_partition_query=True
        )
    )

    latest_by_location = {}
    history_by_location = {location: [] for location in LOCATIONS}

    for item in items:
        location = item.get("location")
        if location not in LOCATIONS:
            continue

        if location not in latest_by_location:
            latest_by_location[location] = {
                "location": location,
                "windowEnd": item.get("windowEnd"),
                "avgIceThickness": item.get("avgIceThickness"),
                "avgSurfaceTemp": item.get("avgSurfaceTemp"),
                "maxSnowAccumulation": item.get("maxSnowAccumulation"),
                "avgExternalTemp": item.get("avgExternalTemp"),
                "readingCount": item.get("readingCount"),
                "safetyStatus": item.get("safetyStatus"),
                "statusClass": safe_status_class(item.get("safetyStatus")),
            }

        if len(history_by_location[location]) < 12:
            history_by_location[location].append({
                "windowEnd": item.get("windowEnd"),
                "avgIceThickness": item.get("avgIceThickness"),
                "avgSurfaceTemp": item.get("avgSurfaceTemp"),
                "safetyStatus": item.get("safetyStatus")
            })

        if len(latest_by_location) == len(LOCATIONS) and all(
            len(history_by_location[loc]) >= 12 for loc in LOCATIONS
        ):
            break

    latest_cards = []
    for location in LOCATIONS:
        latest_cards.append(
            latest_by_location.get(
                location,
                {
                    "location": location,
                    "windowEnd": None,
                    "avgIceThickness": None,
                    "avgSurfaceTemp": None,
                    "maxSnowAccumulation": None,
                    "avgExternalTemp": None,
                    "readingCount": 0,
                    "safetyStatus": "No Data",
                    "statusClass": "unsafe",
                },
            )
        )

    # Oldest to newest for chart display
    for location in LOCATIONS:
        history_by_location[location].reverse()

    return jsonify({
        "latest": latest_cards,
        "history": history_by_location,
        "generatedAt": datetime.utcnow().isoformat() + "Z"
    })


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
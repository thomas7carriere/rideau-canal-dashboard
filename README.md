## Dashboard Repository

## Overview

The Rideau Canal Safety Monitoring Dashboard is a web-based application that visualizes real-time environmental sensor data collected from simulated canal locations. The dashboard retrieves aggregated data from Azure Cosmos DB and displays ice safety conditions using charts, status indicators, and location-specific data cards. The system supports continuous monitoring of ice conditions and provides an interface for viewing safety status from multiple locations.

**Dashboard Features:**
- Real-time data display for three locations
- Safety status classification (Safe, Caution, Unsafe)
- Automatic data refresh every 30 seconds
- Historical trend visualization for the last hour
- Visual indicators for ice safety conditions

**Technologies Used**
- Python
- Flask
- Azure Cosmos DB
- Azure App Service
- Azure Stream Analytics
- HTML / CSS / JavaScript
- Chart.js
- python-dotenv

## Prerequisites:
- Python
- Azure Cosmos DB (DB name: CanalDB, Container name: SensorData). If these values are different ensure the environment variables match.

## Configuration

The following environmental variables are required in a .env file:
```
COSMOS_ENDPOINT: https://your-cosmos-account.documents.azure.com:443/
COSMOS_KEY: your-primary-key
COSMOS_DATABASE: CanalDB
COSMOS_CONTAINER: SensorData
```

## API Endpoints

- GET / -> returns the dashboard interface (HTML page)
- GET /api/dashboard -> Retrieves the latest sensor data and records from Cosmos DB. This endpoint is used by the dashboard to update itself.
**Response Example**
```
{
  "latest": [
    {
      "location": "Dow's Lake",
      "avgIceThickness": 24.6,
      "avgSurfaceTemp": -6.2,
      "maxSnowAccumulation": 1.4,
      "readingCount": 28,
      "safetyStatus": "Caution"
    }
  ],
  "history": {
    "Dow's Lake": []
  }
}
```

## Deployment 

**Running Locally**
1. If running locally, the environment variables can be configured in a .env file in the project directory.
2. Install the necessary requirements using pip and run app.py in the directory of the application.
3. Access the dashboard at http://localhost:5000/

**Running on Azure App Service**
1. If deploying to Azure App Service, these can be configured in the environment variables menu in the App Service dashboard.
2. To run on Azure App Service, fork this repository and provide it as the deployment source for your Azure Web App. 
3. Configure your environment variables and set the proper startup command "gunicorn -w 2 -b 0.0.0.0:$PORT app:app"

## Dashboard Features



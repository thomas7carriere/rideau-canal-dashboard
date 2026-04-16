## rideau-canal-dashboard

## Environmental Variables:

Requires the following environmental variables:

- COSMOS_ENDPOINT:
- COSMOS_KEY:
- COSMOS_DATABASE:
- COSMOS_CONTAINER:

## Installation and Deployment 

**Running Locally **
1. If running locally, the environment variables can be configured in a .env file in the project directory.
2. Install the necessary requirements using pip and run app.py in the directory of the application.
3. Access the dashboard at http://localhost:5000/

**Running on Azure App Service**
1. If deploying to Azure App Service, these can be configured in the environment variables menu in the App Service dashboard.
2. To run on Azure App Service, fork this repository and provide it as the deployment source for your Azure Web App. 
3. Configure your environment variables and set the proper startup command "gunicorn -w 2 -b 0.0.0.0:$PORT app:app"

## Dashboard Features
Real-time updates
Charts and visualizations
Safety status indicators

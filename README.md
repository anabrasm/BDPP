# Big Data for Public Policy Project
**Ana Brás Monteiro, Theodor Friederiszick, Carole Marullaz**

You can view this app here: [green-energy-innovation.fly.dev](https://green-energy-innovation.fly.dev/)

## Description
This web app is a visualizing tool that documents different trends regarding clean energy innovations across the world. Specifically, it displays the number of innovations in fossil fuel and renewable energy innovations, as well as their share in total energy innovations, for each country over the period 2000-2017. It uses a color scheme to allow for a global comparison of countries for each year and each measure. Additionally, users can conveniently look at the country-specific innovation trend for each type of measures by clicking on the country. 

## Project Structure

- `input/`: This directory contains a subset of the PATSTAT data that the project requires

- `src/`: This directory contains the Python scripts used for data cleaning, processing, and running the application:

  - `clean_data.py`: This script performs some initial processing on the raw data. It categorizes innovations by patent type and country, and does some basic computations and reshaping of the data. 
  
  - `process_data.py`: This script is responsible for preparing the data for visualization in the application. It converts country codes to match with the map, filters the relevant data and polishes the data so it is fully ready for the application. 
  
  - `run_app.py`: This script sets up and starts the Dash application. It uses the processed data to create the interactive visualizations.
  
  - `app_layout.py`: This file contains a function that sets up the layout of the Dash application. It is used by `run_app.py` to structure the user interface of the application.

## Run Locally

1. Ensure the project dependencies are installed
   -  [pipenv](https://pypi.org/project/pipenv/) 
   -  [make](https://www.gnu.org/software/make/)
2. Run the project:

   ```
   make
   ```
3. Access the project locally through http://localhost:8050/  


## Deployment

To deploy the application, you'll need access to the project on fly.io. 

To deploy the app, run the following [flyctl](https://fly.io/docs/hands-on/install-flyctl/) command: 

```shell
fly deploy 
```
# Big Data for Public Policy Project
**Ana Brás Monteiro, Theodor Friederiszick, Carole Marullaz**

You can view this app here: [green-energy-innovation.fly.dev](https://green-energy-innovation.fly.dev/)

## Description
This web app is a visualizing tool that documents different trends regarding clean energy innovations across the world. Specifically, it displays the number of innovations in fossil fuel and renewable energy innovations, as well as their share in total energy innovations, for each country over the period 2000-2017. It uses a color scheme to allow for a global comparison of countries for each year and each measure. Additionally, users can conveniently look at the country-specific innovation trend for each type of measures by clicking on the country. 
## Run Locally

1. Ensure the project dependencies are installed
   -  pipenv 
   -  make
2. Run the project:

   ```
   make
   ```
   


## Deployment

To deploy the application, you'll need access to the project on fly.io. 

To deploy the app, run the following [flyctl](https://fly.io/docs/hands-on/install-flyctl/) command: 

```shell
fly deploy 
```
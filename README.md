# Python / Plotly Dash Web Application with Microsoft AAD Authentication

This project is an example of adding Microsoft AAd authentication to a [plotly dash](<https://plotly.com/dash/>) web application.

To enable AAD auth, we actually use flask, and then inject the flask server into the dash app. Dash uses flask under the covers, we are simply using our own flask server to allow for this customization! This approach is taken from the excellent example here:
    <https://hackersandslackers.com/plotly-dash-with-flask/>

Additionally, it uses flask blueprints to provide routes for authentication. The blueprint should be useable by multiple applications, so should not contain application specific logic or config. If you prefer, you can take just the blueprint code and drop into your existing well organized flask application, hey presto you have AAD authentication!


## Getting started

You'll need an 'app registration' registered in Azure for this tutorial. You can get a free subscription at <portal.azure.com>. Then add an app reg like <https://docs.microsoft.com/en-us/azure/active-directory/develop/quickstart-register-app>: 

Copy application/appsettings.json and rename the copy to application/appsettings.Development.json. 
- Add your AAD details into this file
- add a Rapid API key which you can get from https://rapidapi.com/sportcontentapi/api/rugby-live-data/.


### Running project with docker

You'll first need to install docker desktop - leave all defaults including using linux containers. Then run docker container with `docker-compose up --build`.

You can also debug the app running in docker container, from vscode, by running the "Docker: Python - Flask" launch configuration, which will launch your browser on a random port ~32700.

### Running project with conda

To create a conda env with all of the required dependencies for this project, first make sure you have deactivated any env (base is ok): `conda deactivate`. Then, run the following on the command line in the same directory as this readme:

``` bash
conda env remove -n dashenv
conda env create -f environment.yml python=3.7
conda activate dashenv
```

Then run the project with

```bash
python wsgi.py
```

You can also debug the app from vscode by running the "Python:Flask" launch configuration, and navigating to <http://localhost:5000>. You will need to restart vscode after the conda env is created, then select the conda env as the Python Interpreter, for this to work.

## Deployment

Deploying to an Azure Container Web App:

First, push your docker image to docker hub or other container registry (e.g. Azure CR). Then run:
```
docker-compose build
docker tag my-dash-app:latest {{docker hub account}}/my-dash-app:latest
docker push {{docker hub account}}/my-dash-app:latest
```

Then, follow something like <https://code.visualstudio.com/docs/containers/app-service> to deploy it.

## Contact

- andy.sprague44@gmail.com

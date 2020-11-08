# Python / Plotly Dash Web Application with Microsoft AAD Authentication

This project is an example of adding Microsoft AAd authentication to a platly dash web application.

Plotly dash (<https://plotly.com/dash/>), is a way to define responsive web applications purely in python, no javascript knowledge required! This project uses plotly dash with a flask server injected to give access to flask functions such as AAD authentication. This apporoach copies the example here:
    <https://hackersandslackers.com/plotly-dash-with-flask/>

Additionally, it uses flask blueprints to provide routes for authentication. The blueprint should be useable by multiple applications, so should not contain application specific logic or config.


## Getting started

First, copy appsettings.json and rename copy to appsettings.Development.json. Add your AAD details into this file, and add a Rapid API key which you can get from https://rapidapi.com/sportcontentapi/api/rugby-live-data/.


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

You can also debug the app from vscode by running the "Python:Flask" launch configuration, and navigating to <http://localhost:5000>.

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

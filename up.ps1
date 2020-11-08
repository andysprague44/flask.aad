#Authenticate to Azure Container Registry to pull base image
# To log-in:
#   az login
#   az account set --subscription "NEPHILA-DEV"
#   az acr login --name nephiladev01

docker-compose pull
docker-compose up --build -d

## General python Flask API template

##### Required installs:
`pipenv`, `docker`

#### When you first open the project
Run `pipenv install` in the top level directory

#### Run development server
Run `flask run` in top level directory


#### To build a container:
```bash
docker build -t <container_name> .  # e.g  <container_name> = command-service
```

#### To run a container:
```bash
docker run -p 5000:5000 <container_name> 
```
Note: press Cntrl + C to stop (same thing on both Mac and Windows)dock
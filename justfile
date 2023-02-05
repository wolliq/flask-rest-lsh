# https://github.com/casey/just
image_name := 'df-train-flask-lsh:dev'

build:
    docker build -t {{image_name}} .

run:
    docker run -d -p 5005:5000 -w /app -v "$(pwd):/app" {{image_name}}

shell:
    docker exec -it {{image_name}} -- bash

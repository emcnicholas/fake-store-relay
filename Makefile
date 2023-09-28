NAME:="tr-05-docker-relay"
PORT:="9090"

all: test build

black:
	black code/ -l 90 -t py311 --skip-magic-trailing-comma --exclude=payloads_for_tests.py
build: stop
	docker build -q -t $(NAME) .;
	docker run -dp $(PORT):$(PORT) --name $(NAME) $(NAME)
flake: black
	flake8 code/
test: flake
	cd code; coverage run --source api/ -m pytest --verbose tests/unit/ && coverage report --fail-under=80; cd -
test_lf:
	cd code; coverage run --source api/ -m pytest --verbose -vv --lf tests/unit/ && coverage report --fail-under=80; cd -
scout:
	docker scout cves $(NAME)
stop:
	docker stop $(NAME); docker rm $(NAME); true

# --------------------------------------------------------------------- #
# If ngrok can be used by you then you can run below make commands
# --------------------------------------------------------------------- #

up: down build expose
down: unexpose stop

expose:
	ngrok http $(PORT) > /dev/null &
echo_ngrok:
	curl -s localhost:4040/api/tunnels | jq -r ".tunnels[0].public_url"
unexpose:
	pkill ngrok; true

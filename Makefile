USERNAME ?= your_username
PASSWORD ?= your_password
NUMBER ?= 2

all: login scrape


login:
	@echo "Running login.py with USERNAME=$(USERNAME) and PASSWORD=$(PASSWORD)..."
	python login.py -u $(USERNAME) -p $(PASSWORD)

scrape:
	@echo "Running scrape.py with NUMBER=$(NUMBER)..."
	python scrape.py --number $(NUMBER)


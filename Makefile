IMAGE_NAME=my_etl_image

build:
	docker build -t $(IMAGE_NAME) .

run-main: build
	docker run --rm -v ${PWD}/data:/app/data $(IMAGE_NAME) python main.py --start-date=2025-06-04 --end-date=2025-06-06

run-scheduler: build
	docker run --rm -v ${PWD}/data:/app/data $(IMAGE_NAME) python scheduler.py

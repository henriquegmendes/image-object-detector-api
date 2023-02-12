init-venv:
	python3 -m venv venv && \
	source venv/bin/activate

install:load-yolo-ncn
	pip install -r requirements.txt

unit-test:
	pytest

freeze:
	pip freeze > requirements.txt

serve:
	uvicorn main:app --reload --debug

load-yolo-ncn:
	sh load-yolo-ncn.sh
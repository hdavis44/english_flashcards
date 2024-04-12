run_api_dev:
	uvicorn fast.api:app --host 0.0.0.0 --port 8080 --reload

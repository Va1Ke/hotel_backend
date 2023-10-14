# hotel_backend
* To run an app use:
```
uvicorn kids_galaxy.main:app --host 0.0.0.0 --port 80
```
* Update requirements:
```
pip freeze > requirements.txt
```
* Update venv due to a requirements:
```
pip install -r requirements.txt
```
* Run docker-compose:
```
docker-compose up --build
```
* Make migrations:
```
docker exec -it <container_id> bash
alembic revision --autogenerate -m "first migration"
alembic upgrade head
```
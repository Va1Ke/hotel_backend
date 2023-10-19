# hotel_backend


* Update requirements:
```
pip freeze > requirements.txt
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
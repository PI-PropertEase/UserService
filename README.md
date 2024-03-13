# UserService
Microservice responsible for authentication and authorization aspects.

#### Build Image
```bash
sudo docker build -t my-postgres-db ./ ;
```

#### Run Image
```bash
sudo docker run --env-file .env -d --name my-postgresdb-container -p 5432:5432 my-postgres-db ;
```

#### PSQL (Postgres Command Line Interface)
```bash
sudo docker exec -it container_number /bin/bash ;
psql -d user_db -U propertease ;
```

#### Pre-requirements
```bash
sudo apt-get install libpq-dev python-dev
```


#### Setup venv
```bash
python -m venv venv;
source venv/bin/activate;
pip install -r requirements;
```

#### Run FastAPI
```bash
source venv/bin/activate;
uvicorn UserService.main:app --reload;
```



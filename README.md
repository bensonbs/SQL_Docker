# SQL_Docker

### Step 1. Create compose

```
git clone https://github.com/bensonbs/SQL_Docker
```

```
cd SQL_Docker
```

**Modify path to SQL_Docker in `docker-compose.yml`**
```yaml
    volumes:
      - PATH\TO\SQL_Docker\work:/home/jovyan/work
```

```shell
docker compose up -d
```

### Step 2. Into mssql container
```shell
docker exec -it mssql_container /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P Aa123456
```

### Step 3. Create data table
```SQL
CREATE TABLE students (id INT IDENTITY(1,1) PRIMARY KEY, name TEXT NOT NULL, age INT);
INSERT INTO students (name, age) VALUES ('Benson', 25);
ALTER TABLE students ADD entry_timestamp datetime;
INSERT INTO students (name, age, entry_timestamp) VALUES ('Benson', 25, GETDATE());
GO
```

**[CTRL + C] to exit**

### Step 4. Into jupyter notenook

- Go to `localhost:8888` (you can get token in jupyter_notebook docker logs)

- Setup env `cd work` and run command `sudo sh install.sh`

- Open `connect.ipynb` to test connect





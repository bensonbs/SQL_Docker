# SQL_Docker

### Step 1. build docker image and compose

```
git clone https://github.com/bensonbs/SQL_Docker
```

```
cd SQL_Docker
```

```
docker build -t sql-scipy-notebook .
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
- Open `work/connect.ipynb` to test connect





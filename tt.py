import pyodbc

# Define connection string parameters
server = '127.0.0.1,1433'  # Change to your Docker host IP if needed, 1433 is the default SQL Server port
username = 'sa'
password = 'Aa123456'  # your actual password
driver = '{ODBC Driver 17 for SQL Server}'  # Make sure this driver is installed on your machine

# Establish the connection (without specifying a database)
connection_string = f"DRIVER={driver};SERVER={server};UID={username};PWD={password}"
conn = pyodbc.connect(connection_string)

# Fetch database names
cursor = conn.cursor()
cursor.execute("SELECT name FROM sys.databases")
rows = cursor.fetchall()

# Print database names
for row in rows:
    print(row.name)

# Close the connection
conn.close()

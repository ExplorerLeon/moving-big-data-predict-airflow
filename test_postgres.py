import psycopg2
import csv

MOUNT_DIR = "."
db_endpoint = "de-mbd-predict-rds.csmkqpd6tkho.eu-west-1.rds.amazonaws.com"

# The function that uploads data to the RDS database, it is called upon later.

def upload_to_postgres(**kwargs):

	# Write a function that will upload data to your Postgres Database

    conn = psycopg2.connect(
        host = db_endpoint,
        database = "postgres",
        user = "postgres",
        password = "postgres",
        port = "5432"
    )

    with open(f"{MOUNT_DIR}/code/insert_data.sql", "r") as q:
        query = q.read()
        print(query)

    cur = conn.cursor()

    with open(f"{MOUNT_DIR}/../Output/historical_stock_data.csv", "r") as stocks_data:
        reader = csv.reader(stocks_data)

        for n, r in enumerate(reader):
            print(n)
            print(r)
            cur.execute(query, r)
            if n > 10:
                break

    conn.commit()

    cur.close()
    conn.close()

    return "CSV Uploaded to postgres database"


upload_to_postgres()

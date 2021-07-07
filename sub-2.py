from clickhouse_driver import Client
from datetime import datetime

if __name__ == "__main__":
    client = Client("127.0.0.1", port="9002")

    client.execute("CREATE DATABASE IF NOT EXISTS billing")

    client.execute(r'''CREATE TABLE IF NOT EXISTS billing.transactions(
                      timestamp DateTime,
                      currency String,
                      value Float64)
                      ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/billing.transactions', '{replica}')
                      PARTITION BY currency
                      ORDER BY timestamp''')

    client.execute("INSERT INTO billing.transactions (timestamp, currency, value) VALUES", \
        [(datetime.utcnow(), "voltage", 72.8), (datetime.utcnow(), "humidity", 39.8), \
            (datetime.utcnow(), "temperature", 88.13)])
    
    data = client.execute("SELECT * FROM billing.transactions")

    for row in data:
        print("Timestamp", row[0], sep=": ")
        print("currency", row[1], sep=": ")
        print("Value", row[2], sep=": ")
        print()
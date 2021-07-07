from clickhouse_driver import Client

subs = [
    ("127.0.0.1", "9001"),
    ("127.0.0.1", "9002"),
    ("127.0.0.1", "9003"),
    ("127.0.0.1", "9004")
]
master = ("127.0.0.1", "9000")

for sub in subs:
    client = Client(sub[0], port=sub[1])

    client.execute("CREATE DATABASE IF NOT EXISTS history")

    client.execute(r'''CREATE TABLE IF NOT EXISTS history.measures(
                      timestamp DateTime,
                      parameter String,
                      value Float64)
                      ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard}/history.measures', '{replica}')
                      PARTITION BY parameter
                      ORDER BY timestamp''')

client = Client(master[0], port=master[1])

client.execute("CREATE DATABASE IF NOT EXISTS history")

client.execute('''CREATE TABLE IF NOT EXISTS history.measures(
                  timestamp DateTime,
                  parameter String,
                  value Float64)
                  ENGINE = Distributed(example_cluster, history, measures, rand())''')

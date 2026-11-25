# qau

PySpark helpers for Databricks: Kafka, Avro, JDBC, SFTP and CSV.

## Requirements

- Python 3.12+
- Databricks Runtime 16+ or serverless environment 3+

Spark comes from the runtime, so qau does not install it.

## Install

```
%pip install git+https://github.com/mbezrukyi/qau
```

## Secrets

Each connection has its own secret scope. The keys are the config's fields.

| Config           | Keys                                                    |
| ---------------- | ------------------------------------------------------- |
| `KafkaConfig`    | `bootstrap`, `jaas`, `security_protocol`, `sasl_mechanism` |
| `RegistryConfig` | `url`, `auth` (`key:secret`)                              |
| `JDBCConfig`     | `url`, `user`, `password`, `driver`                       |
| `SFTPConfig`     | `host`, `username`, `password`, `port` (optional, 22)     |

```
databricks secrets create-scope dev-kafka
databricks secrets put-secret dev-kafka bootstrap --string-value broker:9092
```

## Usage

```python
from qau import avro, config, csv, frames, jdbc, kafka, sftp
```

Load a config from its scope, or build it by hand:

```python
kafka_config = config.load(kafka.KafkaConfig, scope='dev-kafka')
registry_config = config.load(avro.RegistryConfig, scope='dev-registry')
```

Kafka reads and writes a batch. `key` and `value` stay raw bytes:

```python
df = kafka.read('orders', kafka_config, starting_offsets='earliest')
kafka.write(df, 'orders-copy', kafka_config)
```

Avro follows the Confluent wire format. `decode` turns the column into a
struct by each record's registry schema and adds `<column>_schema_id`. It runs
a Spark job to collect the schema ids. `encode` needs the schema and its id:

```python
decoded = avro.decode(df, 'value', registry_config)
encoded = avro.encode(decoded, 'value', schema, schema_id=100001)
```

JDBC and CSV return a DataFrame. CSV options go to Spark's reader:

```python
table = jdbc.read('public.orders', config.load(jdbc.JDBCConfig, scope='dev-jdbc'))
rows = csv.read('/Volumes/main/default/orders.csv', header=True)
```

SFTP yields a [paramiko `SFTPClient`][sftp-client] for one connection. It
accepts unknown host keys:

```python
with sftp.connect(config.load(sftp.SFTPConfig, scope='dev-sftp')) as client:
    names = client.listdir('/inbound')
```

`flatten` expands structs into `parent__child` columns, explodes arrays into
rows and casts every value to string. `unpivot` turns each column of each row
into a `key`, `value` row; the columns must share one type, as after
`flatten`:

```python
pairs = frames.unpivot(frames.flatten(decoded))
```

[sftp-client]: https://docs.paramiko.org/en/stable/api/sftp.html

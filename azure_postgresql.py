from sqlalchemy import create_engine, text
from azure.keyvault.secrets import SecretClient
from azure.identity import WorkloadIdentityCredential

# Azure Key Vault Configuration
keyvault = "secret-prod"
KVUri = f"https://{keyvault}.vault.azure.net"
credential = WorkloadIdentityCredential()
client = SecretClient(vault_url=KVUri, credential=credential)

user = "sdeabhi"
database = "patch"
secret_name = f"prod-custom-psql-{database}-{user.replace('_', '-')}"
host = "prod-custom-psql.postgres.database.azure.com"

eng = create_engine(f"postgresql+psycopg2://{user.replace('-', '_')}:{client.get_secret(secret_name).value}@{host}:5432/{database}")

table_creation_query = """
CREATE TABLE IF NOT EXISTS temp (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    age INT NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

with eng.connect() as conn:
    conn.execute(text(table_creation_query))
    conn.commit()

print("Table 'temp' created successfully in the 'mpprdtce' database.")

# ---------------------------------------------------------- view tables in the database -------------------------------------------------------

with eng.connect() as conn:
    result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';"))
    tables = result.fetchall()

for table in tables:
    print(table[0])

# ---------------------------------------------------------- view columns in the table ---------------------------------------------------------

with eng.connect() as conn:
    result = conn.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'temp';"))
    columns = result.fetchall()

for column in columns:
    print(column)

# ---------------------------------------------------------- view data in the table -----------------------------------------------------------

with eng.connect() as conn:
    result = conn.execute(text("SELECT * FROM temp;"))
    rows = result.fetchall()

for row in rows:
    print(row)
import pandas as pd
import sqlite3
from faker import Faker

# Step 1: Generate fake data and save to Excel
fake = Faker()
data = [{
    "id": i,
    "name": fake.name(),
    "email": fake.email(),
    "purchase_amount": round(fake.random_number(digits=5)/100, 2),
    "purchase_date": fake.date_this_decade()
} for i in range(1, 101)]

df = pd.DataFrame(data)
df.to_excel("sales_data.xlsx", index=False)
print("Excel file created.")

# Step 2: Load, clean, and insert into SQLite DB
df = pd.read_excel("sales_data.xlsx")

# Validation
df.dropna(inplace=True)
df["purchase_amount"] = df["purchase_amount"].apply(lambda x: max(x, 0))

# Insert into database
conn = sqlite3.connect("sales.db")
df.to_sql("sales", conn, if_exists="replace", index=False)

# Test query
print(pd.read_sql("SELECT * FROM sales LIMIT 5;", conn))
conn.close()

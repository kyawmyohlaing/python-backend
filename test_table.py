import requests
import json

# Test creating a table
table_data = {
    "table_number": 2,
    "capacity": 6
}

response = requests.post(
    "http://localhost:8088/api/tables/",
    headers={"Content-Type": "application/json"},
    data=json.dumps(table_data)
)

print(f"Create table: {response.status_code} - {response.json()}")

# Test getting all tables again (should now have one table)
response = requests.get("http://localhost:8088/api/tables/")
print(f"Get tables after creation: {response.status_code} - {response.json()}")
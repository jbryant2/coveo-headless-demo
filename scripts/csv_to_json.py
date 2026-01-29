import csv
import json

input_csv = "data/products-1000.csv"
output_json = "data/products-1000.json"

results = []

with open(input_csv, newline="", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)

    for row in reader:
        results.append({
            "id": row.get("Internal ID") or row.get("Index"),
            "title": row.get("Name"),
            "description": row.get("Description"),
            "brand": row.get("Brand"),
            "category": row.get("Category"),
            "price": float(row["Price"]) if row.get("Price") else None,
            "currency": row.get("Currency"),
            "stock": int(row["Stock"]) if row.get("Stock") else 0,
            "availability": row.get("Availability"),
            "color": row.get("Color"),
            "size": row.get("Size"),
            "ean": row.get("EAN")
        })

with open(output_json, "w", encoding="utf-8") as jsonfile:
    json.dump(results, jsonfile, indent=2, ensure_ascii=False)

print("✅ CSV successfully converted to JSON")

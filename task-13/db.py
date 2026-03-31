import random
from datetime import datetime, timedelta

def get_sales_data():
    data = []
    regions = ["North", "South", "East", "West"]

    for i in range(30):
        day = i + 1
        for r in regions:
            data.append({
                "date": f"2026-01-{day:02d}",
                "region": r,
                "revenue": random.randint(5000, 20000)
            })

    return data
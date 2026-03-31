import matplotlib.pyplot as plt
from collections import defaultdict

def generate_charts(data):
    region_totals = defaultdict(int)
    daily_totals = defaultdict(int)

    for d in data:
        region_totals[d["region"]] += d["revenue"]
        daily_totals[d["date"]] += d["revenue"]

    # Bar chart
    plt.figure()
    plt.bar(region_totals.keys(), region_totals.values())
    plt.title("Revenue by Region")
    plt.savefig("reports/bar.png")
    plt.close()

    # Line chart
    plt.figure()
    plt.plot(list(daily_totals.keys()), list(daily_totals.values()))
    plt.xticks(rotation=45)
    plt.title("Daily Sales Trend")
    plt.savefig("reports/line.png")
    plt.close()

    return region_totals, daily_totals
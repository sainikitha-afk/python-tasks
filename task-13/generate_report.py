from db import get_sales_data
from charts import generate_charts
from jinja2 import Template
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet
import os

print("=== Report Generation ===")

# Step 1: Data
print("[1/5] Loading data... OK")
data = get_sales_data()

# Step 2: Charts
print("[2/5] Generating charts...")
region_totals, daily = generate_charts(data)

# Step 3: Summary
total_revenue = sum(region_totals.values())
units = len(data)
avg_order = round(total_revenue / units, 2)

warning = region_totals["West"] < region_totals["North"]

# Step 4: Template
print("[3/5] Rendering template...")
with open("template.html") as f:
    template = Template(f.read())

html = template.render(
    total_revenue=total_revenue,
    units=units,
    avg_order=avg_order,
    warning=warning
)

# Step 5: PDF
print("[4/5] Generating PDF...")

os.makedirs("reports", exist_ok=True)

doc = SimpleDocTemplate("reports/report.pdf")
styles = getSampleStyleSheet()

elements = []
elements.append(Paragraph("Monthly Sales Report — January 2026", styles["Title"]))
elements.append(Paragraph(f"Total Revenue: {total_revenue}", styles["Normal"]))
elements.append(Paragraph(f"Units Sold: {units}", styles["Normal"]))
elements.append(Paragraph(f"Avg Order Value: {avg_order}", styles["Normal"]))

elements.append(Image("reports/bar.png", width=400, height=200))
elements.append(Image("reports/line.png", width=400, height=200))

if warning:
    elements.append(Paragraph("WARNING: West region declined", styles["Normal"]))

doc.build(elements)

print("[5/5] Done!")
print("Output: reports/report.pdf")
# Power BI Dashboard Specification

## Page 1 — Executive Overview
**KPI cards**
- Total Projects
- Total Ticket Value (Cr)
- Booked Records
- Booking Conversion %
- Average Ticket Price (Cr)

**Visuals**
- Line chart: Purchase Quarter × Bookings, legend = Micro Market
- Bar chart: Builder × Booked Ticket Value
- Donut: Booking Status
- Slicers: Builder, Micro Market, Quarter, Configuration

## Page 2 — Builder & Market
- Clustered bar: Builder × Total Ticket Value
- Table: Builder, Avg Ticket Price, Bookings, Conversion %
- Matrix: Builder × Purchase Quarter × Booked Ticket Value
- Bar: Micro Market × Conversion %
- Drill-through: Project ID / builder detail

## Page 3 — Customer & Product
- Donut: Configuration × Bookings
- 100% stacked column: Sales Channel × Booking Status
- Clustered column: Possession Status × Booking Status, legend = Buyer Type
- Buyer Type distribution
- Optional text analysis of Buyer Comments if a validated sentiment workflow is added

## Page 4 — Amenity & Geography
- Scatter: Amenity Score × Booking Conversion %, size = Project Count
- Map: Micro Market or latitude/longitude when geographic columns exist
- Top/bottom micro-markets
- Amenity score distribution

## DAX measures

```DAX
Total Projects = DISTINCTCOUNT(luxury_housing_sales[project_id])

Total Ticket Value (Cr) =
SUM(luxury_housing_sales[ticket_price_cr])

Booked Records =
CALCULATE(
    COUNTROWS(luxury_housing_sales),
    luxury_housing_sales[booking_flag] = 1
)

Booking Conversion % =
DIVIDE(
    [Booked Records],
    COUNTROWS(luxury_housing_sales),
    0
)

Average Ticket Price (Cr) =
AVERAGE(luxury_housing_sales[ticket_price_cr])

Booked Ticket Value (Cr) =
CALCULATE(
    [Total Ticket Value (Cr)],
    luxury_housing_sales[booking_flag] = 1
)
```

Format `Booking Conversion %` as Percentage and currency-like ticket measures as decimal values in Crores.

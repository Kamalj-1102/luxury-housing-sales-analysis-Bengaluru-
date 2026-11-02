# Luxury Housing Sales Analysis – Bengaluru

An end-to-end real-estate analytics project covering **Python ETL → SQL → Power BI**.

## Project objective
Build an enterprise-style analytics pipeline for a 100,000+ row luxury-housing dataset. The pipeline cleans and transforms raw data with Python, loads the curated table into MySQL/PostgreSQL/SQL Server through SQLAlchemy, validates the database with SQL, and provides a Power BI dashboard design for business analysis.

> **Dataset note:** The original training dataset is referenced by the project brief but is not bundled in this repository. Put the CSV in `data/raw/` locally. Do not commit private/proprietary data.

## Business questions
1. How have bookings changed quarter by quarter across micro-markets?
2. Which builders have the highest ticket sales and average ticket size?
3. Does amenity score relate to booking conversion?
4. Which micro-markets have the highest/lowest conversion?
5. Which configurations are most in demand?
6. Which sales channels contribute most to successful bookings?
7. Which builders dominate each quarter?
8. How does possession status relate to buyer type and booking?
9. Where are projects concentrated in Bengaluru?
10. Which five builders lead on revenue and booking success?

## Architecture

```text
Raw CSV
  │
  ▼
Python / Pandas
  ├── standardize column names
  ├── clean numeric/text/date fields
  ├── handle missing values
  ├── feature engineering
  └── data-quality report
  │
  ▼
Curated CSV
  │
  ▼
SQLAlchemy
  │
  ▼
Relational DB
  ├── schema
  ├── validation queries
  └── analytical views
  │
  ▼
Power BI
  ├── KPI cards
  ├── trends
  ├── builder analysis
  ├── conversion analysis
  ├── configuration/channel analysis
  └── map / geographic analysis
```

## Expected columns
`Project_ID`, `Micro_Market`, `Builder`, `Ticket_Price_Cr`, `Configuration`, `Possession_Status`, `Amenity_Score`, `Booking_Status`, `Purchase_Quarter`, `Sales_Channel`, `Buyer_Type`, `Buyer_Comments`.

The code also tolerates common variations such as spaces/case differences and several common aliases.

## Quick start

### 1. Create environment

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Add the dataset

Place the CSV at:

```text
data/raw/luxury_housing_sales.csv
```

Or pass another path with `--input`.

### 3. Run the ETL

```bash
python -m src.pipeline --input data/raw/luxury_housing_sales.csv
```

Outputs:
- `data/processed/luxury_housing_sales_clean.csv`
- `data/processed/data_quality_report.csv`

### 4. Load to SQL

Set a database URL:

```bash
# Windows PowerShell
$env:DATABASE_URL="mysql+pymysql://user:password@localhost:3306/real_estate"

# macOS/Linux
export DATABASE_URL="postgresql+psycopg2://user:password@localhost:5432/real_estate"
```

Then:

```bash
python -m src.load_sql
```

### 5. Validate

Run `sql/validation_queries.sql` in your database client.

## Suggested Power BI model

Use the SQL table `luxury_housing_sales` as the main fact table.

Recommended measures:

```DAX
Total Projects = DISTINCTCOUNT(luxury_housing_sales[Project_ID])

Total Ticket Value (Cr) =
SUM(luxury_housing_sales[Ticket_Price_Cr])

Booked Records =
CALCULATE(
    COUNTROWS(luxury_housing_sales),
    luxury_housing_sales[Booking_Flag] = 1
)

Booking Conversion % =
DIVIDE(
    [Booked Records],
    COUNTROWS(luxury_housing_sales),
    0
)

Average Ticket Price (Cr) =
AVERAGE(luxury_housing_sales[Ticket_Price_Cr])
```

### Dashboard pages

**1. Executive Overview**
- Total projects
- Total ticket value
- Booked records
- Booking conversion %
- Average ticket price
- Quarterly booking trend

**2. Market & Builder**
- Revenue by builder
- Average ticket price by builder
- Builder × quarter matrix
- Micro-market conversion ranking

**3. Customer & Product**
- Configuration demand
- Buyer type distribution
- Sales channel performance
- Possession status vs booking

**4. Amenity & Geography**
- Amenity score vs conversion scatter
- Bengaluru micro-market map
- Project concentration
- Top-performing markets

## GitHub checklist
- [x] Modular Python ETL
- [x] Flexible file paths
- [x] SQL schema and validation
- [x] SQLAlchemy database loader
- [x] DAX measures
- [x] Power BI dashboard specification
- [x] Data-quality report
- [x] Tests
- [x] `.gitignore`
- [ ] Add your actual CSV locally
- [ ] Publish your `.pbix` only if your data-sharing policy permits it
- [ ] Add screenshots to `powerbi/screenshots/`

## Project evaluation mapping

| Evaluation area | Repository evidence |
|---|---|
| Python Cleaning – 25% | `src/cleaning.py`, `src/pipeline.py`, tests |
| SQL Integration – 25% | `sql/schema.sql`, `src/load_sql.py`, validation SQL |
| Power BI Design – 30% | `powerbi/dashboard_spec.md`, DAX measures |
| Insight Quality – 10% | `powerbi/business_insights.md` |
| Documentation – 10% | This README + pipeline docs |

## Important
Do not claim business findings until the real dataset has been processed. The repository contains an analysis framework; actual findings should be generated from the supplied data.

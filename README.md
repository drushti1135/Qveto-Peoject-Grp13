# E-Commerce Retail Sales Analysis — VS Code + PostgreSQL

This starter project contains the supplied raw and cleaned datasets, PostgreSQL table setup, validation queries, sales analysis queries, KPI calculations, customer queries, and CSV export examples.

## Requirements
- Windows 10/11
- PostgreSQL installed and running
- VS Code
- A PostgreSQL VS Code extension (or `psql` command-line client)

## Dataset
The cleaned CSV has 12,000 rows and 18 columns. The SQL table matches those 18 columns.

## Setup
1. Open this folder in VS Code.
2. Connect to PostgreSQL. Use the port configured on your machine (often 5432 or 5433); do not assume a port.
3. Open `SQL/01_database.sql` while connected to the default `postgres` database and run it once. If the database already exists, skip this step.
4. Connect to database `ecommerce_analysis`.
5. Run `SQL/02_table_creation.sql`.
6. Import the cleaned CSV using `psql` and `\\copy` (recommended because it reads the file from your computer).

Example PowerShell command (change port if needed):

```powershell
psql -h localhost -p 5433 -U postgres -d ecommerce_analysis
```

At the `psql` prompt, run the following command, changing the path to the actual folder location:

```sql
\\copy ecommerce_sales FROM 'C:/YOUR/PATH/Ecommerce_Retail_Analysis_VSCode/Dataset/ecommerce_retail_transactions_cleaned.csv' WITH (FORMAT CSV, HEADER TRUE, ENCODING 'UTF8');
```

Expected import message: `COPY 12000`.

7. Run `SQL/03_import_validation.sql` to verify the import.
8. Run `SQL/04_sales_queries.sql`, `SQL/05_kpi_calculations.sql`, and `SQL/06_customer_analysis.sql`.
9. To export query outputs, edit the destination paths in `SQL/07_export_examples.sql`, uncomment the desired `\\copy` commands, and execute them inside `psql`. Ensure the Results directory exists.

## Important calculation definitions
Primary realized-sales KPIs use records meeting all three conditions:
- `Order_Status = 'Delivered'`
- `Quantity > 0`
- `Flag_Future_Date = FALSE`

Net sales formula:

`Quantity * Unit_Price_USD * (1 - Discount_Percent / 100)`

AOV = eligible net sales / eligible distinct delivered orders.

Cancellation and return rates in the KPI file use all distinct orders as the denominator and the respective status as the numerator. Keep this definition consistent in reports.

## Verified reference values for the supplied cleaned CSV
These are reference checks, not a substitute for running the SQL in your own database:

| Measure | Reference value |
|---|---:|
| Cleaned rows | 12,000 |
| Unique orders | 12,000 |
| Unique customers | 3,374 |
| Eligible delivered orders | 6,451 |
| Eligible units sold | 13,374 |
| Eligible net sales | USD 764,592.24 |
| Eligible average order value | USD 118.52 |
| Delivered records (all) | 6,578 |
| Cancelled orders | 1,196 |
| Returned orders | 1,015 |
| Shipped orders | 1,816 |
| Pending orders | 1,395 |
| Average available customer rating | 3.90 / 5 |

## Profit limitation
The supplied transaction dataset does not include product cost, shipping expense, packaging cost, or operating expense. Therefore, actual profit and profit margin cannot be calculated from the supplied files. The optional SQL template in `05_kpi_calculations.sql` shows how to calculate gross profit after a verified per-product cost table is supplied. Do not label sales revenue as profit.

## Handover scope
- Member 4: receive cleaned dataset and exported SQL summaries; Member 4 performs EDA and business insight work.
- Member 5: receive cleaned dataset, KPI definitions, and outputs for Power BI; Member 5 builds the dashboard.
- Member 6: receive schema, SQL scripts, KPI formulas/results, and data limitations; Member 6 writes documentation and prepares presentation.

This package does not perform the EDA, dashboard, documentation, recommendations, or presentation tasks assigned to those members.

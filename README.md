# Sales & Business Performance Analytics Dashboard

## Project Overview

This project focuses on analysing e-commerce retail transaction data to understand sales performance, customer behaviour, product categories, and overall business operations.

The objective is to transform raw transaction data into meaningful business insights using data cleaning, SQL queries, Python-based Exploratory Data Analysis (EDA), and Power BI visualisation.

**Project:** Project 3 – Sales & Business Performance Analytics Dashboard  
**Team:** Group 13  
**Team Size:** 6 Members  
**Domain:** Data Analytics

## Project Objectives

- Analyse overall sales and business performance.
- Calculate important business KPIs.
- Identify top-performing product categories and countries.
- Analyse customer ratings and payment preferences.
- Understand order statuses, cancellations, and returns.
- Create visualisations and a Power BI dashboard.
- Provide data-driven business recommendations.

## Dataset Information

- **Dataset Name:** E-Commerce Sales and Customer Analytics
- **Source:** [Kaggle – E-Commerce Sales and Customer Analytics](https://www.kaggle.com/datasets/datascikhan/e-commerce-sales-and-customer-analytics)
- **Original Records:** 12,180
- **Cleaned Records:** 12,000
- **Final Columns:** 18

The dataset contains transaction, customer, product, sales, discount, payment, date, and order-status information.

## Tools and Technologies

| Tool | Purpose |
|---|---|
| Excel / CSV | Dataset inspection and preparation |
| Python | Data cleaning and exploratory analysis |
| Pandas | Data manipulation |
| PostgreSQL | Database management |
| SQL | Data querying and KPI calculations |
| Power BI | Dashboard and visualisation |
| GitHub | Project collaboration and version control |

## Repository Structure

```text
Sales-Business-Performance-Analytics/
│
├── data/
│   └── Dataset files
│
├── notebook/
│   └── Python notebooks and analysis scripts
│
├── sql/
│   ├── results/
│   │   ├── category_sales.csv
│   │   ├── country_sales.csv
│   │   ├── customer_ratings.csv
│   │   ├── kpi_summary.csv
│   │   ├── order_status.csv
│   │   ├── monthly_sales.csv
│   │   ├── payment_method.csv
│   │   └── top_customers.csv
│   │
│   ├── 01_database.sql
│   ├── 02_table_creation.sql
│   ├── 03_import_validation.sql
│   ├── 04_sales_queries.sql
│   ├── 05_kpi_calculations.sql
│   ├── 06_customer_analysis.sql
│   └── 07_export_examples.sql
│
└── report/
    │
    ├── EDA/
    │   ├── charts/
    │   │   ├── adv_charts/
    │   │   │   ├── Quantity_Distribution.png
    │   │   │   ├── Sales_Distribution.png
    │   │   │   └── Sales_Outlier_Boxplot.png
    │   │   │
    │   │   ├── 01_monthly_sales_trend.png
    │   │   ├── 02_category_sales.png
    │   │   ├── 03_country_sales.png
    │   │   ├── 04_order_status.png
    │   │   ├── 05_customer_ratings.png
    │   │   ├── 06_payment_method.png
    │   │   ├── 07_top_customers.png
    │   │   ├── 08_city_wise_sales.png
    │   │   └── 09_year_wise_sales.png
    │   │
    │   ├── EDA_Business_Insights.txt
    │   ├── eda_category_sales.csv
    │   ├── eda_city_sales.csv
    │   ├── eda_country_sales.csv
    │   ├── eda_customer_ratings.csv
    │   ├── eda_data_quality_summary.csv
    │   ├── eda_kpi_summary.csv
    │   ├── eda_monthly_sales.csv
    │   ├── eda_order_status.csv
    │   ├── eda_payment_analysis.csv
    │   ├── eda_top_10_customers.csv
    │   ├── eda_year_sales.csv
    │   └── monthly_sales_validation.csv
    │
    ├── cleaned_data/
    │   ├── cleaning_summary.csv
    │   └── data_quality_report.csv
    │
    ├── dashboard/
    │   ├── PowerBI_Dashboard_Report.pdf
    │   ├── Ecommerce_Retail_Analysis_Presentation.pptx
    │   └── Ecommerce_Retail_Project_Documentation.docx
    │
    └── Ecommerce_Retail_SQL_Results_Verification_1.csv
```

*Note: The tree highlights the files and folders visible in the repository and the final deliverables you plan to keep. Other files may also be present.*

## Project Workflow

1. **Dataset Selection and Cleaning:** Selected the e-commerce dataset, handled duplicate and missing values, and performed data quality checks.
2. **SQL Analysis and KPI Calculation:** Used SQL queries to analyse the data and calculate important business KPIs.
3. **Exploratory Data Analysis:** Used Python to explore sales trends, product categories, countries, customers, ratings, and order statuses.
4. **Dashboard Development:** Created visualisations to present important business performance indicators.
5. **Final Presentation and Documentation:** Prepared the final presentation and project documentation covering the workflow, findings, and recommendations.

## Key Performance Indicators

The project focuses on the following KPIs:

- Total Sales
- Total Orders
- Average Order Value (AOV)
- Customer Count
- Cancellation Rate
- Return Rate

## Key Findings

The analysis highlights:

- Electronics as the highest-selling product category.
- UAE as the highest-sales country in the analysed dataset.
- Delivered orders as the largest order-status category.
- Customer ratings and payment preferences across transactions.
- Sales trends and patterns that can support business decisions.

## Team Collaboration

The project was completed collaboratively by a team of six members. Each member contributed to different stages of the project, including data preparation, SQL analysis, exploratory data analysis, dashboard development, and documentation.

GitHub was used to organise project files and manage team contributions.

## Final Outcome

The project provides an overview of e-commerce retail sales and business performance through data cleaning, SQL analysis, KPI calculations, Python visualisations, and a Power BI dashboard.

It demonstrates how data analytics can help businesses understand performance, identify patterns, and make informed decisions.

---

**Project:** Sales & Business Performance Analytics Dashboard  
**Team:** Group 13

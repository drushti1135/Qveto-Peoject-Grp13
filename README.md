# Task 1: Dataset Selection and Cleaning

## Overview
This task involved selecting an e-commerce retail transactions dataset and preparing it for further analysis.

## Dataset Details
- Original dataset: 12,180 rows and 13 columns.
- Cleaned dataset: 12,000 rows and 18 columns.

## Cleaning Activities
- Removed 180 duplicate records.
- Standardised date formats.
- Standardised payment method values.
- Standardised country names.
- Handled missing shipping city values.
- Filled missing discount values using the median (5%).
- Added flags to identify future dates, zero quantities, negative quantities and other unusual records.
- Added a provisional transaction value column.

## Files Included
- `ecommerce_retail_transactions_raw.csv` – Original dataset.
- `ecommerce_retail_transactions_cleaned.csv` – Cleaned dataset.
- `cleaning_summary.csv` – Summary of cleaning activities.
- `data_quality_report.csv` – Data quality checks and results.

## Data Limitations
Some unusual values, including zero and negative quantities and future-dated transactions, were retained and flagged because the dataset is synthetic and their actual meaning could not be verified.

## Outcome
The cleaned dataset is prepared for the next stage of the project: SQL queries and KPI calculations.

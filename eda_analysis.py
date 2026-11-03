# ============================================================
# E-COMMERCE RETAIL SALES ANALYSIS
# Member 4 - Exploratory Data Analysis (EDA)
# ============================================================

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Resolve all paths relative to this Python file. Keep the CSV in
# the Dataset folder, or place it beside this script.
BASE_DIR = Path(__file__).resolve().parent
DATA_FILENAME = "ecommerce_retail_transactions_cleaned.csv"
DATA_CANDIDATES = [
    BASE_DIR / "Dataset" / DATA_FILENAME,
    BASE_DIR / DATA_FILENAME,
]
DATA_FILE = next((p for p in DATA_CANDIDATES if p.exists()), None)
if DATA_FILE is None:
    raise FileNotFoundError(
        f"Dataset not found. Place {DATA_FILENAME} inside the 'Dataset' "
        f"folder next to this script. Checked: {DATA_CANDIDATES}"
    )

OUTPUT_DIR = BASE_DIR / "EDA_Output"
CHART_DIR = OUTPUT_DIR / "Charts"
REPORT_DIR = OUTPUT_DIR / "Reports"
ADVANCED_CHART_DIR = CHART_DIR / "Advanced_Charts"
for folder in (CHART_DIR, REPORT_DIR, ADVANCED_CHART_DIR):
    folder.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid")
print("Loading dataset:", DATA_FILE)
df = pd.read_csv(DATA_FILE)

required_columns = [
    "Order_ID", "Customer_ID", "Order_Date", "Product_Category",
    "Quantity", "Unit_Price_USD", "Discount_Percent", "Payment_Method",
    "Shipping_City", "Country", "Order_Status", "Customer_Rating",
    "Flag_Future_Date"
]
missing_columns = [c for c in required_columns if c not in df.columns]
if missing_columns:
    raise ValueError(f"Required columns missing from dataset: {missing_columns}")

# Dataset date strings use DD-MM-YYYY. Explicit format avoids month/day ambiguity.
df["Order_Date"] = pd.to_datetime(
    df["Order_Date"].astype(str).str.strip(),
    format="%d-%m-%Y",
    errors="coerce"
)
for col in ["Quantity", "Unit_Price_USD", "Discount_Percent", "Customer_Rating"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Normalize the future-date flag without relying on mixed string/boolean values.
future_flag = df["Flag_Future_Date"].astype(str).str.strip().str.lower().isin(
    ["true", "1", "yes"]
)
status = df["Order_Status"].astype(str).str.strip().str.lower()
df["Net_Sales_USD"] = (
    df["Quantity"] * df["Unit_Price_USD"] * (1 - df["Discount_Percent"] / 100)
)

# Same eligible-sales logic used in the earlier EDA submission.
eligible = (status == "delivered") & (df["Quantity"] > 0) & (~future_flag)
sales_df = df.loc[eligible].copy()
# Exclude invalid dates from time-based analyses only; retain them in other EDA.
valid_date_sales = sales_df.loc[sales_df["Order_Date"].notna()].copy()

# KPI summary
sales_total = sales_df["Net_Sales_USD"].sum()
total_order_records = len(df)
delivered_order_count = sales_df["Order_ID"].nunique()
customer_count = sales_df["Customer_ID"].nunique()
units_sold = sales_df["Quantity"].sum()
aov = sales_total / delivered_order_count if delivered_order_count else 0
cancelled = df.loc[status == "cancelled", "Order_ID"].nunique()
returned = df.loc[status == "returned", "Order_ID"].nunique()
unique_orders = df["Order_ID"].nunique()
cancel_rate = cancelled / unique_orders * 100 if unique_orders else 0
return_rate = returned / unique_orders * 100 if unique_orders else 0
ratings = sales_df["Customer_Rating"].dropna()
avg_rating = ratings.mean() if not ratings.empty else float("nan")

kpis = pd.DataFrame({"Metric": [
    "Total Eligible Sales (USD)", "Total Order Records", "Unique Order IDs",
    "Eligible Delivered Orders", "Purchasing Customers", "Total Units Sold",
    "Average Order Value (USD)", "Cancellation Rate (%)", "Return Rate (%)",
    "Average Customer Rating"
], "Value": [
    round(sales_total, 2), total_order_records, unique_orders, delivered_order_count,
    customer_count, int(units_sold), round(aov, 2), round(cancel_rate, 2),
    round(return_rate, 2), round(avg_rating, 2) if pd.notna(avg_rating) else None
]})
kpis.to_csv(REPORT_DIR / "eda_kpi_summary.csv", index=False)

# Monthly sales
monthly = (valid_date_sales.assign(Sales_Month=valid_date_sales["Order_Date"].dt.to_period("M").astype(str))
           .groupby("Sales_Month", as_index=False)["Net_Sales_USD"].sum())
monthly.to_csv(REPORT_DIR / "eda_monthly_sales.csv", index=False)
plt.figure(figsize=(13, 6))
sns.lineplot(data=monthly, x="Sales_Month", y="Net_Sales_USD", marker="o")
plt.title("Monthly Sales Trend Analysis"); plt.xlabel("Month"); plt.ylabel("Net Sales (USD)")
plt.xticks(rotation=60); plt.tight_layout(); plt.savefig(CHART_DIR/"01_monthly_sales_trend.png", dpi=250); plt.close()

# Category-wise sales
category_sales = (sales_df.groupby("Product_Category", as_index=False)
                  .agg(Total_Sales=("Net_Sales_USD", "sum"), Units_Sold=("Quantity", "sum"),
                       Orders=("Order_ID", "nunique"))
                  .sort_values("Total_Sales", ascending=False))
category_sales.to_csv(REPORT_DIR/"eda_category_sales.csv", index=False)
plt.figure(figsize=(11, 6)); sns.barplot(data=category_sales, x="Total_Sales", y="Product_Category", color="steelblue")
plt.title("Sales by Product Category"); plt.xlabel("Net Sales (USD)"); plt.ylabel("Product Category")
plt.tight_layout(); plt.savefig(CHART_DIR/"02_category_sales.png", dpi=250); plt.close()

# Country-wise sales
country_sales = (sales_df.groupby("Country", as_index=False)["Net_Sales_USD"].sum()
                 .sort_values("Net_Sales_USD", ascending=False))
country_sales.to_csv(REPORT_DIR/"eda_country_sales.csv", index=False)
plt.figure(figsize=(11, 6)); sns.barplot(data=country_sales, x="Net_Sales_USD", y="Country", color="steelblue")
plt.title("Country-wise Sales Performance"); plt.xlabel("Net Sales (USD)"); plt.ylabel("Country")
plt.tight_layout(); plt.savefig(CHART_DIR/"03_country_sales.png", dpi=250); plt.close()

# NEW: City-wise sales (source column is Shipping_City, not City)
city_data = sales_df.copy()
city_data["Shipping_City"] = city_data["Shipping_City"].fillna("Unknown").astype(str).str.strip()
city_data.loc[city_data["Shipping_City"] == "", "Shipping_City"] = "Unknown"
city_sales = (city_data.groupby("Shipping_City", as_index=False)
              .agg(Total_Sales=("Net_Sales_USD", "sum"), Orders=("Order_ID", "nunique"),
                   Customers=("Customer_ID", "nunique"), Units_Sold=("Quantity", "sum"))
              .sort_values("Total_Sales", ascending=False))
city_sales.to_csv(REPORT_DIR/"eda_city_sales.csv", index=False)
plt.figure(figsize=(12, 8)); sns.barplot(data=city_sales, x="Total_Sales", y="Shipping_City", color="steelblue")
plt.title("City-wise Sales Performance"); plt.xlabel("Net Sales (USD)"); plt.ylabel("Shipping City")
plt.tight_layout(); plt.savefig(CHART_DIR/"08_city_wise_sales.png", dpi=250); plt.close()

# NEW: Year-wise sales
valid_date_sales["Sales_Year"] = valid_date_sales["Order_Date"].dt.year
year_sales = (valid_date_sales.groupby("Sales_Year", as_index=False)
              .agg(Total_Sales=("Net_Sales_USD", "sum"), Orders=("Order_ID", "nunique"),
                   Customers=("Customer_ID", "nunique"), Units_Sold=("Quantity", "sum"))
              .sort_values("Sales_Year"))
year_sales.to_csv(REPORT_DIR/"eda_year_sales.csv", index=False)
plt.figure(figsize=(9, 5)); sns.barplot(data=year_sales, x="Sales_Year", y="Total_Sales", color="steelblue")
plt.title("Year-wise Sales Performance"); plt.xlabel("Year"); plt.ylabel("Net Sales (USD)")
plt.tight_layout(); plt.savefig(CHART_DIR/"09_year_wise_sales.png", dpi=250); plt.close()

# Order status analysis
order_status = (df.groupby("Order_Status", as_index=False)["Order_ID"].nunique()
                .rename(columns={"Order_ID":"Order_Count"}).sort_values("Order_Count", ascending=False))
order_status.to_csv(REPORT_DIR/"eda_order_status.csv", index=False)
plt.figure(figsize=(8, 8)); plt.pie(order_status["Order_Count"], labels=order_status["Order_Status"], autopct="%1.1f%%", startangle=90)
plt.title("Order Status Distribution"); plt.tight_layout(); plt.savefig(CHART_DIR/"04_order_status.png", dpi=250); plt.close()

# Customer ratings
rating_counts = ratings.value_counts().sort_index().rename_axis("Customer_Rating").reset_index(name="Response_Count")
rating_counts.to_csv(REPORT_DIR/"eda_customer_ratings.csv", index=False)
plt.figure(figsize=(9, 5)); sns.countplot(data=sales_df, x="Customer_Rating", hue="Customer_Rating", palette="viridis", legend=False)
plt.title("Customer Rating Distribution"); plt.xlabel("Customer Rating"); plt.ylabel("Number of Ratings")
plt.tight_layout(); plt.savefig(CHART_DIR/"05_customer_ratings.png", dpi=250); plt.close()

# Payment method analysis
payment = (sales_df.groupby("Payment_Method", as_index=False)
           .agg(Total_Sales=("Net_Sales_USD", "sum"), Order_Count=("Order_ID", "nunique"))
           .sort_values("Total_Sales", ascending=False))
payment.to_csv(REPORT_DIR/"eda_payment_analysis.csv", index=False)
plt.figure(figsize=(10, 6)); sns.barplot(data=payment, x="Total_Sales", y="Payment_Method", color="steelblue")
plt.title("Sales by Payment Method"); plt.xlabel("Net Sales (USD)"); plt.ylabel("Payment Method")
plt.tight_layout(); plt.savefig(CHART_DIR/"06_payment_method.png", dpi=250); plt.close()

# Top 10 customers
top_customers = (sales_df.groupby("Customer_ID", as_index=False)
                 .agg(Total_Sales=("Net_Sales_USD", "sum"), Order_Count=("Order_ID", "nunique"))
                 .sort_values("Total_Sales", ascending=False).head(10))
top_customers.to_csv(REPORT_DIR/"eda_top_10_customers.csv", index=False)
plt.figure(figsize=(11, 6)); sns.barplot(data=top_customers, x="Total_Sales", y="Customer_ID", color="steelblue")
plt.title("Top 10 Customers by Sales"); plt.xlabel("Net Sales (USD)"); plt.ylabel("Customer ID")
plt.tight_layout(); plt.savefig(CHART_DIR/"07_top_customers.png", dpi=250); plt.close()

# Advanced charts
valid_line_values = df.loc[df["Provisional_Line_Value_USD"].gt(0), "Provisional_Line_Value_USD"] if "Provisional_Line_Value_USD" in df else df.loc[df["Net_Sales_USD"].gt(0), "Net_Sales_USD"]
plt.figure(figsize=(10, 6)); sns.histplot(valid_line_values, bins=30, kde=True, color="steelblue")
plt.title("Sales Value Distribution"); plt.xlabel("Sales Value (USD)"); plt.ylabel("Frequency")
plt.tight_layout(); plt.savefig(ADVANCED_CHART_DIR/"Sales_Distribution.png", dpi=250); plt.close()
plt.figure(figsize=(10, 5)); sns.boxplot(x=valid_line_values, color="steelblue")
plt.title("Sales Value - Outlier Analysis"); plt.xlabel("Sales Value (USD)")
plt.tight_layout(); plt.savefig(ADVANCED_CHART_DIR/"Sales_Outlier_Boxplot.png", dpi=250); plt.close()
positive_quantity = df.loc[df["Quantity"].gt(0), "Quantity"]
plt.figure(figsize=(10, 6)); sns.countplot(x=positive_quantity, color="steelblue")
plt.title("Quantity Distribution"); plt.xlabel("Quantity per Record"); plt.ylabel("Number of Records")
plt.tight_layout(); plt.savefig(ADVANCED_CHART_DIR/"Quantity_Distribution.png", dpi=250); plt.close()

# Data quality summary
quality = pd.DataFrame({"Metric":["Total Rows","Total Columns","Duplicate Rows","Missing Values","Invalid Dates","Valid Eligible Sales Dates"],
                        "Value":[len(df), len(df.columns), int(df.duplicated().sum()), int(df.isna().sum().sum()), int(df["Order_Date"].isna().sum()), len(valid_date_sales)]})
quality.to_csv(REPORT_DIR/"eda_data_quality_summary.csv", index=False)

# Monthly coverage validation
monthly_validation = monthly.copy()
monthly_validation["Sales_Year"] = monthly_validation["Sales_Month"].str[:4].astype(int)
monthly_validation["Month_Number"] = monthly_validation["Sales_Month"].str[5:7].astype(int)
monthly_validation.to_csv(REPORT_DIR/"monthly_sales_validation.csv", index=False)

# Business insights (values derived from current dataset)
best_category = category_sales.iloc[0]
lowest_category = category_sales.iloc[-1]
best_country = country_sales.iloc[0]
best_city = city_sales.iloc[0]
best_year = year_sales.loc[year_sales["Total_Sales"].idxmax()] if not year_sales.empty else None
best_payment = payment.iloc[0]
insights = [
    "E-COMMERCE BUSINESS INSIGHTS", "="*45, "",
    f"1. Total eligible net sales: ${sales_total:,.2f}.",
    f"2. Dataset contains {len(df):,} order records and {unique_orders:,} unique Order_ID values.",
    f"3. Eligible delivered orders: {delivered_order_count:,}.",
    f"4. Purchasing customers: {customer_count:,}.",
    f"5. Average order value: ${aov:,.2f}.",
    f"6. Highest sales category: {best_category['Product_Category']} (${best_category['Total_Sales']:,.2f}).",
    f"7. Lowest sales category: {lowest_category['Product_Category']} (${lowest_category['Total_Sales']:,.2f}).",
    f"8. Highest sales country: {best_country['Country']} (${best_country['Net_Sales_USD']:,.2f}).",
    f"9. Highest sales city: {best_city['Shipping_City']} (${best_city['Total_Sales']:,.2f}).",
    f"10. Highest sales year in the available dataset: {int(best_year['Sales_Year'])} (${best_year['Total_Sales']:,.2f})." if best_year is not None else "10. Year-wise sales could not be calculated.",
    f"11. Highest sales payment method: {best_payment['Payment_Method']} (${best_payment['Total_Sales']:,.2f}).",
    f"12. Cancellation rate: {cancel_rate:.2f}%; return rate: {return_rate:.2f}%.",
    f"13. Average customer rating among available eligible ratings: {avg_rating:.2f}." if pd.notna(avg_rating) else "13. Average customer rating is unavailable.",
    "", "DATA LIMITATIONS", "="*45,
    "Actual profit cannot be calculated because product cost, shipping cost, and operating expenses are not available.",
    "The dataset's city field is Shipping_City; city-wise results use this column.",
    "2026 contains a partial period in this dataset; do not compare it with full years without noting the coverage difference.",
    "Monthly/yearly analysis excludes rows with invalid or missing Order_Date values.",
    "Sales revenue must not be reported as profit."
]
(REPORT_DIR/"EDA_Business_Insights.txt").write_text("\n".join(insights), encoding="utf-8")

print("\nEDA completed successfully.")
print("Dataset rows:", len(df))
print("Eligible delivered records:", len(sales_df))
print(f"Total eligible sales: ${sales_total:,.2f}")
print("City-wise sales rows:", len(city_sales), "| Year-wise rows:", len(year_sales))
print("Charts:", len(list(CHART_DIR.glob("*.png"))) + len(list(ADVANCED_CHART_DIR.glob("*.png"))))
print("Reports:", len(list(REPORT_DIR.glob("*"))))
print("Output folder:", OUTPUT_DIR)

-- IMPORT: Run the following command in psql (not in a normal SQL editor).
-- Replace the path with the full path on your own computer.
-- \copy ecommerce_sales FROM 'C:/YOUR/PATH/Dataset/ecommerce_retail_transactions_cleaned.csv' WITH (FORMAT CSV, HEADER TRUE, ENCODING 'UTF8');

-- Validate import
SELECT COUNT(*) AS total_rows FROM ecommerce_sales;
SELECT COUNT(DISTINCT order_id) AS unique_orders,
       COUNT(DISTINCT customer_id) AS unique_customers
FROM ecommerce_sales;

SELECT column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'public' AND table_name = 'ecommerce_sales'
ORDER BY ordinal_position;

SELECT * FROM ecommerce_sales LIMIT 10;

-- Data-quality checks
SELECT
  COUNT(*) FILTER (WHERE customer_rating IS NULL) AS missing_ratings,
  COUNT(*) FILTER (WHERE shipping_city = 'Unknown') AS unknown_cities,
  COUNT(*) FILTER (WHERE flag_future_date IS TRUE) AS future_date_flags,
  COUNT(*) FILTER (WHERE flag_zero_quantity IS TRUE) AS zero_quantity_flags,
  COUNT(*) FILTER (WHERE flag_negative_quantity IS TRUE) AS negative_quantity_flags,
  COUNT(*) FILTER (WHERE flag_negative_status_mismatch IS TRUE) AS negative_status_mismatch_flags
FROM ecommerce_sales;

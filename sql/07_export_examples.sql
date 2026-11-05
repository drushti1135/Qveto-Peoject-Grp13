-- Run these \copy commands inside psql, not in a standard SQL editor.
-- Create the Results folder first. Replace the example path with your actual absolute path.

-- Monthly sales export
-- \copy (SELECT DATE_TRUNC('month', order_date)::date AS sales_month, ROUND(SUM(quantity*unit_price_usd*(1-discount_percent/100.0)),2) AS monthly_sales_usd FROM ecommerce_sales WHERE order_status='Delivered' AND quantity>0 AND flag_future_date IS FALSE GROUP BY 1 ORDER BY 1) TO 'C:/YOUR/PATH/Results/monthly_sales.csv' WITH (FORMAT CSV, HEADER TRUE);

-- Category sales export
-- \copy (SELECT product_category, ROUND(SUM(quantity*unit_price_usd*(1-discount_percent/100.0)),2) AS total_sales_usd, SUM(quantity) AS units_sold FROM ecommerce_sales WHERE order_status='Delivered' AND quantity>0 AND flag_future_date IS FALSE GROUP BY product_category ORDER BY total_sales_usd DESC) TO 'C:/YOUR/PATH/Results/category_sales.csv' WITH (FORMAT CSV, HEADER TRUE);

-- Country sales export
-- \copy (SELECT country, ROUND(SUM(quantity*unit_price_usd*(1-discount_percent/100.0)),2) AS total_sales_usd FROM ecommerce_sales WHERE order_status='Delivered' AND quantity>0 AND flag_future_date IS FALSE GROUP BY country ORDER BY total_sales_usd DESC) TO 'C:/YOUR/PATH/Results/country_sales.csv' WITH (FORMAT CSV, HEADER TRUE);

-- Order status export
-- \copy (SELECT order_status, COUNT(DISTINCT order_id) AS order_count FROM ecommerce_sales GROUP BY order_status ORDER BY order_count DESC) TO 'C:/YOUR/PATH/Results/order_status.csv' WITH (FORMAT CSV, HEADER TRUE);

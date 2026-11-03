-- All sales queries below use the same primary realized-sales definition:
-- Delivered orders, positive quantities, and not future-dated.
-- Net sales = quantity * unit price * (1 - discount percentage / 100).

-- 1. Monthly net sales
SELECT DATE_TRUNC('month', order_date)::date AS sales_month,
       ROUND(SUM(quantity * unit_price_usd * (1 - discount_percent / 100.0)), 2) AS monthly_sales_usd
FROM ecommerce_sales
WHERE order_status = 'Delivered' AND quantity > 0 AND flag_future_date IS FALSE
GROUP BY 1 ORDER BY 1;

-- 2. Yearly net sales
SELECT EXTRACT(YEAR FROM order_date)::int AS sales_year,
       ROUND(SUM(quantity * unit_price_usd * (1 - discount_percent / 100.0)), 2) AS annual_sales_usd
FROM ecommerce_sales
WHERE order_status = 'Delivered' AND quantity > 0 AND flag_future_date IS FALSE
GROUP BY 1 ORDER BY 1;

-- 3. Sales by product category
SELECT product_category,
       ROUND(SUM(quantity * unit_price_usd * (1 - discount_percent / 100.0)), 2) AS total_sales_usd,
       SUM(quantity) AS units_sold
FROM ecommerce_sales
WHERE order_status = 'Delivered' AND quantity > 0 AND flag_future_date IS FALSE
GROUP BY product_category ORDER BY total_sales_usd DESC;

-- 4. Top 10 products by units sold
SELECT product_name, SUM(quantity) AS units_sold,
       ROUND(SUM(quantity * unit_price_usd * (1 - discount_percent / 100.0)), 2) AS revenue_usd
FROM ecommerce_sales
WHERE order_status = 'Delivered' AND quantity > 0 AND flag_future_date IS FALSE
GROUP BY product_name ORDER BY units_sold DESC LIMIT 10;

-- 5. Sales by country
SELECT country,
       ROUND(SUM(quantity * unit_price_usd * (1 - discount_percent / 100.0)), 2) AS total_sales_usd
FROM ecommerce_sales
WHERE order_status = 'Delivered' AND quantity > 0 AND flag_future_date IS FALSE
GROUP BY country ORDER BY total_sales_usd DESC;

-- 6. Orders by status (all statuses)
SELECT order_status, COUNT(DISTINCT order_id) AS order_count
FROM ecommerce_sales GROUP BY order_status ORDER BY order_count DESC;

-- 7. Sales by payment method
SELECT payment_method,
       ROUND(SUM(quantity * unit_price_usd * (1 - discount_percent / 100.0)), 2) AS total_sales_usd,
       COUNT(DISTINCT order_id) AS order_count
FROM ecommerce_sales
WHERE order_status = 'Delivered' AND quantity > 0 AND flag_future_date IS FALSE
GROUP BY payment_method ORDER BY total_sales_usd DESC;

-- 8. Sales by shipping city (top 10)
SELECT shipping_city,
       ROUND(SUM(quantity * unit_price_usd * (1 - discount_percent / 100.0)), 2) AS total_sales_usd
FROM ecommerce_sales
WHERE order_status = 'Delivered' AND quantity > 0 AND flag_future_date IS FALSE
GROUP BY shipping_city ORDER BY total_sales_usd DESC LIMIT 10;

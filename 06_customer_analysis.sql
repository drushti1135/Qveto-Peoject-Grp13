-- Top 10 customers by net sales
SELECT customer_id, COUNT(DISTINCT order_id) AS delivered_orders,
       ROUND(SUM(quantity * unit_price_usd * (1 - discount_percent / 100.0)), 2) AS customer_sales_usd
FROM ecommerce_sales
WHERE order_status = 'Delivered' AND quantity > 0 AND flag_future_date IS FALSE
GROUP BY customer_id ORDER BY customer_sales_usd DESC LIMIT 10;

-- Customer rating distribution
SELECT customer_rating, COUNT(*) AS response_count
FROM ecommerce_sales WHERE customer_rating IS NOT NULL
GROUP BY customer_rating ORDER BY customer_rating;

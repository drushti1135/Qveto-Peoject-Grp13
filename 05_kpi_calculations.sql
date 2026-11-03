-- Primary sales KPIs: delivered + positive quantity + not future-dated.
-- Note: dataset has no product cost; actual profit/profit margin cannot be calculated.

-- 1. Sales, eligible orders, units, customers, AOV and average selling price
WITH eligible AS (
  SELECT *, quantity * unit_price_usd * (1 - discount_percent / 100.0) AS net_sales
  FROM ecommerce_sales
  WHERE order_status = 'Delivered' AND quantity > 0 AND flag_future_date IS FALSE
)
SELECT
  ROUND(SUM(net_sales), 2) AS total_sales_usd,
  COUNT(DISTINCT order_id) AS eligible_delivered_orders,
  SUM(quantity) AS units_sold,
  COUNT(DISTINCT customer_id) AS purchasing_customers,
  ROUND(SUM(net_sales) / NULLIF(COUNT(DISTINCT order_id), 0), 2) AS average_order_value_usd,
  ROUND(SUM(net_sales) / NULLIF(SUM(quantity), 0), 2) AS average_selling_price_per_unit_usd
FROM eligible;

-- 2. All-order status KPIs
SELECT
  COUNT(DISTINCT order_id) AS all_orders,
  COUNT(DISTINCT order_id) FILTER (WHERE order_status = 'Delivered') AS delivered_orders,
  COUNT(DISTINCT order_id) FILTER (WHERE order_status = 'Cancelled') AS cancelled_orders,
  COUNT(DISTINCT order_id) FILTER (WHERE order_status = 'Returned') AS returned_orders,
  COUNT(DISTINCT order_id) FILTER (WHERE order_status = 'Shipped') AS shipped_orders,
  COUNT(DISTINCT order_id) FILTER (WHERE order_status = 'Pending') AS pending_orders,
  ROUND(100.0 * COUNT(DISTINCT order_id) FILTER (WHERE order_status = 'Cancelled') /
        NULLIF(COUNT(DISTINCT order_id), 0), 2) AS cancellation_rate_percent,
  ROUND(100.0 * COUNT(DISTINCT order_id) FILTER (WHERE order_status = 'Returned') /
        NULLIF(COUNT(DISTINCT order_id), 0), 2) AS return_rate_percent
FROM ecommerce_sales;

-- 3. Gross sales before discounts, discount value and net sales (eligible records)
SELECT
  ROUND(SUM(quantity * unit_price_usd), 2) AS gross_sales_before_discount_usd,
  ROUND(SUM(quantity * unit_price_usd * discount_percent / 100.0), 2) AS discount_amount_usd,
  ROUND(SUM(quantity * unit_price_usd * (1 - discount_percent / 100.0)), 2) AS net_sales_after_discount_usd
FROM ecommerce_sales
WHERE order_status = 'Delivered' AND quantity > 0 AND flag_future_date IS FALSE;

-- 4. Average customer rating (available ratings only)
SELECT ROUND(AVG(customer_rating), 2) AS average_customer_rating,
       COUNT(customer_rating) AS rating_count
FROM ecommerce_sales WHERE customer_rating IS NOT NULL;

-- 5. Profit template: requires a verified cost per unit for every product.
-- Do not report profit until product_cost data is supplied and validated.
-- CREATE TABLE product_cost (product_name VARCHAR(150) PRIMARY KEY, cost_per_unit NUMERIC(12,2) NOT NULL CHECK (cost_per_unit >= 0));
-- SELECT SUM(e.quantity * e.unit_price_usd * (1-e.discount_percent/100.0)) AS revenue,
--        SUM(e.quantity * p.cost_per_unit) AS cost,
--        SUM(e.quantity * (e.unit_price_usd * (1-e.discount_percent/100.0)-p.cost_per_unit)) AS gross_profit
-- FROM ecommerce_sales e JOIN product_cost p USING (product_name)
-- WHERE e.order_status='Delivered' AND e.quantity>0 AND e.flag_future_date IS FALSE;

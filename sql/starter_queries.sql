-- Sales by category
SELECT category, SUM(gross_sales) AS gross_sales
FROM business_data
GROUP BY category
ORDER BY gross_sales DESC;

-- Return rate by category (row-based demo definition)
SELECT category,
       SUM(CASE WHEN LOWER(order_status) LIKE '%return%' THEN 1 ELSE 0 END) AS returned_rows,
       SUM(CASE WHEN LOWER(order_status) NOT LIKE '%cancel%' THEN 1 ELSE 0 END) AS non_cancelled_rows,
       1.0 * SUM(CASE WHEN LOWER(order_status) LIKE '%return%' THEN 1 ELSE 0 END)
       / NULLIF(SUM(CASE WHEN LOWER(order_status) NOT LIKE '%cancel%' THEN 1 ELSE 0 END), 0) AS return_rate
FROM business_data
GROUP BY category;

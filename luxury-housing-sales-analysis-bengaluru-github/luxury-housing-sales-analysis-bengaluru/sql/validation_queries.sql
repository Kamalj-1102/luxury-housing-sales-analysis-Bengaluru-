-- 1. Row count
SELECT COUNT(*) AS total_rows
FROM luxury_housing_sales;

-- 2. Booking status distribution
SELECT booking_status, COUNT(*) AS records
FROM luxury_housing_sales
GROUP BY booking_status
ORDER BY records DESC;

-- 3. Average ticket price by builder
SELECT
    builder,
    COUNT(*) AS records,
    ROUND(AVG(ticket_price_cr), 2) AS avg_ticket_price_cr,
    ROUND(SUM(CASE WHEN booking_flag = 1 THEN ticket_price_cr ELSE 0 END), 2)
        AS booked_ticket_value_cr
FROM luxury_housing_sales
GROUP BY builder
ORDER BY booked_ticket_value_cr DESC;

-- 4. Conversion by micro-market
SELECT
    micro_market,
    COUNT(*) AS total_records,
    SUM(booking_flag) AS booked_records,
    ROUND(100.0 * SUM(booking_flag) / NULLIF(COUNT(*), 0), 2) AS conversion_pct
FROM luxury_housing_sales
GROUP BY micro_market
ORDER BY conversion_pct DESC;

-- 5. Quarterly booking trend
SELECT
    purchase_quarter,
    SUM(booking_flag) AS bookings,
    COUNT(*) AS total_records,
    ROUND(100.0 * SUM(booking_flag) / NULLIF(COUNT(*), 0), 2) AS conversion_pct
FROM luxury_housing_sales
GROUP BY purchase_quarter
ORDER BY purchase_quarter;

-- 6. Configuration demand
SELECT configuration, SUM(booking_flag) AS bookings, COUNT(*) AS records
FROM luxury_housing_sales
GROUP BY configuration
ORDER BY bookings DESC;

-- 7. Sales channel performance
SELECT
    sales_channel,
    COUNT(*) AS records,
    SUM(booking_flag) AS bookings,
    ROUND(100.0 * SUM(booking_flag) / NULLIF(COUNT(*), 0), 2) AS conversion_pct
FROM luxury_housing_sales
GROUP BY sales_channel
ORDER BY conversion_pct DESC;

-- 8. Top five builders by booked ticket value
SELECT
    builder,
    ROUND(SUM(CASE WHEN booking_flag = 1 THEN ticket_price_cr ELSE 0 END), 2)
        AS booked_ticket_value_cr,
    ROUND(AVG(ticket_price_cr), 2) AS avg_ticket_price_cr
FROM luxury_housing_sales
GROUP BY builder
ORDER BY booked_ticket_value_cr DESC
LIMIT 5;

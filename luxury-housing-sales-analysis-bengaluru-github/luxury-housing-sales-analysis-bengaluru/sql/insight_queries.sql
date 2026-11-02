-- Builder contribution by quarter
SELECT
    builder,
    purchase_quarter,
    ROUND(SUM(CASE WHEN booking_flag = 1 THEN ticket_price_cr ELSE 0 END), 2)
        AS booked_value_cr
FROM luxury_housing_sales
GROUP BY builder, purchase_quarter
ORDER BY purchase_quarter, booked_value_cr DESC;

-- Amenity score buckets and conversion
SELECT
    CASE
        WHEN amenity_score < 40 THEN 'Low'
        WHEN amenity_score < 70 THEN 'Medium'
        ELSE 'High'
    END AS amenity_band,
    COUNT(*) AS records,
    SUM(booking_flag) AS bookings,
    ROUND(100.0 * SUM(booking_flag) / NULLIF(COUNT(*), 0), 2) AS conversion_pct
FROM luxury_housing_sales
WHERE amenity_score IS NOT NULL
GROUP BY amenity_band
ORDER BY amenity_band;

-- Possession status vs booking
SELECT
    possession_status,
    booking_status,
    COUNT(*) AS records
FROM luxury_housing_sales
GROUP BY possession_status, booking_status
ORDER BY possession_status, records DESC;

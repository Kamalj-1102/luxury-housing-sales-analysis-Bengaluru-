CREATE TABLE IF NOT EXISTS luxury_housing_sales (
    project_id VARCHAR(100),
    micro_market VARCHAR(150),
    builder VARCHAR(200),
    ticket_price_cr DECIMAL(18,4),
    configuration VARCHAR(50),
    possession_status VARCHAR(100),
    amenity_score DECIMAL(10,2),
    booking_status VARCHAR(100),
    purchase_quarter VARCHAR(50),
    sales_channel VARCHAR(100),
    buyer_type VARCHAR(100),
    buyer_comments TEXT,
    area_sqft DECIMAL(18,2),
    price_per_sqft DECIMAL(18,2),
    quarter_number INTEGER,
    booking_flag SMALLINT
);

CREATE INDEX idx_lhs_builder ON luxury_housing_sales(builder);
CREATE INDEX idx_lhs_market ON luxury_housing_sales(micro_market);
CREATE INDEX idx_lhs_quarter ON luxury_housing_sales(purchase_quarter);
CREATE INDEX idx_lhs_booking ON luxury_housing_sales(booking_status);

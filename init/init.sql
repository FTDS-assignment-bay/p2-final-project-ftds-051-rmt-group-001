CREATE DATABASE olist_raw;
CREATE DATABASE olist_processed;

\connect olist_raw;

CREATE TABLE customers (
    customer_id VARCHAR PRIMARY KEY,
    customer_unique_id VARCHAR,
    customer_zip_code_prefix INT,
    customer_city VARCHAR,
    customer_state VARCHAR
);

CREATE TABLE orders (
    order_id VARCHAR PRIMARY KEY,
    customer_id VARCHAR,
    order_status VARCHAR,
    order_purchase_timestamp TIMESTAMP,
    order_approved_at TIMESTAMP,
    order_delivered_carrier_date TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP
);

CREATE TABLE order_items (
    order_id VARCHAR,
    order_item_id INT,
    product_id VARCHAR,
    seller_id VARCHAR,
    shipping_limit_date TIMESTAMP,
    price NUMERIC,
    freight_value NUMERIC,
    PRIMARY KEY (order_id, order_item_id)
);

CREATE TABLE order_payments (
    order_id VARCHAR,
    payment_sequential INT,
    payment_type VARCHAR,
    payment_installments INT,
    payment_value NUMERIC
);

CREATE TABLE order_reviews (
    review_id VARCHAR,
    order_id VARCHAR,
    review_score INT,
    review_comment_title TEXT,
    review_comment_message TEXT,
    review_creation_date TIMESTAMP,
    review_answer_timestamp TIMESTAMP
);

CREATE TABLE products (
    product_id VARCHAR PRIMARY KEY,
    product_category_name VARCHAR,
    product_name_length INT,
    product_description_length INT,
    product_photos_qty INT,
    product_weight_g NUMERIC,
    product_length_cm NUMERIC,
    product_height_cm NUMERIC,
    product_width_cm NUMERIC
);

CREATE TABLE sellers (
    seller_id VARCHAR PRIMARY KEY,
    seller_zip_code_prefix INT,
    seller_city VARCHAR,
    seller_state VARCHAR
);

CREATE TABLE product_category_translation (
    product_category_name VARCHAR PRIMARY KEY,
    product_category_name_english VARCHAR
);

\connect olist_processed;

-- =========================
-- DIMENSION: CUSTOMER
-- =========================
CREATE TABLE dim_customer (
    customer_key SERIAL PRIMARY KEY,
    customer_id VARCHAR UNIQUE,
    customer_unique_id VARCHAR,
    customer_zip_code_prefix INT,
    customer_city VARCHAR,
    customer_state VARCHAR
);

-- =========================
-- DIMENSION: ORDER STATUS
-- =========================
CREATE TABLE dim_order_status (
    order_status_key SERIAL PRIMARY KEY,
    order_status VARCHAR UNIQUE
);

-- =========================
-- DIMENSION: PAYMENT TYPE
-- =========================
CREATE TABLE dim_payment_type (
    payment_type_key SERIAL PRIMARY KEY,
    payment_type VARCHAR UNIQUE
);

-- =========================
-- FACT: ORDERS
-- =========================
CREATE TABLE fact_orders (
    order_id VARCHAR PRIMARY KEY,

    customer_key INT REFERENCES dim_customer(customer_key),
    order_status_key INT REFERENCES dim_order_status(order_status_key),
    payment_type_key INT REFERENCES dim_payment_type(payment_type_key),

    order_purchase_timestamp TIMESTAMP,

    total_items NUMERIC,
    total_order_value NUMERIC,
    total_freight NUMERIC,
    avg_item_price NUMERIC,
    total_payment_value NUMERIC,
    max_installments NUMERIC,

    is_canceled INT
);

-- =========================
-- DIMENSION: PRODUCT
-- =========================
CREATE TABLE dim_product (
    product_key SERIAL PRIMARY KEY,
    product_id VARCHAR UNIQUE,
    product_category_name VARCHAR,
    product_name_length INT,
    product_description_length INT,
    product_photos_qty INT,
    product_weight_g NUMERIC,
    product_length_cm NUMERIC,
    product_height_cm NUMERIC,
    product_width_cm NUMERIC
);

-- =========================
-- FACT: ORDER ITEMS (Non-Aggregated Star)
-- Grain: 1 row = 1 order_item
-- =========================
CREATE TABLE fact_order_items (
    order_item_key SERIAL PRIMARY KEY,

    order_id VARCHAR,
    order_item_id INT,

    customer_key INT REFERENCES dim_customer(customer_key),
    product_key INT REFERENCES dim_product(product_key),
    order_status_key INT REFERENCES dim_order_status(order_status_key),
    payment_type_key INT REFERENCES dim_payment_type(payment_type_key),

    order_purchase_timestamp TIMESTAMP,

    price NUMERIC,
    freight_value NUMERIC,

    is_canceled INT
);
# Model Prediction Schema Documentation

This document explains how to use the `model_schema.json` file for the prediction interface.

The goal of this schema is to allow the Streamlit application to dynamically generate the input form required by the machine learning model.

By following this schema structure, Data Scientists can update model features without modifying application code.

---

# Overview

The schema defines:

- Model metadata
- Target variable
- Feature inputs
- Input validation rules
- UI configuration

The Streamlit application reads this schema and automatically builds the prediction form.

---

# Top Level Fields

## model_name

Required.

Name of the model used by the application.

Example:

order_cancellation_model_v1

Used for:

- model version tracking
- debugging
- documentation

## version

Required.

Version of the model schema.

Increase this when:

- model is retrained
- features change
- feature validation rules change

## target

Required.

The prediction target produced by the model.

Example:

is_canceled

Important:
This field is NOT used as input during prediction.

## description

Optional.

Short explanation of the model purpose.

Example:

Predict cancellation risk for e-commerce orders.

---

# Features Section

The `features` list defines all model inputs.

Each object inside the list represents one input field.

Example:

{
  "name": "total_items",
  "type": "int"
}

---

# Feature Fields

## name

Required.

The exact column name used during model training.

Rules:

- Must match training dataframe column name
- Must be unique
- No spaces allowed

Example:

total_items
customer_state
payment_type

## label

Optional but recommended.

Human readable name shown in the UI.

Example:

Total Items
Customer State

If omitted, the UI will display the raw column name.

## type

Required.

Defines the UI input type.

Supported types:

int
float
categorical
string
datetime
boolean

---

# Numeric Features

Example:

{
  "name": "total_items",
  "type": "int",
  "min": 1,
  "max": 50,
  "default": 1
}

## min

Optional.

Minimum allowed value.

Used to prevent invalid inputs.

## max

Optional.

Maximum allowed value.

## default

Optional.

Default value shown when the UI loads.

## step

Optional.

Controls decimal increments for float values.

Example:

0.01

---

# Categorical Features

Example:

{
  "name": "payment_type",
  "type": "categorical",
  "options": ["credit_card","boleto","voucher","debit_card"]
}

## options

Required for categorical features.

Defines dropdown choices available in the UI.

These must match the categories used during model training.

---

# String Features

Example:

{
  "name": "customer_city",
  "type": "string",
  "placeholder": "Enter customer city"
}

## placeholder

Optional helper text shown inside the input field.

## regex

Optional validation rule.

Example:

^[0-9]{5}$

Useful for structured inputs like ZIP codes.

---

# Boolean Features

Example:

{
  "name": "is_repeat_customer",
  "type": "boolean"
}

Rendered in UI as a checkbox.

---

# Datetime Features

Example:

{
  "name": "order_purchase_timestamp",
  "type": "datetime"
}

Used when features such as:

- hour
- weekday
- month

are derived from timestamps.

---

# Hidden Features

Example:

{
  "name": "order_hour",
  "type": "int",
  "hidden": true
}

Hidden features are used internally by the model but not shown in the UI.

---

# Derived Features

Example:

{
  "name": "order_day_of_week",
  "type": "categorical",
  "derived_from": "order_purchase_timestamp"
}

This indicates the feature is created from another feature.

Used for documentation purposes.

---

# Minimal Valid Feature

This is the smallest valid definition:

{
  "name": "total_items",
  "type": "int"
}

All other fields are optional.

---

# Best Practices

1. Feature names must match training dataset columns.
2. Only add validation rules when necessary.
3. Update schema version when retraining the model.
4. Ensure categorical options match training data.

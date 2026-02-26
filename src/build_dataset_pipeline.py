import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os
import scipy.stats as stats

# Functions
def exportCleanCSV(df, fileName):
    df.to_csv(f"{PATH_TO_EXPORT}{fileName}")

def addIsCanceled(df):
    df['is_canceled'] = 0
    df.loc[
        df['order_status'] == 'canceled',
        'is_canceled'
    ] = 1
    
    return df

# Code
orders = pd.read_csv("../data/raw/olist_orders_dataset.csv")
order_items = pd.read_csv("../data/raw/olist_order_items_dataset.csv")
payments = pd.read_csv("../data/raw/olist_order_payments_dataset.csv")
customers = pd.read_csv("../data/raw/olist_customers_dataset.csv")
products = pd.read_csv("../data/raw/olist_products_dataset.csv")

# Constants
PATH_TO_EXPORT = "../data/cleaned/"

def main():
    try:
        #not aggregate version
        df = orders.merge(order_items, on='order_id')
        df = df.merge(payments, on='order_id')
        df = df.merge(customers, on='customer_id')
        df = df.merge(products, on='product_id')
        
        df = addIsCanceled(df)
        order_item_dataset = df.drop(columns=['seller_id','product_category_name'], axis=1)
        exportCleanCSV(order_item_dataset, "order_item_dataset.csv")

        
        # Aggregate order_id
        order_agg = order_items.groupby("order_id").agg(
            total_items=("order_item_id", "count"),
            total_order_value=("price", "sum"),
            total_freight=("freight_value", "sum"),
            avg_item_price=("price", "mean")
        ).reset_index()
        
        # payment aggregate
        payments_agg = payments.groupby("order_id").agg(
            payment_type=("payment_type", lambda x: x.mode()[0]),
            total_payment_value=("payment_value", "sum"),
            max_installments=("payment_installments", "max")
        ).reset_index()
        
        df_agg = orders.merge(order_agg, on='order_id')
        df_agg = df_agg.merge(payments_agg, on='order_id')
        df_agg = df_agg.merge(customers, on='customer_id')
        
        df_agg = addIsCanceled(df_agg)
        exportCleanCSV(df_agg, "order_agg_modeling_v0_1.csv")
        
    except Exception as e:
        print(f"error on - {e}")

if __name__ == "__main__":
    main()
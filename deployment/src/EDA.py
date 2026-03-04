import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
from scipy.stats import chi2_contingency

# overview EDA page
def overview():

    # first subheading
    st.markdown('## Dataset Information:')

    # add source data
    st.markdown(
        """
        <small>
        Source of Dataset :
        <a href="https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce">
        Brazilian-ECommerce-Public-Dataset-by-Olist
        </a>
        </small>
        """,
        unsafe_allow_html=True
    )

    st.write("") # space

    st.markdown('In this project, the exploratory data analysis conducted with 2 datasets:')

    # dataset 1
    st.markdown(
        """
        ### Dataset 1: `modelling_df`
        > Order-item level dataset resulted from merge between raw datas. 
        Each row represent one product from a single order. 
        One order can have multiple rows for each product.
        """
    )
    st.markdown(
        """
        | Column | Description |
        | --- | --- |
        | `order_id` | order identifier |
        | `customer_id` | key to the orders dataset where each order has unique customer_id |
        | `order_status` | status of the order (delivered, shipped, canceled, etc) |
        | `order_purchase_timestamp` | purchase timestamp of a single order |
        | `order_approved_at` | payment approval timestamp of a single order |
        | `order_delivered_carrier_date` | order posting timestamp when handled to the logistic partner |
        | `order_delivered_customer_date` | actual delivery date to the customer of a single order |
        | `order_estimated_delivery_date` | estimated delivery date to the customer of a single order |
        | `order_item_id` | sequential number identifying number of items included in the same order |
        | `product_id` | product unique identifier |
        | `shipping_limit_date` | seller shipping limit date for handling the order over to the logistic partner |
        | `price` | item price of product from single order |
        | `freight_value` | item freigth value (if an order has more than one item, the freight value is splitted between items) |
        | `payment_sequential` | sequence of customer payment method (can be more than one payment method) of a single order |
        | `payment_type` | method of payment chosen by the customer of a single order |
        | `payment_installments` | number of installments for payment chosen by the customer of a single order |
        | `payment_value` | transaction value of a single order for eaach payment sequential |
        | `customer_unique_id` | unique identifier of a customer |
        | `customer_zip_code_prefix` | first five digits of customer zip code |
        | `customer_city` | customer city name |
        | `customer_state` | customer state |
        | `product_name_lenght` | number of characters extracted from the product name |
        | `product_description_lenght` | number of characters extracted from the product description |
        | `product_photos_qty` | number of product published photos |
        | `product_weight_g` | product weight measured in grams |
        | `product_length_cm` | product length measured in centimeters |
        | `product_height_cm` | product height measured in centimeters |
        | `product_width_cm` | product width measured in centimeters |
        | `is_canceled` | status whether an order is canceled or not (`1` = canceled orders, `0` = non-canceled orders) |
        """
    )

    # dataset 2
    st.markdown(
        """
        ### Dataset 2: `order_agg_modeling`
        > The dataset that has been aggregated to be in a grain version. 
        One row represent one orders, without breakdown of product from a single order.
        """
    )
    st.markdown(
        """
        | Column | Description |
        | --- | --- |
        | `order_id` | order identifier |
        | `customer_id` | key to the orders dataset where each order has unique customer_id |
        | `order_status` | status of the order (delivered, shipped, canceled, etc) |
        | `order_purchase_timestamp` | purchase timestamp of a single order |
        | `order_approved_at` | payment approval timestamp of a single order |
        | `order_delivered_carrier_date` | order posting timestamp when handled to the logistic partner |
        | `order_delivered_customer_date` | actual delivery date to the customer of a single order |
        | `order_estimated_delivery_date` | estimated delivery date to the customer of a single order |
        | `total_items` | number of products of a single order |
        | `total_order_value` | total price of products of a single order |
        | `total_freight` | freigth value of a single order |
        | `avg_item_price` | average price of products of a single order |
        | `payment_type` | method of payment chosen by the customer of a single order |
        | `max_installments` | maximum number of installments for payment chosen by the customer of a single order |
        | `total_payment_value` | total transaction value of a single order |
        | `customer_unique_id` | unique identifier of a customer |
        | `customer_zip_code_prefix` | first five digits of customer zip code |
        | `customer_city` | customer city name |
        | `customer_state` | customer state |
        | `is_canceled` | status whether an order is canceled or not (`1` = canceled orders, `0` = non-canceled orders) |

        ---
        """
    )

    # second subheading
    st.markdown('## Background of the Study:')
    st.markdown(
        """
        Indonesia's digital economy continues to grow rapidly, 
        with e-commerces as the main contributor to national Gross Merchandise Value (GMV). 
        According to the *Google, Temasek, and Bain & Company report* (e-Conomy SEA 2025), 
        Indonesia's e-commerce GMV reached approximately **US$71 billions**, 
        growing at double-digit rates annually. 
        This rapid growth presents significant operational challenges for retailers and online platforms. 
        As transaction volumes increase across multiple cities, 
        online retailers must handle thousands of daily orders across various product categories, 
        shipping methods, and payment options. 
        However, this rapid growth also have one of the challenges of operational risks, 
        that is **order cancellations**.

        Order cancellations can negatively impact business performance in several ways 
        such as lost revenue opportunities, inefficient inventory allocation, inaccurate 
        demand planning, etc. The impact becomes more critical in COD (Cash on Delivery) 
        transactions, where cancelled orders may generate additional logistics and reverse-shipping 
        costs. Also geographic factors and shipping options can further influence order completion 
        rates as well. These issues directly affect revenue realization and operational efficiency. 
        Therefore, transactional data must be properly structured and analyzed to better understand 
        cancellation patterns and support data-driven decision-making.

        Retail companies store detailed order transactional data, including order value, 
        product categories, shipping methods, payment types, geographic location, and order timestamps. 
        These features have meaningful signals that can help explain cancellation behavior. 
        Rather than analyzing cancellations only descriptively, companies need a more structured 
        and predictive approach to identify high-risk orders earlier and manage operational risk 
        more effectively.

        Source: [e-Conomy-SEA-2025-ekonomi-digital-Indonesia]
        (https://blog.google/intl/id-id/company-news/outreach-initiatives/e-conomy-sea-2025-ekonomi-digital-indonesia-mendekati-gmv-us100-miliar)

        ---
        """
    )

    # third subheading
    st.markdown('## Problem Statement and Objective:')
    st.markdown(
        """
        Despite having rich historical transactional data, the company currently analyzes cancellations 
        only in a descriptive and reactive manner. There is no structured analytical framework to 
        systematically identify patterns and risk factors associated with cancelled orders. 
        Resulted operational decisions are made **after** cancellation occur, rather than being 
        informed by proactive insights.

        Therefore, the **historical order transactional data** will be analyzed to identify 
        **patterns and risk factors associated with cancelled orders** through structured data analysis. 
        The problem can be translated into the following business questions:

        1. What is the overall cancellation rate in the historical dataset?
        2. How are cancellations distributed across customers? 
        3. How is the cancellation rate for each product? 
        4. Which payment methods are associated with higher cancellation rate?
        5. When do order cancellations most frequently occur?
        6. Where do order cancellation most frequently occur, based on customer location?
        7. Which features show the strongest relationship with order cancellations?
        8. For the top 3 features, are the differences between cancelled and non-cancelled 
        orders are statistically significant?
        """
    )

    # closing statement
    st.info("All of the above questions for exploratory data analysis (EDA) is answered on each specific page tabs.")

# load data
def load_data():
    df = pd.read_csv('https://raw.githubusercontent.com/FTDS-assignment-bay/p2-final-project-ftds-051-rmt-group-001/refs/heads/main/data/cleaned/modelling_df_v0_1.csv', 
                     index_col=0) # use index column
    df_agg = pd.read_csv('https://raw.githubusercontent.com/FTDS-assignment-bay/p2-final-project-ftds-051-rmt-group-001/refs/heads/main/data/cleaned/order_agg_modeling_v0_1.csv',
                         index_col=0) # use index column
    return df, df_agg

# preprocess clean missing data before EDA
def data_clean(df, agg_status=False):

    ## drop date columns
    df = df.drop(columns=[
        'order_approved_at', 'order_delivered_carrier_date', 
        'order_delivered_customer_date', 'order_estimated_delivery_date'
    ], axis=1)
    
    if not agg_status: # for df

        ## impute order item columns
        missing_order_items = df[df['order_item_id'].isna()]
        missing_index = missing_order_items.index
        df.loc[missing_index, 'order_item_id'] = 0
        df.loc[missing_index, 'price'] = 0
        df.loc[missing_index, 'freight_value'] = 0
        df.loc[missing_index, 'product_id'] = 'no_item'
        df = df.drop(columns=['shipping_limit_date'], axis = 1)

        ## drop rows where missing payment data columns
        df = df.dropna(subset=['payment_sequential']) # since other columns follows

        ## drop rows where missing product detail columns
        df = df.dropna(subset=['product_name_lenght']) # since other columns follows
        df = df.dropna(subset=['product_weight_g']) # since other columns suspected to follows

    else: # for df_agg

        ## impute order item columns
        missing_order_items = df[df['total_items'].isna()] # check based on column `total_items`
        missing_index = missing_order_items.index
        df.loc[missing_index, 'total_items'] = 0.0
        df.loc[missing_index, 'total_order_value'] = 0.0
        df.loc[missing_index, 'total_freight'] = 0.0
        df.loc[missing_index, 'avg_item_price'] = 0.0

        ## drop rows where missing payment data columns
        df = df.dropna(subset=['payment_type']) # since other columns follows

    return df

# for EDA question 1
def eda_q1(df, df_agg):

    st.markdown(
        """
        ---
        ## 1. Overall Cancellation Rate
        ---
        """
    )
    st.markdown(
        """
        We will analyze the overall cancellation rate on both dataset, the non-aggregated one 
        (`modelling_df` that assigned on variable `df`) also on aggregated dataset 
        (`order_agg_modeling` that assigned on variable `df_agg`).
        """
    )

    col1, col2, col3 = st.columns([10.9, 0.2, 10.9])

    with col1:
        
        ## first part
        st.markdown('First the overall cancellation rate on `df`:')
        # overall cancel rate for `df`
        cancel_rate_df= (
            df['is_canceled']
            .value_counts(normalize=True)
            .rename({0: 'Not Canceled', 1: 'Canceled'})
        )
        st.dataframe(cancel_rate_df)

        ## first pie chart for `df`
        fig = plt.figure(figsize=(8, 8))
        plt.pie(
            cancel_rate_df.values,
            labels= ["Not_cancel","Cancel"],
            autopct="%1.2f%%", # show 2 numbers after decimal
            explode=[0,0],
            wedgeprops={'width':0.3}
        )
        plt.legend(loc='upper right')
        plt.title('Cancellation Rate from Non-Aggregated Dataset', fontsize=16, fontweight='bold', y = 1)
        plt.tight_layout()
        st.pyplot(fig)

        ## insight after first pie chart
        st.markdown(
            """
            This distribution from dataset `modelling_df` shows that most orders are not canceled, 
            with a very low cancellation rate of around 0.48% of total transactions. 
            This indicates that cancellations are not a systemic issue, but rather a relatively 
            rare occurrence likely triggered by certain conditions or factors, such as payment methods, 
            specific customer behavior, or particular transaction situations. 

            Since `modelling_df` is structured at the **order-item level** 
            (where one order can appear in multiple rows if it contains multiple products), 
            this result reflects the cancellation distribution at the product-line level. 
            This indicates that our data at this granularity is already **severely imbalanced**.
            """
        )

    with col2: # vertical divider
        st.html(
            '''
                <style>
                    .vertical-line {
                        border-left: 2px solid rgba(49, 51, 63, 0.2);
                        height: 1080px;
                        margin: auto;
                    }
                </style>
                <div class="vertical-line"></div>
            '''
        )

    with col3:
    ## second part

        st.markdown(
            """
            If we check the aggregated dataset on `df_agg` (each row represents one unique order):
            """
        )
        # overall cancel rate for `df_agg`
        cancel_rate_agg= (
            df_agg['is_canceled']
            .value_counts(normalize=True)
            .rename({0: 'Not Canceled', 1: 'Canceled'})
        )
        st.dataframe(cancel_rate_agg)

        ## second pie chart for `df_agg`
        fig = plt.figure(figsize=(8, 8))
        plt.pie(
            cancel_rate_agg.values,
            labels= ["Not_cancel","Cancel"],
            autopct="%1.2f%%", # show 2 numbers after decimal
            explode=[0,0],
            wedgeprops={'width':0.3}
        )
        plt.legend(loc='upper right')
        plt.title('Cancellation Rate from Aggregated Dataset', fontsize=16, fontweight='bold', y=1)
        plt.tight_layout()
        st.pyplot(fig)

        ## insight after second pie chart
        st.markdown(
            """
            Similar to the distribution observed in `modelling_df`, the dataset `order_agg_modeling` 
            also shows that most orders are not canceled, with a cancellation rate of approximately 
            0.63% (similar cancellation rate as previously 0.48%). This further suggests that 
            cancellations are relatively rare events rather than a systemic operational issue.

            Since `order_agg_modeling` is structured at the **order level** 
            (where each row represents one unique order), this result reflects the true transaction-
            level cancellation behavior. This confirms that the target variable remains 
            **severely imbalanced**, even after aggregating from the order-item level to the 
            order-level dataset.       
            """
        )
    
    st.markdown(
        """
        Additionally, this findings suggests that breaking down transactions into individual 
        product lines may not be necessary for the modeling process. 
        This suggestion will be further evaluated in EDA question 3 later.  
        """
    )

# for EDA question 2
def eda_q2(df, df_agg):
    
    st.markdown(
        """
        ---
        ### 2. Distribution of Cancellation Across Customers
        ---
        """
    )

    col1, col2, col3 = st.columns([10.9, 0.2, 10.9])

    with col1:
        
        ## first part
        st.markdown('First, if we check the distribution on `df`:')
        # Group data by `customer_unique_id` to analyze cancellations by customer on Dataset `modelling_df`
        number_cancel_percustomer= df.groupby("customer_unique_id")["is_canceled"].sum()
        top_10 = number_cancel_percustomer.sort_values(ascending=False).head(10) # for example show top 10
        # Visualize the top 10 customer cancellations for `df`
        fig = plt.figure(figsize=(10, 6))
        sns.barplot(top_10,orient='h')
        plt.xlabel('Number of Cancellations')
        plt.ylabel('Customer Unique ID')
        plt.title('Top 10 Customer Cancellations for Non-Aggregated Dataset', fontsize=16, fontweight='bold', y=1)
        plt.tight_layout()
        st.pyplot(fig)

        ## insight after first part
        st.markdown(
            """
            Based on dataset `modelling_df`, show that order cancellations are not evenly distributed 
            across all customers, but are concentrated among a small number of customers with a high 
            frequency of cancellations. Customers with unique ID `2592816433dfbb3051af91ba91625de5` 
            have the highest number of cancellations reached 9 times, while other customers in top 5 
            were in the range of 5–6 cancellations, indicating the presence of a recurring behavior pattern 
            (repeat cancellation behavior), but not so many number of cancellations.
            """
        )

    with col2: # vertical divider
        st.html(
            '''
                <div class="divider-vertical-line"></div>
                <style>
                    .divider-vertical-line {
                        border-left: 2px solid rgba(49, 51, 63, 0.2);
                        height: 660px;
                        margin: auto;
                    }
                </style>
            '''
        )

    with col3:
        
        ## second part
        st.markdown('If we check on `df_agg` also:')
        # Group data by `customer_unique_id` to analyze cancellations by customer on Dataset `order_agg_modeling`
        num_cancel_percustomer_agg= df_agg.groupby("customer_unique_id")["is_canceled"].sum()
        top_10_agg = num_cancel_percustomer_agg.sort_values(ascending=False).head(10)
        # Visualize the top 10 customer cancellations for `df_agg`
        fig = plt.figure(figsize=(10, 6))
        sns.barplot(top_10_agg,orient='h')
        plt.xlabel('Number of Cancellations')
        plt.ylabel('Customer Unique ID')
        plt.title('Top 10 Customer Cancellations for Aggregated Dataset', fontsize=16, fontweight='bold', y=1)
        plt.tight_layout()
        st.pyplot(fig)

        ## insight after second part
        st.markdown(
            """
            Similar to the distribution observed in `modelling_df`, the aggregated dataset 
            `order_agg_modeling` shows that customer-level cancellations still relatively limited in 
            frequency, with the highest number of cancellations per customer is three orders, 
            but most customers who canceled have only one canceled order at most. 
            However, the lower number compared to the non-aggregated dataset can be explained 
            by the difference in granularity because in `modeelling_df` cancellations are recorderd 
            at order-item level, meaning a single canceled order containing multiple products may 
            be counted multiple times. On the other hand, `order_agg_modeling` records cancellations 
            strictly at the order level, counting each canceled order only once and therefore 
            providing a clearer representation of actual customer behavior.
            """
        )

    st.markdown(
        """
        This contrast highlights a key structural difference between the two datasets. 
        While `modelling_df` is suitable for analyzing detailed behavioral patterns at 
        the item per transaction level, it may overemphasize customers with multi-product 
        orders, potentially skewing higher-level insights. On the other hand, 
        `order_agg_modeling` provides a more stable and representative view of 
        cancellation behavior at the order and customer level, making it more appropriate 
        for strategic EDA and subsequent modeling without bias from product-level duplication.
        """
    )

# for EDA question 3
def eda_q3(df):
    
    st.markdown(
        """
        ---
        ### 3. Cancellation Rate for Each Product
        ---
        """
    )

    st.markdown(
        """
        We can only check cancellation rate per product on non-aggregated data, 
        that is we will use `df`. To ensure statistical relevance and avoid distortion 
        from low-volume products, we only includew products with **at least 10 total orders** 
        for this analysis.
        """
    )

    ## main part
    # Group by product_id to calculate total orders and total cancellations
    product_stats = df.groupby('product_id')['is_canceled'].agg(
        total_orders='count',
        total_canceled='sum'
    )
    # Threshold at least 10 orders
    product_stats_filtered = product_stats[product_stats['total_orders'] >= 10]
    # Calculate cancellation rate
    product_stats_filtered['cancel_rate'] = (
        product_stats_filtered['total_canceled'] /
        product_stats_filtered['total_orders']
    )
    st.write('Top 30 highest cancellation rate:')
    # Sort by highest cancellation rate
    product_stats_filtered = product_stats_filtered.sort_values(
        by='cancel_rate', ascending=False
    )
    # Show the top 30 products with the highest cancellation rate
    st.dataframe(product_stats_filtered.sort_values(
        by='cancel_rate', ascending=False
    ).head(30))

    ## visual part
    st.write('The visual for 10 highest cancellation rate')
    # Select the top 10 products with the highest cancellation rate
    top_10_products = product_stats_filtered.sort_values(
        by='cancel_rate', ascending=False
    ).head(10)
    # Visualize the top 10 product with the highest cancellation rate
    fig = plt.figure(figsize=(10, 6))
    sns.barplot(
        x=top_10_products['cancel_rate'],
        y=top_10_products.index,
        orient='h'
    )
    plt.xlabel('Cancellation Rate')
    plt.ylabel('Product ID')
    plt.title('Top 10 Products with Highest Cancellation Rate', fontweight='bold', fontsize=16, y=1)
    st.pyplot(fig)

    ## insight after plot
    st.markdown(
        """
        The results show that even after minimum 10-orders threshold, cancellation rates across 
        products still relatively close in numbers and not differ drastically. Even though a small 
        number of products have slightly higher rates (17-18%), from previous table shows these 
        rates are mostly because relative small order volumes (10 - 23 total orders). In most cases, 
        the rates correspond to only one or two canceled orders, rather than a consistently high 
        cancellation pattern.

        This indicates that the observed variation in product-level cancellation rates is largely 
        influenced by limited sample sizes rather than strong product-specific risk singals. 
        There are no clear evidence that certain products systematically drive cancellations 
        at a meaningful scale.

        Given this matter, incorporating order-item granularity into the modeling process is 
        unlikely to provide meaningful predictive advantage. Therefore, using the aggregated 
        order-level dataset remains sufficient and more appropriate for the subsequent modeling 
        process. We will use the aggregated data only (`order_agg_modeling` that stored on 
        variable `df_agg`) for further EDA questions.
        """
    )

# for EDA question 4
def eda_q4(df_agg):
    
    st.markdown(
        """
        ---
        ### 4. Cancellation Rate by Payment Type
        ---
        """
    )
    st.markdown('We can answer such questions by checking the cancellation rates per payment type:')

    ## first part
    # Group data by `payment_type` and 
    # calculate the total number of cancelled orders and total order for each payment method
    cancel_by_payment = df_agg.groupby('payment_type')['is_canceled'].agg(
        total_orders='count',
        total_canceled='sum'
    )
    # Calculate cancellation rate
    cancel_by_payment['cancel_rate'] = (
        cancel_by_payment['total_canceled'] / 
        cancel_by_payment['total_orders']
    )
    # Sort by highest cancellation rate
    cancel_by_payment = cancel_by_payment.sort_values(
        by='cancel_rate', ascending=False
    )
    st.dataframe(cancel_by_payment)

    ## visual part
    # Make a visuzaliation of cancel by payment
    fig = plt.figure(figsize=(10,6))
    sns.barplot(
        x=cancel_by_payment.index,
        y=cancel_by_payment['cancel_rate']
    )
    plt.ylabel('Cancellation Rate')
    plt.xlabel('Payment Type')
    plt.title('Cancellation Rate by Payment Type', fontsize=16, fontweight='bold', y=1)
    plt.xticks(rotation=0)
    st.pyplot(fig)
    st.write('If we plot by exclude `not_defined`:') # add statement
    # Make a visuzaliation of cancel by payment -- exclude not_defined
    filtered_payment = cancel_by_payment.drop('not_defined')
    fig = plt.figure(figsize=(10,6))
    sns.barplot(
        x=filtered_payment.index,
        y=filtered_payment['cancel_rate']
    )
    plt.ylabel('Cancellation Rate')
    plt.xlabel('Payment Type')
    plt.title('Cancellation Rate by Payment Type (Excluding not_defined)', fontweight='bold')
    plt.xticks(rotation=0)
    st.pyplot(fig)

    ## insight after plot
    st.markdown(
        """
        The first plot shows that the `not_defined` payment type has 100% cancellation rate; 
        however this category is based on extremely low transaction volume, so does not 
        represent a stable behavioral pattern. After excluding `not_defined`, 
        the second plot indicates that cancellation rates across valid payment types 
        remain relatively low, with `voucher` has slightly higher rate compared to 
        `credit_card`, `boleto`, and `debit_card`. Overall, the differences are moderate 
        and do not suggest that payment type alone strongly drives cancellation behavior.        
        """
    )

# for EDA question 5
def eda_q5(df_agg):
    
    st.markdown(
        """
        ---
        ### 5. Temporal Pattern of Order Cancellations
        ---
        """
    )
    st.markdown(
        """
        Following the process on data cleaning earlier, we will use column 
        `order_purchase_timestamp` for answering "when do order cancellations occur?" 
        because in this project we focus to the canclletion of order 
        **prior the order approved by the system**. As below with `df_agg`:
        """
    )

    ## main part
    # Convert the order purchase timestamp column to datetime format
    df_agg['order_purchase_timestamp'] = pd.to_datetime(df_agg["order_purchase_timestamp"])
    # declarate cancelled orders on a weekly basis
    cancel_date_agg = df_agg.set_index("order_purchase_timestamp")["is_canceled"].resample("W").sum()
    # Visualize plot of cancel_date_agg
    fig = plt.figure(figsize=(12,6))
    plt.plot(cancel_date_agg.index, cancel_date_agg.values)
    plt.title('Order Cancellations Trend', fontsize=16, fontweight='bold', y=1)
    st.pyplot(fig)

    ## insight after plot
    st.markdown(
        """
        Based on the cancellation pattern over time, there is no clear seasonal or 
        temporal trend that consistently drives order cancellations. 
        The cancellation activity appears to fluctuate irregularly without forming 
        a predictable pattern. This suggests that order cancellations are largely 
        situational and spontaneous, likely influenced by individual buyer decisions, 
        payment issues, or other external factors, rather than being planned or driven
        by specific time periods.        
        """
    )

# for EDA question 6
def eda_q6(df_agg):
    
    st.markdown(
        """
        ---
        ### 6. Geographic Distribution of Order Cancellations
        ---
        """
    )
    st.markdown(
        """
        For this question, we will use column `customer_state` on `df_agg`, 
        that depict customer city location to check number of cancellations across customer cities:
        """
    )

    ## main part
    # Group data by customer city and count the total
    cancel_by_location = df_agg.groupby('customer_state')['is_canceled'].sum().sort_values(ascending=False)
    # Select the top 10 cities
    top_10_state = cancel_by_location.head(10)
    # Make a visuzaliation of cancel by location
    fig = plt.figure(figsize=(10, 6))
    sns.barplot(top_10_state,orient='h')
    plt.xlabel('Number of Cancellations')
    plt.ylabel('Customer City')
    plt.title('Cancellations per Customer City Location', fontsize=16, fontweight='bold', y=1)
    plt.tight_layout()
    st.pyplot(fig)

    ## insight after plot
    st.markdown(
        """
        The results show that `SP` **State of São Paulo** has the highest number of cancelled 
        orders by a wide margin, with **327 cancellations**, followed by `RJ` 
        **State of Rio de Janeiro** with **86 cancellations** and `MG` **State of Minas Gerais** 
        with 64 cancellations. Other states such as `RS` **State of Rio Grande do Sul** and 
        `PR` **State of Paraná** record noticeably fewer cancellations, with 25 and 22 cancellations 
        respectively, while the remaining states contribute relatively small numbers.

        This pattern likely reflects the higher transaction volume in major states, 
        particularly those with large metropolitan areas, rather than a higher inherent 
        tendency for customers in these states to cancel orders.        
        """
    )

# for EDA question 7
def eda_q7(df_agg):
    
    st.markdown(
        """
        ---
        ### 7. Feature Correlation with Order Cancellations
        ---
        """
    )
    st.markdown(
        """
        We can split this question into numerical features and categorical features.
        """
    )

    ## first part
    st.markdown('First, if we check top numerical features that have strongest relationship with order cancellations:')
    # Select only numerical columns to compute the Pearson correlation matrix and extract correlations with is_canceled
    numeric_df_agg = df_agg.select_dtypes(include='number').dropna()
    numeric_df_agg = numeric_df_agg.drop(columns=['customer_zip_code_prefix'], axis = 1) # drop zip code because not numerical features
    st.dataframe(numeric_df_agg.corr()['is_canceled'].drop('is_canceled').sort_values(ascending=False))

    ## insight of first part
    st.markdown(
        """
        The correlation results shows that top numerical features are `total_items`, 
        `total_payment_value`, and `total-freight` are the strongest if we take the 
        absolute value of correlation value.
        > We order top features by taking absolute value of correlation, because negative 
        correlation value means the strong features but with 

        However, the negative correlation value means the correlation of the feature with 
        cancellation orders are as strong as the positive but inverse one. For example 
        if we take a look at `total_payment_value` and `total_freight` have almost same 
        relationship strongness with cancellation orders. We can say the higher number of 
        `total_payment_value` the more likely order will cancelled, meanwhile the higher 
        number of `total_freight` the less likely order will cancelled.

        However, by above result we can see all numerical features have relatively small 
        relationship with cancellation orders, due to low number of correlation values. 
        Since the magnitude of the correlation is very small **|r| < 0.05**, this indicates 
        only a weak linear relationship for all above features.        
        """
    )

    ## second part
    st.markdown('Next, we analyze the categorical features:')
    st.markdown(
        """
        Several columns are excluded from this analysis for the following reasons. 
        The `order_purchase_timestamp` column is dropped because time-series analysis 
        will not be used in the modeling phase, and this variable will instead be utilized 
        later for feature engineering. Columns such as `order_id`, `customer_id`, 
        `customer_unique_id`, and `order_status` are removed because they originate 
        from primary keys, candidate primary keys, or directly reflect the target variable.

        Additionally, `customer_zip_code_prefix` and `customer_city` are excluded due to 
        overlapping geographical information that is already represented by `customer_state`. 
        To avoid redundancy and multicollinearity, we retain only the higher-level geographic feature.

        As a result, the categorical analysis focuses on two key variables: 
        `payment_type` and `customer_state`, which are considered the most relevant and 
        non-redundant categorical features for evaluating their relationship with order cancellations.

        > We will repeat the process of checking correlation like this on modeling phase 
        later with respect only to the train set. This section only for EDA purposes to gain 
        information from pure historical dataset
        """
    )
    st.markdown(
        """
        We will use Chi-Square to check relationship of both features `payment_type` and 
        `customer_state` with order cancellations, or we can say:

        - **H0 (null hypothesis)**: there is **no** relationship between cancelled orders 
        and non cancelled orders with respect of *X* feature
        - **H1 (alternative hypothesis)**: there **is a significant** relationship between 
        cancelled orders and non cancelled orders with respect of *X* feature

        where *X* is feature `payment_type` and `customer_state` will be check one by one.
        """
    )
    # Check correlation for categorical column use chi-squared
    categorical_features = ['payment_type', 'customer_state']
    results = []
    for col in categorical_features:
        contingency = pd.crosstab(df_agg[col], df_agg['is_canceled'])
        chi2, p, dof, exp = chi2_contingency(contingency)
        
        results.append({
            'feature': col,
            'chi_square': chi2,
            'p_value': p
        })
    chi_square_results = pd.DataFrame(results).sort_values(
        by='chi_square', ascending=False
    )
    st.dataframe(chi_square_results)

    ## insight of second part
    st.markdown(
        """
        Based on above output, both features have the p-value < 0.05, means we reject null 
        hypothesis. Therefore, there is statistically significant relationship between 
        cancelled and non-cancelled orders with respect of both features.

        The Chi-Square test results show that `payment_type` has a very strong and 
        statistically significant relationship with order cancellations, indicated by 
        a **very high chi-square statistic (847.85)** and a **p-value close to zero**. 
        This suggests that cancellation behavior is strongly associated with the payment 
        method used, making `payment_type` one of the most influential categorical features 
        in explaining order cancellations.

        Meanwhile, `customer_state` also shows a statistically significant relationship 
        with order cancellations **chi-square= 47.94 and p-value = 0.0055**, 
        but with more weaker association strength compared to `payment_type`. 
        Given the large sample size, even moderate differences can produce small p-values, 
        but the much higher chi-square value (`payment_type`) indicates its association with 
        cancellation is stronger than that of geographic location (`customer_state`).
        """
    )

# for EDA question 8
def eda_q8(df_agg):
    
    st.markdown(
        """
        ---
        ### 8. Statistical Significance of Top Predictive Features
        ---
        """
    )
    st.markdown("""
    In this section, means the top 3 numerical features that earlier we have from 
    question no.7. If we take the absolute value of correlation value earlier on 
    question 7, we have top 3 by order `total_items`, `total_payment_value`, and 
    `total_freight`.

    We will check for these 3 features whether the differences between cancelled and 
    non-cancelled orders are statistically significant.
    """)
    st.markdown("**H0 (null hypothesis)**:")
    st.latex(r"\mu_{cancelled} = \mu_{not\_cancelled}")
    st.markdown("**H1 (alternative hypothesis)**:")
    st.latex(r"\mu_{cancelled} \neq \mu_{not\_cancelled}")

    ## main part
    # List of top numerical features to be tested
    features = ['total_items', 'total_payment_value', 'total_freight']
    # Loop feature to perform statistical testing
    for col in features:
        cancelled = df_agg[df_agg['is_canceled'] == 1][col]
        not_cancelled = df_agg[df_agg['is_canceled'] == 0][col]
        
        # Perform t-test
        t_stat, p_value = ttest_ind(cancelled, not_cancelled, equal_var=False, nan_policy='omit')
        
        # Print the t-statistic and p-value
        st.write(f"{col}: t-stat = {t_stat:.3f}, p-value = {p_value:.5f}")
    
    ## insight
    st.markdown(
        """
        The independent t-test results indicate that all three seelcted numerical features 
        (`total_items`, `total_payment_value`, and `total_freight`) show statistically 
        significant differences between cancelled and non-cancelled orders 
        (p < 0.05, reject the null hypothesis). However, while statistically significant, 
        it is important to note that the significance is influenced by the large sample size. 
        Therefore, although these features differ between the two groups, the practical effect 
        size should be interpreted with caution.

        Based on the findings from this EDA section, these features provide useful insights 
        into potential drivers of cancellation behavior. Nevertheless, during the modeling phase, 
        feature selection and correlation analysis will be repeated using only the training set, 
        rather than the full historical dataset, to ensure proper validation and avoid data leakage.
        """
    )

# main runner for whole page
def eda_page():

    st.title("Exploratory Data Analysis")

    st.html("""
    <small>
    This section presents exploratory analysis and business insights
    derived from the historical dataset.
    </small>
    """)

    # call function for load data
    df, df_agg = load_data()

    # clean data
    df = data_clean(df, False) # non-agg
    df_agg = data_clean(df_agg, True) # agg

    tab1, tab2, tab3, tab4 = st.tabs([
        "Introduction",
        "Overview",
        "Transaction Analysis",
        "Location & Feature Analysis"
    ])

    with tab1:

        # introduction overview
        overview()

    with tab2:
        
        # question 1
        eda_q1(df, df_agg)

        # question 2
        eda_q2(df, df_agg)

    with tab3:

        # question 3
        eda_q3(df)

        # question 4
        eda_q4(df_agg)

        # question 5
        eda_q5(df_agg)

    with tab4:

        # question 6
        eda_q6(df_agg)

        # question 7
        eda_q7(df_agg)

        # question 8
        eda_q8(df_agg)


if __name__ == '__main__':
    eda_page()
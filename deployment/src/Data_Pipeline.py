import pandas as pd 
import streamlit as st
import os
import plotly.express as px

BASE_PATH="https://raw.githubusercontent.com/KevinH2810/olist-raw-dataset/main/"

# LOAD DATASET
olist_raw_tables = {
    "customers": "olist_customers_dataset.csv",
    "order items": "olist_order_items_dataset.csv",
    "order payments": "olist_order_payments_dataset.csv",
    "order reviews": "olist_order_reviews_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "product category translation": "product_category_name_translation.csv"
}

relationships = {
    ("orders", "order items"): {
        "join_key": "order_id",
        "type": "One-to-Many"
    },
    ("orders", "order payments"): {
        "join_key": "order_id",
        "type": "One-to-Many"
    },
    ("orders", "customers"): {
        "join_key": "customer_id",
        "type": "Many-to-One"
    },
    ("order items", "products"): {
        "join_key": "product_id",
        "type": "Many-to-One"
    }
}

threshold_config = {
    # Critical (0% tolerance)
    "order_id": 0.0,
    "customer_id": 0.0,
    "order_status": 0.0,

    # Financial (low tolerance)
    "total_order_value": 0.02,
    "total_payment_value": 0.02,

    # Derived / Optional
    "avg_item_price": 0.05,
    "total_freight": 0.05
}

# Cached Functions
@st.cache_data
def load_table(path):
    return pd.read_csv(path)

@st.cache_data
def aggregate_order_items(df):
    return (
        df.groupby("order_id")
        .agg(
            total_items=("order_item_id", "count"),
            total_order_value=("price", "sum"),
            total_freight=("freight_value", "sum"),
            avg_item_price=("price", "mean")
        )
        .reset_index()
    )

@st.cache_data
def aggregate_payments(df):
    return (
        df.groupby("order_id")
        .agg(
            total_payment_value=("payment_value", "sum"),
            payment_count=("payment_sequential", "count")
        )
        .reset_index()
    )

# Functions

def overview():
    st.subheader("Raw Dataset Overview")

    summary_data = []

    for table_name, file_name in olist_raw_tables.items():
        file_path = os.path.join(BASE_PATH, file_name)
        df = pd.read_csv(file_path)
        # df = load_table(file_path)
        summary_data.append({
            "dataset_name": table_name,
            "row_count": len(df),
            "column_count": df.shape[1]
        })

    summary_df = pd.DataFrame(summary_data)
    st.dataframe(summary_df)

def calcMissingValues(df_selected):

    try:
        # Calculate missing %
        missing_summary = (
            df_selected.isnull().mean()
            .reset_index()
            .rename(columns={"index": "column", 0: "missing_rate"})
        )

        missing_summary["missing_rate"] = missing_summary["missing_rate"] * 100

        missing_summary = missing_summary.sort_values(
            "missing_rate", ascending=False
        )

        status_list = []

        for _, row in missing_summary.iterrows():
            col = row["column"]
            miss = row["missing_rate"]

            threshold = threshold_config.get(col, 5.0)  # default 5%

            if miss > threshold:
                status = "🔴 Critical"
            elif miss > threshold * 0.5:
                status = "🟡 Warning"
            else:
                status = "🟢 Healthy"

            status_list.append(status)

        missing_summary["threshold (%)"] = missing_summary["column"].apply(
            lambda x: threshold_config.get(x, 5.0)
        )

        missing_summary["status"] = status_list

        # ---------------------------------
        # Display
        # ---------------------------------

        st.markdown("### Missing Value Monitoring")

        st.dataframe(missing_summary)

        st.bar_chart(
            missing_summary.set_index("column")["missing_rate"]
        )

        # ---------------------------------
        # Global Alert
        # ---------------------------------

        if "🔴 Critical" in missing_summary["status"].values:
            st.error("⚠️ Critical missing value detected. Pipeline requires attention.")
        elif "🟡 Warning" in missing_summary["status"].values:
            st.warning("⚠️ Some columns approaching threshold limit.")
        else:
            st.success("✅ All monitored columns within acceptable threshold.")

    except Exception as e:
        print(f"error -- {e}")

def datasetRelationship():
    valid_pairs = list(relationships.keys())

    display_pairs = [
        f"{a.replace('_',' ').title()} and {b.replace('_',' ').title()}"
        for a, b in valid_pairs
    ]

    st.subheader("Relationship Diagnostics")

    with st.form("relationship_form"):

        selected_display = st.selectbox(
            "Select Table Relationship",
            display_pairs
        )

        run_button = st.form_submit_button("Run Diagnostics")

    # Only run after button pressed
    if run_button:

        # Map back to actual tables
        index = display_pairs.index(selected_display)
        table_a, table_b = valid_pairs[index]

        join_key = relationships[(table_a, table_b)]["join_key"]

        df_a = load_table(os.path.join(BASE_PATH, olist_raw_tables[table_a]))
        df_b = load_table(os.path.join(BASE_PATH, olist_raw_tables[table_b]))

        st.markdown(
            f"### LEFT JOIN: `{table_a}` → `{table_b}` on `{join_key}`"
        )

        # LEFT JOIN simulation
        merged = df_a.merge(
            df_b[[join_key]].drop_duplicates(),
            on=join_key,
            how="left",
            indicator=True
        )

        total_a = len(df_a)
        matched = (merged["_merge"] == "both").sum()
        unmatched = (merged["_merge"] == "left_only").sum()

        overlap_rate = matched / total_a if total_a > 0 else 0

        # Cardinality
        child_count = df_b.groupby(join_key).size()
        avg_children = child_count.mean()

        # Metrics
        col1, col2, col3 = st.columns(3)

        col1.metric("Total Rows (Left Table)", total_a)
        col2.metric("Matched Rows", matched)
        col3.metric("Unmatched Rows", unmatched)

        st.metric("Match Rate", f"{overlap_rate:.2%}")
        st.metric("Avg Linked Records", round(avg_children, 2))

        st.markdown("### Insight")

        st.write(
            f"""
            Using **LEFT JOIN**, all records from `{table_a}` are preserved.

            - {overlap_rate:.2%} of `{table_a}` records have matching entries in `{table_b}`.
            - {unmatched} records from `{table_a}` do NOT have corresponding entries in `{table_b}`.
            - On average, each `{table_a}` record links to **{round(avg_children, 2)}** `{table_b}` records.
            """
        )

def pipeline():
    st.subheader("Pipeline Construction")

    step = st.selectbox(
        "Select Pipeline Step",
        [
            "Overview",
            "Aggregation",
            "Merge",
            "Aggregate vs Non-Aggregate Dataset Comparison",
            "Join Strategy Impact",
            "Final Dataset"
        ]
    )

    if step == "Overview":

        st.markdown("""
        The modeling dataset is constructed through structured transformation:

        1. Load raw relational tables  
        2. Aggregate item-level and payment-level data  
        3. Merge transactional tables at order level  
        4. Create target variable (`is_cancelled`)  
        5. Produce final modeling dataset (1 row = 1 order)
        """)

    elif step == "Aggregation":

        st.markdown("### Order Items Aggregation")

        order_items = load_table(
            os.path.join(BASE_PATH, olist_raw_tables["order items"])
        )

        total_rows = len(order_items)
        unique_orders = order_items["order_id"].nunique()

        col1, col2, col3 = st.columns(3)
        col1.metric("Raw Rows (Items)", total_rows)
        col2.metric("Unique Orders", unique_orders)
        col3.metric("Avg Items per Order", round(total_rows / unique_orders, 2))

        order_items_agg = aggregate_order_items(order_items)

        col4, col5 = st.columns(2)
        col4.metric("Rows After Aggregation", len(order_items_agg))
        col5.metric("Compression Ratio", f"{len(order_items_agg)/total_rows:.2%}")

        with st.expander("Show Aggregated Order Items Sample"):
            st.dataframe(order_items_agg.head())

        st.markdown("---")

        st.markdown("### Payment Aggregation")

        order_payments = load_table(
            os.path.join(BASE_PATH, olist_raw_tables["order payments"])
        )

        payments_agg = aggregate_payments(order_payments)

        col6, col7 = st.columns(2)
        col6.metric("Raw Payment Rows", len(order_payments))
        col7.metric("Aggregated Rows", len(payments_agg))

        with st.expander("Show Aggregated Payment Sample"):
            st.dataframe(payments_agg.head())

    elif step == "Merge":

        orders = load_table(
            os.path.join(BASE_PATH, olist_raw_tables["orders"])
        )

        order_items = load_table(
            os.path.join(BASE_PATH, olist_raw_tables["order items"])
        )

        order_payments = load_table(
            os.path.join(BASE_PATH, olist_raw_tables["order payments"])
        )

        order_items_agg = aggregate_order_items(order_items)
        payments_agg = aggregate_payments(order_payments)

        merged_df = (
            orders
            .merge(order_items_agg, on="order_id", how="left")
            .merge(payments_agg, on="order_id", how="left")
        )

        col1, col2 = st.columns(2)
        col1.metric("Orders (Base)", len(orders))
        col2.metric("After Merge", len(merged_df))

        with st.expander("Show Merged Dataset Sample"):
            st.dataframe(merged_df.head())

    elif step == "Aggregate vs Non-Aggregate Dataset Comparison":

        st.markdown("### Dataset Grain Comparison")

        order_items = load_table(
            os.path.join(BASE_PATH, olist_raw_tables["order items"])
        )

        order_items_agg = aggregate_order_items(order_items)

        # Non-aggregated stats
        raw_rows = len(order_items)
        raw_unique_orders = order_items["order_id"].nunique()
        raw_duplicates = raw_rows - raw_unique_orders

        # Aggregated stats
        agg_rows = len(order_items_agg)
        agg_unique_orders = order_items_agg["order_id"].nunique()
        agg_duplicates = agg_rows - agg_unique_orders

        flow_df = pd.DataFrame({
            "Stage": ["Non-Aggregated (Item Level)", "Aggregated (Order Level)"],
            "Rows": [raw_rows, agg_rows]
        })

        fig = px.bar(
            flow_df,
            x="Stage",
            y="Rows",
            text="Rows",
            title="Row Compression After Aggregation"
        )

        fig.update_traces(textposition="outside")

        st.plotly_chart(fig, use_container_width=True)
        
        # =============
        dup_df = pd.DataFrame({
            "Dataset": ["Non-Aggregated", "Aggregated"],
            "Duplicate Order IDs": [raw_duplicates, agg_duplicates]
        })

        fig = px.bar(
            dup_df,
            x="Dataset",
            y="Duplicate Order IDs",
            text="Duplicate Order IDs",
            title="Duplicate Order IDs Before vs After Aggregation"
        )

        fig.update_traces(textposition="outside")

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        **Comparison Insight**

        - Non-aggregated dataset contains multiple rows per order.
        - Aggregated dataset ensures one row per order.
        - Aggregation is required to align dataset grain with cancellation prediction target.
        """)
        
        st.caption("Aggregation removes duplicate order entries and aligns dataset grain to order-level modeling.")

    elif step == "Join Strategy Impact":
        joinAnalysis()

    elif step == "Final Dataset":

        orders = load_table(
            os.path.join(BASE_PATH, olist_raw_tables["orders"])
        )

        order_items = load_table(
            os.path.join(BASE_PATH, olist_raw_tables["order items"])
        )

        order_payments = load_table(
            os.path.join(BASE_PATH, olist_raw_tables["order payments"])
        )

        order_items_agg = aggregate_order_items(order_items)
        payments_agg = aggregate_payments(order_payments)

        merged_df = (
            orders
            .merge(order_items_agg, on="order_id", how="left")
            .merge(payments_agg, on="order_id", how="left")
        )

        merged_df["is_cancelled"] = (
            merged_df["order_status"] == "canceled"
        ).astype(int)

        col1, col2 = st.columns(2)
        col1.metric("Total Rows", len(merged_df))
        col2.metric("Total Columns", merged_df.shape[1])

        st.metric(
            "Cancellation Rate",
            f"{merged_df['is_cancelled'].mean():.2%}"
        )

        with st.expander("Show Final Dataset Sample"):
            st.dataframe(merged_df.sample(10))
    
def joinAnalysis():
    st.subheader("LEFT vs INNER Join Impact")

    # ----------------------------
    # Load Data
    # ----------------------------
    orders = load_table(
        os.path.join(BASE_PATH, olist_raw_tables["orders"])
    )

    order_items = load_table(
        os.path.join(BASE_PATH, olist_raw_tables["order items"])
    )

    order_items_agg = aggregate_order_items(order_items)

    # ----------------------------
    # Perform Joins
    # ----------------------------
    inner_df = orders.merge(
        order_items_agg,
        on="order_id",
        how="inner"
    )

    left_df = orders.merge(
        order_items_agg,
        on="order_id",
        how="left",
        indicator=True
    )

    lost_orders = left_df[left_df["_merge"] == "left_only"]

    total_orders = len(orders)
    inner_count = len(inner_df)
    lost_count = len(lost_orders)
    loss_rate = lost_count / total_orders

    # ----------------------------
    # Top Metrics
    # ----------------------------
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Original Orders", total_orders)
    col2.metric("After INNER JOIN", inner_count)
    col3.metric("Orders Lost", lost_count)
    col4.metric("Loss Rate", f"{loss_rate:.2%}")

    st.divider()

    # ----------------------------
    # Distribution Comparison
    # ----------------------------
    if lost_count > 0:

        import plotly.express as px
        import pandas as pd

        # Lost distribution
        lost_dist = (
            lost_orders["order_status"]
            .value_counts(normalize=True)
            .reset_index()
        )
        lost_dist.columns = ["order_status", "lost_percentage"]
        lost_dist["lost_percentage"] *= 100

        # Overall distribution
        overall_dist = (
            orders["order_status"]
            .value_counts(normalize=True)
            .reset_index()
        )
        overall_dist.columns = ["order_status", "overall_percentage"]
        overall_dist["overall_percentage"] *= 100

        # Merge for comparison
        compare_df = pd.merge(
            lost_dist,
            overall_dist,
            on="order_status",
            how="left"
        ).fillna(0)

        st.markdown("### Status Distribution Comparison")

        fig = px.bar(
            compare_df,
            x="order_status",
            y=["lost_percentage", "overall_percentage"],
            barmode="group",
            labels={"value": "Percentage (%)", "variable": "Group"},
            title="Lost Orders vs Overall Orders (by Status)"
        )

        st.plotly_chart(fig, use_container_width=True)

        # ----------------------------
        # Insight Block
        # ----------------------------

        dominant_status = compare_df.sort_values(
            "lost_percentage", ascending=False
        ).iloc[0]["order_status"]

        st.markdown("### Interpretation")

        st.markdown(f"""
        Most dropped orders belong to **{dominant_status}** status.

        Orders without `order_items` records are primarily those that
        were terminated early in the transaction lifecycle (e.g., unavailable or canceled).

        However, the presence of other statuses (such as shipped)
        indicates that using INNER JOIN would remove valid transactional records.

        Therefore, LEFT JOIN is retained to preserve full transactional integrity
        for downstream analytics and cancellation modeling.
        """)

        if "shipped" in compare_df["order_status"].values:
            shipped_lost = compare_df.loc[
                compare_df["order_status"] == "shipped",
                "lost_percentage"
            ].values[0]

            if shipped_lost > 0:
                st.error(
                    "INNER JOIN removed shipped orders — this represents a data integrity risk."
                )

    st.caption(
        "LEFT JOIN preserves all orders, including those without item records. "
        "INNER JOIN removes orders that lack corresponding order_items entries."
    )
    
def run():
    
    st.title("Data Pipeline & Quality Overview")

    tab1, tab2, tab3, tab4 = st.tabs([
        "Raw Overview",
        "Missing Monitor",
        "Diagnostics",
        "Pipeline Construction"
    ])
    
    with tab1:
        overview()
        
    with tab2:
        st.subheader("Missing Value Monitor")
        # your selectbox + missing code here
        selected_table = st.selectbox(
            "Select table to inspect missing values:",
            list(olist_raw_tables.keys())
        )
        path = os.path.join(BASE_PATH, olist_raw_tables[selected_table])
        df_selected = load_table(path)
        
        calcMissingValues(df_selected)

    with tab3:
        datasetRelationship()  

        st.markdown("""
        - One **order** can contain multiple **order_items**
        - One **order** can have multiple **payments**
        - One **customer** can place multiple **orders**
        - Each **order_item** references a **product**
        """)
    
    with tab4:
        pipeline()

if __name__ == '__main__':
    run()
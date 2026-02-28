<p align="center">
  <img src="./src/order_guardian-logo.png" width="300" alt="Order Guardian Logo">
</p>

<h1 align="center">Order Guardian</h1>

<p align="center">
  <i>"Predict the Risk, Secure the Order"</i>
</p>

---

# Data Engineering Note

there's some `missing values` in the dataset, and for example in column `order_delivered_customer_date` the value is missing for `order_status`=`invoiced`. this is not a data faulty but business missing conditions, which is why it will not be removed or handled in DE phase

2 data cleaned set:


`modelling_df_v0_1`: is a dataset that merge between raw datas. 1 row = 1 product. 1 order can have multiple row for each product

`order_agg_modeling_v0_1`: is a dataset that has been aggregated to be in a grain version. 1 row = 1 order.

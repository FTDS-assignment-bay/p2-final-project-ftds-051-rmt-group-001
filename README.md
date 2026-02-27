[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=22872683&assignment_repo_type=AssignmentRepo)

# Data Engineering Note

there's some `missing values` in the dataset, and for example in column `order_delivered_customer_date` the value is missing for `order_status`=`invoiced`. this is not a data faulty but business missing conditions, which is why it will not be removed or handled in DE phase

2 data cleaned set:


`modelling_df_v0_1`: is a dataset that merge between raw datas. 1 row = 1 product. 1 order can have multiple row for each product

`order_agg_modeling_v0_1`: is a dataset that has been aggregated to be in a grain version. 1 row = 1 order.


# Data Science Note
kolom yang tidak di pakai `'customer_id','order_id','customer_unique_id','order_status','is_canceled'`
reason : `kolom primary key, candidate primary key, dan kolom target`

kolom yang ingin di drop, tapi masih di pakai : `'order_delivered_carrier_date','order_delivered_customer_date','order_estimated_delivery_date'`
reason : apakah mungkin jika kolom date kosong akan di predict cancel ? 

Missing Value pada kolom Data tidak bergantung pada order status canceled.
ada status Canceled tapi ada order_date (refund ?)

untuk `'total_items','total_order_value','total_freight','avg_item_price'` masih on investigate pola missingnya.

Data Missing : 
order_delivered_customer_date    2356 [drop Candidate]
order_delivered_carrier_date     1174 [drop Candidate]
total_items                       172 [on investigate]
total_order_value                 172 [on investigate]
total_freight                     172 [on investigate]
avg_item_price                    172 [on investigate]
order_approved_at                 160 [on investigate]
payment_type                        1 [input unknown]
total_payment_value                 1 [input 0]
max_installments                    1 [input 0]

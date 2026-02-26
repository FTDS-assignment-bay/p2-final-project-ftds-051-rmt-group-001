[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=22872683&assignment_repo_type=AssignmentRepo)

# Data Engineering Note

there's some `missing values` in the dataset, and for example in column `order_delivered_customer_date` the value is missing for `order_status`=`invoiced`. this is not a data faulty but business missing conditions, which is why it will not be removed or handled in DE phase

2 data cleaned set:


`modelling_df_v0_1`: is a dataset that merge between raw datas. 1 row = 1 product. 1 order can have multiple row for each product

`order_agg_modeling_v0_1`: is a dataset that has been aggregated to be in a grain version. 1 row = 1 order.

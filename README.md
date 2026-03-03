<p align="center">
  <img src="./src/order_guardian-logo.png" width="300" alt="Order Guardian Logo">
</p>

<p align="center">
  <i>"Detecting Risk, Delivering Trust"</i>
</p>

# References Link

- [Dataset-Source](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
- [Google-Slides](https://docs.google.com/presentation/d/17xGm80vCwvWv92I0NEuK2LxuqmuJVPEYhLiWFFzEE04/edit?usp=sharing)
- [Tableau-Dashboard-DA](https://public.tableau.com/app/profile/maulana.malik.fajri/viz/FinalProject_17725074492550/Dashboard1)
- [HuggingFace-Deployment](https://huggingface.co/spaces/Heizsenberg/order-guardian)

---

# Data Engineering Note

there's some `missing values` in the dataset, and for example in column `order_delivered_customer_date` the value is missing for `order_status`=`invoiced`. this is not a data faulty but business missing conditions, which is why it will not be removed or handled in DE phase

2 data cleaned set:


`modelling_df_v0_1`: is a dataset that merge between raw datas. 1 row = 1 product. 1 order can have multiple row for each product

`order_agg_modeling_v0_1`: is a dataset that has been aggregated to be in a grain version. 1 row = 1 order.

---

# Data Analysis Note

All EDA insights and code with 8 business questions completed in file `'/EDA/EDA ver_1.ipynb'`
- Question 1 - 2 use both dataset, non-aggregated and aggregated ones
- Question 3, only use non-aggregated dataset
- Questin 4 and so on use aggregated dataset
# Data Science Note   
kolom yang tidak di pakai `'customer_id','order_id','customer_unique_id','order_status','is_canceled'`   
reason : `kolom primary key, candidate primary key, dan kolom target`   

kolom yang ingin di drop, tapi masih di pakai : `'order_delivered_carrier_date','order_delivered_customer_date','order_estimated_delivery_date'`   
reason : apakah mungkin jika kolom date kosong akan di predict cancel ?    

Missing Value pada kolom Data tidak bergantung pada order status canceled.    
ada status Canceled tapi ada order_date (refund ?)    

untuk `'total_items','total_order_value','total_freight','avg_item_price'` masih on investigate pola missingnya.    

Data Missing :    
[drop Candidate] order_delivered_customer_date    2356    
[drop Candidate] order_delivered_carrier_date     1174    
[on investigate] total_items                       172    
[on investigate] total_order_value                 172    
[on investigate] total_freight                     172    
[on investigate] avg_item_price                    172    
[on investigate] order_approved_at                 160    
[input unknown]  payment_type                        1    
[input 0]        total_payment_value                 1    
[input 0]        max_installments                    1    


Base Model : Logistic Reg
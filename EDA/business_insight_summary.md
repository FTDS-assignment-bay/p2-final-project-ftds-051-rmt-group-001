Business Insight & Implications

1. Most Impactful Features on Order Cancellation

Based on the EDA results and statistical testing, order cancellations are not driven by a single factor, but rather by a combination of multiple features.
The most impactful features include:
- Payment type, which shows the strongest statistical association with order cancellation.
- Numerical features such as total_items, total_payment_value, and total_freight, which exhibit statistically significant        differences between canceled and non-canceled orders, although their practical effect sizes are relatively small.
- Customer location (state), particularly SP (São Paulo), which records the highest number of cancellations.

2. Business Approach Simulation (Risk Based Thinking)

Since the Olist dataset doesnt explicitly provide cancellation reasons, the most realistic business approach is to classify orders based on risk levels, rather than attempting to explain individual cancellation reasons.

In this context:
- Orders are categorized into **High Risk** and **Low Risk** groups.
- Risk categories are determines by a combination of features such as:
    - Payment type
    - Transaction valuee
    - Number of items
    - Customer location
This approach is more actionable for business decision-making compared to purely descriptive analysis.

3. Business Insight from Payment Type (Voucher & High Risk Order)
EDA results indicate that:
- Voucher payments have a higher cancellation rate compared to other payment methods (excluding the not_defined category, which has a very small volume).
- This suggests that vouchers provide greater flexibility to customers, making cancellation decisions easier.

4. Business implications:
If a customer or order is predicted as high risk, the business may apply strategies such as:
- Limiting or disabling voucher usage, free shipping, and stackable promotions (voucher + cashback).
- Restricting voucher usage for high-value orders.
- Applying additional validation steps before order processing.
- Limiting certain voucher combinations in high-risk regions.
- Disabling specific payment methods for high-risk orders.

5. Location Based Insight
Although São Paulo (SP) has the highest number of order cancellations, EDA results show that this is primarily driven by the very large transaction volume in the region, rather than a higher tendency of customers in SP to cancel orders.

However, from a business perspective:
- SP remains a priority region for operational risk monitoring.
- The combination of SP + certain payment types (e.g., voucher) can be treated as a stronger risk signal.

Potential strategis include
- Special monitoring for orders from SP using high-risk payment types.
- Adjusting campaigns or promotional strategies based on regional risk profiles.
<p align="center">
  <img src="./src/order_guardian-logo.png" width="300" alt="Order Guardian Logo">
</p>

<p align="center">
  <i>"Detecting Risk, Delivering Trust"</i>
</p>

---

# Business Overview

## 1. Project Overview

**Order Guardian** is a predictive analytics system designed to identify and monitor high-risk e-commerce orders before operational resources are fully allocated. 

As digital commerce continues to grow, order cancellations have become a significant operational challenge. High cancellation rates can result in revenue not being realized, inefficient inventory allocation, and additional logistic costs, particularly in Cash-on-Delivery (COD) transactions where fulfillment costs may already be incurred before payment is secured.

Order Guardian transforms structured transactional data into actionable risk insights through predictive modeling. By identifying high-risk orders at checkout, the company can take preventive actions to reduce operational waste and improve revenue realization.

The goal of this system is not to eliminate cancellations entirely, but to manage cancellation risk more effectively through data-driven decision support.

## 2. Business Problem

Despite having detailed transcational data, the company currently may handles cancellations reactively, often after logistics and operational resources have already been allocated.

Order cancellations create several business risks:

- Revenue that was expected is not realized
- Inventory is temporarily reserved for orders that do not complete
- Logistics and reverse shipping costs increase, especially in COD transactions

Without a structured risk management mechanism, the company lacks visibility into which orders are more likely to cancel. This limits the ability to apply targeted interventions before fulfillment begins.

However, implementing strict restrictions across all customers is not ideal, as it may negatively impact customer experience and order conversion.

Therefore, the core business challenge is balancing two priorities:
- Reducing cancellation-related operational losses
- Maintaining normal customer purchasing flow without unnecessary restriction

Order Guardian is designed to help the company apply control only to orders that carry higher cancellation risk, instead of restricting all customers. This allows the business to reduce operational loss while keeping the purchasing process stable for most users.

## 3. Business Objective

The objective of Order Guardian is to reduce operational exposure caused by order cancellations by identifying high-risk orders before fulfillment begins.

Specifically, this project aims to:
- Reduce cancellation rate within identified high-risk orders
- Apply targeted control measures without broadly restricting all customers
- Maintain stable order conversion while minimizing operational waste 

The system focuses on risk-based management rather than eliminating cancellations entirely.

## 4. Business Impact Simulation (Conceptual)

To estimate potential business impact, a simulation as follow:

- Total orders: 100,000
- Current cancellation rate: 0.6% (600 cancelled orders)
- Estimated operational cost per cancelled order: $8 (including logistics handling, reverse shipping, processing)

Estimated total operational loss: 600 $\times$ $8 = $4,800

By using Order Guardian, the system ranks orders by risk level. Suppose the top 10% highest-risk orders (10,000 orders in this simulation) accounts to 40% of total cancellations (on this 10,000 orders there are 240 cancelled orders).

If targeted intervention (suppose by disable COD feature, or require prepayment, etc) reduces cancellations in this segment by 25%, then:
- Prevented cancellations: 60 orders
- Estimated cost savings: 60 $\times$ $8 = $480

This represents a potential 10% reduction in total cancellation-related operational loss, while applying intervention only to a limited portion of total transactions.

## 5. Success Metrics


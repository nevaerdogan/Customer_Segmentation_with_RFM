🛍️ FLO Customer Segmentation with RFM Analysis A comprehensive customer segmentation project using RFM (Recency, Frequency, Monetary) analysis to help FLO develop targeted marketing strategies for different customer segments.

Business Problem FLO, a leading retail company, wants to segment its customers and determine targeted marketing strategies for each segment. By analyzing customer behaviors and creating behavioral clusters, FLO aims to: -Identify high-value customer segments -Develop personalized marketing campaigns -Optimize resource allocation for customer retention -Increase customer lifetime value

Dataset Size: 20,000 customers

Methodology RFM Analysis RFM is a proven marketing analysis technique that segments customers based on three key dimensions: 
R - Recency How recently did the customer make a purchase? Lower recency = More engaged customer Scored from 1 (least recent) to 5 (most recent)

F - Frequency How often does the customer make purchases? Higher frequency = More loyal customer Scored from 1 (lowest) to 5 (highest)

M - Monetary How much money does the customer spend? Higher monetary value = More valuable customer Scored from 1 (lowest) to 5 (highest)

Analysis Workflow Data Preparation ↓ RFM Metrics Calculation ↓ RFM Scoring (1-5 scale) ↓ Customer Segmentation ↓ Actionable Insights

Project Structure
flo-rfm-analysis/ 
│ ├── flo_rfm_analysis.py # Main analysis script
├── README.md # Project documentation
│ ├── data/ 
│ └── flo_data_20k.csv # Customer data (not included)
│ └── outputs/ 
├── yeni_marka_hedef_müşteri_id.csv # Target customers for new brand 
└── indirim_hedef_müşteri_ids.csv # Target customers for discount campaign

Business Applications Case Study 1: New Women's Shoe Brand Launch Objective: Promote a premium women's shoe brand Target Audience:

Loyal customers (Champions & Loyal Customers segments) Interested in women's category Higher purchasing power

Output: yeni_marka_hedef_müşteri_id.csv Expected Impact:

Higher conversion rates due to targeted approach Better ROI on marketing spend Increased brand awareness among high-value customers

Case Study 2: Men's & Children's Products Discount Campaign Objective: Re-engage past customers and attract new ones with 40% discount Target Audience:

At-risk customers (can't_loose, at_risk, about_to_sleep) New customers Interested in men's or children's categories

Output: indirim_hedef_müşteri_ids.csv

Neva Erdogan, 🔗 www.linkedin.com/in/nevaerdogan

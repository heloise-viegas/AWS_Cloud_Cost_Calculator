# 🧾 AWS Billing Dashboard & CloudWatch Alerts

A **serverless AWS billing monitoring system** that tracks, visualizes, and alerts you when cloud spending exceeds defined thresholds.  
This project combines **AWS Lambda**, **CloudWatch**, **S3**, and **Cost Explorer** to give you a clear view of weekly costs and trends — all through an automated **dashboard** and **alerting system**.
<img width="1903" height="926" alt="image" src="https://github.com/user-attachments/assets/bcc967b5-ec09-40c0-be5c-70090820b7c6" />

---

Problem:
Tracking AWS costs manually is time-consuming and lacks visibility into weekly trends or sudden cost spikes.

System/Solution:
A serverless AWS Billing Dashboard using Lambda, Cost Explorer, and S3 — automating weekly cost collection, comparison, and visualization with CloudWatch alerts for thresholds.

Result:
Real-time cost insights, weekly trend comparisons, and proactive alerts help control AWS expenses efficiently and transparently.

## 🚀 Features

- **Automated Weekly Billing Reports** using AWS Cost Explorer.  
- **Interactive Web Dashboard** hosted on S3 or CloudFront.  
- **Service-wise Cost Breakdown** in tables and charts.  
- **Week-over-Week Comparison** with percentage changes.  
- **CloudWatch Alarms** that trigger when total cost exceeds threshold.  
- **CloudWatch Dashboard** to visualize total and service-level costs.  
- **Serverless Deployment** — no manual maintenance required.

---

## 🏗️ Architecture Overview

```text
+----------------------+
|  AWS Cost Explorer   |
+----------+-----------+
           |
           v
+----------------------+
|      AWS Lambda      |
| - Fetches current &  |
|   previous week's    |
|   billing data        |
| - Compares reports    |
| - Stores JSON in S3   |
+----------+-----------+
           |
           v
+----------------------+
|       Amazon S3      |
| - billing_report.json |
| - comparison_report.json |
| - index.html dashboard  |
+----------+-----------+
           |
           v
+----------------------+
|  Browser Dashboard   |
| - Visual charts      |
| - Comparison tables  |
| - Weekly insights    |
+----------+-----------+
           |
           v
+----------------------+
| CloudWatch Alarm &   |
| Dashboard Monitoring |
+----------------------+
```

---

## 🎯 Project Goals

1. **Track AWS resource costs weekly** with visual dashboards.  
2. **Automatically alert** when total spending crosses a defined threshold.  
3. **Create a CloudWatch dashboard** for cost visualization and alert monitoring.

---

## ⚙️ Setup Steps

### **1️⃣ Enable Billing Alerts for the AWS Account**

Before creating alarms, you must enable billing data to appear in CloudWatch.

**Steps:**
1. Sign in to the **AWS Management Console** as root or billing admin.  
2. Go to **Billing and Cost Management → Preferences**.  
3. Under *Cost Management Preferences*, enable:  
   - ✅ “Receive Billing Alerts”  
   - ✅ “Activate IAM Access”  
4. Save changes.  
5. Wait a few hours for billing metrics to populate in **CloudWatch → Metrics → Billing**.

---

### **2️⃣ Create the CloudWatch Alarm**

**Goal:** Trigger an alert when the total AWS cost exceeds a defined threshold (e.g., $10).

**Steps:**
1. Go to **CloudWatch → Alarms → All alarms → Create alarm**.  
2. Choose metric:
   ```
   Billing → Total Estimated Charge → USD
   ```
3. Set condition:
   - Threshold type: `Static`
   - Whenever cost **is greater than** `10`
4. Configure actions:
   - Create or select an **SNS topic**
   - Add your **email address** for alerts
5. Name the alarm, e.g., `AWSBillingThresholdExceeded`
6. Click **Create alarm**
<img width="1908" height="848" alt="image" src="https://github.com/user-attachments/assets/ecd07ab4-d6a4-4e87-9f5c-52cc1ce68604" />
<img width="1377" height="422" alt="image" src="https://github.com/user-attachments/assets/e01e483c-6646-443e-89e2-48304c596173" />


---

### **3️⃣ Create a CloudWatch Dashboard**

**Goal:** Display total cost and attach the alarm widget.

**Steps:**
1. Go to **CloudWatch → Dashboards → Create dashboard**
2. Choose Billing Dashboard that is pre created and select Add.  
3. Choose a name (e.g., `BillingDashboard`)  
4. Add widgets:
   - **Alarm widget:**  
     - Add the alarm created earlier (`AWSBillingThresholdExceeded`)
5. Save the dashboard.  
Now you have a real-time cost visualization + alert display.

---

### **4️⃣ Create S3 Bucket for Website Hosting**

**Steps:**
1. Go to **S3 → Create bucket**
   - Enable *Block all public access* → **OFF**
   - Enable *Static website hosting*
2. Under **Properties → Static website hosting**, choose:
   - Hosting type: *Host a static website*
   - Index document: `index.html`
3. Upload:
   - `index.html`
   - `billing_report.json`
   - `comparison_report.json`
4. Copy and save the **Bucket Website URL**.

---

### **5️⃣ Create AWS Lambda Function**

Use the custom script **`custom_billing_lambda.py`** to fetch AWS Cost Explorer data.

**Lambda Responsibilities:**
- Fetch weekly billing data via `get_cost_and_usage`
- Compare current vs. previous week
- Save:
  - `billing_report.json`
  - `comparison_report.json`
- Upload to S3

---

### **6️⃣ Create the Dashboard UI**

Create a responsive HTML/JS dashboard (`index.html`) that:
- Loads JSON data from S3  
- Displays charts
- Contains two tables:
  - Current week billing
  - Week-over-week comparison

---

### **7️⃣ Upload the UI to S3**

Upload the `index.html` file to your S3 bucket.
The   `billing_report.json` and  `comparison_report.json` will be uploaded to s3 by the lambda function.

---

### **8️⃣ Assign Permissions to Lambda**

Attach an IAM role with permissions:

```json
{
  "Effect": "Allow",
  "Action": [
    "ce:GetCostAndUsage",
    "s3:GetObject",
    "s3:PutObject"
  ],
  "Resource": "*"
}
```

Add environment variable:
```
BUCKET_NAME = your-s3-bucket-name
```
This can be configured in the Lambda configuration settings and accessed as a environment variable in the code.<img width="1775" height="829" alt="image" src="https://github.com/user-attachments/assets/4f474393-0a3c-4142-bbcd-edf3a212ebcf" />


---

### **9️⃣ Deploy & Test**

- Trigger Lambda manually or via **EventBridge (weekly)**.  
- Verify:
  - `billing_report.json` and `comparison_report.json` in S3.  
  - Dashboard loads updated data.  
  - CloudWatch alarm triggers when threshold is exceeded.
    <img width="1519" height="492" alt="image" src="https://github.com/user-attachments/assets/9e622060-1bd4-4713-980f-c64791346863" />


---

## 🧩 Data Structure

### billing_report.json
```json
{
  "Amazon EC2": 12.5,
  "Amazon S3": 3.2,
  "AWS Lambda": 0.8,
  "Total": 16.5
}
```

### comparison_report.json
```json
{
  "services": {
    "Amazon EC2": {
      "previous": 10.5,
      "current": 12.5,
      "diff": 2.0,
      "percent_change": 19.05
    }
  }
}
```

---
## 🧰 Tech Stack

| Component | Technology |
|------------|-------------|
| Backend | AWS Lambda (Python 3.x) |
| Data Source | AWS Cost Explorer |
| Storage | Amazon S3 |
| Frontend | HTML, CSS, JavaScript |
| Charts | Chart.js |
| Monitoring | Amazon CloudWatch |
| Scheduler | Amazon EventBridge |

---
## 👩‍💻 Author

**Heloise Viegas**
DevOps Engineer • AWS | Kubernetes | Terraform | CI/CD
📧 *(https://www.linkedin.com/in/heloise-viegas/)*


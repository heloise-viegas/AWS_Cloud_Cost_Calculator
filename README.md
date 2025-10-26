# 🧾 AWS Billing Dashboard

A **serverless web dashboard** that visualizes and compares **AWS billing data** week-over-week using AWS Cost Explorer, S3, and Lambda.
The dashboard displays current weekly costs, historical comparisons, and service-wise cost breakdowns in both table and chart formats.

---

## 🚀 Features

* **Automated Data Fetching:**
  AWS Lambda fetches weekly cost and usage data from **Cost Explorer**.

* **Dynamic Dashboard:**
  HTML + JavaScript front-end hosted on **S3 (Static Website)** or **CloudFront**.

* **Service-wise Breakdown:**
  Displays AWS services and their corresponding costs in a scrollable table.

* **Week-over-Week Comparison:**
  Compares current week’s costs with the previous week, showing % changes.

* **Auto-updating Reports:**
  Lambda updates JSON files in S3 that the dashboard reads from dynamically.

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
| - Scrollable tables  |
| - Weekly comparison  |
+----------------------+
```

---

## ⚙️ AWS Lambda

### **Lambda Responsibilities**

* Fetches weekly billing data via **Cost Explorer API** (`get_cost_and_usage`).
* Reads previous week’s report from S3.
* Compares the two reports and calculates:

  * Difference
  * Percent change
* Saves:

  * `billing_report.json` — current week’s data
  * `comparison_report.json` — comparison results

### **Environment Setup**

#### IAM Permissions Required by Lamba:

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

#### Environment Variables:

| Variable      | Description                           |
| ------------- | ------------------------------------- |
| `BUCKET_NAME` | Name of the S3 bucket hosting reports |

---
### **JSON Files Used:**

| File                     | Purpose                  |
| ------------------------ | ------------------------ |
| `billing_report.json`    | Weekly AWS billing data  |
| `comparison_report.json` | Weekly comparison report |

---

## 📂 S3 Folder Structure

```
my-billing-dashboard/
│
├── index.html                # Dashboard UI
├── billing_report.json       # Current week's data
└── comparison_report.json    # Week-over-week comparison
```

---

## 🧠 Data Format

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
    },
    "Amazon S3": {
      "previous": 3.5,
      "current": 3.2,
      "diff": -0.3,
      "percent_change": -8.57
    }
  }
}
```

---

## 🧩 Deployment Steps

### 1️⃣ Create an S3 Bucket

* Enable **Static Website Hosting**
* Upload:

  * `index.html`
  * `billing_report.json`
  * `comparison_report.json`

### 2️⃣ Deploy the Lambda Function

* Add environment variable `BUCKET_NAME`
* Attach permissions for `ce:GetCostAndUsage` and S3 read/write
* Schedule it using **EventBridge (weekly)**

### 3️⃣ Access the Dashboard

* Open the S3 bucket’s **Static Website URL** (or distribute via CloudFront).

---

## 🧰 Tech Stack

| Component   | Technology              |
| ----------- | ----------------------- |
| Backend     | AWS Lambda (Python 3.x) |
| Data Source | AWS Cost Explorer       |
| Storage     | Amazon S3               |
| Frontend    | HTML, CSS, JavaScript   |
| Charts      | Chart.js                |
| Scheduler   | Amazon EventBridge      |

---

## 👩‍💻 Author

**Heloise Viegas**
DevOps Engineer • AWS | Kubernetes | Terraform | CI/CD
📧 *(https://www.linkedin.com/in/heloise-viegas/)*


# 📊 MaxDiff Scaling — Simple Count Method with Visualizations

This repository contains a **Python implementation** of **MaxDiff (Maximum Difference Scaling)** using the **Simple Count method**, along with confidence interval estimation and visualization.

It is the **first part of a larger series** exploring MaxDiff methodologies (Simple Count, Logistic Regression, Hierarchical Bayes) and their **applied use cases across retail, marketing, HR/people analytics, healthcare, and technology**.

---

## 📌 What is MaxDiff?

MaxDiff (or Best–Worst Scaling) is a survey-based technique where respondents are shown small sets of items and asked:

* Which is **most important**?
* Which is **least important**?

Compared to rating scales (1–5 stars, Likert), MaxDiff:
✔️ Forces **trade-offs**
✔️ Reduces **rating biases**
✔️ Produces clear, **rank-ordered preferences**

Example (Retail product features):

* Set 1 → Most: *Free Shipping*, Least: *Easy Returns*
* Set 2 → Most: *Same-Day Delivery*, Least: *Discounts*

---

## 📂 Repository Contents

* **`max_diff_scaling.py`** → main script

  * Simulates toy survey responses
  * Computes simple-count preference scores
  * Estimates ~95% confidence intervals (approximate)
  * Generates two key plots:

    1. **CI Lollipop Plot** → Statistical view (scores + confidence intervals)
    2. **Executive Bar Chart** → Leadership view (0–100 scaled utilities)
  * Saves outputs as CSV + PNGs

* **`outputs/`** (auto-created) → contains results after running the script:

  * `maxdiff_simplecount_results.csv` → Tabular results with scores + CI
  * `maxdiff_simplecount_ci.png` → Lollipop plot with CI
  * `maxdiff_scaled_bar.png` → Executive 0–100 bar chart

---

## ⚙️ Installation

Clone the repo and install dependencies:

```bash
git clone https://github.com/srishti2906/maxdiff-scaling.git
cd maxdiff-scaling

# (optional) create a virtual environment
python -m venv .venv
source .venv/bin/activate   # on Linux/Mac
.venv\Scripts\activate      # on Windows

# install requirements
pip install -r requirements.txt
```

---

## ▶️ Usage

Run the script to simulate data and generate outputs:

```bash
python max_diff_scaling.py
```

Results will be saved in the `outputs/` folder.

---

## 📊 Example Outputs

**1️⃣ MaxDiff Simple-Count Scores with ~95% CI**
(Statistical view: dots = mean score, bars = CI, zero = neutral baseline)

**2️⃣ MaxDiff — Executive View (Scaled Utilities)**
(Leadership view: rescaled 0–100, shows priority order & gaps)

---

## 🔮 Roadmap
This repo will grow as the series progresses:

Article 1 → Simple Count Method ✅
Article 2 → 🔜
Article 3 → 🔜
Article 4 → 🔜
Article 5 → 🔜
Article 6 → 🔜
Article 7 → 🔜

Follow along with the articles + code for **hands-on learning**.

---

## 📎 References

* Orme, B. “Getting Started with MaxDiff” — Sawtooth Software
* Louviere, Flynn, Marley. *Best-Worst Scaling: Theory, Methods and Applications*

---

## 🏷️ Tags

#MaxDiff #DataScience #SurveyDesign #RetailAnalytics #MarketingAnalytics #DecisionScience #Python

---

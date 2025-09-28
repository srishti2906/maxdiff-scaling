# MaxDiff Scaling — Simple Count Method with Visualizations

This repository contains a Python implementation of **MaxDiff Scaling (Maximum Difference Scaling)** using the **Simple Count method**.  
It is part of a larger series exploring MaxDiff for applied analytics across retail, HR/people analytics, marketing, and more.

---

## 📌 What is MaxDiff?
MaxDiff (or Best-Worst Scaling) is a survey-based technique where respondents are shown sets of items and asked:
- Which is **most important**?
- Which is **least important**?

Compared to rating scales (1–5 stars, Likert), MaxDiff:
- Forces **trade-offs**
- Reduces **rating biases**
- Produces clear, **rank-ordered preferences**

---

## 📂 Contents
- `max_diff_scaling.py` → main script  
  - Simulates toy survey responses
  - Computes simple-count preference scores
  - Estimates ~95% confidence intervals
  - Generates two plots:
    1. **CI Lollipop plot** (scores with confidence intervals)
    2. **Executive bar chart** (scaled 0–100 utilities)
  - Saves results as CSV + PNGs

- `outputs/` (created after running script) → contains:
  - `maxdiff_simplecount_results.csv`
  - `maxdiff_simplecount_ci.png`
  - `maxdiff_scaled_bar.png`

---

## ⚙️ Installation

Clone the repo and install dependencies:

```bash
git clone [https://github.com/<your-username>/maxdiff-scaling.git](https://github.com/srishti2906/maxdiff-scaling.git)
cd maxdiff-scaling

# (optional) create a virtual environment
python -m venv .venv
source .venv/bin/activate

# install requirements
pip install -r requirements.txt

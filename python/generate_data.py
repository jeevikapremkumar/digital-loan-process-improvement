"""
Generate a SIMULATED digital loan application dataset (12,000 applications, 2025).
All data is synthetic and created for a portfolio project. Patterns (e.g. document
upload friction, slow manual verification) are deliberately built in so the analysis
has realistic business problems to find. Replace with a real dataset if available.
"""
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
N = 12000

STAGES = {1: "Application Started", 2: "Personal Details", 3: "Document Upload",
          4: "Verification", 5: "Credit Assessment", 6: "Decision"}

rows = []
for i in range(N):
    date = pd.Timestamp("2025-01-01") + pd.Timedelta(days=int(rng.integers(0, 365)))
    channel = rng.choice(["Branch", "Online", "Mobile App"], p=[0.35, 0.40, 0.25])
    loan_type = rng.choice(["Personal", "Home", "Auto", "Education"], p=[0.40, 0.20, 0.25, 0.15])
    amount = {"Personal": rng.integers(50, 500), "Home": rng.integers(1500, 8000),
              "Auto": rng.integers(400, 1500), "Education": rng.integers(200, 1200)}[loan_type] * 1000
    age = int(np.clip(rng.normal(35, 9), 21, 65))
    employment = rng.choice(["Salaried", "Self-Employed", "Student/Other"], p=[0.60, 0.30, 0.10])
    credit = int(np.clip(rng.normal(690, 70), 300, 850))

    # Documents complete on first attempt (digital channels struggle more)
    p_docs = {"Branch": 0.86, "Online": 0.60, "Mobile App": 0.52}[channel]
    docs_ok = rng.random() < p_docs

    reached, status, drop_stage, reason = 1, None, None, None
    verif_days = doc_days = credit_days = 0
    resubmissions = 0

    # Stage 1 -> 2
    if rng.random() < (0.05 + (0.03 if channel == "Mobile App" else 0)):
        status, drop_stage = "Abandoned", 1
    else:
        reached = 2
    # Stage 2 -> 3
    if status is None:
        if rng.random() < 0.09:
            status, drop_stage = "Abandoned", 2
        else:
            reached = 3
    # Stage 3 Document upload
    if status is None:
        doc_days = int(rng.integers(1, 3))
        p_drop = 0.07 if docs_ok else 0.30
        if channel != "Branch":
            p_drop += 0.04
        if amount > 1_000_000:
            p_drop += 0.03
        if not docs_ok:
            resubmissions = int(rng.integers(1, 3))
            doc_days += resubmissions * int(rng.integers(2, 5))
        if rng.random() < p_drop:
            status, drop_stage = "Abandoned", 3
        else:
            reached = 4
    # Stage 4 Verification (manual, slow for self-employed)
    manual = employment != "Salaried"
    if status is None:
        base = {"Branch": rng.integers(2, 5), "Online": rng.integers(3, 7),
                "Mobile App": rng.integers(3, 7)}[channel]
        verif_days = int(base + (rng.integers(2, 5) if manual else 0))
        p_drop = min(0.04 + 0.012 * verif_days, 0.30)
        if rng.random() < p_drop:
            status, drop_stage = "Abandoned", 4
        else:
            reached = 5
    # Stage 5 -> 6 Credit assessment and decision
    if status is None:
        credit_days = int(rng.integers(1, 4))
        reached = 6
        reject_p = 0.08 + max(0, (650 - credit)) / 400
        if not docs_ok and rng.random() < 0.15:
            status, reason = "Rejected", "Incomplete / Invalid Documents"
        elif rng.random() < reject_p:
            status = "Rejected"
            reason = rng.choice(["Low Credit Score", "High Debt-to-Income", "Verification Mismatch"],
                                p=[0.55, 0.30, 0.15])
        else:
            status = "Approved"

    decided = status in ("Approved", "Rejected")
    total_days = doc_days + verif_days + credit_days + 1 if decided else None
    rows.append(dict(
        application_id=f"LN{100000 + i}", application_date=date.date(), channel=channel,
        loan_type=loan_type, loan_amount=int(amount), applicant_age=age, employment_type=employment,
        credit_score=credit, docs_complete_first_attempt=int(docs_ok), resubmissions=resubmissions,
        manual_verification=int(manual), furthest_stage=reached, final_status=status,
        drop_stage=STAGES.get(drop_stage) if drop_stage else None,
        rejection_reason=reason, verification_days=verif_days, days_to_decision=total_days))

df = pd.DataFrame(rows)
df.to_csv("../data/loan_applications.csv", index=False)
print(df.shape)
print(df.final_status.value_counts(normalize=True).round(3))

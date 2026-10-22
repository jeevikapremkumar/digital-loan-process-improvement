"""Build the KPI dashboard (PNG) and the improvement scenario model from the SQL result CSVs."""
import pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

O = "../outputs/"
NAVY, RED, GREY, LIGHT = "#1F3A5F", "#D1495B", "#8A94A6", "#E8ECF2"
plt.rcParams.update({"font.family": "DejaVu Sans", "axes.spines.top": False, "axes.spines.right": False})

k = pd.read_csv(O + "q1_overall_kpis.csv").iloc[0]
funnel = pd.read_csv(O + "q2_funnel.csv")
chan = pd.read_csv(O + "q4_channel_performance.csv")
docs = pd.read_csv(O + "q5_document_completeness_impact.csv")
rej = pd.read_csv(O + "q8_rejection_reasons.csv")
emp = pd.read_csv(O + "q6_processing_time_by_employment.csv")
trend = pd.read_csv(O + "q9_monthly_trend.csv")
val = pd.read_csv(O + "q10_value_lost_to_abandonment.csv").iloc[0]

fig = plt.figure(figsize=(16, 10), facecolor="white")
fig.text(0.04, 0.955, "Digital Loan Application Process: Performance Dashboard", fontsize=20, fontweight="bold", color=NAVY)
fig.text(0.04, 0.925, "Simulated dataset | 12,000 applications | Jan-Dec 2025 | Currency in \u20b9", fontsize=10.5, color=GREY)

# KPI tiles
tiles = [("Total Applications", f"{int(k.total_applications):,}", NAVY),
         ("Approval Rate", f"{k.approval_rate_pct}%", NAVY),
         ("Abandonment Rate", f"{k.abandonment_rate_pct}%", RED),
         ("Avg Days to Decision", f"{k.avg_days_to_decision}", RED),
         ("Value Lost at Doc Upload", f"\u20b9{val.lost_at_document_upload_millions:,.0f}M", RED)]
for i, (t, v, c) in enumerate(tiles):
    ax = fig.add_axes([0.04 + i * 0.19, 0.80, 0.175, 0.095]); ax.axis("off")
    ax.add_patch(plt.Rectangle((0, 0), 1, 1, color=LIGHT, transform=ax.transAxes))
    ax.add_patch(plt.Rectangle((0, 0), 0.02, 1, color=c, transform=ax.transAxes))
    ax.text(0.08, 0.60, v, fontsize=22, fontweight="bold", color=c, transform=ax.transAxes)
    ax.text(0.08, 0.17, t, fontsize=10.5, color="#333", transform=ax.transAxes)

def pos(r, c):
    return [0.06 + c * 0.32, 0.43 - r * 0.40, 0.26, 0.28]

# 1 Funnel
ax = fig.add_axes(pos(0, 0)); ax.set_title("Funnel: % lost vs previous stage", loc="left", fontweight="bold", color=NAVY)
vals = funnel.applications.tolist(); labels = funnel.stage.tolist()
ax.barh(labels[::-1], vals[::-1], color=NAVY)
for i, (lab, v) in enumerate(zip(labels, vals)):
    prev = vals[i - 1] if i else v
    drop = f"  (-{100*(prev-v)/prev:.0f}%)" if i and v < prev else ""
    ax.text(v + 100, len(vals) - 1 - i, f"{v:,}{drop}", va="center", fontsize=9, color=RED if drop and 100*(prev-v)/prev > 15 else "#333")
ax.set_xlim(0, 15500); ax.tick_params(axis="y", labelsize=9)

# 2 Abandonment by channel
ax = fig.add_axes(pos(0, 1)); ax.set_title("Abandonment Rate by Channel (%)", loc="left", fontweight="bold", color=NAVY)
cols = [RED if v == chan.abandonment_rate_pct.max() else NAVY for v in chan.abandonment_rate_pct]
ax.bar(chan.channel, chan.abandonment_rate_pct, color=cols)
for i, v in enumerate(chan.abandonment_rate_pct): ax.text(i, v + 0.8, f"{v}%", ha="center", fontsize=10)
ax.set_ylim(0, 50)

# 3 Document completeness
ax = fig.add_axes(pos(0, 2)); ax.set_title("Document Completeness: Abandonment %", loc="left", fontweight="bold", color=NAVY)
lab = ["Complete\nfirst attempt", "Incomplete /\nresubmission"]
v = [docs[docs.document_status.str.startswith("Complete")].abandonment_rate_pct.iloc[0],
     docs[docs.document_status.str.startswith("Incomplete")].abandonment_rate_pct.iloc[0]]
ax.bar(lab, v, color=[NAVY, RED], width=0.5)
for i, x in enumerate(v): ax.text(i, x + 1, f"{x}%", ha="center", fontsize=10)
ax.set_ylim(0, 62)

# 4 Rejection reasons
ax = fig.add_axes(pos(1, 0)); ax.set_title("Rejection Reasons (% of rejections)", loc="left", fontweight="bold", color=NAVY)
r = rej.sort_values("pct_of_rejections")
ax.barh(r.rejection_reason, r.pct_of_rejections, color=NAVY)
for i, x in enumerate(r.pct_of_rejections): ax.text(x + 0.5, i, f"{x}%", va="center", fontsize=10)
ax.set_xlim(0, 52); ax.tick_params(axis="y", labelsize=9)

# 5 Days by employment
ax = fig.add_axes(pos(1, 1)); ax.set_title("Avg Days to Decision by Employment", loc="left", fontweight="bold", color=NAVY)
cols = [RED if x > 11 else NAVY for x in emp.avg_days_to_decision]
ax.bar(emp.employment_type, emp.avg_days_to_decision, color=cols)
for i, x in enumerate(emp.avg_days_to_decision): ax.text(i, x + 0.2, f"{x}", ha="center", fontsize=10)
ax.set_ylim(0, 15)

# 6 Monthly trend
ax = fig.add_axes(pos(1, 2)); ax.set_title("Monthly Approval vs Abandonment (%)", loc="left", fontweight="bold", color=NAVY)
m = [s[5:] for s in trend.month]
ax.plot(m, trend.approval_rate_pct, color=NAVY, marker="o", label="Approval")
ax.plot(m, trend.abandonment_rate_pct, color=RED, marker="o", label="Abandonment")
ax.legend(frameon=False, fontsize=9, loc="center right"); ax.set_ylim(25, 65); ax.tick_params(axis="x", labelsize=8)

fig.savefig(O + "dashboard.png", dpi=130, bbox_inches="tight"); print("dashboard saved")

# ---------------- Improvement scenario (ASSUMPTION-BASED) ----------------
df = pd.read_csv("../data/loan_applications.csv")
reached4 = (df.furthest_stage >= 4).sum()
conv_after_docs = (df.final_status == "Approved").sum() / reached4
doc_abandon = ((df.final_status == "Abandoned") & (df.drop_stage == "Document Upload")).sum()
avg_loan = df[df.final_status == "Approved"].loan_amount.mean()
rows = []
for recov in (0.20, 0.30, 0.40):
    extra = doc_abandon * recov * conv_after_docs
    rows.append(dict(scenario=f"Recover {int(recov*100)}% of doc-upload abandonments",
                     extra_approved_loans=round(extra), approval_rate_after_pct=round(100 * (k.approved + extra) / k.total_applications, 1),
                     extra_approved_value_millions=round(extra * avg_loan / 1e6)))
pd.DataFrame(rows).to_csv(O + "scenario_projection.csv", index=False)
print(pd.DataFrame(rows).to_string(index=False)); print("conv_after_docs", round(conv_after_docs, 3), "avg_loan", round(avg_loan))

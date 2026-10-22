"""Low-fidelity wireframes (TO-BE mobile screens) drawn with matplotlib."""
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

NAVY, GREY, LIGHT, RED, GREEN = "#1F3A5F", "#8A94A6", "#E8ECF2", "#D1495B", "#2A9D8F"
fig, axes = plt.subplots(1, 3, figsize=(15, 9), facecolor="white")

def phone(ax, title, subtitle):
    ax.set_xlim(0, 100); ax.set_ylim(0, 190); ax.axis("off"); ax.set_aspect("equal")
    ax.add_patch(FancyBboxPatch((2, 2), 96, 186, boxstyle="round,pad=0,rounding_size=8", fc="white", ec="#333", lw=2))
    ax.add_patch(Rectangle((2, 168), 96, 20, fc=NAVY, ec="none"))
    ax.text(50, 178, title, color="white", ha="center", va="center", fontsize=12, fontweight="bold")
    ax.text(50, 197, subtitle, ha="center", fontsize=10.5, color=NAVY, fontweight="bold")

def box(ax, x, y, w, h, text, fc=LIGHT, ec="#BBB", tc="#333", fs=9, bold=False, r=3):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}", fc=fc, ec=ec, lw=1))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=tc, fontweight="bold" if bold else "normal")

def label(ax, x, y, t, fs=8.5, c="#555"): ax.text(x, y, t, fontsize=fs, color=c, va="center")

# Screen 1: Eligibility
ax = axes[0]; phone(ax, "Apply for a Loan", "1. Instant Eligibility Check")
label(ax, 10, 158, "Loan type"); box(ax, 10, 143, 80, 12, "Personal Loan      \u25be")
label(ax, 10, 133, "Loan amount (\u20b9)"); box(ax, 10, 118, 80, 12, "5,00,000")
label(ax, 10, 108, "Monthly income (\u20b9)"); box(ax, 10, 93, 80, 12, "60,000")
label(ax, 10, 83, "Employment"); box(ax, 10, 68, 80, 12, "Salaried      \u25be")
box(ax, 10, 38, 80, 22, "You may be eligible for\nup to \u20b96,00,000 at 10.5% p.a.\n(indicative)", fc="#D5EFEB", ec=GREEN, tc="#1B6B61", fs=9)
box(ax, 10, 12, 80, 16, "Continue", fc=NAVY, ec=NAVY, tc="white", fs=11, bold=True)

# Screen 2: Guided upload
ax = axes[1]; phone(ax, "Upload Documents", "2. Guided Upload + Real-Time Validation")
ax.add_patch(Rectangle((10, 154), 80, 4, fc=LIGHT, ec="none")); ax.add_patch(Rectangle((10, 154), 40, 4, fc=NAVY, ec="none"))
label(ax, 10, 148, "Step 2 of 4  |  Est. time left: 3 min", fs=8)
items = [("ID proof (Aadhaar / PAN)", "\u2713 Verified", GREEN, "#D5EFEB"),
         ("Address proof", "\u2713 Verified", GREEN, "#D5EFEB"),
         ("Last 3 months' salary slips", "\u26a0 Image blurry", RED, "#F9D5DA"),
         ("Bank statement (6 months)", "Upload", GREY, LIGHT)]
y = 125
for name, st, c, bg in items:
    box(ax, 10, y, 80, 16, "", fc=bg, ec=c); label(ax, 14, y + 11, name, fs=8.5, c="#222"); label(ax, 14, y + 4.5, st, fs=8, c=c); y -= 21
box(ax, 10, 38, 80, 18, "Salary slip is unclear. Retake the photo\nin good light or upload a PDF.   [Retake]", fc="#FFF4E0", ec="#E9A23B", fs=8.2)
box(ax, 10, 12, 80, 16, "Save & Continue Later", fc=NAVY, ec=NAVY, tc="white", fs=10.5, bold=True)

# Screen 3: Tracker
ax = axes[2]; phone(ax, "Application Status", "3. Transparent Status Tracker")
label(ax, 10, 155, "Application ID: LN100245", fs=9, c="#222"); label(ax, 10, 147, "Expected decision: in 6 days", fs=8.5, c=GREEN)
steps = [("Application submitted", "Done", True), ("Documents verified", "Done", True), ("Income & KYC verification", "In progress (auto)", False),
         ("Credit assessment", "Pending", False), ("Decision & offer", "Pending", False)]
y = 128
for i, (s, st, done) in enumerate(steps):
    ax.add_patch(plt.Circle((16, y + 4), 4, fc=GREEN if done else ("white" if i > 2 else NAVY), ec=GREEN if done else NAVY, lw=1.5))
    if i < len(steps) - 1: ax.plot([16, 16], [y - 8, y - 1], color="#CCC", lw=1.5)
    label(ax, 25, y + 7, s, fs=9, c="#222"); label(ax, 25, y + 0.5, st, fs=8, c=GREY); y -= 17
box(ax, 10, 30, 80, 14, "Notify me by SMS / WhatsApp  \u2713", fc=LIGHT, fs=9)
box(ax, 10, 10, 80, 14, "Chat with loan advisor", fc=NAVY, ec=NAVY, tc="white", fs=10, bold=True)

fig.suptitle("Low-Fidelity Wireframes: Proposed Digital Loan Application (Mobile)", fontsize=16, fontweight="bold", color=NAVY, y=0.99)
fig.savefig("../outputs/wireframes.png", dpi=130, bbox_inches="tight"); print("wireframes saved")

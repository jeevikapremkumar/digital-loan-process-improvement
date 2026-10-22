"""Render AS-IS and TO-BE loan process maps with Graphviz."""
import subprocess

def render(name, dot):
    open(f"../outputs/{name}.dot", "w").write(dot)
    subprocess.run(["dot", "-Tpng", "-Gdpi=130", f"../outputs/{name}.dot", "-o", f"../outputs/{name}.png"], check=True)

HEAD = '''digraph G { rankdir=LR; bgcolor="white"; pad=0.3; nodesep=0.35; ranksep=0.45;
node [shape=box, style="rounded,filled", fontname="Helvetica", fontsize=11, margin="0.15,0.1"];
edge [fontname="Helvetica", fontsize=9, color="#555555"];
'''
NAVY, RED, GREEN, LIGHT = "#1F3A5F", "#D1495B", "#2A9D8F", "#E8ECF2"

as_is = HEAD + f'''
label=<<b>AS-IS: Current Loan Application Process</b><br/><font point-size="10">Avg 10.8 days to decision | 37.1% abandonment | red = pain points</font>>; labelloc=t; fontname="Helvetica"; fontsize=16;
start [label="Customer starts\\napplication", fillcolor="{LIGHT}"];
form [label="Fill long\\npersonal-details form", fillcolor="{LIGHT}"];
docs [label="Upload documents\\n(no real-time validation)", fillcolor="#F9D5DA", color="{RED}"];
check [label="Manual document\\ncheck by staff", fillcolor="#F9D5DA", color="{RED}"];
bad [shape=diamond, label="Docs\\ncomplete?", fillcolor="{LIGHT}"];
resub [label="Customer notified by\\nphone / email;\\nresubmits (2-8 days)", fillcolor="#F9D5DA", color="{RED}"];
verify [label="Manual verification\\n(employment & income)\\navg 3.9 to 6.9 days", fillcolor="#F9D5DA", color="{RED}"];
credit [label="Credit assessment\\n1-3 days", fillcolor="{LIGHT}"];
dec [label="Decision\\ncommunicated", fillcolor="{LIGHT}"];
drop [label="Applicant abandons\\n(37.1% overall;\\n41% of drop-offs at document stage)", shape=box, fillcolor="{RED}", fontcolor="white"];
start -> form -> docs -> check -> bad;
bad -> verify [label="Yes (about 67%)"]; bad -> resub [label="No (about 33%)"];
resub -> check [label="loop", style=dashed]; resub -> drop [label="50% abandon", color="{RED}"];
verify -> credit -> dec; verify -> drop [label="longer wait,\\nmore drop-off", color="{RED}"];
}}
'''

to_be = HEAD + f'''
label=<<b>TO-BE: Proposed Digital Loan Application Process</b><br/><font point-size="10">Targets: 8 days or less to decision | abandonment under 30% | green = improvements</font>>; labelloc=t; fontname="Helvetica"; fontsize=16;
start [label="Customer starts\\napplication", fillcolor="{LIGHT}"];
elig [label="Instant eligibility check\\n+ pre-filled details\\n(shorter form)", fillcolor="#D5EFEB", color="{GREEN}"];
docs [label="Guided document upload\\nwith checklist and\\nreal-time validation", fillcolor="#D5EFEB", color="{GREEN}"];
auto [shape=diamond, label="Auto-validation\\npassed?", fillcolor="{LIGHT}"];
fix [label="Instant on-screen fix\\nprompt (same session)", fillcolor="#D5EFEB", color="{GREEN}"];
verify [label="Automated e-KYC and\\nincome verification;\\nstaff review exceptions only", fillcolor="#D5EFEB", color="{GREEN}"];
track [label="Status tracker +\\nSMS / app alerts\\nat every stage", fillcolor="#D5EFEB", color="{GREEN}"];
credit [label="Credit assessment\\n1-2 days", fillcolor="{LIGHT}"];
dec [label="Decision\\ncommunicated digitally", fillcolor="{LIGHT}"];
start -> elig -> docs -> auto;
auto -> verify [label="Yes"]; auto -> fix [label="No"]; fix -> auto [label="re-check", style=dashed];
verify -> credit -> dec; verify -> track [style=dotted, arrowhead=none]; credit -> track [style=dotted, arrowhead=none];
}}
'''
render("as_is_process", as_is); render("to_be_process", to_be); print("process maps done")

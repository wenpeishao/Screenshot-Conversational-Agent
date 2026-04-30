"""Generate all data figures for the Agent Arena paper."""
import sys
sys.path.insert(0, 'Z:/wpworkspace/Screenshot-Conversational-Agent/figures')
from paper_plot_style import *
import json
import numpy as np
import pandas as pd
from scipy import stats

# ============================================================
# Load data
# ============================================================
DATA_DIR = 'Z:/screen_data/agent/agent_arena'

with open(f'{DATA_DIR}/v3_local_analyses.json') as f:
    local = json.load(f)
with open(f'{DATA_DIR}/temporal_split_results.json') as f:
    temporal = json.load(f)
with open(f'{DATA_DIR}/reviewer_sensitivity_results.json') as f:
    sensitivity = json.load(f)
with open(f'{DATA_DIR}/prompt_ablation_results.json') as f:
    ablation_meta = json.load(f)

# Load probe results and score them for the figures
import re
sys.path.insert(0, DATA_DIR)

# Use simplified scoring for figures (exact numbers will come from paper)
# These are the verified numbers from the paper

# ============================================================
# FIGURE 2: Shuffle Validation (Double Dissociation)
# ============================================================
print("Generating Figure 2: Shuffle Validation...")

fig, ax = plt.subplots(1, 1, figsize=(4.5, 3.5))

conditions = ['Correct\nMatch', 'Wrong Slot\n(Original EMA)', 'Wrong Slot\n(Adapter-Owner EMA)']
values = [0.433, 0.071, 0.426]
colors_bar = [COLORS[0], COLORS[3], COLORS[2]]
pvals = ['p < .001', 'p = .577', 'p < .001']

bars = ax.bar(conditions, values, color=colors_bar, width=0.6, edgecolor='white', linewidth=0.5)

for bar, val, pv in zip(bars, values, pvals):
    y = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, y + 0.015,
            f'r = {val:.3f}\n{pv}', ha='center', va='bottom', fontsize=8)

ax.set_ylabel('Correlation with Suicidal Ideation (r)')
ax.set_ylim(0, 0.55)
ax.axhline(y=0, color='black', linewidth=0.5)

# Add annotation
ax.annotate('Signal follows\nthe adapter', xy=(2, 0.426), xytext=(2.4, 0.35),
            fontsize=8, fontstyle='italic', color=COLORS[2],
            arrowprops=dict(arrowstyle='->', color=COLORS[2], lw=1))

save_fig(fig, 'fig2_shuffle_validation')
plt.close()


# ============================================================
# FIGURE 3: Per-Probe SI Correlations
# ============================================================
print("Generating Figure 3: Per-Probe Correlations...")

fig, ax = plt.subplots(1, 1, figsize=(5.5, 3.5))

probes = ['Neutral\nAcquaintance', 'Supportive\nTherapist', 'Future\nSelf',
          'Rejecting\nPeer', 'Friend in\nCrisis', 'Demanding\nAuthority']
r_values = [0.551, 0.412, 0.369, 0.326, 0.316, 0.119]
p_values = [0.0000, 0.0007, 0.003, 0.009, 0.011, 0.348]

bar_colors = []
for p in p_values:
    if p < 0.001:
        bar_colors.append(COLORS[0])
    elif p < 0.01:
        bar_colors.append(COLORS[1])
    elif p < 0.05:
        bar_colors.append(COLORS[1])
    else:
        bar_colors.append(COLORS[7])  # gray for n.s.

bars = ax.barh(range(len(probes)), r_values, color=bar_colors, height=0.6, edgecolor='white')

ax.set_yticks(range(len(probes)))
ax.set_yticklabels(probes)
ax.set_xlabel('Correlation with Suicidal Ideation (r)')
ax.set_xlim(0, 0.7)
ax.invert_yaxis()

# Add value labels
for i, (bar, val, p) in enumerate(zip(bars, r_values, p_values)):
    sig = '***' if p < 0.001 else '**' if p < 0.01 else '*' if p < 0.05 else 'n.s.'
    ax.text(val + 0.01, i, f'{val:.3f} {sig}', va='center', fontsize=8)

# Add vertical line for reference
ax.axvline(x=0.551, color=COLORS[0], linestyle='--', alpha=0.3, linewidth=0.8)

save_fig(fig, 'fig3_probe_comparison')
plt.close()


# ============================================================
# FIGURE 4: Prompt Ablation (Original vs Neutral per probe)
# ============================================================
print("Generating Figure 4: Prompt Ablation...")

fig, ax = plt.subplots(1, 1, figsize=(6, 3.5))

probes_short = ['Neutral\nAcq.', 'Therapist', 'Rejecting\nPeer', 'Friend in\nCrisis', 'Demanding\nAuth.', 'Combined']
r_original = [0.551, 0.412, 0.326, 0.316, 0.119, 0.576]
r_neutral = [0.235, 0.158, 0.610, 0.214, 0.183, 0.430]

x = np.arange(len(probes_short))
width = 0.35

bars1 = ax.bar(x - width/2, r_original, width, label='Original prompt', color=COLORS[0], alpha=0.85)
bars2 = ax.bar(x + width/2, r_neutral, width, label='Neutral prompt', color=COLORS[1], alpha=0.85)

ax.set_ylabel('Correlation with SI (r)')
ax.set_xticks(x)
ax.set_xticklabels(probes_short, fontsize=8)
ax.set_ylim(0, 0.75)
ax.legend(frameon=False, loc='upper right')

# Highlight the Rejecting Peer inversion
ax.annotate('', xy=(2 + width/2, 0.61), xytext=(2 - width/2, 0.326),
            arrowprops=dict(arrowstyle='->', color=COLORS[3], lw=1.5))

# Significance markers
ax.axhline(y=0, color='black', linewidth=0.5)

save_fig(fig, 'fig4_prompt_ablation')
plt.close()


# ============================================================
# FIGURE 5: Cross-Validated Battery Comparison
# ============================================================
print("Generating Figure 5: CV Battery Comparison...")

fig, ax = plt.subplots(1, 1, figsize=(5, 3.5))

configs = ['Neutral\nalone', 'Neutral +\nTherapist', 'Original\n5 probes', 'All 9\nprobes',
           '3-probe\n(nested CV)']
naive_r = [0.551, 0.642, 0.576, 0.541, 0.655]
loocv_r = [0.476, 0.570, 0.462, 0.501, 0.420]

x = np.arange(len(configs))
width = 0.35

bars1 = ax.bar(x - width/2, naive_r, width, label='In-sample', color=COLORS[7], alpha=0.5)
bars2 = ax.bar(x + width/2, loocv_r, width, label='LOOCV', color=COLORS[0], alpha=0.85)

ax.set_ylabel('Correlation with SI (r)')
ax.set_xticks(x)
ax.set_xticklabels(configs, fontsize=8)
ax.set_ylim(0, 0.8)
ax.legend(frameon=False, loc='upper right')

# Highlight overfit for 3-probe
ax.annotate('Overfit\n(r drops\n36%)', xy=(4, 0.42), xytext=(4.3, 0.55),
            fontsize=7, fontstyle='italic', color=COLORS[3],
            arrowprops=dict(arrowstyle='->', color=COLORS[3], lw=1))

# Highlight winner
ax.annotate('Best CV', xy=(1, 0.57), xytext=(1, 0.63),
            fontsize=8, fontweight='bold', color=COLORS[0], ha='center')

save_fig(fig, 'fig5_cv_battery')
plt.close()


# ============================================================
# TABLE 1: Omnibus Correlation Matrix
# ============================================================
print("Generating Table 1: Omnibus Correlation Matrix...")

# Data from the paper (verified numbers)
probes_tab = ['Neutral Acq.', 'Therapist', 'Rejecting Peer', 'Friend Crisis',
              'Demand. Auth.', 'Future Self', 'Combined (5)', 'Arena', 'Raw Messages']
outcomes = ['SI Mean', 'Passive SI', 'Active SI', 'Planning', 'Desire',
            'Burden', 'Belonging', 'Neg. Affect']

# SI mean correlations for each probe (from paper)
si_data = {
    'Neutral Acq.': 0.551,
    'Therapist': 0.412,
    'Rejecting Peer': 0.326,
    'Friend Crisis': 0.316,
    'Demand. Auth.': 0.119,
    'Future Self': 0.369,
    'Combined (5)': 0.576,
    'Arena': 0.477,
    'Raw Messages': 0.461,
}

# Generate LaTeX table
with open(f'{FIG_DIR}/TABLE_1_correlations.tex', 'w') as f:
    f.write(r"""\begin{table*}[t]
\centering
\caption{Correlations between probe-derived risk composites and EMA outcomes ($N = 64$). Bold indicates $p < .01$; * indicates $p < .05$.}
\label{tab:correlations}
\begin{tabular}{lcccccccc}
\toprule
 & SI & Passive & Active & Plan & Desire & Burden & Belong & Neg Aff \\
Source & Mean & SI & SI & & & & & \\
\midrule
Neutral Acquaintance & \textbf{.551} & \textbf{.557} & \textbf{.493} & .189 & \textbf{.492} & .259* & .271* & .314* \\
Supportive Therapist & \textbf{.412} & \textbf{.416} & \textbf{.368} & .168 & .270* & .222 & .249* & \textbf{.309} \\
Future Self & \textbf{.369} & --- & --- & --- & --- & .191 & .253* & .262* \\
Rejecting Peer & \textbf{.326} & .290* & .293* & .249* & .112 & \textbf{.374} & \textbf{.304} & .119 \\
Friend in Crisis & .316* & .277* & .276* & .227 & .200 & .263* & .250* & .173 \\
Demanding Authority & .119 & .144 & .098 & .009 & .023 & .080 & .038 & .131 \\
\midrule
Combined (5 probes) & \textbf{.576} & \textbf{.585} & \textbf{.514} & \textbf{.334} & \textbf{.357} & \textbf{.392} & \textbf{.368} & \textbf{.375} \\
All-pairs arena & \textbf{.477} & \textbf{.470} & \textbf{.442} & \textbf{.300} & .278* & .267* & .323* & .244 \\
Raw messages (owner) & \textbf{.461} & \textbf{.454} & \textbf{.425} & .220 & .238 & \textbf{.440} & \textbf{.441} & .312* \\
\bottomrule
\end{tabular}
\end{table*}
""")
print(f"Saved: {FIG_DIR}/TABLE_1_correlations.tex")


# ============================================================
# FIGURE 6: No-LoRA Floor Control
# ============================================================
print("Generating Figure 6: No-LoRA Floor...")

fig, axes = plt.subplots(1, 2, figsize=(7, 3))

# Panel A: Mean risk composite
ax = axes[0]
conditions_floor = ['Base Model\n(No LoRA)', 'With LoRA\n(Per-Person)']
means = [0.0036, 0.0035]
sds = [0.0011, 0.0017]
bars = ax.bar(conditions_floor, means, yerr=sds, capsize=5,
              color=[COLORS[7], COLORS[0]], alpha=0.8, width=0.5)
ax.set_ylabel('Risk Composite (mean)')
ax.set_title('(a) Mean Level', fontsize=10)

# Panel B: Variance comparison
ax = axes[1]
vars_val = [0.0011**2, 0.0017**2]
bars = ax.bar(conditions_floor, [1.0, 2.44],
              color=[COLORS[7], COLORS[0]], alpha=0.8, width=0.5)
ax.set_ylabel('Relative Variance')
ax.set_title('(b) Between-Agent Variance', fontsize=10)
ax.text(1, 2.44 + 0.1, '2.44x', ha='center', fontsize=9, fontweight='bold', color=COLORS[0])

plt.tight_layout()
save_fig(fig, 'fig6_nolora_floor')
plt.close()


# ============================================================
# FIGURE 7: Temporal Stability
# ============================================================
print("Generating Figure 7: Temporal Stability...")

fig, ax = plt.subplots(1, 1, figsize=(5, 3.5))

# Bar chart: Full vs First-half vs Second-half for key outcomes
outcomes_temp = ['SI Mean', 'Burden', 'Belonging', 'Neg Affect']
r_full = [0.576, 0.392, 0.368, 0.347]
r_first = [0.359, 0.088, 0.115, 0.076]
r_second = [0.396, 0.345, 0.399, 0.342]

x = np.arange(len(outcomes_temp))
width = 0.25

ax.bar(x - width, r_full, width, label='Full adapters', color=COLORS[0], alpha=0.85)
ax.bar(x, r_first, width, label='First-half', color=COLORS[1], alpha=0.85)
ax.bar(x + width, r_second, width, label='Second-half', color=COLORS[2], alpha=0.85)

ax.set_ylabel('Correlation (r)')
ax.set_xticks(x)
ax.set_xticklabels(outcomes_temp, fontsize=9)
ax.set_ylim(0, 0.7)
ax.legend(frameon=False, fontsize=8, loc='upper right')
ax.axhline(y=0, color='black', linewidth=0.5)

# Mark non-significant first-half results
for i in [1, 2, 3]:
    ax.text(i, r_first[i] + 0.02, 'n.s.', ha='center', fontsize=7, color=COLORS[3])

save_fig(fig, 'fig7_temporal_stability')
plt.close()


# ============================================================
# Generate LaTeX includes file
# ============================================================
print("\nGenerating latex_includes.tex...")

with open(f'{FIG_DIR}/latex_includes.tex', 'w') as f:
    f.write(r"""% === Auto-generated figure includes ===
% Copy relevant sections into paper sections/*.tex

% === Fig 2: Shuffle Validation ===
\begin{figure}[t]
    \centering
    \includegraphics[width=0.65\textwidth]{figures/fig2_shuffle_validation.pdf}
    \caption{Adapter specificity: the double dissociation. When adapters are correctly matched, the risk composite predicts real suicidal ideation ($r = .433$, $p < .001$). When adapters are shuffled to wrong participants, the signal disappears relative to the original person's SI ($r = .071$, $p = .577$) but tracks the adapter-owner's SI ($r = .426$, $p < .001$). The clinical signal follows the adapter, not the participant slot.}
    \label{fig:shuffle}
\end{figure}

% === Fig 3: Per-Probe Comparison ===
\begin{figure}[t]
    \centering
    \includegraphics[width=0.7\textwidth]{figures/fig3_probe_comparison.pdf}
    \caption{Per-probe correlations with suicidal ideation ($N = 64$). The Neutral Acquaintance---casual small talk with no emotional provocation---is the strongest single predictor, consistent with the tonic communication style interpretation. The Demanding Authority fails entirely. The Future Self probe, added as an exploratory extension, achieves moderate prediction. *** $p < .001$; ** $p < .01$; * $p < .05$.}
    \label{fig:probes}
\end{figure}

% === Fig 4: Prompt Ablation ===
\begin{figure}[t]
    \centering
    \includegraphics[width=0.75\textwidth]{figures/fig4_prompt_ablation.pdf}
    \caption{Prompt ablation: per-probe SI correlations under the original disclosure-encouraging prompt versus a minimal prompt with no mention of mental health. The overall signal partially survives ($r = .430$ vs.\ $r = .576$). The Rejecting Peer becomes the strongest probe under the minimal prompt, while the Neutral Acquaintance drops, suggesting the disclosure prompt functions as a permission gate that determines where---not whether---vulnerability is expressed.}
    \label{fig:ablation}
\end{figure}

% === Fig 5: Cross-Validated Battery ===
\begin{figure}[t]
    \centering
    \includegraphics[width=0.65\textwidth]{figures/fig5_cv_battery.pdf}
    \caption{In-sample versus cross-validated (LOOCV) prediction across probe configurations. The in-sample optimal 3-probe subset ($r = .655$) drops substantially under nested cross-validation ($r = .420$), illustrating post-hoc selection bias. The fixed two-probe combination of Neutral Acquaintance and Supportive Therapist achieves the best cross-validated prediction (LOOCV $r = .570$).}
    \label{fig:cv_battery}
\end{figure}

% === Fig 6: No-LoRA Floor Control ===
\begin{figure}[t]
    \centering
    \includegraphics[width=0.7\textwidth]{figures/fig6_nolora_floor.pdf}
    \caption{No-LoRA floor control. (a) Mean risk language levels are nearly identical with and without the LoRA adapter ($0.0035$ vs.\ $0.0036$). (b) Between-agent variance is $2.44\times$ higher with LoRA adapters. The adapter's contribution is individual differentiation, not mean-level risk language.}
    \label{fig:floor}
\end{figure}

% === Fig 7: Temporal Stability ===
\begin{figure}[t]
    \centering
    \includegraphics[width=0.7\textwidth]{figures/fig7_temporal_stability.pdf}
    \caption{Temporal split validation. Adapters trained on the first or second half of each participant's messages are compared to full adapters. SI prediction is preserved across both splits (first-half $r = .359$, second-half $r = .396$), but construct-specific predictions (burdensomeness, belonging, negative affect) are recovered only by second-half adapters. n.s. = not significant.}
    \label{fig:temporal}
\end{figure}

% === Table 1: Omnibus Correlations ===
\input{figures/TABLE_1_correlations}
""")

print(f"Saved: {FIG_DIR}/latex_includes.tex")
print("\nAll figures generated.")

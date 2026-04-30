"""Regenerate bar-graph figures with 95% CIs for correlations."""
import sys
sys.path.insert(0, 'Z:/wpworkspace/Screenshot-Conversational-Agent/figures')
from paper_plot_style import *
import numpy as np

def r_ci(r, n, alpha=0.05):
    """95% CI for Pearson r via Fisher z transformation."""
    z = np.arctanh(r)
    se = 1.0 / np.sqrt(n - 3)
    z_crit = 1.96  # for 95%
    lo = np.tanh(z - z_crit * se)
    hi = np.tanh(z + z_crit * se)
    return lo, hi

def ci_err(r, n):
    """Return (lower_err, upper_err) for matplotlib errorbar."""
    lo, hi = r_ci(r, n)
    return r - lo, hi - r

N = 64  # analytic sample

# ============================================================
# FIGURE 3: Per-Probe SI Correlations (horizontal bars + CI)
# ============================================================
print("Generating Figure 3: Per-Probe Correlations with CIs...")

fig, ax = plt.subplots(1, 1, figsize=(5.5, 3.5))

probes = ['Neutral\nAcquaintance', 'Supportive\nTherapist', 'Future\nSelf',
          'Rejecting\nPeer', 'Friend in\nCrisis', 'Demanding\nAuthority']
r_values = [0.551, 0.412, 0.369, 0.326, 0.316, 0.119]
p_values = [0.0000, 0.0007, 0.003, 0.009, 0.011, 0.348]

bar_colors = [COLORS[0] if p < 0.05 else COLORS[7] for p in p_values]

# Compute CIs
ci_lo = [ci_err(r, N)[0] for r in r_values]
ci_hi = [ci_err(r, N)[1] for r in r_values]
xerr = [ci_lo, ci_hi]

bars = ax.barh(range(len(probes)), r_values, xerr=xerr, capsize=3,
               color=bar_colors, height=0.6, edgecolor='white',
               error_kw={'linewidth': 1, 'color': '#555555'})

ax.set_yticks(range(len(probes)))
ax.set_yticklabels(probes)
ax.set_xlabel('Correlation with Suicidal Ideation (r)')
ax.set_xlim(0, 0.75)
ax.invert_yaxis()

for i, (bar, val, p) in enumerate(zip(bars, r_values, p_values)):
    lo, hi = r_ci(val, N)
    sig = '*' if p < 0.05 else ''
    ax.text(hi + 0.01, i, f'{val:.3f}{sig}', va='center', fontsize=8)

ax.axvline(x=0.551, color=COLORS[0], linestyle='--', alpha=0.3, linewidth=0.8)

save_fig(fig, 'fig3_probe_comparison')
plt.close()


# ============================================================
# FIGURE 4: Prompt Ablation (Original vs Neutral per probe)
# ============================================================
print("Generating Figure 4: Prompt Ablation with CIs...")

fig, ax = plt.subplots(1, 1, figsize=(6, 3.5))

probes_short = ['Neutral\nAcq.', 'Therapist', 'Rejecting\nPeer', 'Friend in\nCrisis', 'Demanding\nAuth.', 'Combined']
r_original = [0.551, 0.412, 0.326, 0.316, 0.119, 0.576]
r_neutral = [0.235, 0.158, 0.610, 0.214, 0.183, 0.430]

x = np.arange(len(probes_short))
width = 0.35

# CIs
ci_orig = [[ci_err(r, N)[0] for r in r_original],
           [ci_err(r, N)[1] for r in r_original]]
ci_neut = [[ci_err(r, N)[0] for r in r_neutral],
           [ci_err(r, N)[1] for r in r_neutral]]

bars1 = ax.bar(x - width/2, r_original, width, yerr=ci_orig, capsize=2,
               label='Original prompt', color=COLORS[0], alpha=0.85,
               error_kw={'linewidth': 1, 'color': '#555555'})
bars2 = ax.bar(x + width/2, r_neutral, width, yerr=ci_neut, capsize=2,
               label='Neutral prompt', color=COLORS[1], alpha=0.85,
               error_kw={'linewidth': 1, 'color': '#555555'})

ax.set_ylabel('Correlation with SI (r)')
ax.set_xticks(x)
ax.set_xticklabels(probes_short, fontsize=8)
ax.set_ylim(0, 0.85)
ax.legend(frameon=False, loc='upper right')

# Highlight the Rejecting Peer inversion
ax.annotate('', xy=(2 + width/2, 0.61), xytext=(2 - width/2, 0.326),
            arrowprops=dict(arrowstyle='->', color=COLORS[3], lw=1.5))

ax.axhline(y=0, color='black', linewidth=0.5)

save_fig(fig, 'fig4_prompt_ablation')
plt.close()


# ============================================================
# FIGURE 7: Temporal Stability
# ============================================================
print("Generating Figure 7: Temporal Stability with CIs...")

fig, ax = plt.subplots(1, 1, figsize=(5.5, 3.5))

constructs = ['SI Mean', 'Burden', 'Belonging', 'Neg Affect']
r_full = [0.576, 0.392, 0.368, 0.347]
r_first = [0.359, 0.09, 0.12, 0.08]
r_second = [0.396, 0.34, 0.40, 0.34]
n_split = 66

x = np.arange(len(constructs))
width = 0.25

ci_full = [[ci_err(r, N)[0] for r in r_full],
           [ci_err(r, N)[1] for r in r_full]]
ci_first = [[ci_err(r, n_split)[0] for r in r_first],
            [ci_err(r, n_split)[1] for r in r_first]]
ci_second = [[ci_err(r, n_split)[0] for r in r_second],
             [ci_err(r, n_split)[1] for r in r_second]]

bars1 = ax.bar(x - width, r_full, width, yerr=ci_full, capsize=2,
               label='Full adapters', color=COLORS[0], alpha=0.85,
               error_kw={'linewidth': 1, 'color': '#555555'})
bars2 = ax.bar(x, r_first, width, yerr=ci_first, capsize=2,
               label='First-half', color=COLORS[1], alpha=0.85,
               error_kw={'linewidth': 1, 'color': '#555555'})
bars3 = ax.bar(x + width, r_second, width, yerr=ci_second, capsize=2,
               label='Second-half', color=COLORS[2], alpha=0.85,
               error_kw={'linewidth': 1, 'color': '#555555'})

ax.set_ylabel('Correlation (r)')
ax.set_xticks(x)
ax.set_xticklabels(constructs, fontsize=9)
ax.set_ylim(0, 0.75)
ax.legend(frameon=False, loc='upper right', fontsize=8)

# Mark n.s. for first-half construct-specific
for i in [1, 2, 3]:
    ax.text(x[i], r_first[i] + ci_first[1][i] + 0.02, 'n.s.', ha='center',
            fontsize=7, color=COLORS[3])

save_fig(fig, 'fig7_temporal_stability')
plt.close()


# ============================================================
# FIGURE 2: Shuffle Validation (2-panel with CIs on right)
# ============================================================
print("Generating Figure 2: Shuffle Validation with CIs...")

fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(9, 4),
                                         gridspec_kw={'width_ratios': [1.1, 1]})

import matplotlib.patches as mpatches

# LEFT PANEL: Schematic (same as before)
ax = ax_left
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_title('(a) Shuffle procedure', fontsize=10, fontweight='bold', loc='left', pad=8)

blue = '#2563EB'; green = '#10B981'; red = '#EF4444'; gray = '#9CA3AF'
light_blue = '#DBEAFE'; light_green = '#D1FAE5'

ax.text(5, 9.6, 'Correct matching', fontsize=9, fontweight='bold', ha='center', color='#1F2937')

box_a = mpatches.FancyBboxPatch((0.5, 8.2), 2.2, 1.0, boxstyle='round,pad=0.1',
                                 facecolor=light_blue, edgecolor=blue, linewidth=1.5)
ax.add_patch(box_a)
ax.text(1.6, 8.95, 'Person A', fontsize=8, ha='center', fontweight='bold', color=blue)
ax.text(1.6, 8.5, 'messages', fontsize=7, ha='center', color=blue)

ax.annotate('', xy=(4.0, 8.7), xytext=(2.8, 8.7),
            arrowprops=dict(arrowstyle='->', color=gray, lw=1.5))
ax.text(3.4, 8.9, 'train', fontsize=7, ha='center', color=gray)

box_ad = mpatches.FancyBboxPatch((4.0, 8.2), 2.0, 1.0, boxstyle='round,pad=0.1',
                                  facecolor=light_blue, edgecolor=blue, linewidth=1.5)
ax.add_patch(box_ad)
ax.text(5.0, 8.95, 'Adapter A', fontsize=8, ha='center', fontweight='bold', color=blue)

ax.annotate('', xy=(7.0, 8.7), xytext=(6.1, 8.7),
            arrowprops=dict(arrowstyle='->', color=gray, lw=1.5))

box_conv = mpatches.FancyBboxPatch((7.0, 8.2), 2.5, 1.0, boxstyle='round,pad=0.1',
                                    facecolor='#F3F4F6', edgecolor=gray, linewidth=1.5)
ax.add_patch(box_conv)
ax.text(8.25, 8.95, 'Risk language', fontsize=7.5, ha='center', color='#374151')
ax.text(8.25, 8.5, 'correlate w/ A\'s SI', fontsize=7, ha='center', color=green, fontweight='bold')

ax.text(5, 7.3, 'Shuffled: adapter reassigned to wrong person', fontsize=9,
        fontweight='bold', ha='center', color='#1F2937')

box_b = mpatches.FancyBboxPatch((0.5, 5.1), 2.2, 1.7, boxstyle='round,pad=0.1',
                                 facecolor=light_green, edgecolor=green, linewidth=1.5)
ax.add_patch(box_b)
ax.text(1.6, 6.4, 'Person B', fontsize=8, ha='center', fontweight='bold', color=green)
ax.text(1.6, 5.95, '(different', fontsize=7, ha='center', color=green)
ax.text(1.6, 5.55, 'person)', fontsize=7, ha='center', color=green)

ax.text(3.1, 6.0, '+', fontsize=14, ha='center', va='center', color=gray, fontweight='bold')

box_ad2 = mpatches.FancyBboxPatch((3.5, 5.3), 2.2, 1.3, boxstyle='round,pad=0.1',
                                   facecolor=light_blue, edgecolor=blue, linewidth=1.5)
ax.add_patch(box_ad2)
ax.text(4.6, 6.25, 'Adapter A', fontsize=8, ha='center', fontweight='bold', color=blue)
ax.text(4.6, 5.8, '(from Person A)', fontsize=7, ha='center', color=blue)

ax.annotate('', xy=(6.6, 6.0), xytext=(5.8, 6.0),
            arrowprops=dict(arrowstyle='->', color=gray, lw=1.5))

box_out = mpatches.FancyBboxPatch((6.6, 5.1), 3.0, 1.7, boxstyle='round,pad=0.1',
                                   facecolor='#F3F4F6', edgecolor=gray, linewidth=1.5)
ax.add_patch(box_out)
ax.text(8.1, 6.5, 'Risk language', fontsize=7.5, ha='center', color='#374151')
ax.text(8.1, 5.95, 'vs B\'s SI:', fontsize=7, ha='center', color=red)
ax.text(8.1, 5.55, 'r = .071 (n.s.)', fontsize=7, ha='center', color=red, fontweight='bold')

ax.plot([6.8, 9.4], [5.35, 5.35], color='#E5E7EB', linewidth=0.5)

ax.text(8.1, 4.8, 'Whose SI does', fontsize=7.5, ha='center', color='#374151', fontstyle='italic')
ax.text(8.1, 4.4, 'the output predict?', fontsize=7.5, ha='center', color='#374151', fontstyle='italic')

ax.annotate('', xy=(8.1, 3.7), xytext=(8.1, 4.2),
            arrowprops=dict(arrowstyle='->', color=gray, lw=1.5))

box_ans = mpatches.FancyBboxPatch((5.8, 2.8), 4.6, 0.9, boxstyle='round,pad=0.1',
                                   facecolor='#F0FDF4', edgecolor=green, linewidth=1.5)
ax.add_patch(box_ans)
ax.text(8.1, 3.45, "Person A's SI (the adapter owner):", fontsize=7.5,
        ha='center', color='#065F46', fontweight='bold')
ax.text(8.1, 3.0, 'r = .426, p < .001', fontsize=7.5, ha='center', color=green, fontweight='bold')

# RIGHT PANEL: Bar chart with CIs
ax = ax_right
ax.set_title('(b) Results', fontsize=10, fontweight='bold', loc='left', pad=8)

conditions = ['Correct\nmatch', 'Shuffled\n\u2192 assigned\nperson\'s SI', 'Shuffled\n\u2192 adapter\nowner\'s SI']
values = [0.433, 0.071, 0.426]
colors_bar = ['#2563EB', '#EF4444', '#10B981']
pvals = ['p < .001', 'p = .577', 'p < .001']

ci_lo_s = [ci_err(r, N)[0] for r in values]
ci_hi_s = [ci_err(r, N)[1] for r in values]

bars = ax.bar(conditions, values, yerr=[ci_lo_s, ci_hi_s], capsize=3,
              color=colors_bar, width=0.6, edgecolor='white', linewidth=0.5,
              error_kw={'linewidth': 1, 'color': '#555555'})

for bar, val, pv in zip(bars, values, pvals):
    y = bar.get_height() + ci_hi_s[list(values).index(val)]
    ax.text(bar.get_x() + bar.get_width()/2, y + 0.015,
            f'r = {val:.3f}\n{pv}', ha='center', va='bottom', fontsize=8)

ax.set_ylabel('Correlation with Suicidal Ideation (r)')
ax.set_ylim(-0.1, 0.65)
ax.axhline(y=0, color='black', linewidth=0.5)

ax.annotate('Signal follows\nthe adapter', xy=(2, 0.426), xytext=(2.45, 0.25),
            fontsize=8, fontstyle='italic', color='#10B981',
            arrowprops=dict(arrowstyle='->', color='#10B981', lw=1))

plt.tight_layout()
save_fig(fig, 'fig2_shuffle_validation')
plt.close()

print("All figures regenerated with 95% CIs.")

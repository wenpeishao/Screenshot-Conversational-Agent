"""Generate fig2: Shuffle Validation with schematic + results."""
import sys
sys.path.insert(0, 'Z:/wpworkspace/Screenshot-Conversational-Agent/figures')
from paper_plot_style import *
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch

fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(11, 5.0),
                                         gridspec_kw={'width_ratios': [1.3, 1],
                                                      'wspace': 0.35})

# ============================================================
# LEFT PANEL: Schematic of the shuffle procedure
# ============================================================
ax = ax_left
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)
ax.axis('off')
ax.set_title('(a) Shuffle procedure', fontsize=10, fontweight='bold', loc='left', pad=8)

# Colors
blue = '#2563EB'
green = '#10B981'
red = '#EF4444'
gray = '#9CA3AF'
light_blue = '#DBEAFE'
light_green = '#D1FAE5'
light_red = '#FEE2E2'

# --- TOP: Correct matching ---
ax.text(5, 9.6, 'Correct matching', fontsize=9, fontweight='bold', ha='center', color='#1F2937')

# Person A
box_a = mpatches.FancyBboxPatch((0.5, 8.2), 2.2, 1.0, boxstyle='round,pad=0.1',
                                 facecolor=light_blue, edgecolor=blue, linewidth=1.5)
ax.add_patch(box_a)
ax.text(1.6, 8.95, 'Person A', fontsize=8, ha='center', fontweight='bold', color=blue)
ax.text(1.6, 8.5, 'messages', fontsize=7, ha='center', color=blue)

# Arrow
ax.annotate('', xy=(4.0, 8.7), xytext=(2.8, 8.7),
            arrowprops=dict(arrowstyle='->', color=gray, lw=1.5))
ax.text(3.4, 8.9, 'train', fontsize=7, ha='center', color=gray)

# Adapter A
box_ad = mpatches.FancyBboxPatch((4.0, 8.2), 2.0, 1.0, boxstyle='round,pad=0.1',
                                  facecolor=light_blue, edgecolor=blue, linewidth=1.5)
ax.add_patch(box_ad)
ax.text(5.0, 8.95, 'Adapter A', fontsize=8, ha='center', fontweight='bold', color=blue)

# Arrow to conversation
ax.annotate('', xy=(7.0, 8.7), xytext=(6.1, 8.7),
            arrowprops=dict(arrowstyle='->', color=gray, lw=1.5))

# Conversation output
box_conv = mpatches.FancyBboxPatch((7.0, 8.2), 2.5, 1.0, boxstyle='round,pad=0.1',
                                    facecolor='#F3F4F6', edgecolor=gray, linewidth=1.5)
ax.add_patch(box_conv)
ax.text(8.25, 8.95, 'Risk language', fontsize=7.5, ha='center', color='#374151')
ax.text(8.25, 8.5, 'correlate w/ A\'s SI', fontsize=7, ha='center', color=green, fontweight='bold')

# --- BOTTOM: Shuffled ---
ax.text(5, 7.3, 'Shuffled: adapter reassigned to wrong person', fontsize=9,
        fontweight='bold', ha='center', color='#1F2937')

# Person B (gets A's adapter)
box_b = mpatches.FancyBboxPatch((0.5, 5.1), 2.2, 1.7, boxstyle='round,pad=0.1',
                                 facecolor=light_green, edgecolor=green, linewidth=1.5)
ax.add_patch(box_b)
ax.text(1.6, 6.4, 'Person B', fontsize=8, ha='center', fontweight='bold', color=green)
ax.text(1.6, 5.95, '(different', fontsize=7, ha='center', color=green)
ax.text(1.6, 5.55, 'person)', fontsize=7, ha='center', color=green)

# Plus sign
ax.text(3.1, 6.0, '+', fontsize=14, ha='center', va='center', color=gray, fontweight='bold')

# Adapter A (wrong person)
box_ad2 = mpatches.FancyBboxPatch((3.5, 5.3), 2.2, 1.3, boxstyle='round,pad=0.1',
                                   facecolor=light_blue, edgecolor=blue, linewidth=1.5)
ax.add_patch(box_ad2)
ax.text(4.6, 6.25, 'Adapter A', fontsize=8, ha='center', fontweight='bold', color=blue)
ax.text(4.6, 5.8, '(from Person A)', fontsize=7, ha='center', color=blue)

# Arrow
ax.annotate('', xy=(6.6, 6.0), xytext=(5.8, 6.0),
            arrowprops=dict(arrowstyle='->', color=gray, lw=1.5))

# Output box
box_out = mpatches.FancyBboxPatch((6.6, 5.1), 3.0, 1.7, boxstyle='round,pad=0.1',
                                   facecolor='#F3F4F6', edgecolor=gray, linewidth=1.5)
ax.add_patch(box_out)
ax.text(8.1, 6.5, 'Risk language', fontsize=7.5, ha='center', color='#374151')

# Two outcome lines
ax.text(8.1, 5.95, 'vs B\'s SI:', fontsize=7, ha='center', color=red)
ax.text(8.1, 5.55, 'r = .071 (n.s.)', fontsize=7, ha='center', color=red, fontweight='bold')

# Dividing line
ax.plot([6.8, 9.4], [5.35, 5.35], color='#E5E7EB', linewidth=0.5)

# --- Key question ---
box_q = mpatches.FancyBboxPatch((2.8, 3.5), 5.4, 0.9, boxstyle='round,pad=0.1',
                                 facecolor='#F9FAFB', edgecolor='#9CA3AF', linewidth=1.0,
                                 linestyle='--')
ax.add_patch(box_q)
ax.text(5.5, 4.15, 'Key question:', fontsize=7.5, ha='center',
        color='#374151', fontweight='bold')
ax.text(5.5, 3.75, 'Whose SI does the output predict?', fontsize=7.5, ha='center',
        color='#374151')

# Arrow down
ax.annotate('', xy=(5.5, 2.95), xytext=(5.5, 3.45),
            arrowprops=dict(arrowstyle='->', color=gray, lw=1.5))

# Answer box -- keep within x=0..10 axes bounds
box_ans = mpatches.FancyBboxPatch((3.2, 2.0), 4.6, 0.9, boxstyle='round,pad=0.1',
                                   facecolor='#F0FDF4', edgecolor=green, linewidth=1.5)
ax.add_patch(box_ans)
ax.text(5.5, 2.65, "Person A's SI (the adapter owner):", fontsize=7.5,
        ha='center', color='#065F46', fontweight='bold')
ax.text(5.5, 2.2, 'r = .426, p < .001', fontsize=7.5, ha='center', color=green, fontweight='bold')

# ============================================================
# RIGHT PANEL: Bar chart (existing results)
# ============================================================
ax = ax_right
ax.set_title('(b) Results', fontsize=10, fontweight='bold', loc='left', pad=12)

import numpy as np
N_shuf = 64

conditions = ['Correct\nmatch', 'Shuffled\n\u2192 assigned\nperson\'s SI', 'Shuffled\n\u2192 adapter\nowner\'s SI']
values = [0.433, 0.071, 0.426]
colors_bar = ['#2563EB', '#EF4444', '#10B981']
pvals = ['p < .001', 'p = .577', 'p < .001']

# Compute 95% CIs via Fisher z
def r_ci(r, n):
    z = np.arctanh(r)
    se = 1.0 / np.sqrt(n - 3)
    lo = np.tanh(z - 1.96 * se)
    hi = np.tanh(z + 1.96 * se)
    return r - lo, hi - r

ci_lo = [r_ci(v, N_shuf)[0] for v in values]
ci_hi = [r_ci(v, N_shuf)[1] for v in values]

bars = ax.bar(conditions, values, color=colors_bar, width=0.6, edgecolor='white', linewidth=0.5,
              yerr=[ci_lo, ci_hi], capsize=3, error_kw={'linewidth': 0.8, 'color': '#555555'})

for bar, val, pv, chi in zip(bars, values, pvals, ci_hi):
    y = val + chi  # place text above error bar
    ax.text(bar.get_x() + bar.get_width()/2, y + 0.02,
            f'r = {val:.3f}\n{pv}', ha='center', va='bottom', fontsize=8)

ax.set_ylabel('Correlation with Suicidal Ideation (r)')
ax.set_ylim(-0.1, 0.75)
ax.axhline(y=0, color='black', linewidth=0.5)

plt.tight_layout()

outdir = 'Z:/wpworkspace/Screenshot-Conversational-Agent/figures'
fig.savefig(f'{outdir}/fig2_shuffle_validation.pdf', bbox_inches='tight', dpi=300)
fig.savefig(f'{outdir}/fig2_shuffle_validation.png', bbox_inches='tight', dpi=300)
print('Done: fig2_shuffle_validation.pdf + .png')

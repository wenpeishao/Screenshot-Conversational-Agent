"""Generate fig8: Summary of Analyses table."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

fig, ax = plt.subplots(figsize=(12, 8.5))
ax.axis('off')

# Colors
blue_bg = '#EFF6FF'
green_bg = '#ECFDF5'
yellow_bg = '#FFFBEB'
header_color = '#1F2937'
text_color = '#374151'
result_color = '#1F2937'

# Column positions
col_x = [0.02, 0.22, 0.52, 0.88]
col_labels = ['Analysis', 'Question', 'Key Result', 'Section']

# Section headers and rows
# Format: (analysis, question, result, section)
# Consistent reporting: r = .XXX, p < .001/p = .XXX, or descriptive stat with significance
sections = {
    'CORE PARADIGMS': {
        'color': blue_bg,
        'rows': [
            ('All-Pairs Arena', 'Do agents associate with SI?', 'r = .433, p < .001', '3.2'),
            ('Caption-Trained Arena', 'Is signal interpersonal-specific?', 'r = .159, p = .198', '3.3'),
            ('Probe Arena (5 probes)', 'Do probes outperform arena?', 'r = .576, p < .001', '3.4'),
            ('Future Self Probe', 'Does temporal reflection help?', 'r = .369, p = .003', '3.5'),
        ]
    },
    'VALIDATION': {
        'color': green_bg,
        'rows': [
            ('Adapter Shuffle', 'Is signal person-specific?', 'r = .071, p = .577', '3.5'),
            ('Prompt Ablation', 'Is it demand characteristics?', 'r = .430, p < .001', '3.5'),
            ('No-LoRA Floor', 'Does base model produce signal?', 'Variance ratio = 2.44\u00d7', '3.5'),
            ('Temporal Split', 'Is signal temporally stable?', 'SB reliability = .538', '3.5'),
            ('Cross-Validated Battery', 'Which probes generalize?', 'LOOCV r = .570, p < .001', '3.5'),
        ]
    },
    'SENSITIVITY': {
        'color': yellow_bg,
        'rows': [
            ('Verbosity Control', 'Confounded by turn length?', 'r = .438, p < .001', '3.5'),
            ('Training Heterogeneity', 'Confounded by msg count?', 'partial r = .547, p < .001', '3.5'),
            ('Selection Bias', 'Who is excluded?', 'Excluded: fewer messages, p < .001', '4.7'),
        ]
    }
}

y = 0.95
row_h = 0.048
section_gap = 0.015

# Title
ax.text(0.5, y, 'Summary of Analyses', fontsize=16, fontweight='bold',
        ha='center', va='top', color=header_color, transform=ax.transAxes)
y -= 0.06

# Column headers
for x, label in zip(col_x, col_labels):
    ax.text(x, y, label, fontsize=10.5, fontweight='bold', va='top',
            color=header_color, transform=ax.transAxes)
y -= 0.025
ax.plot([0.01, 0.99], [y, y], color='#9CA3AF', linewidth=1, transform=ax.transAxes)
y -= 0.015

for section_name, section_data in sections.items():
    bg_color = section_data['color']
    rows = section_data['rows']

    # Section header
    ax.text(col_x[0], y, section_name, fontsize=10, fontweight='bold',
            va='top', color=header_color, transform=ax.transAxes)
    y -= row_h * 0.6

    # Background rect for section
    rect_y = y - len(rows) * row_h + 0.01
    rect = mpatches.FancyBboxPatch(
        (0.01, rect_y), 0.98, len(rows) * row_h + 0.005,
        boxstyle='round,pad=0.005', facecolor=bg_color, edgecolor='none',
        transform=ax.transAxes, zorder=0
    )
    ax.add_patch(rect)

    for analysis, question, result, sec in rows:
        ax.text(col_x[0] + 0.01, y, analysis, fontsize=9.5, va='top',
                color=text_color, transform=ax.transAxes)
        ax.text(col_x[1], y, question, fontsize=9.5, va='top',
                color=text_color, transform=ax.transAxes)
        ax.text(col_x[2], y, result, fontsize=9.5, va='top',
                fontweight='bold', color=result_color, fontfamily='monospace',
                transform=ax.transAxes)
        ax.text(col_x[3], y, sec, fontsize=9.5, va='top',
                color=text_color, ha='center', transform=ax.transAxes)
        # Light row separator -- centered between this row and next
        sep_y = y - row_h * 0.5
        ax.plot([0.02, 0.98], [sep_y, sep_y],
                color='#E5E7EB', linewidth=0.5, transform=ax.transAxes, zorder=1)
        y -= row_h

    y -= section_gap

# Legend
y -= 0.02
legend_items = [
    (blue_bg, 'Core Paradigms'),
    (green_bg, 'Validation'),
    (yellow_bg, 'Sensitivity'),
]
lx = 0.02
for color, label in legend_items:
    rect = mpatches.FancyBboxPatch(
        (lx, y), 0.025, 0.02,
        boxstyle='round,pad=0.002', facecolor=color, edgecolor='#D1D5DB',
        transform=ax.transAxes
    )
    ax.add_patch(rect)
    ax.text(lx + 0.035, y + 0.01, label, fontsize=9, va='center',
            color=text_color, transform=ax.transAxes)
    lx += 0.16

# Footnote
y -= 0.04
ax.text(0.5, y,
        'N = 64. SB = Spearman\u2013Brown corrected reliability. Neut. = Neutral Acquaintance; Ther. = Supportive Therapist.',
        fontsize=8.5, ha='center', va='top', color='#6B7280', style='italic',
        transform=ax.transAxes)

plt.tight_layout()
outdir = 'Z:/wpworkspace/Screenshot-Conversational-Agent/figures'
fig.savefig(f'{outdir}/fig8_analysis_summary.pdf', bbox_inches='tight', dpi=300)
fig.savefig(f'{outdir}/fig8_analysis_summary.png', bbox_inches='tight', dpi=300)
print('Done: fig8_analysis_summary.pdf + .png')

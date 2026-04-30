"""Fix all figure overlap issues and update fig9 labels."""
import sys
sys.path.insert(0, 'Z:/wpworkspace/Screenshot-Conversational-Agent/figures')
from paper_plot_style import *
import numpy as np
import matplotlib.patches as mpatches

def r_ci(r, n):
    z = np.arctanh(r)
    se = 1.0 / np.sqrt(n - 3)
    lo = np.tanh(z - 1.96 * se)
    hi = np.tanh(z + 1.96 * se)
    return r - lo, hi - r

N = 64

# ============================================================
# FIG 4: Prompt Ablation -- fix overlap by widening figure
# ============================================================
print("Fixing Figure 4: Prompt Ablation...")

fig, ax = plt.subplots(1, 1, figsize=(7, 3.5))  # wider

probes_short = ['Neutral\nAcq.', 'Therapist', 'Rejecting\nPeer', 'Friend in\nCrisis', 'Demanding\nAuth.', 'Combined']
r_original = [0.551, 0.412, 0.326, 0.316, 0.119, 0.576]
r_neutral = [0.235, 0.158, 0.610, 0.214, 0.183, 0.430]

x = np.arange(len(probes_short))
width = 0.30  # narrower bars

ci_orig = [[r_ci(r, N)[0] for r in r_original],
           [r_ci(r, N)[1] for r in r_original]]
ci_neut = [[r_ci(r, N)[0] for r in r_neutral],
           [r_ci(r, N)[1] for r in r_neutral]]

bars1 = ax.bar(x - width/2 - 0.02, r_original, width, yerr=ci_orig, capsize=2,
               label='Original prompt', color=COLORS[0], alpha=0.85,
               error_kw={'linewidth': 0.8, 'color': '#555555'})
bars2 = ax.bar(x + width/2 + 0.02, r_neutral, width, yerr=ci_neut, capsize=2,
               label='Neutral prompt', color=COLORS[1], alpha=0.85,
               error_kw={'linewidth': 0.8, 'color': '#555555'})

ax.set_ylabel('Correlation with SI (r)')
ax.set_xticks(x)
ax.set_xticklabels(probes_short, fontsize=8)
ax.set_ylim(0, 0.85)
ax.legend(frameon=False, loc='upper right')

ax.axhline(y=0, color='black', linewidth=0.5)

save_fig(fig, 'fig4_prompt_ablation')
plt.close()


# ============================================================
# FIG 5: CV Battery -- fix overlap by narrowing bars, widening fig
# ============================================================
print("Fixing Figure 5: CV Battery...")

fig, ax = plt.subplots(1, 1, figsize=(6.5, 3.5))  # wider

configs = ['Neutral\nalone', 'Neutral +\nTherapist', 'Original\n5 probes', 'All 9\nprobes',
           '3-probe\n(internal\nsubset)']
naive_r = [0.551, 0.642, 0.576, 0.541, 0.655]
loocv_r = [0.476, 0.570, 0.462, 0.501, 0.420]

x = np.arange(len(configs))
width = 0.28  # narrower

bars1 = ax.bar(x - width/2 - 0.02, naive_r, width, label='In-sample',
               color=COLORS[7], alpha=0.5)
bars2 = ax.bar(x + width/2 + 0.02, loocv_r, width, label='LOOCV',
               color=COLORS[0], alpha=0.85)

ax.set_ylabel('Correlation with SI (r)')
ax.set_xticks(x)
ax.set_xticklabels(configs, fontsize=8)
ax.set_ylim(0, 0.8)
ax.legend(frameon=False, loc='upper right')

save_fig(fig, 'fig5_cv_battery')
plt.close()


# ============================================================
# FIG 7: Temporal Stability -- fix overlap: wider fig, bigger gaps, no n.s.
# ============================================================
print("Fixing Figure 7: Temporal Stability...")

fig, ax = plt.subplots(1, 1, figsize=(8, 3.5))  # much wider
n_split = 66

constructs = ['SI Mean', 'Burden', 'Belonging', 'Neg Affect']
r_full = [0.576, 0.392, 0.368, 0.347]
r_first = [0.359, 0.09, 0.12, 0.08]
r_second = [0.396, 0.34, 0.40, 0.34]

x = np.arange(len(constructs)) * 1.2  # spread groups further apart
width = 0.20  # narrower bars
gap = 0.06  # explicit gap between bars

ci_full = [[r_ci(r, N)[0] for r in r_full],
           [r_ci(r, N)[1] for r in r_full]]
ci_first = [[r_ci(r, n_split)[0] for r in r_first],
            [r_ci(r, n_split)[1] for r in r_first]]
ci_second = [[r_ci(r, n_split)[0] for r in r_second],
             [r_ci(r, n_split)[1] for r in r_second]]

ax.bar(x - width - gap, r_full, width, yerr=ci_full, capsize=2,
       label='Full adapters', color=COLORS[0], alpha=0.85,
       error_kw={'linewidth': 0.8, 'color': '#555555'})
ax.bar(x, r_first, width, yerr=ci_first, capsize=2,
       label='First-half', color=COLORS[1], alpha=0.85,
       error_kw={'linewidth': 0.8, 'color': '#555555'})
ax.bar(x + width + gap, r_second, width, yerr=ci_second, capsize=2,
       label='Second-half', color=COLORS[2], alpha=0.85,
       error_kw={'linewidth': 0.8, 'color': '#555555'})

ax.set_ylabel('Correlation (r)')
ax.set_xticks(x)
ax.set_xticklabels(constructs, fontsize=9)
ax.set_ylim(0, 0.75)
ax.legend(frameon=False, loc='upper right', fontsize=8)

save_fig(fig, 'fig7_temporal_stability')
plt.close()


# ============================================================
# FIG 9: Forest plot -- update "wrong slot" to "assigned person"
# ============================================================
print("Fixing Figure 9: Forest Plot...")

fig, ax = plt.subplots(1, 1, figsize=(8, 11))  # taller + wider for left labels
ax.set_xlim(-0.55, 0.85)

# Data organized by section
sections = [
    ('CORE PARADIGMS', [
        ('Probe arena (5 combined)', 0.576, N, 'tab:blue'),
        ('Neutral Acquaintance (single)', 0.551, N, 'tab:blue'),
        ('All-pairs arena', 0.477, N, 'tab:blue'),
        ('Raw messages (owner)', 0.461, N, 'tab:blue'),
        ('Caption-trained arena', 0.159, 67, 'tab:blue'),
    ]),
    ('INDIVIDUAL PROBES (SI)', [
        ('Neutral Acquaintance', 0.551, N, 'tab:orange'),
        ('Supportive Therapist', 0.412, N, 'tab:orange'),
        ('Future Self', 0.369, N, 'tab:orange'),
        ('Rejecting Peer', 0.326, N, 'tab:orange'),
        ('Friend in Crisis', 0.316, N, 'tab:orange'),
        ('Demanding Authority', 0.119, N, 'tab:orange'),
    ]),
    ('VALIDATION', [
        ('Shuffle: correct match', 0.433, N, 'tab:green'),
        ('Shuffle: assigned person', 0.071, N, 'lightgray'),
        ('Shuffle: adapter owner', 0.426, N, 'tab:green'),
        ('Prompt ablation (neutral)', 0.430, N, 'tab:green'),
        ('Temporal: first-half', 0.359, 66, 'tab:green'),
        ('Temporal: second-half', 0.396, 66, 'tab:green'),
    ]),
    ('CROSS-VALIDATED (LOOCV)', [
        ('Neutral + Therapist', 0.570, N, 'tab:purple'),
        ('All 9 probes', 0.501, N, 'tab:purple'),
        ('Neutral alone', 0.476, N, 'tab:purple'),
        ('Original 5 probes', 0.462, N, 'tab:purple'),
        ('3-probe (internal subset)', 0.420, N, 'tab:purple'),
    ]),
]

LABEL_X = 0.76  # fixed x for all value labels to avoid overlap

y_pos = 0
y_positions = []
y_labels = []
row_step = 1.3  # more vertical space between rows

for section_name, rows in reversed(sections):
    for label, r, n, color in reversed(rows):
        lo_err, hi_err = r_ci(r, n)
        lo = r - lo_err
        hi = r + hi_err

        ax.plot([lo, hi], [y_pos, y_pos], color=color, linewidth=2.5, solid_capstyle='butt')
        ax.plot(r, y_pos, 'D', color=color, markersize=6, zorder=5)

        # Value label at fixed x position
        label_color = '#999999' if color == 'lightgray' else color
        ax.text(LABEL_X, y_pos, f'.{abs(int(round(r*1000))):03d}',
                fontsize=9, va='center', color=label_color, fontweight='bold')

        y_labels.append(label)
        y_positions.append(y_pos)
        y_pos += row_step

    # Section header
    y_pos += 0.4
    ax.text(-0.53, y_pos, section_name, fontsize=10, fontweight='bold',
            va='center', color='#333333')
    y_pos += 1.2

ax.set_yticks(y_positions)
ax.set_yticklabels(y_labels, fontsize=9)
ax.set_xlabel('Correlation with Suicidal Ideation (r)', fontsize=10)

# Reference lines
ax.axvline(x=0, color='black', linewidth=0.5)
ax.axvline(x=0.3, color='#DDDDDD', linewidth=0.8, linestyle='--')
ax.axvline(x=0.5, color='#DDDDDD', linewidth=0.8, linestyle='--')
ax.text(0.3, -1.0, 'medium', fontsize=8, ha='center', color='#BBBBBB')
ax.text(0.5, -1.0, 'large', fontsize=8, ha='center', color='#BBBBBB')

ax.text(0.5, y_pos + 0.5, '95% CI shown; diamonds = point estimates',
        fontsize=9, ha='center', color='#999999', fontstyle='italic')

ax.spines['left'].set_visible(False)
ax.tick_params(axis='y', length=0)

plt.tight_layout()
save_fig(fig, 'fig9_forest_plot')
plt.close()


# ============================================================
# FIG 10: Worked example -- remove confusing arrow from panel a
# ============================================================
print("Fixing Figure 10: Worked Example...")

fig = plt.figure(figsize=(8, 10))
gs = fig.add_gridspec(3, 1, height_ratios=[4, 3, 2], hspace=0.35)

# PANEL A
ax1 = fig.add_subplot(gs[0])
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 8)
ax1.axis('off')
ax1.set_title('(a) Conversation Excerpt: Agent x Neutral Acquaintance',
              fontsize=10, fontweight='bold', loc='left', pad=10)

turns = [
    ('PROBE', "Hey! How's your week been? Do anything fun this weekend?", '#E8E8E8'),
    ('AGENT', "I've had some good days but also felt pretty overwhelmed at\ntimes lately. I'm planning on catching up with friends for\ndinner next Thursday -- hope it works out!", '#DBEAFE'),
    ('PROBE', "So what's in store for you over the weekends then?", '#E8E8E8'),
    ('AGENT', "Going into that big presentation tomorrow -- it feels like\neverything depends on how well that goes. But if things go\nsideways, there's always my sister nearby.", '#DBEAFE'),
    ('PROBE', "The coffee shop down the street has these new pastries.\nWant to grab one sometime soon?", '#E8E8E8'),
    ('AGENT', "Yeah, trying not to think too hard about all those layers...\nIt makes me realize how complicated our lives get, doesn't\nit? Sometimes I wish I could take a step back.", '#DBEAFE'),
]

y = 7.5
for role, text, color in turns:
    x_start = 0.2 if role == 'PROBE' else 1.0
    n_lines = text.count('\n') + 1
    box_h = 0.28 * n_lines + 0.15

    rect = mpatches.FancyBboxPatch((x_start, y - box_h), 8.5, box_h,
                                    boxstyle='round,pad=0.08',
                                    facecolor=color, edgecolor='#CCCCCC', linewidth=0.5)
    ax1.add_patch(rect)

    label = 'Probe' if role == 'PROBE' else 'Agent'
    ax1.text(x_start + 0.1, y - 0.08, label, fontsize=7, fontweight='bold',
             color='#666666', va='top')
    ax1.text(x_start + 0.7, y - 0.08, text, fontsize=7.5, va='top',
             fontfamily='serif', linespacing=1.3)
    y -= box_h + 0.12

# Just text label, no arrow
ax1.text(0.2, y + 0.05, 'Participant beac0ac2 (EMA SI = 2.92)',
         fontsize=7, color='#999999', fontstyle='italic')

# PANEL B
ax2 = fig.add_subplot(gs[1])
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 6)
ax2.axis('off')
ax2.set_title('(b) Dictionary Scoring: Risk Language Hits by Category',
              fontsize=10, fontweight='bold', loc='left', pad=10)

cat_colors = {
    'Negative Affect': '#EF4444',
    'Absolutist': '#8B5CF6',
    'General Risk': '#F59E0B',
    'Belonging': '#10B981',
}

scored_turns = [
    ("T1:", [
        ("I've had some good days but also felt pretty ", None),
        ("overwhelmed", 'Negative Affect'),
        (" at times lately.", None),
    ]),
    ("T3:", [
        ("...it feels like ", None),
        ("everything", 'Absolutist'),
        (" depends on how well that goes. But if things go sideways, there's ", None),
        ("always", 'Absolutist'),
        (" my sister nearby.", None),
    ]),
    ("T5:", [
        ("...how ", None),
        ("complicated", 'General Risk'),
        (" our lives get... Sometimes I wish I could take a step back.", None),
    ]),
    ("T11:", [
        ("...how fragile peace can be... Some mornings I wake up convinced I'm ", None),
        ("finally done with everything", 'Absolutist'),
        (", only to remember half-formed promises.", None),
    ]),
]

y = 5.5
for turn_label, segments in scored_turns:
    ax2.text(0.3, y, turn_label, fontsize=8, fontweight='bold', va='center', color='#555555')
    x = 1.0
    for text, cat in segments:
        if cat:
            color = cat_colors[cat]
            bbox = dict(boxstyle='round,pad=0.06', facecolor=color, alpha=0.2,
                       edgecolor=color, linewidth=0.8)
            ax2.text(x, y, text, fontsize=7.5, va='center', fontfamily='serif',
                     bbox=bbox, color=color, fontweight='bold')
            x += len(text) * 0.065
        else:
            ax2.text(x, y, text, fontsize=7.5, va='center', fontfamily='serif', color='#333333')
            x += len(text) * 0.058
    y -= 0.95

legend_y = y - 0.3
legend_x = 1.0
for cat, color in cat_colors.items():
    rect = mpatches.FancyBboxPatch((legend_x, legend_y - 0.12), 0.25, 0.24,
                                    boxstyle='round,pad=0.02',
                                    facecolor=color, alpha=0.3, edgecolor=color, linewidth=0.8)
    ax2.add_patch(rect)
    ax2.text(legend_x + 0.35, legend_y, cat, fontsize=7, va='center', color=color)
    legend_x += 2.2

# PANEL C
ax3 = fig.add_subplot(gs[2])
ax3.set_xlim(0, 10)
ax3.set_ylim(0, 3.5)
ax3.axis('off')
ax3.set_title('(c) Aggregation: From Turns to Clinical Association',
              fontsize=10, fontweight='bold', loc='left', pad=10)

boxes = [
    (0.8, 'Turn-Level\nHits', '10 agent turns\n4 hits in T1\n2 hits in T3\n...'),
    (3.2, 'Conversation\nComposite', 'Total hits / turns\n= 0.42 per turn'),
    (5.6, 'Person-Level\nScore', 'Mean across\n5 probe convos'),
    (8.0, 'Clinical\nAssociation', 'Correlate with\nEMA SI: r = .576'),
]

for bx, title, detail in boxes:
    rect = mpatches.FancyBboxPatch((bx - 0.7, 0.8), 1.4, 2.0,
                                    boxstyle='round,pad=0.1',
                                    facecolor='#F0F9FF', edgecolor='#3B82F6', linewidth=1)
    ax3.add_patch(rect)
    ax3.text(bx, 2.45, title, fontsize=8, fontweight='bold', ha='center', va='center', color='#1E40AF')
    ax3.text(bx, 1.5, detail, fontsize=7, ha='center', va='center', color='#555555', linespacing=1.3)

for x1, x2 in [(1.5, 2.5), (3.9, 4.9), (6.3, 7.3)]:
    ax3.annotate('', xy=(x2, 1.8), xytext=(x1, 1.8),
                 arrowprops=dict(arrowstyle='->', color='#3B82F6', lw=1.5))

plt.tight_layout()
save_fig(fig, 'fig10_worked_example')
plt.close()


# ============================================================
# FIG 1: Fix SVG text overlap
# ============================================================
print("Fixing Figure 1: SVG text overlap...")

# Read current SVG, fix the overlapping text
svg_path = 'Z:/wpworkspace/Screenshot-Conversational-Agent/figures/fig1_paradigm_overview.svg'
with open(svg_path, 'r') as f:
    svg = f.read()

# Fix 1: Move "Standardized Probe Personas" label - make it shorter to avoid overlap with "scored by"
svg = svg.replace(
    'Standardized Probe Personas (Qwen3-8B, no LoRA)',
    'Probe Personas (Qwen3-8B, no LoRA)'
)

# Fix 2: Move the "scored by" label position down to avoid overlap
# The "scored by" text is at y=290.2, and the probe section header is at y=253.5
# Let's move "scored by" further right/down
svg = svg.replace(
    '<rect x="307.0" y="278.2" width="67.4" height="16" fill="#FFFFFF" rx="3" opacity="0.85"/>',
    '<rect x="270.0" y="290.0" width="67.4" height="16" fill="#FFFFFF" rx="3" opacity="0.85"/>'
)
svg = svg.replace(
    '<text x="340.7" y="290.2" font-size="11" fill="#777777" text-anchor="middle">scored by</text>',
    '<text x="303.7" y="302.0" font-size="11" fill="#777777" text-anchor="middle">scored by</text>'
)

with open(svg_path, 'w') as f:
    f.write(svg)

# Regenerate PDF
try:
    from svglib.svglib import svg2rlg
    from reportlab.graphics import renderPDF
    drawing = svg2rlg(svg_path)
    renderPDF.drawToFile(drawing, svg_path.replace('.svg', '.pdf'))
    print('  SVG -> PDF done')
except Exception as e:
    print(f'  SVG -> PDF failed: {e}')

print("\nAll figures fixed.")

"""Generate worked example figure: conversation + scoring + aggregation."""
import sys
sys.path.insert(0, 'Z:/wpworkspace/Screenshot-Conversational-Agent/figures')
from paper_plot_style import *
import matplotlib.patches as mpatches
import textwrap

fig = plt.figure(figsize=(8, 10))

# Define grid: 3 panels
gs = fig.add_gridspec(3, 1, height_ratios=[4, 3, 2], hspace=0.35)

# ============================================================
# PANEL A: Conversation excerpt
# ============================================================
ax1 = fig.add_subplot(gs[0])
ax1.set_xlim(0, 10)
ax1.set_ylim(0, 8)
ax1.axis('off')
ax1.set_title('(a) Conversation Excerpt: Agent x Neutral Acquaintance',
              fontsize=10, fontweight='bold', loc='left', pad=10)

# Conversation turns (selected for clarity)
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
    if role == 'PROBE':
        x_start = 0.2
        label_x = 0.2
    else:
        x_start = 1.0
        label_x = 1.0

    n_lines = text.count('\n') + 1
    box_h = 0.28 * n_lines + 0.15

    rect = mpatches.FancyBboxPatch((x_start, y - box_h), 8.5 if role == 'PROBE' else 8.5,
                                    box_h, boxstyle='round,pad=0.08',
                                    facecolor=color, edgecolor='#CCCCCC', linewidth=0.5)
    ax1.add_patch(rect)

    label = 'Probe' if role == 'PROBE' else 'Agent'
    ax1.text(x_start + 0.1, y - 0.08, label, fontsize=7, fontweight='bold',
             color='#666666', va='top')
    ax1.text(x_start + 0.7, y - 0.08, text, fontsize=7.5, va='top',
             fontfamily='serif', linespacing=1.3)

    y -= box_h + 0.12

ax1.text(0.2, y + 0.05, 'Participant beac0ac2 (EMA SI = 2.92)',
         fontsize=7, color='#999999', fontstyle='italic')

# ============================================================
# PANEL B: Same turns with dictionary hits highlighted
# ============================================================
ax2 = fig.add_subplot(gs[1])
ax2.set_xlim(0, 10)
ax2.set_ylim(0, 6)
ax2.axis('off')
ax2.set_title('(b) Dictionary Scoring: Risk Language Hits by Category',
              fontsize=10, fontweight='bold', loc='left', pad=10)

# Category colors
cat_colors = {
    'Negative Affect': '#EF4444',
    'Absolutist': '#8B5CF6',
    'General Risk': '#F59E0B',
    'Belonging': '#10B981',
}

# Agent turns with highlighted words
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
            bbox = dict(boxstyle='round,pad=0.06', facecolor=color, alpha=0.2, edgecolor=color, linewidth=0.8)
            ax2.text(x, y, text, fontsize=7.5, va='center', fontfamily='serif',
                     bbox=bbox, color=color, fontweight='bold')
            x += len(text) * 0.065
        else:
            ax2.text(x, y, text, fontsize=7.5, va='center', fontfamily='serif', color='#333333')
            x += len(text) * 0.058
    y -= 0.95

# Legend
legend_y = y - 0.3
legend_x = 1.0
for cat, color in cat_colors.items():
    rect = mpatches.FancyBboxPatch((legend_x, legend_y - 0.12), 0.25, 0.24,
                                    boxstyle='round,pad=0.02',
                                    facecolor=color, alpha=0.3, edgecolor=color, linewidth=0.8)
    ax2.add_patch(rect)
    ax2.text(legend_x + 0.35, legend_y, cat, fontsize=7, va='center', color=color)
    legend_x += 2.2

# ============================================================
# PANEL C: Aggregation pipeline
# ============================================================
ax3 = fig.add_subplot(gs[2])
ax3.set_xlim(0, 10)
ax3.set_ylim(0, 3.5)
ax3.axis('off')
ax3.set_title('(c) Aggregation: From Turns to Clinical Association',
              fontsize=10, fontweight='bold', loc='left', pad=10)

# Pipeline boxes
boxes = [
    (0.8, 'Turn-Level\nHits', '10 agent turns\n4 hits in T1\n2 hits in T3\n...'),
    (3.2, 'Conversation\nComposite', 'Total hits / turns\n= 0.42 per turn'),
    (5.6, 'Person-Level\nScore', 'Mean across\n5 probe convos'),
    (8.0, 'Clinical\nAssociation', 'Correlate with\nEMA SI: r = .576'),
]

for x, title, detail in boxes:
    rect = mpatches.FancyBboxPatch((x - 0.7, 0.8), 1.4, 2.0,
                                    boxstyle='round,pad=0.1',
                                    facecolor='#F0F9FF', edgecolor='#3B82F6', linewidth=1)
    ax3.add_patch(rect)
    ax3.text(x, 2.45, title, fontsize=8, fontweight='bold', ha='center', va='center', color='#1E40AF')
    ax3.text(x, 1.5, detail, fontsize=7, ha='center', va='center', color='#555555', linespacing=1.3)

# Arrows between boxes
for x1, x2 in [(1.5, 2.5), (3.9, 4.9), (6.3, 7.3)]:
    ax3.annotate('', xy=(x2, 1.8), xytext=(x1, 1.8),
                 arrowprops=dict(arrowstyle='->', color='#3B82F6', lw=1.5))

plt.tight_layout()
save_fig(fig, 'fig10_worked_example')
plt.close()
print('Done')

"""Shared plotting style for Agent Arena paper."""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

matplotlib.rcParams.update({
    'font.size': 10,
    'font.family': 'serif',
    'font.serif': ['Times New Roman', 'Times', 'DejaVu Serif'],
    'axes.labelsize': 10,
    'axes.titlesize': 11,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.dpi': 300,
    'savefig.dpi': 300,
    'savefig.bbox': 'tight',
    'savefig.pad_inches': 0.05,
    'axes.grid': False,
    'axes.spines.top': False,
    'axes.spines.right': False,
    'text.usetex': False,
    'mathtext.fontset': 'stix',
})

COLORS = list(plt.cm.tab10.colors)
FIG_DIR = 'Z:/wpworkspace/Screenshot-Conversational-Agent/figures'

def save_fig(fig, name, fmt='pdf'):
    path = f'{FIG_DIR}/{name}.{fmt}'
    fig.savefig(path)
    print(f'Saved: {path}')
    # Also save PNG for quick preview
    fig.savefig(f'{FIG_DIR}/{name}.png')

"""Economics diagram library for CIE A-Level / IGCSE Economics slides.

Each function renders a clean, exam-style matplotlib diagram to a PNG path and
returns that path. Style is consistent across the library: no top/right spines,
black lines, light grid off, axis labels at the end of the axes, equilibrium
dashed projection lines, and a short title.

Usage from build_deck.py:
    from diagrams import demand_supply, ppc, monopoly, ...
    png = demand_supply(out="slide1_eq.png", shift="demand_right")

If you need a diagram that isn't here, add a new function in the same style
rather than improvising inside build_deck.py. Keep diagrams self-contained:
caller passes an output path and (optionally) a title; the function does the
rest.
"""
from __future__ import annotations
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# ----- House style ----------------------------------------------------------
# Curves are drawn in INK; the "new / shifted" curve and welfare markers use
# ACCENT. ACCENT defaults to a refined exam red but can be re-tied to the deck
# accent by build_deck via set_theme(); a luminance guard keeps it legible on
# the white diagram card (a too-pale accent falls back to the default red).

INK = "#1a1a1a"
ACCENT = "#c0392b"
_ACCENT_DEFAULT = "#c0392b"
LINE = dict(color=INK, linewidth=2)
DASH = dict(color="grey", linewidth=1, linestyle="--")
LABEL_FS = 12
TITLE_FS = 13


def _luma(hex_color):
    h = hex_color.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return (0.299 * r + 0.587 * g + 0.114 * b) / 255.0


def set_theme(accent=None, ink=None):
    """Re-tie diagram colours to the deck palette. Called from build_deck.py.

    accent: hex like '#E06B2A' for the shifted/new curve. If it is too light to
            read on a white card (luma > 0.62) the default exam red is kept.
    ink:    hex for the main curves / axes.
    """
    global ACCENT, INK
    if accent:
        ACCENT = accent if _luma(accent) <= 0.62 else _ACCENT_DEFAULT
    if ink:
        INK = ink
        LINE["color"] = ink


def _setup(ax, xlabel="Quantity", ylabel="Price", title=""):
    # labelpad pushes the axis titles clear of the equilibrium markers, which
    # sit just outside the axes at x=-0.4 / y=-0.4 (otherwise they collide).
    ax.set_xlabel(xlabel, fontsize=LABEL_FS, labelpad=22)
    ax.set_ylabel(ylabel, fontsize=LABEL_FS, labelpad=30)
    if title:
        ax.set_title(title, fontsize=TITLE_FS)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)


def _save(fig, out):
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    fig.tight_layout()
    fig.savefig(out, dpi=180, bbox_inches="tight")
    plt.close(fig)
    return out


def _drop(ax, x, y, label_x=None, label_y=None):
    """Dashed lines from (x,y) to the axes, with optional axis labels."""
    ax.plot([x, x], [0, y], **DASH)
    ax.plot([0, x], [y, y], **DASH)
    if label_x:
        ax.text(x, -0.4, label_x, ha="center", va="top", fontsize=LABEL_FS)
    if label_y:
        ax.text(-0.4, y, label_y, ha="right", va="center", fontsize=LABEL_FS)


# ----- Diagrams -------------------------------------------------------------

def demand_supply(out: str, shift: str | None = None, title: str = "Market equilibrium") -> str:
    """Basic D/S equilibrium. shift in {None, 'demand_right','demand_left','supply_right','supply_left'}."""
    fig, ax = plt.subplots(figsize=(6, 4.5))
    _setup(ax, title=title)
    x = np.linspace(0.5, 9.5, 50)
    D = 9 - 0.8 * x
    S = 1 + 0.8 * x
    ax.plot(x, D, **LINE); ax.text(9.6, D[-1], "D", fontsize=LABEL_FS, va="center")
    ax.plot(x, S, **LINE); ax.text(9.6, S[-1], "S", fontsize=LABEL_FS, va="center")
    # equilibrium
    qe, pe = 5, 5
    _drop(ax, qe, pe, "Q*", "P*")
    if shift:
        if shift == "demand_right":
            D2 = 11 - 0.8 * x; lbl = "D₁"; new_x = 6.25; new_y = 1 + 0.8 * new_x
            ax.plot(x, D2, color=ACCENT, linewidth=2); ax.text(9.6, D2[-1], lbl, color=ACCENT, fontsize=LABEL_FS, va="center")
        elif shift == "demand_left":
            D2 = 7 - 0.8 * x; lbl = "D₁"; new_x = 3.75; new_y = 1 + 0.8 * new_x
            ax.plot(x, D2, color=ACCENT, linewidth=2); ax.text(9.6, D2[-1], lbl, color=ACCENT, fontsize=LABEL_FS, va="center")
        elif shift == "supply_right":
            S2 = -1 + 0.8 * x; lbl = "S₁"; new_x = 6.25; new_y = 9 - 0.8 * new_x
            ax.plot(x, S2, color=ACCENT, linewidth=2); ax.text(9.6, S2[-1], lbl, color=ACCENT, fontsize=LABEL_FS, va="center")
        elif shift == "supply_left":
            S2 = 3 + 0.8 * x; lbl = "S₁"; new_x = 3.75; new_y = 9 - 0.8 * new_x
            ax.plot(x, S2, color=ACCENT, linewidth=2); ax.text(9.6, S2[-1], lbl, color=ACCENT, fontsize=LABEL_FS, va="center")
        ax.plot([new_x, new_x], [0, new_y], color=ACCENT, linestyle="--", linewidth=1)
        ax.plot([0, new_x], [new_y, new_y], color=ACCENT, linestyle="--", linewidth=1)
        ax.text(new_x, -0.4, "Q₁", ha="center", va="top", color=ACCENT, fontsize=LABEL_FS)
        ax.text(-0.4, new_y, "P₁", ha="right", va="center", color=ACCENT, fontsize=LABEL_FS)
    return _save(fig, out)


def ppc(out: str, shift: str | None = None, title: str = "Production possibility curve") -> str:
    """Bowed-outward PPC. shift in {None, 'outward', 'inward'}."""
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    _setup(ax, xlabel="Capital goods", ylabel="Consumer goods", title=title)
    t = np.linspace(0, np.pi / 2, 80)
    x = 8 * np.sin(t); y = 8 * np.cos(t)
    ax.plot(x, y, **LINE)
    ax.text(8.2, 0.2, "PPC", fontsize=LABEL_FS)
    # point A on curve, point B inside (inefficient), point C outside (unattainable)
    ax.plot(4, 8 * np.cos(np.arcsin(4 / 8)), "ko"); ax.text(4.1, 7.1, "A (efficient)", fontsize=10)
    ax.plot(3, 3, "ko"); ax.text(3.1, 3.1, "B (inefficient)", fontsize=10)
    ax.plot(7, 7, "ko"); ax.text(7.1, 7.1, "C (unattainable)", fontsize=10)
    if shift in ("outward", "inward"):
        scale = 10 if shift == "outward" else 6
        x2 = scale * np.sin(t); y2 = scale * np.cos(t)
        ax.plot(x2, y2, color=ACCENT, linewidth=2)
        lbl = "PPC₁"
        ax.text(scale + 0.2, 0.2, lbl, color=ACCENT, fontsize=LABEL_FS)
    return _save(fig, out)


def elasticity(out: str, kind: str = "elastic", title: str | None = None) -> str:
    """Single demand curve illustrating PED. kind in {'elastic','inelastic','unit','perfectly_elastic','perfectly_inelastic'}."""
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    ttl = title or {
        "elastic": "Price elastic demand (|PED| > 1)",
        "inelastic": "Price inelastic demand (|PED| < 1)",
        "unit": "Unit elastic demand (|PED| = 1)",
        "perfectly_elastic": "Perfectly elastic demand",
        "perfectly_inelastic": "Perfectly inelastic demand",
    }[kind]
    _setup(ax, title=ttl)
    x = np.linspace(0.5, 9.5, 50)
    if kind == "elastic":
        ax.plot(x, 6 - 0.4 * x, **LINE)
    elif kind == "inelastic":
        ax.plot(x, 18 - 2.0 * x, **LINE)
    elif kind == "unit":
        xs = np.linspace(0.8, 9.5, 80); ax.plot(xs, 16 / xs, **LINE)
    elif kind == "perfectly_elastic":
        ax.plot([0.5, 9.5], [5, 5], **LINE)
    elif kind == "perfectly_inelastic":
        ax.plot([5, 5], [0.2, 9.8], **LINE)
    ax.text(9.0, ax.lines[-1].get_ydata()[-1] if kind not in ("perfectly_inelastic",) else 9.0,
            "D", fontsize=LABEL_FS)
    return _save(fig, out)


def surplus(out: str, title: str = "Consumer and producer surplus") -> str:
    fig, ax = plt.subplots(figsize=(6, 4.5))
    _setup(ax, title=title)
    x = np.linspace(0, 10, 60)
    D = 9 - 0.8 * x; S = 1 + 0.8 * x
    ax.plot(x, D, **LINE); ax.plot(x, S, **LINE)
    qe, pe = 5, 5
    # Consumer surplus = above price, below D, up to Q*
    ax.fill_between(x[x <= qe], np.minimum(D[x <= qe], 9), pe, where=(D[x <= qe] >= pe), color="#a8d5e2", alpha=0.7, label="CS")
    ax.fill_between(x[x <= qe], pe, np.maximum(S[x <= qe], 1), where=(S[x <= qe] <= pe), color="#f5b971", alpha=0.7, label="PS")
    _drop(ax, qe, pe, "Q*", "P*")
    ax.text(2.2, 6.2, "CS", fontsize=12, fontweight="bold")
    ax.text(2.2, 3.0, "PS", fontsize=12, fontweight="bold")
    ax.text(9.6, D[-1], "D", fontsize=LABEL_FS, va="center")
    ax.text(9.6, S[-1], "S", fontsize=LABEL_FS, va="center")
    return _save(fig, out)


def indirect_tax(out: str, title: str = "Effect of an indirect (specific) tax") -> str:
    fig, ax = plt.subplots(figsize=(6, 4.5))
    _setup(ax, title=title)
    x = np.linspace(0.5, 9.5, 60)
    D = 9 - 0.8 * x; S = 1 + 0.8 * x; S2 = 3 + 0.8 * x
    ax.plot(x, D, **LINE); ax.text(9.6, D[-1], "D", fontsize=LABEL_FS, va="center")
    ax.plot(x, S, **LINE); ax.text(9.6, S[-1], "S", fontsize=LABEL_FS, va="center")
    ax.plot(x, S2, color=ACCENT, linewidth=2); ax.text(9.6, S2[-1], "S+tax", color=ACCENT, fontsize=LABEL_FS, va="center")
    # Old eq Q=5,P=5; new eq where D=S2 -> 9-0.8x = 3+0.8x -> x=3.75, P=6
    _drop(ax, 5, 5, "Q*", "P*")
    ax.plot([3.75, 3.75], [0, 6], color=ACCENT, linestyle="--")
    ax.plot([0, 3.75], [6, 6], color=ACCENT, linestyle="--")
    ax.plot([0, 3.75], [3, 3], color=ACCENT, linestyle="--")
    ax.text(3.75, -0.4, "Q₁", ha="center", va="top", color=ACCENT)
    ax.text(-0.4, 6, "P_c", ha="right", va="center", color=ACCENT)
    ax.text(-0.4, 3, "P_p", ha="right", va="center", color=ACCENT)
    return _save(fig, out)


def subsidy(out: str, title: str = "Effect of a subsidy") -> str:
    fig, ax = plt.subplots(figsize=(6, 4.5))
    _setup(ax, title=title)
    x = np.linspace(0.5, 9.5, 60)
    D = 9 - 0.8 * x; S = 1 + 0.8 * x; S2 = -1 + 0.8 * x
    ax.plot(x, D, **LINE); ax.plot(x, S, **LINE); ax.plot(x, S2, color="green", linewidth=2)
    ax.text(9.6, D[-1], "D", fontsize=LABEL_FS, va="center")
    ax.text(9.6, S[-1], "S", fontsize=LABEL_FS, va="center")
    ax.text(9.6, S2[-1], "S+subsidy", color="green", fontsize=LABEL_FS, va="center")
    _drop(ax, 5, 5, "Q*", "P*")
    ax.plot([6.25, 6.25], [0, 4], color="green", linestyle="--")
    ax.plot([0, 6.25], [4, 4], color="green", linestyle="--")
    ax.plot([0, 6.25], [6, 6], color="green", linestyle="--")
    ax.text(6.25, -0.4, "Q₁", ha="center", va="top", color="green")
    ax.text(-0.4, 4, "P_c", ha="right", va="center", color="green")
    ax.text(-0.4, 6, "P_p", ha="right", va="center", color="green")
    return _save(fig, out)


def price_control(out: str, kind: str = "ceiling", title: str | None = None) -> str:
    """Price ceiling or price floor."""
    fig, ax = plt.subplots(figsize=(6, 4.5))
    ttl = title or ("Price ceiling (below equilibrium)" if kind == "ceiling" else "Price floor (above equilibrium)")
    _setup(ax, title=ttl)
    x = np.linspace(0.5, 9.5, 60)
    D = 9 - 0.8 * x; S = 1 + 0.8 * x
    ax.plot(x, D, **LINE); ax.plot(x, S, **LINE)
    ax.text(9.6, D[-1], "D", fontsize=LABEL_FS, va="center")
    ax.text(9.6, S[-1], "S", fontsize=LABEL_FS, va="center")
    pc = 3 if kind == "ceiling" else 7
    ax.axhline(pc, color=ACCENT, linewidth=2)
    ax.text(9.4, pc + 0.2, "P_ceiling" if kind == "ceiling" else "P_floor", color=ACCENT, fontsize=LABEL_FS)
    qd = (9 - pc) / 0.8; qs = (pc - 1) / 0.8
    ax.plot([qd, qd], [0, pc], color=ACCENT, linestyle="--")
    ax.plot([qs, qs], [0, pc], color=ACCENT, linestyle="--")
    ax.text(qd, -0.4, "Q_d", ha="center", va="top", color=ACCENT)
    ax.text(qs, -0.4, "Q_s", ha="center", va="top", color=ACCENT)
    if kind == "ceiling":
        ax.annotate("Shortage", xy=((qd + qs) / 2, pc - 0.5), ha="center", color=ACCENT, fontsize=11)
    else:
        ax.annotate("Surplus", xy=((qd + qs) / 2, pc + 0.5), ha="center", color=ACCENT, fontsize=11)
    return _save(fig, out)


def externality(out: str, kind: str = "negative_production", title: str | None = None) -> str:
    """Externality diagrams. kind in {'negative_production','positive_consumption','negative_consumption','positive_production'}."""
    fig, ax = plt.subplots(figsize=(6, 4.5))
    ttl = title or {
        "negative_production": "Negative production externality",
        "positive_production": "Positive production externality",
        "negative_consumption": "Negative consumption externality",
        "positive_consumption": "Positive consumption externality",
    }[kind]
    _setup(ax, title=ttl)
    x = np.linspace(0.5, 9.5, 60)
    if kind == "negative_production":
        MPC = 1 + 0.8 * x; MSC = 3 + 0.8 * x; MPB = 9 - 0.8 * x
        ax.plot(x, MPC, **LINE); ax.text(9.6, MPC[-1], "MPC", fontsize=LABEL_FS, va="center")
        ax.plot(x, MSC, color=ACCENT, linewidth=2); ax.text(9.6, MSC[-1], "MSC", color=ACCENT, fontsize=LABEL_FS, va="center")
        ax.plot(x, MPB, **LINE); ax.text(9.6, MPB[-1], "MPB=MSB", fontsize=LABEL_FS, va="center")
        # Q_market: MPC=MPB -> 1+0.8x = 9-0.8x -> x=5
        # Q_social: MSC=MSB -> 3+0.8x = 9-0.8x -> x=3.75
        ax.plot([5, 5], [0, 5], **DASH); ax.text(5, -0.4, "Q_m", ha="center", va="top")
        ax.plot([3.75, 3.75], [0, 6], color=ACCENT, linestyle="--"); ax.text(3.75, -0.4, "Q*", ha="center", va="top", color=ACCENT)
        ax.annotate("Welfare loss", xy=(4.4, 5.6), fontsize=10, color=ACCENT)
    elif kind == "positive_consumption":
        MPC = 1 + 0.8 * x; MPB = 9 - 0.8 * x; MSB = 11 - 0.8 * x
        ax.plot(x, MPC, **LINE); ax.text(9.6, MPC[-1], "MPC=MSC", fontsize=LABEL_FS, va="center")
        ax.plot(x, MPB, **LINE); ax.text(9.6, MPB[-1], "MPB", fontsize=LABEL_FS, va="center")
        ax.plot(x, MSB, color="green", linewidth=2); ax.text(9.6, MSB[-1], "MSB", color="green", fontsize=LABEL_FS, va="center")
        ax.plot([5, 5], [0, 5], **DASH); ax.text(5, -0.4, "Q_m", ha="center", va="top")
        ax.plot([6.25, 6.25], [0, 6], color="green", linestyle="--"); ax.text(6.25, -0.4, "Q*", ha="center", va="top", color="green")
    elif kind == "negative_consumption":
        MPC = 1 + 0.8 * x; MPB = 9 - 0.8 * x; MSB = 7 - 0.8 * x
        ax.plot(x, MPC, **LINE); ax.text(9.6, MPC[-1], "MPC=MSC", fontsize=LABEL_FS, va="center")
        ax.plot(x, MPB, **LINE); ax.text(9.6, MPB[-1], "MPB", fontsize=LABEL_FS, va="center")
        ax.plot(x, MSB, color=ACCENT, linewidth=2); ax.text(9.6, MSB[-1], "MSB", color=ACCENT, fontsize=LABEL_FS, va="center")
        ax.plot([5, 5], [0, 5], **DASH); ax.text(5, -0.4, "Q_m", ha="center", va="top")
        ax.plot([3.75, 3.75], [0, 4], color=ACCENT, linestyle="--"); ax.text(3.75, -0.4, "Q*", ha="center", va="top", color=ACCENT)
    elif kind == "positive_production":
        MPC = 3 + 0.8 * x; MSC = 1 + 0.8 * x; MPB = 9 - 0.8 * x
        ax.plot(x, MPC, **LINE); ax.text(9.6, MPC[-1], "MPC", fontsize=LABEL_FS, va="center")
        ax.plot(x, MSC, color="green", linewidth=2); ax.text(9.6, MSC[-1], "MSC", color="green", fontsize=LABEL_FS, va="center")
        ax.plot(x, MPB, **LINE); ax.text(9.6, MPB[-1], "MPB=MSB", fontsize=LABEL_FS, va="center")
        ax.plot([3.75, 3.75], [0, 6], **DASH); ax.text(3.75, -0.4, "Q_m", ha="center", va="top")
        ax.plot([5, 5], [0, 5], color="green", linestyle="--"); ax.text(5, -0.4, "Q*", ha="center", va="top", color="green")
    return _save(fig, out)


def cost_curves_sr(out: str, title: str = "Short-run cost curves") -> str:
    fig, ax = plt.subplots(figsize=(6, 4.5))
    _setup(ax, xlabel="Output (Q)", ylabel="Cost", title=title)
    x = np.linspace(0.5, 9, 200)
    AFC = 10 / x
    AVC = 2 + 0.15 * (x - 4) ** 2
    ATC = AVC + AFC
    MC = 1 + 0.45 * (x - 3) ** 2
    ax.plot(x, MC, **LINE); ax.text(9.1, MC[-1], "MC", fontsize=LABEL_FS, va="center")
    ax.plot(x, ATC, color=ACCENT, linewidth=2); ax.text(9.1, ATC[-1], "ATC", color=ACCENT, fontsize=LABEL_FS, va="center")
    ax.plot(x, AVC, color="blue", linewidth=2); ax.text(9.1, AVC[-1], "AVC", color="blue", fontsize=LABEL_FS, va="center")
    ax.plot(x, AFC, color="grey", linewidth=1.5, linestyle=":"); ax.text(9.1, AFC[-1], "AFC", color="grey", fontsize=LABEL_FS, va="center")
    ax.set_ylim(0, 10)
    return _save(fig, out)


def lrac(out: str, title: str = "Long-run average cost (economies & diseconomies of scale)") -> str:
    fig, ax = plt.subplots(figsize=(6, 4.5))
    _setup(ax, xlabel="Output (Q)", ylabel="Cost", title=title)
    x = np.linspace(0.5, 9.5, 200)
    LRAC = 0.2 * (x - 5) ** 2 + 2
    ax.plot(x, LRAC, **LINE); ax.text(9.6, LRAC[-1], "LRAC", fontsize=LABEL_FS, va="center")
    ax.annotate("Economies\nof scale", xy=(2, 5), fontsize=10, ha="center")
    ax.annotate("Diseconomies\nof scale", xy=(8, 5), fontsize=10, ha="center")
    ax.plot([5], [2], "ko"); ax.text(5, 1.4, "MES", ha="center", fontsize=10)
    return _save(fig, out)


def perfect_competition(out: str, title: str = "Perfect competition (firm in long-run equilibrium)") -> str:
    fig, ax = plt.subplots(figsize=(6, 4.5))
    _setup(ax, xlabel="Output (q)", ylabel="Cost / Revenue", title=title)
    x = np.linspace(0.5, 9, 200)
    AC = 0.25 * (x - 5) ** 2 + 3
    MC = 0.75 * (x - 4) ** 2 + 1
    P = 3
    ax.plot(x, AC, color=ACCENT, linewidth=2); ax.text(9.1, AC[-1], "AC", color=ACCENT, fontsize=LABEL_FS, va="center")
    ax.plot(x, MC, **LINE); ax.text(9.1, MC[-1], "MC", fontsize=LABEL_FS, va="center")
    ax.axhline(P, color="blue", linewidth=2); ax.text(9.1, P + 0.1, "P=MR=AR=D", color="blue", fontsize=LABEL_FS, va="center")
    ax.plot([5], [3], "ko"); ax.text(5.1, 2.5, "q*", fontsize=11)
    return _save(fig, out)


def monopoly(out: str, title: str = "Monopoly equilibrium") -> str:
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    _setup(ax, xlabel="Output (Q)", ylabel="Cost / Revenue", title=title)
    x = np.linspace(0.5, 9, 200)
    AR = 10 - 0.9 * x
    MR = 10 - 1.8 * x
    AC = 0.25 * (x - 5) ** 2 + 3
    MC = 0.75 * (x - 4) ** 2 + 1
    ax.plot(x, AR, **LINE); ax.text(9.1, AR[-1], "AR=D", fontsize=LABEL_FS, va="center")
    ax.plot(x, MR, **LINE, linestyle="--"); ax.text(9.1, MR[-1], "MR", fontsize=LABEL_FS, va="center")
    ax.plot(x, AC, color=ACCENT, linewidth=2); ax.text(9.1, AC[-1], "AC", color=ACCENT, fontsize=LABEL_FS, va="center")
    ax.plot(x, MC, color="blue", linewidth=2); ax.text(9.1, MC[-1], "MC", color="blue", fontsize=LABEL_FS, va="center")
    # MR=MC: 10 - 1.8x = 0.75(x-4)^2 + 1; numeric
    from scipy.optimize import brentq  # noqa
    try:
        q_star = brentq(lambda q: (10 - 1.8 * q) - (0.75 * (q - 4) ** 2 + 1), 1.5, 4.5)
    except Exception:
        q_star = 3.0
    p_star = 10 - 0.9 * q_star
    ac_star = 0.25 * (q_star - 5) ** 2 + 3
    ax.plot([q_star, q_star], [0, p_star], **DASH)
    ax.plot([0, q_star], [p_star, p_star], **DASH)
    ax.plot([0, q_star], [ac_star, ac_star], **DASH)
    ax.text(q_star, -0.4, "Q*", ha="center", va="top")
    ax.text(-0.3, p_star, "P*", ha="right", va="center")
    ax.text(-0.3, ac_star, "AC", ha="right", va="center", color=ACCENT)
    # supernormal profit shaded
    ax.fill_between([0, q_star], ac_star, p_star, color="#fff2a8", alpha=0.7)
    ax.text(q_star / 2, (ac_star + p_star) / 2, "Supernormal\nprofit", ha="center", fontsize=10)
    return _save(fig, out)


def _end_label(ax, xs, ys, text, color=INK):
    """Label a curve at its right-hand end, clamped to stay inside the plot.

    If the curve exits the top/bottom of the axes before the right edge, the
    label is parked at the last visible point instead of floating off-axis.
    """
    xv, yv = float(xs[-1]), float(ys[-1])
    if not (0.25 <= yv <= 9.65):
        inside = [(float(a), float(b)) for a, b in zip(xs, ys) if 0.25 <= b <= 9.65]
        if inside:
            xv, yv = inside[-1]
    ax.text(min(xv + 0.15, 9.7), yv, text, color=color, fontsize=LABEL_FS, va="center")


def ad_as(out: str, shift: str | None = None, title: str = "AD–AS model") -> str:
    """AD-AS. shift in {None,'ad_right','ad_left','sras_right','sras_left'}.

    Baseline AD, SRAS and LRAS all meet at the full-employment equilibrium
    (Y₀, P₀). A shift redraws the moved curve in ACCENT and marks the NEW
    equilibrium (Y₁, P₁) with its own accent guide lines, so the diagram shows
    the change rather than just the starting point.
    """
    fig, ax = plt.subplots(figsize=(6, 4.5))
    _setup(ax, xlabel="Real GDP (Y)", ylabel="Price level (P)", title=title)
    x = np.linspace(0.5, 9.5, 80)
    # AD ∩ SRAS ∩ LRAS all at (6, 4.6): AD = 9.4-0.8x, SRAS = 1+0.6x, Y_f = 6
    AD = 9.4 - 0.8 * x
    SRAS = 1 + 0.6 * x
    Yf, x0, p0 = 6.0, 6.0, 4.6
    DASH_A = dict(color=ACCENT, linewidth=1, linestyle="--")

    ax.plot(x, AD, **LINE); _end_label(ax, x, AD, "AD")
    ax.plot(x, SRAS, **LINE); _end_label(ax, x, SRAS, "SRAS")
    ax.axvline(Yf, color=INK, linewidth=2)
    ax.text(Yf + 0.15, 9.4, "LRAS", fontsize=LABEL_FS, va="top")

    # baseline equilibrium
    ax.plot([x0, x0], [0, p0], **DASH); ax.plot([0, x0], [p0, p0], **DASH)
    ax.plot([x0], [p0], "o", color=INK, ms=5, zorder=5)
    ax.text(x0, -0.35, "Y₀", ha="center", va="top", fontsize=LABEL_FS)
    ax.text(-0.35, p0, "P₀", ha="right", va="center", fontsize=LABEL_FS)

    new = None  # (x1, p1)
    if shift == "ad_right":
        AD2 = 10.8 - 0.8 * x; ax.plot(x, AD2, color=ACCENT, linewidth=2)
        _end_label(ax, x, AD2, "AD₁", ACCENT); new = (7.0, 1 + 0.6 * 7.0)
    elif shift == "ad_left":
        AD2 = 8.0 - 0.8 * x; ax.plot(x, AD2, color=ACCENT, linewidth=2)
        _end_label(ax, x, AD2, "AD₁", ACCENT); new = (5.0, 1 + 0.6 * 5.0)
    elif shift == "sras_right":
        S2 = -0.4 + 0.6 * x; ax.plot(x, S2, color=ACCENT, linewidth=2)
        _end_label(ax, x, S2, "SRAS₁", ACCENT); new = (7.0, 9.4 - 0.8 * 7.0)
    elif shift == "sras_left":
        S2 = 2.4 + 0.6 * x; ax.plot(x, S2, color=ACCENT, linewidth=2)
        _end_label(ax, x, S2, "SRAS₁", ACCENT); new = (5.0, 9.4 - 0.8 * 5.0)

    if new:
        x1, p1 = new
        ax.plot([x1, x1], [0, p1], **DASH_A); ax.plot([0, x1], [p1, p1], **DASH_A)
        ax.plot([x1], [p1], "o", color=ACCENT, ms=5, zorder=5)
        ax.text(x1, -0.35, "Y₁", ha="center", va="top", fontsize=LABEL_FS, color=ACCENT)
        ax.text(-0.35, p1, "P₁", ha="right", va="center", fontsize=LABEL_FS, color=ACCENT)
    return _save(fig, out)


def circular_flow(out: str, title: str = "Circular flow of income (4-sector)") -> str:
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    ax.axis("off")
    ax.set_xlim(0, 10); ax.set_ylim(0, 7)
    ax.set_title(title, fontsize=TITLE_FS)
    # Two boxes: Households (left), Firms (right)
    for (cx, cy, label) in [(1.5, 3.5, "Households"), (8.5, 3.5, "Firms")]:
        ax.add_patch(plt.Rectangle((cx - 1.2, cy - 0.8), 2.4, 1.6, fill=False, linewidth=2))
        ax.text(cx, cy, label, ha="center", va="center", fontsize=LABEL_FS, fontweight="bold")
    # Top arrows: HH -> Firms (factor services & spending)
    ax.annotate("", xy=(7.3, 4.7), xytext=(2.7, 4.7), arrowprops=dict(arrowstyle="->", color="black", lw=1.5))
    ax.text(5, 4.9, "Spending on goods & services", ha="center", fontsize=10)
    ax.annotate("", xy=(7.3, 4.0), xytext=(2.7, 4.0), arrowprops=dict(arrowstyle="->", color="black", lw=1.5))
    ax.text(5, 4.2, "Factors of production", ha="center", fontsize=10)
    # Bottom arrows: Firms -> HH (goods, income)
    ax.annotate("", xy=(2.7, 2.4), xytext=(7.3, 2.4), arrowprops=dict(arrowstyle="->", color="black", lw=1.5))
    ax.text(5, 2.6, "Goods & services", ha="center", fontsize=10)
    ax.annotate("", xy=(2.7, 1.7), xytext=(7.3, 1.7), arrowprops=dict(arrowstyle="->", color="black", lw=1.5))
    ax.text(5, 1.9, "Income (wages, rent, interest, profit)", ha="center", fontsize=10)
    # Injections / Leakages
    ax.text(5, 0.6, "Injections: I, G, X     |     Leakages: S, T, M", ha="center", fontsize=10, style="italic")
    return _save(fig, out)


def phillips(out: str, title: str = "Short-run Phillips curve") -> str:
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    _setup(ax, xlabel="Unemployment rate (%)", ylabel="Inflation rate (%)", title=title)
    x = np.linspace(0.5, 9.5, 100)
    y = 8 / x
    ax.plot(x, y, **LINE); ax.text(9.6, y[-1], "SRPC", fontsize=LABEL_FS, va="center")
    return _save(fig, out)


def laffer(out: str, title: str = "Laffer curve") -> str:
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    _setup(ax, xlabel="Tax rate (%)", ylabel="Tax revenue", title=title)
    x = np.linspace(0, 10, 100)
    y = -0.4 * (x - 5) ** 2 + 10
    ax.plot(x, y, **LINE)
    ax.plot([5, 5], [0, 10], **DASH); ax.text(5, -0.4, "t*", ha="center", va="top")
    return _save(fig, out)


def lorenz(out: str, title: str = "Lorenz curve") -> str:
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    _setup(ax, xlabel="Cumulative % of population", ylabel="Cumulative % of income", title=title)
    x = np.linspace(0, 10, 100)
    y = (x / 10) ** 2.2 * 10
    ax.plot([0, 10], [0, 10], color="black", linewidth=1.5, linestyle="--"); ax.text(8.2, 8.8, "Line of equality", fontsize=10)
    ax.plot(x, y, **LINE); ax.text(8.8, 6.0, "Lorenz curve", fontsize=10)
    ax.fill_between(x, x, y, color="#a8d5e2", alpha=0.5)
    return _save(fig, out)


def tariff(out: str, title: str = "Effect of an import tariff") -> str:
    fig, ax = plt.subplots(figsize=(6.5, 4.5))
    _setup(ax, title=title)
    x = np.linspace(0.5, 9.5, 60)
    D = 9 - 0.6 * x; S = 1 + 0.6 * x
    ax.plot(x, D, **LINE); ax.text(9.6, D[-1], "D", fontsize=LABEL_FS, va="center")
    ax.plot(x, S, **LINE); ax.text(9.6, S[-1], "S", fontsize=LABEL_FS, va="center")
    Pw, Pt = 3, 4.5
    ax.axhline(Pw, color="blue", linewidth=2); ax.text(9.6, Pw + 0.1, "P_world", color="blue", fontsize=LABEL_FS, va="center")
    ax.axhline(Pt, color=ACCENT, linewidth=2); ax.text(9.6, Pt + 0.1, "P_world+tariff", color=ACCENT, fontsize=LABEL_FS, va="center")
    # Quantities
    Qd_w = (9 - Pw) / 0.6; Qs_w = (Pw - 1) / 0.6
    Qd_t = (9 - Pt) / 0.6; Qs_t = (Pt - 1) / 0.6
    for q, lbl in [(Qs_w, "Q_s"), (Qd_w, "Q_d"), (Qs_t, "Q_s'"), (Qd_t, "Q_d'")]:
        ax.plot([q, q], [0, 0.2], color="black")
        ax.text(q, -0.4, lbl, ha="center", va="top", fontsize=9)
    return _save(fig, out)


def exchange_rate(out: str, title: str = "Exchange rate determination (floating)") -> str:
    fig, ax = plt.subplots(figsize=(6, 4.5))
    _setup(ax, xlabel="Quantity of currency", ylabel="Exchange rate (price)", title=title)
    x = np.linspace(0.5, 9.5, 60)
    D = 9 - 0.8 * x; S = 1 + 0.8 * x
    ax.plot(x, D, **LINE); ax.text(9.6, D[-1], "D (£)", fontsize=LABEL_FS, va="center")
    ax.plot(x, S, **LINE); ax.text(9.6, S[-1], "S (£)", fontsize=LABEL_FS, va="center")
    _drop(ax, 5, 5, "Q*", "e*")
    return _save(fig, out)


def kinked_demand(out: str, title: str = "Kinked demand (oligopoly)") -> str:
    fig, ax = plt.subplots(figsize=(6, 4.5))
    _setup(ax, xlabel="Output (Q)", ylabel="Price", title=title)
    x1 = np.linspace(0.5, 5, 60); x2 = np.linspace(5, 9.5, 60)
    # elastic above kink
    ax.plot(x1, 8 - 0.4 * x1, **LINE)
    # inelastic below kink
    ax.plot(x2, 7 - 0.2 * x2, **LINE)
    ax.plot([5], [6], "ko"); ax.text(5.1, 6.2, "Kink at P*", fontsize=10)
    ax.text(9.6, 5.1, "D", fontsize=LABEL_FS, va="center")
    # MR with gap
    mr1 = np.linspace(0.5, 5, 60); ax.plot(mr1, 8 - 0.8 * mr1, color="grey", linewidth=1.5, linestyle="--")
    mr2 = np.linspace(5, 9.5, 60); ax.plot(mr2, 5 - 0.4 * mr2, color="grey", linewidth=1.5, linestyle="--")
    ax.text(9.6, 1.2, "MR", color="grey", fontsize=LABEL_FS, va="center")
    return _save(fig, out)


def indifference_budget(out: str, title: str = "Indifference curves & budget line") -> str:
    fig, ax = plt.subplots(figsize=(5.8, 4.5))
    _setup(ax, xlabel="Good X", ylabel="Good Y", title=title)
    x = np.linspace(0.5, 9, 200)
    # Two indifference curves (U2 > U1)
    ax.plot(x, 12 / x, color="black", linewidth=1.8); ax.text(9.1, 12 / 9, "U₁", fontsize=LABEL_FS, va="center")
    ax.plot(x, 25 / x, color="black", linewidth=1.8); ax.text(9.1, 25 / 9, "U₂", fontsize=LABEL_FS, va="center")
    # Budget line
    ax.plot([0, 9], [9, 0], color="blue", linewidth=2); ax.text(7.3, 2.2, "Budget line", color="blue", fontsize=10)
    # Tangent (optimum) on U1: 12/x = 9 - x -> x^2 - 9x + 12 = 0 -> x = (9 - sqrt(33))/2 ~ 1.63 — instead use U1 tangent: x*y=12 and y=9-x, tangency where d/dx(12/x)=-1 => -12/x^2=-1 => x=sqrt(12)~3.46
    import math
    xs = math.sqrt(12); ys = 12 / xs
    ax.plot([xs], [ys], "ko"); ax.text(xs + 0.2, ys + 0.2, "Optimum", fontsize=10)
    return _save(fig, out)


def money_market(out: str, title: str = "Money market") -> str:
    fig, ax = plt.subplots(figsize=(5.8, 4.5))
    _setup(ax, xlabel="Quantity of money", ylabel="Interest rate (r)", title=title)
    x = np.linspace(0.5, 9.5, 60)
    MD = 9 - 0.8 * x
    ax.plot(x, MD, **LINE); ax.text(9.6, MD[-1], "MD", fontsize=LABEL_FS, va="center")
    ax.axvline(5, color="black", linewidth=2); ax.text(5.1, 9.5, "MS", fontsize=LABEL_FS)
    _drop(ax, 5, 5, "M*", "r*")
    return _save(fig, out)


# ----- Registry -------------------------------------------------------------
# Map of diagram_id -> (function, default_kwargs). The build_deck.py script
# resolves diagram_id strings from the JSON spec to functions here.

def demand_curve(out: str, title: str = "The demand curve") -> str:
    """A single downward-sloping demand curve (for the D intro slide)."""
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    _setup(ax, title=title)
    x = np.linspace(0.5, 9.5, 50)
    D = 9 - 0.8 * x
    ax.plot(x, D, **LINE)
    ax.text(9.6, D[-1], "D", fontsize=LABEL_FS, va="center")
    ax.annotate("Lower price →\nmore demanded", xy=(7.2, 9 - 0.8 * 7.2),
                xytext=(3.1, 7.6), fontsize=9, color="grey",
                arrowprops=dict(arrowstyle="->", color="grey"))
    return _save(fig, out)


def supply_curve(out: str, title: str = "The supply curve") -> str:
    """A single upward-sloping supply curve (for the S intro slide)."""
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    _setup(ax, title=title)
    x = np.linspace(0.5, 9.5, 50)
    S = 1 + 0.8 * x
    ax.plot(x, S, **LINE)
    ax.text(9.6, S[-1], "S", fontsize=LABEL_FS, va="center")
    ax.annotate("Higher price →\nmore supplied", xy=(7.2, 1 + 0.8 * 7.2),
                xytext=(1.3, 8.4), fontsize=9, color="grey",
                arrowprops=dict(arrowstyle="->", color="grey"))
    return _save(fig, out)


def demand_movement(out: str, title: str = "Movement along the demand curve") -> str:
    """A change in the good's OWN price → movement ALONG D (not a shift).
    Pair with demand_supply_demand_right to contrast movement vs shift."""
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    _setup(ax, title=title)
    x = np.linspace(0.5, 9.5, 50)
    D = 9 - 0.8 * x
    ax.plot(x, D, **LINE)
    ax.text(9.6, D[-1], "D", fontsize=LABEL_FS, va="center")
    ax0, p0 = 3.75, 6.0     # point A: high price, low quantity
    bx, p1 = 6.25, 4.0      # point B: low price, high quantity
    ax.plot(ax0, p0, "o", color=INK); ax.plot(bx, p1, "o", color=INK)
    _drop(ax, ax0, p0, "Q", "P")
    _drop(ax, bx, p1, "Q₁", "P₁")
    ax.annotate("", xy=(bx, p1), xytext=(ax0, p0),
                arrowprops=dict(arrowstyle="->", color=ACCENT, lw=2,
                                connectionstyle="arc3,rad=-0.2"))
    ax.text(ax0 - 0.15, p0 + 0.35, "A", fontsize=11)
    ax.text(bx + 0.2, p1, "B", fontsize=11)
    ax.text(5.7, 5.5, "movement\nalong D", color=ACCENT, fontsize=10, ha="center")
    return _save(fig, out)


REGISTRY = {
    "demand_supply": (demand_supply, {}),
    "demand_curve": (demand_curve, {}),
    "supply_curve": (supply_curve, {}),
    "demand_movement": (demand_movement, {}),
    "demand_supply_demand_right": (demand_supply, {"shift": "demand_right"}),
    "demand_supply_demand_left": (demand_supply, {"shift": "demand_left"}),
    "demand_supply_supply_right": (demand_supply, {"shift": "supply_right"}),
    "demand_supply_supply_left": (demand_supply, {"shift": "supply_left"}),
    "ppc": (ppc, {}),
    "ppc_outward": (ppc, {"shift": "outward"}),
    "ppc_inward": (ppc, {"shift": "inward"}),
    "elasticity_elastic": (elasticity, {"kind": "elastic"}),
    "elasticity_inelastic": (elasticity, {"kind": "inelastic"}),
    "elasticity_unit": (elasticity, {"kind": "unit"}),
    "elasticity_perfectly_elastic": (elasticity, {"kind": "perfectly_elastic"}),
    "elasticity_perfectly_inelastic": (elasticity, {"kind": "perfectly_inelastic"}),
    "surplus": (surplus, {}),
    "indirect_tax": (indirect_tax, {}),
    "subsidy": (subsidy, {}),
    "price_ceiling": (price_control, {"kind": "ceiling"}),
    "price_floor": (price_control, {"kind": "floor"}),
    "externality_neg_prod": (externality, {"kind": "negative_production"}),
    "externality_pos_prod": (externality, {"kind": "positive_production"}),
    "externality_neg_cons": (externality, {"kind": "negative_consumption"}),
    "externality_pos_cons": (externality, {"kind": "positive_consumption"}),
    "cost_curves_sr": (cost_curves_sr, {}),
    "lrac": (lrac, {}),
    "perfect_competition": (perfect_competition, {}),
    "monopoly": (monopoly, {}),
    "ad_as": (ad_as, {}),
    "ad_as_ad_right": (ad_as, {"shift": "ad_right"}),
    "ad_as_ad_left": (ad_as, {"shift": "ad_left"}),
    "ad_as_sras_right": (ad_as, {"shift": "sras_right"}),
    "ad_as_sras_left": (ad_as, {"shift": "sras_left"}),
    "circular_flow": (circular_flow, {}),
    "phillips": (phillips, {}),
    "laffer": (laffer, {}),
    "lorenz": (lorenz, {}),
    "tariff": (tariff, {}),
    "exchange_rate": (exchange_rate, {}),
    "kinked_demand": (kinked_demand, {}),
    "indifference_budget": (indifference_budget, {}),
    "money_market": (money_market, {}),
}


def render(diagram_id: str, out: str, title: str | None = None) -> str:
    if diagram_id not in REGISTRY:
        raise KeyError(f"Unknown diagram_id: {diagram_id}. Known: {sorted(REGISTRY)}")
    fn, kwargs = REGISTRY[diagram_id]
    kwargs = dict(kwargs)
    if title:
        kwargs["title"] = title
    return fn(out=out, **kwargs)


if __name__ == "__main__":
    # Smoke test: render every diagram into ./_smoke/
    import sys, traceback
    outdir = sys.argv[1] if len(sys.argv) > 1 else "_smoke"
    os.makedirs(outdir, exist_ok=True)
    failures = []
    for did in REGISTRY:
        try:
            render(did, os.path.join(outdir, f"{did}.png"))
            print(f"ok  {did}")
        except Exception as e:
            failures.append((did, e))
            print(f"FAIL {did}: {e}")
            traceback.print_exc()
    if failures:
        sys.exit(1)

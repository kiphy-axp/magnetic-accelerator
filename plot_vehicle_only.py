"""
IYPT 2026 Problem 8 — Vehicle-Only 3D Isometric Diagram
Two disc magnets + rigid axle. Clean academic style.
"""

import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# ── Style ─────────────────────────────────────────────────────
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial Unicode MS', 'PingFang SC', 'Heiti SC', 'STHeiti', 'Arial'],
    'font.size': 9, 'axes.titlesize': 12, 'axes.labelsize': 10,
    'figure.dpi': 200,
})

# ── Geometry (mm) ─────────────────────────────────────────────
R   = 10.0    # disc radius
T   = 5.0     # disc half-thickness (along y)
GAP = 40.0    # axle length (inner gap between discs)
AXL_R = 2.5   # axle radius

# Derived positions
yL = -GAP/2 - T    # left disc centre y
yR = +GAP/2 + T    # right disc centre y
axle_y0 = yL + T   # axle starts at inner face of left disc
axle_y1 = yR - T   # axle ends at inner face of right disc

# Colors
C_DISC      = '#E8953B'
C_DISC_EDGE = '#B8732A'
C_AXLE      = '#6E7681'
C_AXLE_EDGE = '#4A4E54'
C_MARK      = '#FFFFFF'

# ── Helpers ────────────────────────────────────────────────────
def cyl_faces_y(cx, cy, cz, r, half_len, n=48):
    """Cylinder along y-axis, centred at (cx,cy,cz)."""
    th = np.linspace(0, 2*np.pi, n, endpoint=False)
    xc = cx + r*np.cos(th)
    zc = cz + r*np.sin(th)
    y0, y1 = cy - half_len, cy + half_len
    faces = []
    # side quads
    for i in range(n):
        j = (i + 1) % n
        faces.append([
            [xc[i], y0, zc[i]], [xc[j], y0, zc[j]],
            [xc[j], y1, zc[j]], [xc[i], y1, zc[i]]])
    # end caps
    for yi in (y0, y1):
        for i in range(n):
            j = (i + 1) % n
            faces.append([[xc[i], yi, zc[i]], [xc[j], yi, zc[j]], [cx, yi, cz]])
    return faces


def draw_cyl_y(ax, cx, cy, cz, r, half_len, color, edgecolor=None, alpha=1.0, n=48):
    faces = cyl_faces_y(cx, cy, cz, r, half_len, n)
    if edgecolor is None:
        edgecolor = color
    pc = Poly3DCollection(faces, facecolor=color, edgecolor=edgecolor,
                          linewidths=0.25, alpha=alpha, zsort='average')
    ax.add_collection3d(pc)
    return pc


def arrow3d(ax, s, d, L, color='#333', lw=1.5, hs=0.6):
    """Simple 3D arrow: line + cone."""
    e = s + d * L
    ax.plot3D([s[0], e[0]], [s[1], e[1]], [s[2], e[2]], color=color, lw=lw)
    # perpendiculars
    p1 = np.array([-d[1], d[0], 0.])
    if np.linalg.norm(p1) < 1e-9:
        p1 = np.array([0., -d[2], d[1]])
    p1 /= np.linalg.norm(p1)
    p2 = np.cross(d, p1)
    cr, ch = hs*0.3, hs
    base = e - d*ch
    for i in range(12):
        a1, a2 = 2*np.pi*i/12, 2*np.pi*(i+1)/12
        v0 = base + cr*(np.cos(a1)*p1 + np.sin(a1)*p2)
        v1 = base + cr*(np.cos(a2)*p1 + np.sin(a2)*p2)
        tri = [v0.tolist(), v1.tolist(), e.tolist()]
        ax.add_collection3d(Poly3DCollection(
            [tri], facecolor=color, edgecolor=None, alpha=0.9, zsort='average'))


# ── Figure ────────────────────────────────────────────────────
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# ── Axle ──────────────────────────────────────────────────────
draw_cyl_y(ax, 0, (axle_y0 + axle_y1)/2, 0, AXL_R, (axle_y1 - axle_y0)/2,
           C_AXLE)

# ── Left disc ─────────────────────────────────────────────────
draw_cyl_y(ax, 0, yL, 0, R, T, C_DISC, edgecolor=C_DISC_EDGE)
# face highlight ring
for sign in [-1, +1]:
    ring = []
    for a in np.linspace(0, 2*np.pi, 72):
        ring.append([R*np.cos(a), yL + sign*T, R*np.sin(a)])
    xs, ys, zs = zip(*ring)
    ax.plot(xs, ys, zs, color=C_DISC_EDGE, lw=0.5, alpha=0.6)

# ── Right disc ────────────────────────────────────────────────
draw_cyl_y(ax, 0, yR, 0, R, T, C_DISC, edgecolor=C_DISC_EDGE)
for sign in [-1, +1]:
    ring = []
    for a in np.linspace(0, 2*np.pi, 72):
        ring.append([R*np.cos(a), yR + sign*T, R*np.sin(a)])
    xs, ys, zs = zip(*ring)
    ax.plot(xs, ys, zs, color=C_DISC_EDGE, lw=0.5, alpha=0.6)

# ── Magnetization arrows (radial, on outer faces) ─────────────
arr_len = R * 0.65
for y_sign, yc in [(-1, yL), (+1, yR)]:
    arrow3d(ax, np.array([0., yc + y_sign*T, 0.]),
            np.array([0.707, 0., 0.707]), arr_len,
            color='#CC3333', lw=1.8, hs=1.8)

# ── Axle center axis (dashed) ─────────────────────────────────
ax.plot([0, 0], [yL - T - 4, yR + T + 4], [0, 0],
        color=C_AXLE_EDGE, lw=0.8, ls='--', alpha=0.5)

# ── Dimension annotations ─────────────────────────────────────
# Disc radius (vertical dimension on right disc)
dz = 10
ax.plot([0, 0], [yR + T + 3, yR + T + 3], [0, R], color='#555555', lw=0.8)
ax.plot([0, 0], [yR + T + 1, yR + T + 5], [0, 0], color='#555555', lw=0.8)
ax.plot([0, 0], [yR + T + 1, yR + T + 5], [R, R], color='#555555', lw=0.8)
ax.text(2, yR + T + 4, R/2, 'rd', fontsize=8, color='#555555', ha='left', va='center')

# Disc thickness
ax.plot([0, 0], [yR - T, yR + T], [-R - 4, -R - 4], color='#555555', lw=0.8)
ax.plot([0, 0], [yR - T, yR - T], [-R - 6, -R - 2], color='#555555', lw=0.8)
ax.plot([0, 0], [yR + T, yR + T], [-R - 6, -R - 2], color='#555555', lw=0.8)
ax.text(2, yR, -R - 6, 'td', fontsize=8, color='#555555', ha='left', va='top')

# Axle length (between inner faces)
ax.plot([0, 0], [axle_y0, axle_y1], [-R - 4, -R - 4], color='#555555', lw=0.8)
ax.text(2, (axle_y0+axle_y1)/2, -R - 5, 'Laxle', fontsize=8, color='#555555', ha='left', va='top')

# ── Labels ────────────────────────────────────────────────────
ax.text(0, yL, R + 4, '盘状磁体\n(Magnetic Disc)', fontsize=7.5, ha='center',
        color=C_DISC_EDGE, fontstyle='italic')
ax.text(0, yR, R + 4, '盘状磁体\n(Magnetic Disc)', fontsize=7.5, ha='center',
        color=C_DISC_EDGE, fontstyle='italic')
ax.text(0, (yL + yR)/2, AXL_R + 3, '刚性轴\n(Axle)', fontsize=7.5, ha='center',
        color=C_AXLE_EDGE, fontstyle='italic')

# Pole markers (N/S labels on disc faces)
for y_sign, yc in [(+1, yL), (-1, yR)]:
    ax.text(R*0.45, yc + y_sign*(T+1.2), R*0.45, 'N', fontsize=8,
            fontweight='bold', color='#CC3333', ha='center', va='center')
    ax.text(-R*0.45, yc - y_sign*(T+1.2), -R*0.45, 'S', fontsize=8,
            fontweight='bold', color='#3366CC', ha='center', va='center')

# ── Coordinate axes ───────────────────────────────────────────
org = np.array([-R-8, yL-T-10, -R-6])
al = 18
arrow3d(ax, org, np.array([1,0,0]), al, '#D64545', lw=1.6, hs=2.2)
arrow3d(ax, org, np.array([0,1,0]), al, '#3A8C5C', lw=1.6, hs=2.2)
arrow3d(ax, org, np.array([0,0,1]), al, '#4A7FB5', lw=1.6, hs=2.2)
ax.text(org[0]+al+3, org[1], org[2], 'x', fontsize=11, fontweight='bold',
        color='#D64545', ha='center')
ax.text(org[0], org[1]+al+3, org[2], 'y', fontsize=11, fontweight='bold',
        color='#3A8C5C', ha='center')
ax.text(org[0], org[1], org[2]+al+3, 'z', fontsize=11, fontweight='bold',
        color='#4A7FB5', ha='center')

# ── View ──────────────────────────────────────────────────────
ax.view_init(elev=22, azim=-55)
pad = 12
ax.set_xlim(-R-pad, R+pad)
ax.set_ylim(yL-T-pad, yR+T+pad)
ax.set_zlim(-R-pad, R+pad)

ax.set_xlabel('x', fontsize=11, labelpad=6)
ax.set_ylabel('y', fontsize=11, labelpad=6)
ax.set_zlabel('z', fontsize=11, labelpad=6)

ax.xaxis.pane.fill = False; ax.xaxis.pane.set_edgecolor('#DDDDDD')
ax.yaxis.pane.fill = False; ax.yaxis.pane.set_edgecolor('#DDDDDD')
ax.zaxis.pane.fill = False; ax.zaxis.pane.set_edgecolor('#DDDDDD')
ax.grid(True, alpha=0.2, lw=0.3)
ax.set_box_aspect([2*R+2*pad, (yR+T+pad)-(yL-T-pad), 2*R+2*pad])

ax.set_title(
    'IYPT 2026 Problem 8 — Vehicle: Two Magnetic Discs on a Rigid Axle\n'
    '两根盘状磁体 + 刚性轴车辆三维轴测图',
    fontsize=12, fontweight='bold', pad=16, color='#2D3339')

# ── Legend ────────────────────────────────────────────────────
import matplotlib.patches as mp
legend_elements = [
    mp.Patch(facecolor=C_DISC, edgecolor=C_DISC_EDGE, label='盘状磁体 (Magnetic Disc)'),
    mp.Patch(facecolor=C_AXLE, edgecolor=C_AXLE_EDGE, label='刚性轴 (Rigid Axle)'),
]
ax.legend(handles=legend_elements, loc='upper right', fontsize=7.5,
          framealpha=0.9, edgecolor='#CCCCCC',
          bbox_to_anchor=(1.05, 0.98))

# ── Save ──────────────────────────────────────────────────────
import os
out_png = '/Users/jiaoyixuan/Desktop/vs_code/磁力加速器/figures/vehicle_only_isometric.png'
out_pdf = out_png.replace('.png', '.pdf')
os.makedirs(os.path.dirname(out_png), exist_ok=True)
fig.tight_layout()
fig.savefig(out_png, dpi=250, bbox_inches='tight', facecolor='white', edgecolor='none')
fig.savefig(out_pdf, format='pdf', bbox_inches='tight', facecolor='white', edgecolor='none')
print(f'✓ {out_png}')
print(f'✓ {out_pdf}')

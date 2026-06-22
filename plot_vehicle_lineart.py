"""
Vehicle-only clean line-art isometric — no axes, no text.
Academic technical-drawing style.
"""

import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

plt.rcParams.update({'figure.dpi': 200})

# ── Geometry ──────────────────────────────────────────────────
R   = 10.0    # disc radius
T   = 5.0     # disc half-thickness (y)
GAP = 40.0    # inner gap
AXL = 2.5     # axle radius

yL = -GAP/2 - T
yR = +GAP/2 + T
ay0 = yL + T
ay1 = yR - T

# ── Technical-drawing palette ─────────────────────────────────
WHITE     = '#FAFAFA'
LINE_DISC = '#3A3A3A'
LINE_AXLE = '#555555'
FILL_DISC = '#F5EDE3'
FILL_AXLE = '#EAEAEA'
HATCH     = '#D8D0C4'

# ── Cylinder helper ───────────────────────────────────────────
def cyl_faces_y(cx, cy, cz, r, hl, n=64):
    th = np.linspace(0, 2*np.pi, n, endpoint=False)
    xc = cx + r*np.cos(th); zc = cz + r*np.sin(th)
    y0, y1 = cy - hl, cy + hl
    faces = []
    for i in range(n):
        j = (i+1)%n
        faces.append([[xc[i],y0,zc[i]],[xc[j],y0,zc[j]],
                      [xc[j],y1,zc[j]],[xc[i],y1,zc[i]]])
    for yi in (y0, y1):
        for i in range(n):
            j = (i+1)%n
            faces.append([[xc[i],yi,zc[i]],[xc[j],yi,zc[j]],[cx,yi,cz]])
    return faces

def draw_cyl(ax, cx, cy, cz, r, hl, fc, ec, lw=0.4, n=64, za=1.0):
    f = cyl_faces_y(cx, cy, cz, r, hl, n)
    pc = Poly3DCollection(f, facecolor=fc, edgecolor=ec,
                          linewidths=lw, alpha=za, zsort='average')
    ax.add_collection3d(pc)

# ── Cross-hatch lines for disc faces ──────────────────────────
def hatch_disc_face(ax, cx, cy, cz, r, n_lines=7):
    """Subtle radial hatching on disc end faces."""
    for yi in [cy - T, cy + T]:
        for i in range(1, n_lines):
            frac = i / (n_lines + 1)
            rr = r * 0.25 + r * 0.7 * frac
            ring = []
            for a in np.linspace(0, 2*np.pi, 80):
                ring.append([cx + rr*np.cos(a), yi, cz + rr*np.sin(a)])
            xs, ys, zs = zip(*ring)
            ax.plot(xs, ys, zs, color=HATCH, lw=0.2, alpha=0.5)

# ── Figure ────────────────────────────────────────────────────
fig = plt.figure(figsize=(10, 8), facecolor='white')
ax = fig.add_subplot(111, projection='3d')

# Axle
draw_cyl(ax, 0, (ay0+ay1)/2, 0, AXL, (ay1-ay0)/2, FILL_AXLE, LINE_AXLE, lw=0.35)

# Left disc
draw_cyl(ax, 0, yL, 0, R, T, FILL_DISC, LINE_DISC, lw=0.45)
hatch_disc_face(ax, 0, yL, 0, R)

# Right disc
draw_cyl(ax, 0, yR, 0, R, T, FILL_DISC, LINE_DISC, lw=0.45)
hatch_disc_face(ax, 0, yR, 0, R)

# ── Hidden-line axle through disc (dashed) ────────────────────
ax.plot([0, 0], [yL - T, yR + T], [0, 0],
        color=LINE_AXLE, lw=0.5, ls=(0, (3, 2)), alpha=0.35, zorder=0)

# ── Clean view ────────────────────────────────────────────────
ax.view_init(elev=24, azim=-52)
m = 14
ax.set_xlim(-R-m, R+m)
ax.set_ylim(yL-T-m, yR+T+m)
ax.set_zlim(-R-m, R+m)

ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
ax.xaxis.pane.fill = False; ax.yaxis.pane.fill = False; ax.zaxis.pane.fill = False
ax.xaxis.pane.set_edgecolor('none')
ax.yaxis.pane.set_edgecolor('none')
ax.zaxis.pane.set_edgecolor('none')
ax.grid(False)
ax.set_axis_off()
ax.set_box_aspect([2*R+2*m, (yR+T+m)-(yL-T-m), 2*R+2*m])

# ── Save ──────────────────────────────────────────────────────
import os
p = '/Users/jiaoyixuan/Desktop/vs_code/磁力加速器/figures/vehicle_lineart_isometric.png'
os.makedirs(os.path.dirname(p), exist_ok=True)
fig.tight_layout(pad=0)
fig.savefig(p, dpi=300, bbox_inches='tight', facecolor='white', edgecolor='none')
fig.savefig(p.replace('.png', '.pdf'), format='pdf', bbox_inches='tight',
            facecolor='white', edgecolor='none')
print(f'✓ {p}')
print(f'✓ {p.replace(".png", ".pdf")}')

import matplotlib.pyplot as plt
import numpy.random as rnd
from matplotlib.patches import Ellipse
from matplotlib.pyplot import scatter
import numpy as np

NUM = 250
path = 'D://Work//ecg//pyecgdel//Data//shiller//record_2321//lead_i//rr_ellipse_pca.txt'
ellipse = np.loadtxt(path)
ellipse.tolist()

e = Ellipse(xy=[ellipse[0], ellipse[1]], width=ellipse[2], height=ellipse[3], angle=ellipse[4])

fig = plt.figure(0)
ax = fig.add_subplot(111, aspect='equal')
ax.add_artist(e)
e.set_clip_box(ax.bbox)
e.set_alpha(rnd.rand())
e.set_facecolor(rnd.rand(3))

ax.set_xlim(0, 2)
ax.set_ylim(0, 2)

path = 'D://Work//ecg//pyecgdel//Data//shiller//record_2321//lead_i//rr_dist.txt'
rr_dist = np.loadtxt(path)
rr_dist.tolist()
x = rr_dist[:-1]
y = rr_dist[1:]

sc = scatter(x, y)


plt.show()
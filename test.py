import numpy as np
from PIL import Image

FNAME = '/home/default/Downloads/QRMallikarjun Konakamurthy.png'
img = Image.open(FNAME).convert('RGBA')
x = np.array(img)
r, g, b, a = np.rollaxis(x, axis=-1)
r[a == 0] = 255
g[a == 0] = 255
b[a == 0] = 255
x = np.dstack([r, g, b, a])
img = Image.fromarray(x, 'RGB')
img.save('/home/default/Desktop/QRMallikarjun Konakamurthy.jpeg')


from __future__ import print_function, division

from vecutils import * # téléchargez vecutils ici

vertices = farray([
    -0.5, 0.0, 0, 1.0,
    0.0, 0.5, 0, 1.0,
    0.5, 0.0, 0, 1.0,

    0.0, 0.0, 0, 1.0,
    0.25, 0.0, 0, 1.0,
    0.25, -0.6, 0, 1.0,

    0.0, 0.0, 0, 1.0,
    -0.25, 0.0, 0, 1.0,
    -0.25, -0.6, 0, 1.0,

    0.0, 0.0, 0, 1.0,
    0.25, -0.6, 0, 1.0,
    -0.25, -0.6, 0, 1.0,
])

taille = len(vertices)
print(taille//4)

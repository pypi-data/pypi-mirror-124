#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2021 CORIA
"""pyBOS demonstration script.

This script is not intented to only be useful for pedagogical purposes.
It is not either a lecture about BOS but only a demonstration
of what can be done with the library pyBOS.
"""


# First we import packages that we'll use later.
from pathlib import Path

import matplotlib.pyplot as plt
import xarray as xr

# Then we import stuff fron the pyBOS library
from pybos.extraction import idz2n
from pybos.laplacian import solve_BOS
from pybos.physical_laws import polynomial
from pybos.reader import DANTEC_DAT, reader
from pybos.vector_calculus import amplitude, divergence

# We define some of the parameter that we'll need later

fig_show = 1  # plot only the temperature
# fig_show = 2 # plot the temperature and U, V, norm and the divergence
# fig_show = 3 # plot all

reverse = True  # if reference image and final image are reversed (should not happen !)
crop = True
filt_method = "gaussian"

"################################### READING THE DATA #############################################"
# We use the `reader` function to read the data.
# It must be a `.csv` type file (including dome of the tecplot's `.plt.` files)
#
# If possible prefer using the calibration from Dantec/Davis and avoid importing data in pixel.
im_datafile = Path("data/example_data_2d.dat")
cols = 2, 3, 6, 7  # pix for now
scale = 1 / (2560 * ((283 - 26) / 319) / 384)  # pix to mm

data = reader(im_datafile, DANTEC_DAT, usecols=cols, scale=scale, unit="mm")
if reverse:
    data["U"] *= -1
    data["V"] *= -1

if fig_show >= 3:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 3))
    data.U.plot.pcolormesh(ax=ax1, cmap=plt.cm.jet)
    data.V.plot.pcolormesh(ax=ax2, cmap=plt.cm.jet)
    ax1.axis("equal")
    ax2.axis("equal")
    fig.tight_layout()
    plt.show()

"################################## PREPARING THE DATA ############################################"
# You may want to crop the data to remove reflection and other defects.
# Here we are only using the `isel` method of `Xarray`'s `Dataset`.
roi = {"x": slice(None, None), "y": slice(None, None)}
if crop:
    pix1, piy1 = 244, 117
    pix2, piy2 = 2321, 2012
    Pix_size = 8

    pix1 = int((pix1 - Pix_size + 0.5) / Pix_size)
    pix2 = int((pix2 - Pix_size + 0.5) / Pix_size)
    piy1 = int((piy1 - Pix_size + 0.5) / Pix_size)
    piy2 = int((piy2 - Pix_size + 0.5) / Pix_size)

    piy1, piy2 = data.dims["y"] - piy2, data.dims["y"] - piy1

    roi = {"x": slice(pix1, pix2), "y": slice(piy1, piy2)}
cropped_data = data.isel(roi)  # type: ignore

if fig_show >= 3:
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 3))
    data.U.plot.pcolormesh(ax=ax1, cmap=plt.cm.jet)
    (cropped_data.U * 0.0).plot.pcolormesh(ax=ax1, alpha=0.5, add_colorbar=False)
    data.V.plot.pcolormesh(ax=ax2, cmap=plt.cm.jet)
    (cropped_data.V * 0.0).plot.pcolormesh(ax=ax2, alpha=0.5, add_colorbar=False)
    ax1.axis("equal")
    ax2.axis("equal")
    fig.tight_layout()
    plt.show()

# You may also want to filter the data. Here we are only using standard filter from `scipy`.
# In order to keep the `Xarray`'s `Dataset` data format, we use the `apply_ufunc` wrapper.
if filt_method == "gaussian":
    from scipy.ndimage import gaussian_filter

    sigma = 2, 2

    def filter_(x: float) -> float:
        """Apply a gaussian filter."""
        return gaussian_filter(x, sigma=sigma, order=0, mode="nearest")


elif filt_method == "spline":
    from scipy.signal import spline_filter

    lmbda = 2

    def filter_(x: float) -> float:
        """Apply a spline filter."""
        return spline_filter(x, lmbda=lmbda)


filtered_data = xr.apply_ufunc(filter_, cropped_data, keep_attrs=True)

# There is a function for computing the displacement's amplitude and divergence.
filtered_data["divergence"] = divergence(filtered_data)
print(f"mean(divergence)={float(filtered_data.divergence.mean())}")

if fig_show >= 2:
    filtered_data["amplitude"] = amplitude(filtered_data)

    fig, axs = plt.subplots(2, 2, figsize=(9, 9))
    filtered_data.U.plot.pcolormesh(ax=axs[0][0], cmap=plt.cm.jet)
    filtered_data.V.plot.pcolormesh(ax=axs[0][1], cmap=plt.cm.jet)
    filtered_data.amplitude.plot.pcolormesh(ax=axs[1][0], cmap=plt.cm.jet)
    filtered_data.divergence.plot.pcolormesh(ax=axs[1][1], cmap=plt.cm.jet)

    for axx in axs:
        for axy in axx:
            axy.axis("equal")
    fig.tight_layout()
    plt.show()

"######################################## Resolution ##############################################"
# Now we define the properties of the experiment (size of the tank, boundary conditions)
# and the physical law for converting refracting index to to temperature and conversely.

d = 190  # for cube # 0.003 for aquarium # [mm] pattern-tank distance
w = 400  # [mm] tank width "h" in [Plakina et al 2012]
n0 = 1.00027  # [] refractive index of the air

n_T, T_n = polynomial()

T_left = 7.5
T_right = 39.5

idz_top = idz_bottom = None
idz_left = n_T(T_left) * w
idz_right = n_T(T_right) * w

# And compute the refractive index

idz = solve_BOS(filtered_data.divergence, w, d, n0, idz_top, idz_bottom, idz_left, idz_right)
res = idz.to_dataset()

# using a 2d hypothesis
res["n"] = idz2n(res.idz, w, method="2d")

if fig_show >= 3:
    fig, ax = plt.subplots()
    res.n.plot.pcolormesh(ax=ax, cmap=plt.cm.jet)
    ax.axis("equal")
    fig.tight_layout()
    plt.show()

# That we can convert to temperature using the aformentionned law
res["T"] = T_n(res.n)

fig, ax = plt.subplots()
res.T.plot.pcolormesh(ax=ax, cmap=plt.cm.jet, vmin=0, vmax=50)
ax.axis("equal")
fig.tight_layout()
fig.savefig("Temperature_2d.png", dpi=200)

if fig_show >= 1:
    plt.show()

# Now it is your turn to use the library ;) !

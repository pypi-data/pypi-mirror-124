#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2021 CORIA

"""Physical laws."""

import xarray as xr


def linear(source: str = "water_reglin", dn_over_dT: float = -1.01e-4):
    """Linear laws for n(T) and T(n).

    for `dn_over_dT`
     * water_reglin: linear regression for water [4-45°C]
     * paraffin_reglin: linear regression for paraffin C18H38
     * Lipkin: Lipkin&Kurtz 61
    """
    # dn/dT = drho/dT * (n0-1)/rho0, K-1 par gladstone-Dale

    if source == "water_reglin":
        dn_over_dT = -1.01e-4
    elif source == "paraffin_reglin":
        dn_over_dT = -3.89e-4
    elif source == "Lipkin":
        dn_over_dT = -6.9e-04 * 0.6
    elif source == "custom":
        pass
    else:
        raise ValueError(f"dn_over_dT {dn_over_dT} unknown")

    def n_T(T):
        n = dn_over_dT * T

        if isinstance(n, xr.DataArray):
            n.name = "n"
            n.attrs["units"] = "dimensionless"
            n.attrs["long_name"] = "Refractive index"
        return n

    def T_n(n):
        T = -n / dn_over_dT

        if isinstance(n, xr.DataArray):
            T.name = "T"
            T.attrs["units"] = "°C"
            T.attrs["long_name"] = "Temperature"
        return T

    return n_T, T_n


def polynomial():
    """Polynomial laws for n(T) and T(n) (2nd order)."""
    a_n, b_n, c_n = -1.4924302650e-6, -2.7825685771e-5, 1.3340392319
    a_T, b_T, c_T = -1.3644133349e6, 3.6249437078e6, -2.4076210909e6

    def n_T(T):
        n = a_n * (T ** 2) + b_n * T + c_n

        if isinstance(n, xr.DataArray):
            n.name = "n"
            n.attrs["units"] = "dimensionless"
            n.attrs["long_name"] = "Refractive index"
        return n

    def T_n(n):
        T = a_T * (n ** 2) + b_T * n + c_T

        if isinstance(n, xr.DataArray):
            T.name = "T"
            T.attrs["units"] = "°C"
            T.attrs["long_name"] = "Temperature"
        return T

    return n_T, T_n


def gladstone_dale(n: xr.DataArray, G: float = 0.000229) -> xr.DataArray:
    """Gladston-Dale relation to convert refractive index to density."""
    density = (n - 1) / G

    density.name = "density"
    density.attrs["units"] = "Kg/m³"
    density.attrs["long_name"] = "Density"
    return density


def ideal_gaz(density: xr.DataArray, p: float, M: float) -> xr.DataArray:
    """Ideal gaz law to convert density to temperature."""
    R = 8.3144621  # [J/K/mol] Arrhenius constant
    T0 = 273.15  # Kelvin to °C

    T = p * M / (density * R) - T0  # pv=nRT

    T.name = "T"
    T.attrs["units"] = "°C"
    T.attrs["long_name"] = "Temperature"

    return T

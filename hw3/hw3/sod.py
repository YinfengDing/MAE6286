"""Module with helper functions for HW3."""

import numpy


def analytical_solution(t, x, left_state, right_state,
                        diaphragm=0.0, gamma=1.4):
    """Compute the analytical solution of the Sod's test at a given time.

    Parameters
    ----------
    t : float
        The time.
    x : numpy.ndarray
        Coordinates along the tube (as a 1D array of floats).
    left_state : tuple or list
        Initial density, velocity, and pressure values
        on left side of the diaphragm.
        The argument should be a tuple or list with 3 floats.
    right_state : tuple or list
        Initial density, velocity, and pressure values
        on right side of the diaphragm.
        The argument should be a tuple or list with 3 floats.
    diaphragm : float, optional
        Location of the diaphgram (membrane), by default 0.0.
    gamma : float, optional
        Heat capacity ratio, by default 1.4.

    Returns
    -------
    tuple of numpy.ndarray objects
        The density, velocity, and pressure along the tube at the given time.
        This is a tuple with 3 elements: (density, velocity, pressure).
        Each element is a 1D NumPy array of floats.

    """
    def speed_of_sound(rho, p, gamma=1.4):
        a = numpy.sqrt(gamma * p / rho)
        return a

    def rarefaction_state(x, t, left_state, gamma=1.4, x0=0.0):
        rhoL, _, pL = left_state
        aL = speed_of_sound(rhoL, pL, gamma=gamma)
        Gamma = (gamma - 1) / (gamma + 1)
        beta = (gamma - 1) / (2 * gamma)
        a = Gamma * (x0 - x) / t + (1 - Gamma) * aL
        v = (1 - Gamma) * (aL - (x0 - x) / t)
        rho = rhoL * (a / aL)**(1 / beta / gamma)
        p = pL * (rho / rhoL)**gamma
        return rho, v, p, a

    # Front of the rarefaction wave.
    rho1, v1, p1 = left_state
    a1 = speed_of_sound(rho1, p1, gamma=gamma)
    # Front of the shock wave.
    rho5, v5, p5 = right_state
    a5 = speed_of_sound(rho5, p5, gamma=gamma)
    # Define some useful parameters.
    Gamma = (gamma - 1) / (gamma + 1)
    beta = (gamma - 1) / (2 * gamma)

    # Iteratively compute the pressure across the discontinuity line.
    tol, maxiter = 1e-1, 1000
    p3, v2, v4, ite = p1, 0.0, 2 * tol, 0
    while abs(v2 - v4) > tol and ite < maxiter:
        ite += 1
        p3 = p3 - 0.5 * (p3 + p5) if (v2 < v4) else p3 + 0.5 * (p3 + p5)
        v4 = (p3 - p5) * numpy.sqrt((1 - Gamma) / (rho5 * (p3 + Gamma * p5)))
        v2 = ((p1**beta - p3**beta) * numpy.sqrt((1 - Gamma**2) *
                                                 p1**(1 / gamma) /
                                                 (Gamma**2 * rho1)))
    if ite == maxiter:
        print('Reached maximum number of iterations ({}): error = {}'
              .format(ite, abs(v2 - v4)))

    # Constant pressure across the contact discontinuity.
    p4 = p3
    # Rankine-Hugoniot jump condition.
    rho4 = rho5 * (p4 + Gamma * p5) / (p5 + Gamma * p4)
    # Velocity in the region just behind the rarefaction wave.
    v3 = v5 + (p3 - p5) / numpy.sqrt(rho5 / 2 * ((gamma + 1) * p3 +
                                                 (gamma - 1) * p5))
    # Constant velocity across the contact discontinuity.
    v4 = v3
    # Adiabatic gas law.
    rho3 = rho1 * (p3 / p1)**(1.0 / gamma)

    # Location of the diaphragm.
    x0 = diaphragm
    # Location of the rarefaction wave head.
    x1 = x0 - a1 * t
    # Location of the rarefaction wave trail.
    x2 = x0 + (v3 / (1 - Gamma) - a1) * t
    # Location of the contact discontinuity.
    x3 = x0 + v3 * t
    # Shock velocity.
    vs = v4 * rho4 / rho5 / (rho4 / rho5 - 1)
    # Location of the shock.
    x4 = x0 + vs * t

    rho = numpy.zeros_like(x)
    v = numpy.zeros_like(x)
    p = numpy.zeros_like(x)
    # Front of rarefaction wave.
    mask = numpy.where(x <= x1)
    rho[mask], v[mask], p[mask] = rho1, v1, p1
    # Rarefaction wave.
    mask = numpy.where(numpy.logical_and(x > x1, x <= x2))
    rho[mask], v[mask], p[mask], _ = rarefaction_state(x[mask], t, (rho1, v1, p1))
    # Behind the rarefaction wave and left of the contact discontinuity.
    mask = numpy.where(numpy.logical_and(x > x2, x <= x3))
    rho[mask], v[mask], p[mask] = rho3, v3, p3
    # Behind the shock and right of the contact discontinuity.
    mask = numpy.where(numpy.logical_and(x > x3, x <= x4))
    rho[mask], v[mask], p[mask] = rho4, v4, p4
    # Front of the shock.
    mask = numpy.where(x > x4)
    rho[mask], v[mask], p[mask] = rho5, v5, p5

    return rho, v, p

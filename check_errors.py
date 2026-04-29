import math


def check_errors(S, K, K1, K2, K3, K4, T, T1, T2, t_a, sigma, q, r) -> True:
    """
    Function to check potential inputs errors.
    """

    if S > 200 or S < 0:
        raise ValueError("The Underlying price must be between 0 and 200")

    for k in [K, K1, K2, K3, K4]:
        if k is not None and not (0 <= k <= 200):
            raise ValueError("Strikes must be between 0 and 200")

    for t in [T, T1, T2]:
        if t is not None and not (t > 0):
            raise ValueError("The Maturity must be greater than 0")

    if t_a is not None:
        if t_a < 0 or T < t_a:
            raise ValueError("t_a must be equal or less than the maturity and greater than 0")

    if sigma <= 0.0:
        raise ValueError("The Volatility must be higher than 0")
    
    if q > 1 or q < 0.0:
        raise ValueError("The Dividend yield must be between 0 and 1")

    if r > 0.895 or r < -0.1:
        raise ValueError("The Risk-free rate must be between -0.1 and 0.9")

    if (K4 is not None) and (K3 is not None) and (K2 is not None) and (K1 is not None):
        if not math.isclose(K4 - K3, K3 - K2, rel_tol=1e-9):
            raise ValueError("All strike prices must be equidistant, so K4 - K3 = K3 - K2 = K2 - K1")

    if (K3 is not None) and (K2 is not None) and (K1 is not None):
        if not math.isclose(K3 - K2, K2 - K1, rel_tol=1e-9):
            raise ValueError("All strike prices must be equidistant, so K3 - K2 = K2 - K1")
    
    if K1 is not None and K2 is not None and K1 >= K2:
        raise ValueError("K2 must be greater than K1")

    if K2 is not None and K3 is not None and K2 >= K3:
        raise ValueError("K3 must be greater than K2")

    if K3 is not None and K4 is not None and K3 >= K4:
        raise ValueError("K4 must be greater than K3")
    
    if T2 is not None and T2 < T1:
        raise ValueError("T2 must be greater than T1")

    return True
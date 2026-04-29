from math import exp, sqrt, log
from scipy.stats import norm
import blackscholes as bs
import math


class OptionWrapper:
    def __init__(self, option, sign = 1 or -1):
        self.option = option
        self.sign = sign
    def vega(self):
        return self.sign * self.option.vega()
    def theta(self):
        return self.sign * self.option.theta()
    def rho(self):
        return self.sign * self.option.rho()
    def delta(self):
        return self.sign * self.option.delta()
    def gamma(self):
        return self.sign * self.option.gamma()

class BlackScholesCallShort(OptionWrapper):
    def __init__(self, S, K, T, sigma, q, r):
        super().__init__(bs.BlackScholesCall(S=S, K=K, T=T, sigma=sigma, q=q, r=r),sign=-1)

class BlackScholesPutShort(OptionWrapper):
    def __init__(self, S, K, T, sigma, q, r):
        super().__init__(bs.BlackScholesPut(S=S, K=K, T=T, sigma=sigma, q=q, r=r),sign=-1)

class BlackScholesBearSpreadShort(OptionWrapper):
    def __init__(self, S, K1, K2, T, sigma, q, r):
        super().__init__(bs.BlackScholesBearSpread(S=S, K1=K2, K2=K1, T=T, sigma=sigma, q=q, r=r),sign=-1)

class BlackScholesBearSpreadLong(OptionWrapper):
    def __init__(self, S, K1, K2, T, sigma, q, r):
        super().__init__(bs.BlackScholesBearSpread(S=S, K1=K2, K2=K1, T=T, sigma=sigma, q=q, r=r),sign=1)

class BlackScholesBullSpreadLong(OptionWrapper):
    def __init__(self, S, K1, K2, T, sigma, q, r):
        super().__init__(bs.BlackScholesBullSpread(S=S, K1=K1, K2=K2, T=T, sigma=sigma, q=q, r=r),sign=1)

class BlackScholesBullSpreadShort(OptionWrapper):
    def __init__(self, S, K1, K2, T, sigma, q, r):
        super().__init__(bs.BlackScholesBullSpread(S=S, K1=K1, K2=K2, T=T, sigma=sigma, q=q, r=r),sign=-1)

class BlackscholesCalendarCallSpreadLong(OptionWrapper):
    def __init__(self, S, K1, K2, T1, T2, sigma, q, r):
        super().__init__(bs.BlackScholesCalendarCallSpread(S=S, K1=K1, K2=K2, T1=T2, T2=T1, sigma=sigma, q=q, r=r),sign=1)

class BlackscholesCalendarCallSpreadShort(OptionWrapper):
    def __init__(self, S, K1, K2, T1, T2, sigma, q, r):
        super().__init__(bs.BlackScholesCalendarCallSpread(S=S, K1=K1, K2=K2, T1=T2, T2=T1, sigma=sigma, q=q, r=r),sign=-1)

class BlackScholesCalendarPutSpreadLong(OptionWrapper):
    def __init__(self, S, K1, K2, T1, T2, sigma, q, r):
        super().__init__(bs.BlackScholesCalendarPutSpread(S=S, K1=K1, K2=K2, T1=T2, T2=T1, sigma=sigma, q=q, r=r),sign=1)

class BlackScholesCalendarPutSpreadShort(OptionWrapper):
    def __init__(self, S, K1, K2, T1, T2, sigma, q, r):
        super().__init__(bs.BlackScholesCalendarPutSpread(S=S, K1=K1, K2=K2, T1=T2, T2=T1, sigma=sigma, q=q, r=r),sign=-1)

class BinaryCall():
    def __init__(self, S: float, K1: float, T1: float, r: float, sigma: float):
        self.S, self.K, self.T, self.r, self.sigma = S, K1, T1, r, sigma
        self.d1 = (1.0 / (self.sigma * sqrt(self.T))) * (log(self.S / self.K) + (self.r + 0.5 * self.sigma**2) * self.T)
        self.d2 = self.d1 - self.sigma * sqrt(self.T)

    def price(self) -> float:
        return exp(-self.r * self.T) * norm.cdf(self.d2)

    def delta(self) -> float:
        return exp(-self.r * self.T) * norm.pdf(self.d2) / (self.S * self.sigma * sqrt(self.T))
    
    def vega(self) -> float:
        return -exp(-self.r * self.T) * norm.pdf(self.d2) * self.d1 / self.sigma
    
    def rho(self) -> float:
        return -self.T * exp(-self.r * self.T) * norm.cdf(self.d2)
    
    def gamma(self) -> float:
        return -exp(-self.r * self.T) * norm.pdf(self.d2) * self.d2 / (self.S**2 * self.sigma**2 * self.T)
    
    def theta(self) -> float:
        term1 = -self.r * exp(-self.r * self.T) * norm.cdf(self.d2)
        term2 = exp(-self.r * self.T) * norm.pdf(self.d2) * ((log(self.S / self.K) / (2 * self.sigma * self.T**1.5))
            - (self.r / (self.sigma * sqrt(self.T)))- (self.sigma / (2 * sqrt(self.T))))
        return term1 + term2

class BinaryPut():
    def __init__(self, S: float, K1: float, T1: float, r: float, sigma: float):
        self.S, self.K, self.T, self.r, self.sigma = S, K1, T1, r, sigma
        self.d1 = (1.0 / (self.sigma * sqrt(self.T))) * (log(self.S / self.K) + (self.r + 0.5 * self.sigma**2) * self.T)
        self.d2 = self.d1 - self.sigma * sqrt(self.T)

    def price(self) -> float:
        return exp(-self.r * self.T) * norm.cdf(-self.d2)

    def delta(self) -> float:
        return -exp(-self.r * self.T) * norm.pdf(self.d2) / (self.S * self.sigma * sqrt(self.T))
    
    def vega(self) -> float:
        return exp(-self.r * self.T) * norm.pdf(self.d2) * self.d1 / self.sigma
    
    def rho(self) -> float:
        return self.T * exp(-self.r * self.T) * norm.cdf(-self.d2)
    
    def gamma(self) -> float:
        return exp(-self.r * self.T) * norm.pdf(self.d2) * self.d2 / (self.S**2 * self.sigma**2 * self.T)
    
    def theta(self) -> float:
        term1 = -self.r * exp(-self.r * self.T) * norm.cdf(-self.d2)
        term2 = -exp(-self.r * self.T) * norm.pdf(self.d2) * ((log(self.S / self.K) / (2 * self.sigma * self.T**1.5))
            - (self.r / (self.sigma * sqrt(self.T))) - (self.sigma / (2 * sqrt(self.T))))
        return term1 + term2

class BinaryCallLong(OptionWrapper):
    def __init__(self, S, K, T, sigma, q, r):
        super().__init__(BinaryCall(S=S, K1=K, T1=T, sigma=sigma, r=r),sign=1)

class BinaryCallShort(OptionWrapper):
    def __init__(self, S, K, T, sigma, q, r):
        super().__init__(BinaryCall(S=S, K1=K, T1=T, sigma=sigma, r=r),sign=-1)

class BinaryPutLong(OptionWrapper):
    def __init__(self, S, K, T, sigma, q, r):
        super().__init__(BinaryPut(S=S, K1=K, T1=T, sigma=sigma, r=r),sign=1)

class BinaryPutShort(OptionWrapper):
    def __init__(self, S, K, T, sigma, q, r):
        super().__init__(BinaryPut(S=S, K1=K, T1=T, sigma=sigma, r=r),sign=-1)

def _gbs(option_type, fs, x, t, r, v, q) -> list:
    b = r - q
    t__sqrt = math.sqrt(t)
    d1 = (math.log(fs / x) + (b + (v * v) / 2) * t) / (v * t__sqrt)
    d2 = d1 - v * t__sqrt

    if option_type == "c":
        value = fs * math.exp((b - r) * t) * norm.cdf(d1) - x * math.exp(-r * t) * norm.cdf(d2)
        delta = math.exp((b - r) * t) * norm.cdf(d1)
        gamma = math.exp((b - r) * t) * norm.pdf(d1) / (fs * v * t__sqrt)
        theta = -(fs * v * math.exp((b - r) * t) * norm.pdf(d1)) / (2 * t__sqrt) - (b - r) * fs * math.exp(
            (b - r) * t) * norm.cdf(d1) - r * x * math.exp(-r * t) * norm.cdf(d2)
        vega = math.exp((b - r) * t) * fs * t__sqrt * norm.pdf(d1)
        rho = x * t * math.exp(-r * t) * norm.cdf(d2)
    else:
        value = x * math.exp(-r * t) * norm.cdf(-d2) - (fs * math.exp((b - r) * t) * norm.cdf(-d1))
        delta = -math.exp((b - r) * t) * norm.cdf(-d1)
        gamma = math.exp((b - r) * t) * norm.pdf(d1) / (fs * v * t__sqrt)
        theta = -(fs * v * math.exp((b - r) * t) * norm.pdf(d1)) / (2 * t__sqrt) + (b - r) * fs * math.exp(
            (b - r) * t) * norm.cdf(-d1) + r * x * math.exp(-r * t) * norm.cdf(-d2)
        vega = math.exp((b - r) * t) * fs * t__sqrt * norm.pdf(d1)
        rho = -x * t * math.exp(-r * t) * norm.cdf(-d2)

    return [value, delta, gamma, theta, vega, rho]

def _asian_76(option_type, S, K, T, t_a, r, sigma, q):

    if abs(T - t_a) < 1e-8:
        v_a = sigma
    else:
        m = (2 * math.exp((sigma ** 2) * T)
             - 2 * math.exp((sigma ** 2) * t_a) * (1 + (sigma ** 2) * (T - t_a))) / (
            (sigma ** 4) * ((T - t_a) ** 2))

        m = max(m, 1e-10)
        v_a = math.sqrt(math.log(m) / T)

    return _gbs(option_type, S, K, T, r, v_a, q)

class OptionWrapper1:
    def __init__(self, option, sign = 1 or -1):
        self.option = option
        self.sign = sign
    def vega(self):
        return self.sign * self.option[4]
    def theta(self):
        return self.sign * self.option[3]
    def rho(self):
        return self.sign * self.option[5]
    def delta(self):
        return self.sign * self.option[1]
    def gamma(self):
        return self.sign * self.option[2]

class AsianOptionsCallLong(OptionWrapper1):
    def __init__(self, S, K, T, sigma, t_a, r, q):
        super().__init__(_asian_76(option_type="c", S=S, K=K, T=T, t_a=t_a, sigma=sigma, r=r, q=q),sign=1)

class AsianOptionsCallShort(OptionWrapper1):
    def __init__(self, S, K, T, sigma, t_a, r, q):
        super().__init__(_asian_76(option_type="c", S=S, K=K, T=T, t_a=t_a, sigma=sigma, r=r, q=q),sign=-1)

class AsianOptionsPutLong(OptionWrapper1):
    def __init__(self, S, K, T, sigma, t_a, r, q):
        super().__init__(_asian_76(option_type="p", S=S, K=K, T=T, t_a=t_a, sigma=sigma, r=r, q=q),sign=1)

class AsianOptionsPutShort(OptionWrapper1):
    def __init__(self, S, K, T, sigma, t_a, r, q):
        super().__init__(_asian_76(option_type="p", S=S, K=K, T=T, t_a=t_a, sigma=sigma, r=r, q=q),sign=-1)

import blackscholes as bs
import app.functions as fn
import pandas as pd
import numpy as np
import inspect


list_of_derivatives = {
    'Long Call Option' : bs.BlackScholesCall,
    'Long Put Option' : bs.BlackScholesPut,
    'Short Call Option' : fn.BlackScholesCallShort,
    'Short Put Option' : fn.BlackScholesPutShort,
    'Long Straddle' : bs.BlackScholesStraddleLong,
    'Short Straddle' : bs.BlackScholesStraddleShort,
    'Long Strangle' : bs.BlackScholesStrangleLong,
    'Short Strangle' : bs.BlackScholesStrangleShort,
    'Long Butterfly' : bs.BlackScholesButterflyLong,
    'Short Butterfly' : bs.BlackScholesButterflyShort,
    'Long Iron Condor' : bs.BlackScholesIronCondorLong,
    'Short Iron Condor' : bs.BlackScholesIronCondorShort,
    'Short Iron Butterfly' : bs.BlackScholesIronButterflyShort,
    'Long Iron Butterfly' : bs.BlackScholesIronButterflyLong,
    'Long Binary Call' : fn.BinaryCallLong,
    'Short Binary Call' : fn.BinaryCallShort,
    'Long Binary Put' : fn.BinaryPutLong,
    'Short Binary Put' : fn.BinaryPutShort,
    'Long Bear Spread' : fn.BlackScholesBearSpreadLong,
    'Short Bear Spread' : fn.BlackScholesBearSpreadShort,
    'Long Bull Spread' : fn.BlackScholesBullSpreadLong,
    'Short Bull Spread' : fn.BlackScholesBullSpreadShort,
    'Long Calendar Call Spread' : fn.BlackscholesCalendarCallSpreadLong,
    'Short Calendar Call Spread' : fn.BlackscholesCalendarCallSpreadShort,
    'Long Calendar Put Spread' : fn.BlackScholesCalendarPutSpreadLong,
    'Short Calendar Put Spread' : fn.BlackScholesCalendarPutSpreadShort,
    'Long Asian Call' : fn.AsianOptionsCallLong,
    'Short Asian Call' : fn.AsianOptionsCallShort,
    'Long Asian Put' : fn.AsianOptionsPutLong,
    'Short Asian Put' : fn.AsianOptionsPutShort
}


class File():

    def __init__(self):

        self._param_columns = ["S", "K", "K1", "K2", "K3", "K4", "T", "T1", "T2", "t_a", "sigma", "q", "r"]
        self.number = 0

        self.S = np.arange(1,200,1)
        self.R = np.arange(-0.1, 0.895, 0.005)

        self.derivatives_types = [None] * 10

        self.deltas = np.zeros((10, 199))
        self.vegas = np.zeros((10, 199))
        self.rhos = np.zeros((10, 199))
        self.gammas = np.zeros((10, 199))
        self.thetas = np.zeros((10, 199))
        self.overall = np.zeros((5, 199))

        self.datas = pd.DataFrame(columns=self._param_columns, index=[n for n in range(10)])

        self.allowed_params = {}

        for name, cls in list_of_derivatives.items():
            sig = inspect.signature(cls.__init__)
            self.allowed_params[name] = set(sig.parameters.keys())

    def _build_kwargs(self, base_params : pd.DataFrame, variable : int | float, derivative_type : str, vector_type: str = "s") -> dict:

        params = {
            "S": variable if vector_type == 's' else base_params["S"],
            "K": base_params["K"],
            "K1": base_params["K1"],
            "K2": base_params["K2"],
            "K3": base_params["K3"],
            "K4": base_params["K4"],
            "T": base_params["T"],
            "T1": base_params["T1"],
            "T2": base_params["T2"],
            "t_a": base_params["t_a"],
            "sigma": base_params["sigma"],
            "q": base_params["q"],
            "r": variable if vector_type == 'r' else base_params["r"]
        }

        allowed_params = self.allowed_params[derivative_type]
        return {k: v for k, v in params.items() if k in allowed_params and v is not None}

    def _compute_greek(self, derivative_type : str, i : int, greek : str, ) -> np.array:

        my_class = list_of_derivatives.get(derivative_type)
        row = self.datas.iloc[i]

        my_vector = self.R if greek == "Rho" else self.S
        vec_ty = "r" if greek == "Rho" else "s"

        return np.array([
        getattr(my_class(**self._build_kwargs(row, el, derivative_type, vec_ty)), greek.lower())()
        for el in my_vector
        ])

    def _compute_portfolio(self) -> None:

        all_greeks = [self.deltas, self.gammas, self.vegas, self.thetas, self.rhos]

        for m, greek_matrix in enumerate(all_greeks):
            self.overall[m] = greek_matrix.sum(axis=0)

    def add_element(self, derivative_type : str, data : list) -> None:

        self.datas.loc[self.number] = data
        self.derivatives_types[self.number] = derivative_type

        self.deltas[self.number] = self._compute_greek(derivative_type, self.number, "Delta")
        self.gammas[self.number] = self._compute_greek(derivative_type, self.number, "Gamma")
        self.vegas[self.number] = self._compute_greek(derivative_type, self.number, "Vega")
        self.thetas[self.number] = self._compute_greek(derivative_type, self.number, "Theta")
        self.rhos[self.number] = self._compute_greek(derivative_type, self.number, "Rho")

        if self.number == 9:
            self.number = 0
        else:
            self.number += 1

        self._compute_portfolio()

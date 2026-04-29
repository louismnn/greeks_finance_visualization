from app.check_errors import check_errors
from CTkMessagebox import CTkMessagebox
import customtkinter as ctk
import pandas as pd


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")


class DerivativeInput():

    def __init__(self):
        self.s = 100.0
        self.t = 0.5
        self.sigma = 0.15
        self.q = 0.0
        self.r = 0.02
        self.k1 = 90.0
        self.k2 = 100.0
        self.k3 = 110.0
        self.k4 = 120.0
        self.t1 = 1.0
        self.t2 = 1.5

        self.boll_table = pd.DataFrame({
            "s": [True, True, True, True, True, True],
            "k": [True, False, False, False, False, True],
            "k1": [False, True, True, True, True, False], 
            "k2": [False, True, True, True, True, False],
            "k3": [False, False, True, True, False, False],
            "k4": [False, False, False, True, False, False],
            "t": [True, True, True, True, False, True],
            "t1": [False, False, False, False, True, False],
            "t2": [False, False, False, False, True, False],
            "t_a": [False, False, False, False, False, True],
            "sigma": [True, True, True, True, True, True],
            "q": [True, True, True, True, True, True],
            "r": [True, True, True, True, True, True]
            })

        self.translate_names = {
            "s": "S (Underlying Price):",
            "k": "K (Strike Price):",
            "k1": "K1 (First Strike Price):", 
            "k2": "K2 (Second Strike Price):",
            "k3": "K3 (Third Strike Price):",
            "k4": "K4 (Fourth Strike Price):",
            "t": "T (Time to Maturity in Year):",
            "t1": "T1 (First Time to Maturity in Year):",
            "t2": "T2 (Second Time to Maturity in year):",
            "t_a": "t (Average Calculation Time):",
            "sigma": "Sigma (Annual Volatility):",
            "q": "q (Dividend Yield):",
            "r": "r (Risk-Free Rate):"
            }
            
        self.default_values = {
            "s": self.s,
            "k": self.k1,
            "k1": self.k1,
            "k2": self.k2,
            "k3": self.k3,
            "k4": self.k4,
            "t": self.t1,
            "t1": self.t1,
            "t2": self.t2,
            "t_a": self.t,
            "sigma": self.sigma,
            "r": self.r,
            "q": self.q
            }
        
        self.dict_of_derivatives = {
            'Long Call Option': 0,
            'Long Put Option': 0,
            'Short Call Option': 0,
            'Short Put Option': 0,
            'Long Straddle': 0,
            'Short Straddle': 0,
            'Long Binary Call': 0,
            'Short Binary Call': 0,
            'Long Binary Put': 0,
            'Short Binary Put': 0,
            'Long Strangle': 1,
            'Short Strangle': 1,
            'Long Bear Spread': 1,
            'Short Bear Spread': 1,
            'Long Bull Spread': 1,
            'Short Bull Spread': 1,
            'Long Butterfly': 2,
            'Short Butterfly': 2,
            'Short Iron Butterfly': 2,
            'Long Iron Butterfly': 2,
            'Long Iron Condor': 3,
            'Short Iron Condor': 3,
            'Long Calendar Call Spread': 4,
            'Short Calendar Call Spread': 4,
            'Long Calendar Put Spread': 4,
            'Short Calendar Put Spread': 4,
            'Long Asian Call': 5,
            'Short Asian Call': 5,
            'Long Asian Put': 5,
            'Short Asian Put': 5
            }

    def _get_type(self, derivative_type : str) -> int:
        return self.dict_of_derivatives[derivative_type]

    def _build_kwargs(self, base_params : dict) -> dict:

        params = {
            "S": base_params.get("s"),
            "K": base_params.get("k"),
            "K1": base_params.get("k1"),
            "K2": base_params.get("k2"),
            "K3": base_params.get("k3"),
            "K4": base_params.get("k4"),
            "T": base_params.get("t"),
            "T1": base_params.get("t1"),
            "T2": base_params.get("t2"),
            "t_a": base_params.get("t_a"),
            "sigma": base_params.get("sigma"),
            "q": base_params.get("q"),
            "r": base_params.get("r")
        }

        return {k: v for k, v in params.items()}
    
    def _generate_widget(self, number) -> list:

        root = ctk.CTk()
        root.title(self.derivative_type)

        self.font = ctk.CTkFont(family="Helverica", size=12, weight="bold")

        entries = {}

        for j, col_name in enumerate(self.boll_table.columns):
 
            element = self.boll_table.loc[number, col_name]

            if element:
            
                Label = ctk.CTkLabel(root, text=self.translate_names.get(col_name), font=self.font)
                Label.grid(row=j, column=0, padx=10, pady=5)

                Entry = ctk.CTkEntry(root)
                Entry.grid(row=j, column=1, padx=10, pady=5)

                value = self.default_values.get(col_name)
                Entry.insert(0, str(value))

                entries[col_name] = Entry

        def submit():

            values = {}

            for key, Entry in entries.items():
                try:
                    values[key] = float(Entry.get())

                except ValueError:
                    CTkMessagebox(title="Input Error", message="Inputs must be integers or floats")
                    return

            try:
                values = self._build_kwargs(values)
                check_errors(**values)

            except ValueError as e:
                CTkMessagebox(title="Input Error : ", message=e)
                return

            self.values = values
            root.destroy()

        button = ctk.CTkButton(root, text="Submit", text_color="black", hover=True, fg_color= "forest green", hover_color="SpringGreen4", font=self.font, command=submit)
        button.grid(row=15, column=0, columnspan=2, pady=10)

        root.attributes("-topmost", True)

        root.mainloop()

        if not self.values:
            raise Exception("User closed the window without submitting")

        return list(self.values.values())

    def get_data(self, derivative_type: str) -> list:

        self.derivative_type = derivative_type
        num = self._get_type(derivative_type=self.derivative_type)

        return self._generate_widget(number = num)

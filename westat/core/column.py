import pandas as pd


class Column(pd.Series):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'column for westat'

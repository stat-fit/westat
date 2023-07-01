import pandas as pd


class Table(pd.DataFrame):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return 'table for westat'



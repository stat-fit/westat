import numpy as np
import pandas as pd


class Scorecard:
    data = pd.DataFrame()
    target = 'y'
    method = 'tree'
    max_bins = 5
    missing = [np.nan, None, 'nan', 'null', 'NULL']
    precision = 4
    iv_threshold = 0.02
    corr_threshold = 0.8
    language = 'en'
    random_state = 1234

    def __init__(self,
                 data,
                 target='y',
                 method='tree',
                 max_bins=5,
                 missing=[],
                 precision=4,
                 iv=0.02,
                 corr=0.8,
                 pdo=50,
                 base_score=600,
                 test_size=0.3,
                 random_state=1234,
                 language='cn'):
        self.data = data
        self.target = target
        self.method = method
        self.max_bins = max_bins
        self.missing = missing
        self.precision = precision
        self.iv_threshold = iv
        self.corr_threshold = corr
        self.language = language
        self.random_state = random_state

    def woe_iv(self,
               col: str,
               bins: list = [],
               qcut: int = 0,
               missing: list = [np.nan, None, 'nan', 'null', 'NULL'],
               max_bins: int = 5,
               target: str = 'y',
               method: str = 'optb',
               trend: str = 'auto',
               precision: int = 4,
               language: str = 'en'):

        from westat.model.get_woe_iv import get_woe_iv

        data = self.data
        if not missing:
            missing = self.missing
        if not method:
            method = self.method
        if not max_bins:
            max_bins = self.max_bins
        if not precision:
            precision = self.precision
        if not language:
            language = self.language

        result = get_woe_iv(data=data,
                            col=col,
                            bins=bins,
                            qcut=qcut,
                            missing=missing,
                            max_bins=max_bins,
                            target=target,
                            method=method,
                            trend=trend,
                            precision=precision,
                            language=language)
        return result

    def view_woe_iv(self,
                    column_name,
                    bins,
                    qcut,
                    missing,
                    max_bins,
                    target,
                    method,
                    trend,
                    precision,
                    language,
                    color):
        from westat.model.get_woe_iv import view_woe_iv
        result = view_woe_iv(data=self.data,
                             col=column_name,
                             bins=bins,
                             qcut=qcut,
                             missing=missing,
                             max_bins=max_bins,
                             target=target,
                             method=method,
                             trend=trend,
                             precision=precision,
                             language=language,
                             color=color)
        return result

    def fit(self, X, y):
        pass

    def save_excel(self):
        pass

    def data_split(self,
                   data: pd.DataFrame,
                   test_size: float = 0.25,
                   random_state=1234,
                   target: str = 'y'):
        from westat.sample import get_data_partition
        result = get_data_partition(data, test_size, random_state, target)
        return result

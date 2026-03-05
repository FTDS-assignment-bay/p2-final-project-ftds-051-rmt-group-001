import pandas as pd
import __main__

def function_total_items_bin(X):
    X = X.copy()
    X['total_items_bin'] = pd.cut(
        X['total_items'],
        bins=[-1, 0, 1, 3, 5, 1000],
        labels=['no_item','single','few','several','bulk'],
        include_lowest=True
    )
    return X
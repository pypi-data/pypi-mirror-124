import numpy as np
import pandas as pd


def get_simple_df(num_of_rows: int):
	df = pd.DataFrame([{'column1': 1, 'column2': 2} for i in range(num_of_rows)])
	return df


print(get_simple_df(5))

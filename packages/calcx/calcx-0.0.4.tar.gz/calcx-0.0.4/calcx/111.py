from ivey_test import log_returns
import pandas as pd
df = pd.DataFrame()
df['a'] = [1, 2, 3]
a = log_returns(df)
print(a)
import dask.dataframe as dd
import pandas as pd

d = {"col1": [1, 2, 3, 4], "col2": [5, 6, 7, 8]}
df = dd.from_pandas(pd.DataFrame(data=d), npartitions=2)

# output path will be relative to your home directory
output_path = "basic_conda_usage.parquet"
dd.to_parquet(
    df=df,
    path=output_path,
)

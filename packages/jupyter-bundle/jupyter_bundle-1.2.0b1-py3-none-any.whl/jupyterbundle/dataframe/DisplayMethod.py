from typing import Union
from pandas.core.frame import DataFrame as PandasDataFrame
from pyspark.sql import DataFrame as SparkDataFrame
from pysparkbundle.dataframe.DataFrameShowMethodInterface import DataFrameShowMethodInterface
from IPython.core.display import display


class DisplayMethod(DataFrameShowMethodInterface):
    def show(self, df: Union[PandasDataFrame, SparkDataFrame]):
        final_df: PandasDataFrame

        if isinstance(df, PandasDataFrame):
            final_df = df.head()
        elif isinstance(df, SparkDataFrame):
            final_df = df.limit(5).toPandas()
        else:
            raise TypeError(
                "Argument df has to be a pyspark DataFrame (pyspark.sql.DataFrame) or a pandas DataFrame (pandas.core.frame.DataFrame)."
            )

        display(final_df)

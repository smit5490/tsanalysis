import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class Tsdf:
    #TODO: write docstrings
    def __init__(self, df, dt_column):
        assert dt_column in df.columns, f"{dt_column} column not found in dataframe."
        assert isinstance(df[dt_column][0], pd.Timestamp), f"{dt_column} not a datetime field"

        self.df = df
        self.dt_column = dt_column
        self.min_date = df[dt_column].min()
        self.max_date = df[dt_column].max()

    def find_gaps(self, freq="1 day"):
        lag_1 = self.df.dt.shift(periods=1)
        delta = (self.df.dt - lag_1)[1:]

        if all(freq == delta):
            print(f"Time series has no gaps with freq = {freq}")
        else:
            print(f"Time series has gaps")

        delta_index = delta[delta != freq].index
        delta_index = delta_index.append(delta_index-1)
        return self.df.iloc[delta_index]

    def ts_plot(self, y):
        plt.style.use("seaborn")
        plt.plot(self.dt_column, y, data=self.df)
        plt.title(f"Plot of {y}")
        plt.xlabel(self.dt_column)
        plt.ylabel(y)
        plt.show();

    def ts_heatmap(self, fill, y_val, x_val):
        assert y_val in ["day", "month", "year"]
        assert x_val in ["month", "day", "hour"]

        result = self.df
        if y_val == "day":
            result[y_val] = result[self.dt_column].dt.day
        elif y_val == "month":
            result[y_val] = result[self.dt_column].dt.month_name()
        else:
            result[y_val] = result[self.dt_column].dt.year

        if x_val == "month":
            result[x_val] = result[self.dt_column].dt.month_name()
        elif x_val == "day":
            result[x_val] = result[self.dt_column].dt.day
        else:
            result[x_val] = result[self.dt_column].dt.hour

        result = result.pivot_table(index=y_val, columns=x_val, values=fill, aggfunc="sum")
        sns.heatmap(result)
        plt.title(f"Heatmap of {fill}")
        plt.show();









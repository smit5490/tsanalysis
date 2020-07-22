import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


class Tsdf:
    """ Creates a time-series data frame with basic attributes and methods
    Args:
        df (dataframe): A time-series data frame
        dt_column (string): The time-series column name in df

    Attributes:
        df (dataframe): A time-series data frame
        dt_column (string): The time-series column name in df
        min_date (date): Minimum date in time-series.
        max_date (date): Maximum date in time-series.

    """
    def __init__(self, df, dt_column):

        assert dt_column in df.columns, f"{dt_column} column not found in dataframe."
        assert isinstance(df[dt_column][0], pd.Timestamp), f"{dt_column} not a datetime field"

        self.df = df
        self.dt_column = dt_column
        self.min_date = df[dt_column].min()
        self.max_date = df[dt_column].max()

    def find_gaps(self, freq="1 day"):
        """ Find gaps in the time-series
        Args:
            freq (string): Expected frequency of time-series
        Returns:
            Return gaps in time-series, if any
        """
        lag_1 = self.df.dt.shift(periods=1)
        delta = (self.df.dt - lag_1)[1:]

        if all(freq == delta):
            print(f"Time series has no gaps with freq = {freq}")
        else:
            print(f"Time series has gaps")

        delta_index = delta[delta != freq].index
        delta_index = delta_index.append(delta_index - 1)
        return self.df.iloc[delta_index]

    def ts_plot(self, y, start_time=None, end_time=None):
        """Create simple uni-variate line plot of time series
        Args:
            y (string): y-axis plotting variable
            start_time (datetime): first datetime to plot
            end_time (datetime): last datetime to plot
        Returns:
            Returns line plot
        """
        if start_time is None:
            start_time = self.min_date
        if end_time is None:
            end_time = self.max_date
        plt.style.use("seaborn")
        plt.plot(self.dt_column, y, data=self.df[(self.df[self.dt_column] >= start_time) &
                                                 (self.df[self.dt_column] <= end_time)])
        plt.title(f"Plot of {y}")
        plt.xlabel(self.dt_column)
        plt.ylabel(y)
        plt.show();

    def ts_heatmap(self, fill, y_val, x_val):
        """Create heatmap using two time-series axes and a fill variable
        Args:
            fill (string): Variable used to fill heatmap
            y_val (string): y-axis date-time component. Can be either day, month, or year
            x_val (string): x-axis date-time component. Can be either month, day or hour
        Returns:
            Returns heatmap
        """
        assert y_val in ["day", "month", "year"], "y_val must be either day, month, or year"
        assert x_val in ["month", "day", "hour"], "x_val must be either month, day or hour"

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
        if y_val == "month":
            result.index = pd.CategoricalIndex(result.index,
                                               categories=["January", "February", "March", "April", "May", "June",
                                                           "July", "August", "September", "October", "November",
                                                           "December"])
            result.sort_index(inplace = True)

        sns.heatmap(result, cmap="YlOrRd")
        plt.title(f"Heatmap of {fill}")
        plt.show();

    def ts_decomp(self, components):
        """Decomposes time-series into its constituent parts appends to dataframe as columns
        Args:
            components (list): List of time-series components to be used for decomposition
        Returns:
            None
        """
        assert isinstance(components, list), "components must be a list of datetime components"
        if "year" in components:
            self.df["year"] = self.df[self.dt_column].dt.year
        if "month" in components:
            self.df["month"] = self.df[self.dt_column].dt.month_name()
        if "weekday" in components:
            self.df["weekday"] = self.df[self.dt_column].dt.day_name()
        if "day" in components:
            self.df["day"] = self.df[self.dt_column].dt.day
        if "hour" in components:
            self.df["hour"] = self.df[self.dt_column].dt.hour

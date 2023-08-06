import numpy as np
import backtesting_walkfoward.errors as er
import pandas as pd
import backtesting_walkfoward.bokeh_plot as bk
from bokeh.plotting import show


def assert_numpy_date(elements):
    try:
        element = [np.datetime64(i) for i in elements]
        output = np.array(element)
    except Exception as e:
        raise e

    return output


def assert_numpy_elements(element):
    try:
        output = np.array(element)
    except Exception as e:
        raise e

    if output.dtype != float and output.dtype != int and output.dtype != bool:
        print(output.dtype)
        raise er.ArrayNotFloats

    return output


class DataClass:
    """
    Class used as data in the backtesting process.
    The main reason for use this class and don't use dataframe instead in backtesting
    is because this class handle all the filters for the calculations and numba does not works well with pandas.,
    Its simple to works only with numpy arrays.
    """

    p, pv = [None]*2
    buy_enter, buy_close, sell_enter, sell_close = [None]*4

    def __init__(self, data_input, index_date=False, with_indicators=False):
        """

        :param data_input: a dataframe, dictionary or instance that can be converted in dataframe with columns:
        date (datetime),
        open (int or float),
        high (int or float),
        low (int or float),
        close (int or float).
        :param index_date: if your date is as index
        :param with_indicators:
        """

        self._columns_index_false = ['date', 'open', 'high', 'low', 'close']
        self._columns_index_true = ['open', 'high', 'low', 'close']

        if not isinstance(data_input, pd.DataFrame):
            index_date = False

            try:
                data_input = pd.DataFrame(data_input)
            except Exception as e:
                raise e

        columns_index = self._columns_index_false
        if index_date:
            columns_index = self._columns_index_true

        for column in columns_index:
            if column not in data_input.columns:
                print(f'Data frame must have "{column}" as column, be sure all letters is lowered')
                raise er.MissingColumn

        data_input.dropna(inplace=True)

        self.open = assert_numpy_elements(data_input.open)
        self.high = assert_numpy_elements(data_input.high)
        self.low = assert_numpy_elements(data_input.low)
        self.close = assert_numpy_elements(data_input.close)

        self._dict_candle = {
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
        }

        if index_date:
            self.date = assert_numpy_date(data_input.index)
        else:
            self.date = assert_numpy_date(data_input.date)

        self.indicators = {}
        if with_indicators:
            exclude_columns = self._columns_index_false
            if index_date:
                exclude_columns = self._columns_index_true
            data_indicators = data_input.loc[:, [i for i in list(data_input.columns) if i not in exclude_columns]]

            for column in data_indicators.columns:
                self.indicators[column] = assert_numpy_elements(data_indicators[column])

        self._set_dataframe()

    def _set_dataframe(self):
        dict_dataframe = {
            'date': self.date,
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
        }

        self.dataframe = pd.DataFrame(dict_dataframe)

        for key, value in self.indicators.items():
            self.dataframe[key] = value

        if self.buy_enter is not None:
            self.dataframe['buy_enter'] = self.buy_enter

        if self.buy_close is not None:
            self.dataframe['buy_close'] = self.buy_close

        if self.sell_enter is not None:
            self.dataframe['sell_enter'] = self.sell_enter

        if self.sell_close is not None:
            self.dataframe['sell_close'] = self.sell_close

    def update_dict_candle(self):
        self._dict_candle = {
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
        }

    def add_update_indicator(self, name: str, indicator):
        if not isinstance(name, str):
            print(f'The name imput: {name} must be a string')
            raise ValueError

        if len(indicator) != len(self.dataframe):
            print(f'The len of {name} indicator is different of dataframe')
            raise ValueError

        self.indicators[name] = assert_numpy_elements(indicator)
        self._set_dataframe()

    def delete_indicator(self, key: str):
        if not isinstance(key, str):
            print('name must be a string')
            raise ValueError

        if key not in self.indicators.keys():
            print('key not found in indicators')
            raise ValueError

        self.indicators.pop(key)
        self._set_dataframe()

    def plot_bokeh_ohlc(self, title=''):
        try:
            self.p = bk.bokeh_df(self.dataframe, title, volume=False)
            show(self.p)
        except Exception as e:
            raise e

    def plot_bokeh_ohlcv(self, title=''):
        if 'volume' not in self.dataframe.columns:
            print('No volume in dataframe for plot open, high, low, close, volume')
            raise er.NoVolumeInDataframe
        try:
            self.p, self.pv = bk.bokeh_df(self.dataframe, title)
            bk.bokeh_gridplot(self.p, self.pv)
        except Exception as e:
            raise e

    def _set_buy_enter(self, buy_enter):
        self.buy_enter = assert_numpy_elements(buy_enter)
        self._set_dataframe()

    def _set_buy_close(self, buy_close):
        self.buy_close = assert_numpy_elements(buy_close)
        self._set_dataframe()

    def _set_sell_enter(self, sell_enter):
        self.sell_enter = assert_numpy_elements(sell_enter)
        self._set_dataframe()

    def _set_sell_close(self, sell_close):
        self.sell_close = assert_numpy_elements(sell_close)
        self._set_dataframe()

    def plot_bokeh_indicators(self, line_indicators={}, circle_indicators={}, step_indicators={},
                              volume=False, title=''):
        """
        :param line_indicators: dict with {str: str} first string the indicator name second string the color.
        :param circle_indicators: dict with {str: str} first string the indicator name second string the color.
        :param step_indicators: dict with {str: str} first string the indicator name second string the color.
        :param volume: bool, if volume=True its print the indicator volume.
        :param title: str, print the string.
        :return: html, one html in the same folder with the plot of data_class.dataframe.
        """
        if volume:
            if 'volume' not in self.dataframe.columns:
                print('No volume in dataframe for plot open, high, low, close, volume')
                raise er.NoVolumeInDataframe
            try:
                self.p, self.pv = bk.bokeh_df(self.dataframe, title)
            except Exception as e:
                raise e
        else:
            try:
                self.p = bk.bokeh_df(self.dataframe, title, volume=False)
            except Exception as e:
                raise e

        try:
            for key, value in line_indicators.items():
                self.p = bk.bokeh_ohlcv_line(self.dataframe, self.p, key, color=value)
        except Exception as e:
            print(e)

        try:
            for key, value in circle_indicators.items():
                self.p = bk.bokeh_ohlcv_circle(self.dataframe, self.p, key, color=value)
        except Exception as e:
            print(e)

        try:
            for key, value in step_indicators.items():
                self.p = bk.bokeh_ohlcv_step(self.dataframe, self.p, key, color=value)
        except Exception as e:
            print(e)

        if volume:
            bk.bokeh_gridplot(self.p, self.pv)
            return

        show(self.p)

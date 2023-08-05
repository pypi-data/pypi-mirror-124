import datetime
import typing

import QuantConnect.Data
import QuantConnect.Data.Custom


class Quandl(QuantConnect.Data.DynamicData):
    """
    Quandl Data Type - Import generic data from quandl, without needing to define Reader methods.
    This reads the headers of the data imported, and dynamically creates properties for the imported data.
    """

    IsAuthCodeSet: bool
    """Flag indicating whether or not the Quanl auth code has been set yet"""

    @property
    def EndTime(self) -> datetime.datetime:
        """
        The end time of this data. Some data covers spans (trade bars) and as such we want
        to know the entire time span covered
        """
        ...

    @EndTime.setter
    def EndTime(self, value: datetime.datetime):
        """
        The end time of this data. Some data covers spans (trade bars) and as such we want
        to know the entire time span covered
        """
        ...

    @property
    def Period(self) -> datetime.timedelta:
        """Gets a time span of one day"""
        ...

    @typing.overload
    def __init__(self) -> None:
        """Default quandl constructor uses Close as its value column"""
        ...

    @typing.overload
    def __init__(self, valueColumnName: str) -> None:
        """
        Constructor for creating customized quandl instance which doesn't use "Close" as its value item.
        
        This method is protected.
        """
        ...

    def GetSource(self, config: QuantConnect.Data.SubscriptionDataConfig, date: typing.Union[datetime.datetime, datetime.date], isLiveMode: bool) -> QuantConnect.Data.SubscriptionDataSource:
        """
        Quandl Source Locator: Using the Quandl V1 API automatically set the URL for the dataset.
        
        :param config: Subscription configuration object
        :param date: Date of the data file we're looking for
        :param isLiveMode: true if we're in live mode, false for backtesting mode
        :returns: STRING API Url for Quandl.
        """
        ...

    def Reader(self, config: QuantConnect.Data.SubscriptionDataConfig, line: str, date: typing.Union[datetime.datetime, datetime.date], isLiveMode: bool) -> QuantConnect.Data.BaseData:
        """
        Generic Reader Implementation for Quandl Data.
        
        :param config: Subscription configuration
        :param line: CSV line of data from the souce
        :param date: Date of the requested line
        :param isLiveMode: true if we're in live mode, false for backtesting mode
        """
        ...

    @staticmethod
    def SetAuthCode(authCode: str) -> None:
        """Set the auth code for the quandl set to the QuantConnect auth code."""
        ...


class FxcmVolume(QuantConnect.Data.BaseData):
    """
    FXCM Real FOREX Volume and Transaction data from its clients base, available for the following pairs:
        - EURUSD, USDJPY, GBPUSD, USDCHF, EURCHF, AUDUSD, USDCAD,
          NZDUSD, EURGBP, EURJPY, GBPJPY, EURAUD, EURCAD, AUDJPY
        FXCM only provides support for FX symbols which produced over 110 million average daily volume (ADV) during 2013.
        This limit is imposed to ensure we do not highlight low volume/low ticket symbols in addition to other financial
        reporting concerns.
    """

    @property
    def Transactions(self) -> int:
        """Sum of opening and closing Transactions for the entire time interval."""
        ...

    @Transactions.setter
    def Transactions(self, value: int):
        """Sum of opening and closing Transactions for the entire time interval."""
        ...

    @property
    def Volume(self) -> int:
        """
        Sum of opening and closing Volume for the entire time interval.
            The volume measured in the QUOTE CURRENCY.
        """
        ...

    @Volume.setter
    def Volume(self, value: int):
        """
        Sum of opening and closing Volume for the entire time interval.
            The volume measured in the QUOTE CURRENCY.
        """
        ...

    def GetSource(self, config: QuantConnect.Data.SubscriptionDataConfig, date: typing.Union[datetime.datetime, datetime.date], isLiveMode: bool) -> QuantConnect.Data.SubscriptionDataSource:
        """
        Return the URL string source of the file. This will be converted to a stream
        
        :param config: Configuration object
        :param date: Date of this source file
        :param isLiveMode: true if we're in live mode, false for backtesting mode
        :returns: String URL of source file.
        """
        ...

    def Reader(self, config: QuantConnect.Data.SubscriptionDataConfig, line: str, date: typing.Union[datetime.datetime, datetime.date], isLiveMode: bool) -> QuantConnect.Data.BaseData:
        """
        Reader converts each line of the data source into BaseData objects. Each data type creates its own factory method,
            and returns a new instance of the object
            each time it is called. The returned object is assumed to be time stamped in the config.ExchangeTimeZone.
        
        :param config: Subscription data config setup object
        :param line: Line of the source document
        :param date: Date of the requested data
        :param isLiveMode: true if we're in live mode, false for backtesting mode
        :returns: Instance of the T:BaseData object generated by this line of the CSV.
        """
        ...



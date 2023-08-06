from datetime import datetime

import jsonpickle

from .algorum_types import *


class RemoteIndicatorEvaluator(object):
    def __init__(self, client,
                 symbol: TradeSymbol,
                 uid: str) -> object:
        self.Uid = uid
        self.Symbol = symbol
        self.Client = client

    def ema(self, period: float):
        response = self.Client.execute_async(AlgorumWebsocketMessage(
            'get_indicators',
            AlgorumMessageType.Request,
            self.Client.CorIdCounter.increment(),
            jsonpickle.encode(
                GetIndicatorsRequest(
                    self.Uid,
                    [
                        IndicatorRequest(
                            'EMA',
                            {'period': period}
                        )
                    ]
                ), False), None))
        result_val = jsonpickle.decode(response.JsonData)
        return result_val[0]["Result"]

    def preload_candles(self, candle_count: int, preload_end_time: datetime):
        response = self.Client.execute_async(AlgorumWebsocketMessage(
            'preload_candles',
            AlgorumMessageType.Request,
            self.Client.CorIdCounter.increment(),
            jsonpickle.encode(
                PreloadCandlesRequest(self.Uid, candle_count, preload_end_time), False), None))

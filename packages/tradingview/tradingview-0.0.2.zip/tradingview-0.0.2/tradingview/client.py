import dataclasses
from typing import Dict, Union
from websocket import create_connection, WebSocket, WebSocketConnectionClosedException
import json
import re
import random
import string
import requests
import dataclasses
import time
import logging

logger = logging.getLogger(__name__)

@dataclasses.dataclass
class Symbol:
    symbol: str
    chart_session_id: str
    sds: str
    sds_sym: str
    is_completed: bool = False

@dataclasses.dataclass
class OHLC:
    symbol: str
    fetch_time: float
    bar_time: int
    open: float
    high: float
    low: float
    close: float
    volume: float

@dataclasses.dataclass
class OrderBook:
    symbol: str
    fetch_time: float
    bid_size: float
    bid: float
    ask_size: float
    ask: float


class TradingViewWebSocketException(Exception):
    pass

def fetch_japan_symbols() -> list[str]:
    res = requests.get('https://scanner.tradingview.com/japan/scan')
    return [x['s'] for x in res.json()['data']]

class TradingViewWebSocketClient:
    symbols: dict[str, Symbol]

    RE_RESPONS_LENGTH = re.compile(r'~m~(\d+)~m~')
    def __init__(self) -> None:
        self.ws: WebSocket = create_connection(
            'wss://prodata.tradingview.com/socket.io/websocket',
            headers=json.dumps({
                'Origin': 'https://jp.tradingview.com',
            })
        )
        self.symbols = dict()

    def _add_prefix_message(self, msg):
        return f'~m~{len(msg)}~m~{msg}'

    def _parse_response(self, res: str):
        substr = res
        for length in map(int, self.RE_RESPONS_LENGTH.findall(res)):
            substr = substr.lstrip(f'~m~{length}~m~')
            body = substr[0:length]
            substr = substr[length:]
            if body.startswith('h'):
                self.ws.send(res)
            else:
                yield json.loads(body)

    def _generate_session_id(self, prefix: str):
        random_string = ''.join(random.choice(string.ascii_letters) for _ in range(12))
        return f'{prefix}_{random_string}'

    def _extract_ohlc(self, res):
        for sds, value in res['p'][1].items():
            for x in value['s']:
                bar_time, o, h, l, c, v = x['v']
                yield OHLC(self.symbols[sds].symbol, time.time(), int(bar_time), o, h, l, c, v)

    def _send(self, m: str, p: list[Union[str, int, dict]]):
        payload = self._add_prefix_message(json.dumps({'m': m, 'p': p}, separators=(',', ':')))
        self.ws.send(payload)

    def login(self, username, password):
        sign_in_url = 'https://www.tradingview.com/accounts/signin/'
        data = {"username": username, "password": password, "remember": "on"}
        headers = {
            'Referer': 'https://www.tradingview.com',
        }
        response = requests.post(url=sign_in_url, data=data, headers=headers)
        auth_token = response.json()['user']['auth_token']    
        self._send('set_auth_token', [auth_token])

    def add_symbols(self, symbols):
        [self.add_symbol(symbol) for symbol in symbols]

    def add_symbol(self, symbol):
        idx = len(self.symbols) + 1
        sds = f'sds_{idx}'
        sds_sym = f'sds_sym_{idx}'

        chart_session_id = self._generate_session_id('cs')
        self._send('chart_create_session', [chart_session_id, ''])
        self._send('resolve_symbol', [chart_session_id, sds_sym, f'={{\"symbol\":\"{symbol}\",\"adjustment\":\"splits\",\"session\":\"extended\"}}'])
        self.symbols[sds] = Symbol(symbol, chart_session_id, sds, sds_sym)

        # quote_session_id = self._generate_session_id('qs')
        # self._send('quote_create_session', [quote_session_id])
        # self._send('quote_add_symbols', [quote_session_id, symbol])
        # self._send('quote_fast_symbols', [quote_session_id, symbol])
        # return chart_session_id, quote_session_id

    def recv_raw(self):
        while True:
            try:
                result = self.ws.recv()
                for res in self._parse_response(result):
                    yield res
            except WebSocketConnectionClosedException as e:
                logger.warning('websocket is closed.')
                raise e

    def recv_realtime(self):
        for res in self.recv_raw():
            if res.get('m') == 'du':
                for ohlc in self._extract_ohlc(res):
                    yield ohlc 

            if res.get('m') == 'qsd':
                v = res['p'][1]['v']
                if 'trade_loaded' in v and 'bid' in v:
                    v.pop('trade_loaded')
                    yield OrderBook(symbol=res['p'][1]['n'], fetch_time=time.time(), **v)

    def _is_completed(self):
        return all([symbol.is_completed for symbol in self.symbols.values()])

    def fetch_ohlc(self, interval: str = '1', past_bar: int = 1):
        more_bars:  dict[str, int] = dict()

        for symbol in self.symbols.values():
            if past_bar > 5000:
                bar = 5000
                more_bars[symbol.sds] = past_bar - 5000
            else:
                bar = past_bar
            self._send('create_series', [symbol.chart_session_id, symbol.sds, 's1', symbol.sds_sym, interval, bar, ''])

        for res in self.recv_raw():
            if res.get('m') == 'timescale_update':
                for ohlc in self._extract_ohlc(res):
                    yield ohlc

            elif res.get('m') == 'series_completed':
                sds = res.get('p')[1]
                if sds in more_bars:
                    if more_bars[sds] > 5000:
                        more_bars[sds] = more_bars[sds] - 5000
                        bar = 5000
                    else:
                        bar = more_bars.pop(sds)

                    chart_session_id = self.symbols[sds].chart_session_id
                    self._send('request_more_data', [chart_session_id, sds, bar])
                else:
                    self.symbols[sds].is_completed = True

            if self._is_completed():
                break


def set_leverage(exchange, symbol, leverage):
    params = {'symbol': exchange.market_id(symbol), 'leverage': leverage}
    return exchange.fapiPrivate_post_leverage(params)
import pandas_ta as ta


def calculate_indicators(df):
    df['rsi'] = ta.rsi(df['close'], length=14)

    macd = ta.macd(df['close'])

    df['macd'] = macd['MACD_12_26_9']
    df['macd_signal'] = macd['MACDs_12_26_9']

    df['ema20'] = ta.ema(df['close'], length=20)

    return df
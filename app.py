import sys

from cryptofolio import app

if __name__ == "__main__":
    if '--real' in sys.argv:
        app.config['BINANCE'] = 'https://api.binance.com'
        app.config['BYBIT'] = 'https://api.bybit.com'

    app.run(debug=True)

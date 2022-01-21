import sys

from cryptofolio import app

if __name__ == "__main__":
    if '--test' in sys.argv:
        app.config['BINANCE'] = 'https://testnet.binance.vision'
        app.config['BYBIT'] = 'https://api-testnet.bybit.com'

    app.run(debug=True)
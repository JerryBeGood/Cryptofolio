import sys

from cryptofolio import app


def create_app(config_file, app_mode):
    app.config.from_pyfile(config_file)

    if app_mode == '--real':
        app.config['BINANCE'] = 'https://api.binance.com'
        app.config['BYBIT'] = 'https://api.bybit.com'
    else:
        app.config['BINANCE'] = 'https://testnet.binance.vision'
        app.config['BYBIT'] = 'https://api-testnet.bybit.com'

    return app


if __name__ == "__main__":
    create_app(*sys.argv[1:]).run()

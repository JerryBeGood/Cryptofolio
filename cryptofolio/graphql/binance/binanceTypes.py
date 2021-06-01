binanceTypes = '''
    type BinanceAccount {
        totalWalletBalance: String
        availableBalance: String
    }

    # OrderBody is a union type which means it can be either a Market or Limit or StopLoss order.
    union OrderBody = MarketOrder | LimitOrder | StopLossOrder

    interface Order {
        symbol: String!
        side: String!
        type: OrderType!
        timestamp: String!
        recvWindow: Int
    }

    type OrderResult {
        success: Boolean!
        errors: String
        order: OrderBody!
    }

    # In MarketOrder you either define the amount of the base asset you want to buy or sell, or the amount of quote asset you want to spend. That's for what the base field is for.
    type MarketOrder implements Order {
        symbol: String!
        side: String!
        type: OrderType!
        timestamp: String!
        recvWindow: Int
        base: Boolean!
        quantity: Float!
    }

    type LimitOrder implements Order {
        symbol: String!
        side: String!
        type: OrderType!
        timestamp: String!
        recvWindow: Int
        timeInForce: TIN!
        quantity: Float!
        price: Float!
        icebergQty: Float
    }

    type StopLossOrder implements Order {
        symbol: String!
        side: String!
        type: OrderType!
        timestamp: String!
        recvWindow: Int
        quantity: Float!
        stopPrice: Float!
    }

    enum OrderType  {
        MARKET
        LIMIT
        STOP_LOSS
    }

    enum Side {
        BUY
        SELL
    }

    # TIN - TimeInForce
    enum TIN {
        GTC
        IOC
        FOK
    }
'''
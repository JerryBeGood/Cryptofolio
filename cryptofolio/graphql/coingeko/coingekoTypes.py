coingekoTypes = '''
    type Asset {
        id: String!
        symbol: String
        name: String
        current_price: Float
        market_cap: String
        market_cap_rank: Int
        price_change_percentage_24h: Float
        total_volume: String
        circulating_supply: String
        total_supply: String
    }
    type AssetChartData {
        time_stamp: String!
        price: String!
    }
'''
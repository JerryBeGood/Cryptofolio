coingekoQueries = '''
    topAssets(vs_currency: String!, category: String): AssetsResult!
    assetChartData(
    id: String!
    vs_currency: String!
    days: String!
    interval: String!
  ): [AssetChartData]!
'''
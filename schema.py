sql_create_stocks_table = """
CREATE TABLE IF NOT EXISTS Stocks (
    stock_id INTEGER PRIMARY KEY AUTOINCREMENT,
    symbol TEXT NOT NULL UNIQUE,
    company_name TEXT NOT NULL
);
"""

sql_create_trades_table = """
CREATE TABLE IF NOT EXISTS Trades (
    trade_id INTEGER PRIMARY KEY AUTOINCREMENT,
    stock_id INTEGER,
    trader_name TEXT NOT NULL,
    trade_date DATE NOT NULL,
    quantity INTEGER NOT NULL,
    price_per_share REAL NOT NULL,
    trade_type TEXT NOT NULL CHECK(trade_type IN ('buy', 'sell')),
    winner_or_loser TEXT NOT NULL CHECK(winner_or_loser IN ('winner', 'loser')),
    FOREIGN KEY (stock_id) REFERENCES Stocks(stock_id) ON DELETE CASCADE
);
"""
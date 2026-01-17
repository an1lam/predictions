"""Configuration for Manifold Markets Kelly betting."""

# Kelly parameters
TOTAL_BANKROLL = 17619  # mana (full balance)
KELLY_FRACTION = 0.25  # quarter-Kelly
EDGE_THRESHOLD = 0.10  # 10% minimum edge to place bet
MAX_POSITION_PCT = 0.10  # 10% max of bankroll per individual bet
MIN_BET_SIZE = 10  # Skip small bets for one-shot scenario

# Market IDs mapping
MARKET_IDS = {
    "01_metr_horizon": "QOCNqgPOth",
    "02_frontiermath_tier4": "qd9CuLsOZN",
    "03_remote_labor_index": "z6QCs2ULNS",
    "04_openai_proof_qa": "6QyqELA5IE",
    "05_gsobench": "qt6RN658u5",
    "06_epoch_capabilities": "gtLydILZ8O",
    "07_ai_lab_revenues": "QISRd0Zcz9",
    "08_public_importance": "PsnlN5NCpg",
    "09_metr_uplift": "tZq8ZgClZQ",
    "10_yougov_sentiment": "zZUCcuqOun",
}

# Reverse mapping for convenience
MARKET_ID_TO_KEY = {v: k for k, v in MARKET_IDS.items()}

# API configuration
MANIFOLD_API_BASE = "https://api.manifold.markets/v0"

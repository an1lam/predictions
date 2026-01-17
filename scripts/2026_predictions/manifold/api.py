"""Manifold Markets API client."""

import os
import requests
from pathlib import Path
from typing import Any

from dotenv import load_dotenv

from .config import MANIFOLD_API_BASE


def load_api_key() -> str:
    """Load API key from .env file."""
    env_path = Path(__file__).parent.parent.parent.parent / ".env"
    load_dotenv(env_path)

    api_key = os.environ.get("MANIFOLD_API_KEY")
    if api_key:
        return api_key

    raise ValueError("MANIFOLD_API_KEY not found in .env file or environment")


class ManifoldClient:
    """Client for Manifold Markets API."""

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or load_api_key()
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Key {self.api_key}",
            "Content-Type": "application/json",
        })

    def get_market(self, market_id: str) -> dict[str, Any]:
        """Fetch market data by ID.

        Returns the full market object including answers for multiple choice.
        """
        url = f"{MANIFOLD_API_BASE}/market/{market_id}"
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def get_market_positions(self, market_id: str) -> list[dict[str, Any]]:
        """Get current positions in a market."""
        url = f"{MANIFOLD_API_BASE}/market/{market_id}/positions"
        resp = self.session.get(url)
        resp.raise_for_status()
        return resp.json()

    def place_bet(
        self,
        market_id: str,
        answer_id: str,
        amount: float,
        outcome: str = "YES",
    ) -> dict[str, Any]:
        """Place a bet on a multiple choice market.

        Args:
            market_id: The market ID
            answer_id: The answer ID to bet on
            amount: Amount in mana to bet
            outcome: "YES" to buy shares, "NO" to sell

        Returns:
            Bet confirmation response
        """
        url = f"{MANIFOLD_API_BASE}/bet"
        payload = {
            "contractId": market_id,
            "answerId": answer_id,
            "amount": int(amount),
            "outcome": outcome,
        }
        resp = self.session.post(url, json=payload)
        resp.raise_for_status()
        return resp.json()

    def get_my_bets(self, market_id: str | None = None) -> list[dict[str, Any]]:
        """Get my bets, optionally filtered by market."""
        url = f"{MANIFOLD_API_BASE}/bets"
        params = {}
        if market_id:
            params["contractId"] = market_id
        resp = self.session.get(url, params=params)
        resp.raise_for_status()
        return resp.json()


def parse_bucket_boundaries(answer_text: str, market_key: str) -> tuple[float | None, float | None]:
    """Parse bucket boundaries from answer text.

    Handles various formats:
    - "1-2 months" -> (1, 2)
    - "≥7 months" -> (7, inf)
    - "<3 months" -> (-inf, 3)
    - "35%-50%" -> (35, 50)
    - "$35B-$60B" -> (35, 60)
    - etc.

    Returns (lower, upper) bounds. None means unbounded.
    """
    import re

    text = answer_text.strip()

    # Handle percentage-point changes (YouGov sentiment)
    if "pp" in text.lower() or "percentage point" in text.lower():
        # Examples: "-30 to -20pp", "≥+10pp", "<-30pp"
        # Range pattern: "-30 to -20pp" or "-30 to -20 pp"
        range_match = re.search(r'([+-]?\d+(?:\.\d+)?)\s*(?:to|-)\s*([+-]?\d+(?:\.\d+)?)\s*pp', text, re.IGNORECASE)
        if range_match:
            val1 = float(range_match.group(1))
            val2 = float(range_match.group(2))
            return (val1, val2)

        # Boundary pattern: "<-30pp", "≥+10pp"
        boundary_match = re.search(r'([<>≤≥])\s*([+-]?\d+(?:\.\d+)?)\s*pp', text, re.IGNORECASE)
        if boundary_match:
            prefix, val = boundary_match.groups()
            val = float(val)
            if prefix in ['<', '≤']:
                return (None, val)
            elif prefix in ['>', '≥']:
                return (val, None)

    # Handle multipliers (METR uplift)
    if 'x' in text.lower():
        match = re.search(r'([<>≤≥]?)\s*(\d+(?:\.\d+)?)\s*x?\s*(?:to|-)?\s*(\d+(?:\.\d+)?)?\s*x?', text, re.IGNORECASE)
        if match:
            prefix, val1, val2 = match.groups()
            val1 = float(val1)
            if val2:
                val2 = float(val2)
                return (val1, val2)
            elif prefix in ['<', '≤']:
                return (None, val1)
            elif prefix in ['>', '≥']:
                return (val1, None)

    # Handle dollar amounts
    if '$' in text:
        match = re.search(r'\$?(\d+(?:\.\d+)?)\s*B?\s*(?:to|-)?\s*\$?(\d+(?:\.\d+)?)?', text)
        if match:
            val1 = float(match.group(1))
            val2 = float(match.group(2)) if match.group(2) else None
            if val2:
                return (val1, val2)
            # Check for ≥ or <
            if '≥' in text or '>' in text:
                return (val1, None)
            elif '<' in text or '≤' in text:
                return (None, val1)

    # Handle percentages
    if '%' in text:
        match = re.search(r'([<>≤≥]?)\s*(\d+(?:\.\d+)?)\s*%?\s*(?:to|-)?\s*(\d+(?:\.\d+)?)?\s*%?', text)
        if match:
            prefix, val1, val2 = match.groups()
            val1 = float(val1)
            if val2:
                val2 = float(val2)
                return (val1, val2)
            elif prefix in ['<', '≤']:
                return (None, val1)
            elif prefix in ['>', '≥']:
                return (val1, None)

    # Handle months
    if 'month' in text.lower():
        match = re.search(r'([<>≤≥]?)\s*(\d+(?:\.\d+)?)\s*(?:to|-)?\s*(\d+(?:\.\d+)?)?\s*month', text, re.IGNORECASE)
        if match:
            prefix, val1, val2 = match.groups()
            val1 = float(val1)
            if val2:
                val2 = float(val2)
                return (val1, val2)
            elif prefix in ['<', '≤']:
                return (None, val1)
            elif prefix in ['>', '≥']:
                return (val1, None)

    # Handle plain numbers (e.g., Epoch capabilities index)
    match = re.search(r'([<>≤≥]?)\s*(\d+(?:\.\d+)?)\s*(?:to|-)?\s*(\d+(?:\.\d+)?)?', text)
    if match:
        prefix, val1, val2 = match.groups()
        val1 = float(val1)
        if val2:
            val2 = float(val2)
            return (val1, val2)
        elif prefix in ['<', '≤']:
            return (None, val1)
        elif prefix in ['>', '≥']:
            return (val1, None)

    return (None, None)

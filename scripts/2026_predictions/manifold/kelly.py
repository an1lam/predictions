"""Kelly criterion calculations for betting."""

from dataclasses import dataclass
import numpy as np

from .config import KELLY_FRACTION, EDGE_THRESHOLD, MAX_POSITION_PCT, MIN_BET_SIZE


@dataclass
class BetRecommendation:
    """A single bet recommendation."""

    answer_id: str
    answer_text: str
    our_prob: float
    market_prob: float
    edge: float
    kelly_frac: float
    bet_amount: float
    outcome: str  # "YES" or "NO"

    @property
    def is_actionable(self) -> bool:
        """Whether this bet meets our thresholds."""
        return self.bet_amount >= MIN_BET_SIZE and abs(self.edge) >= EDGE_THRESHOLD


def kelly_fraction_for_bet(
    our_prob: float,
    market_prob: float,
    kelly_mult: float = KELLY_FRACTION,
) -> float:
    """Calculate Kelly fraction for a single bet.

    For betting YES on a bucket:
        edge = our_prob - market_prob
        kelly = edge / (1 - market_prob) * kelly_mult

    For betting NO (when we think market is too high):
        edge = market_prob - our_prob
        kelly = edge / market_prob * kelly_mult

    Returns positive fraction for amount to bet.
    """
    if our_prob > market_prob:
        # Bet YES
        edge = our_prob - market_prob
        if market_prob >= 1.0:
            return 0.0
        kelly = (edge / (1 - market_prob)) * kelly_mult
    else:
        # Bet NO
        edge = market_prob - our_prob
        if market_prob <= 0.0:
            return 0.0
        kelly = (edge / market_prob) * kelly_mult

    return max(0, kelly)


def calculate_market_edge(
    our_probs: np.ndarray,
    market_probs: np.ndarray,
) -> float:
    """Calculate total expected edge for a market.

    This is used for bankroll allocation across markets.
    Edge = sum of |our_prob - market_prob| * our_prob for all buckets
    """
    edges = np.abs(our_probs - market_probs) * our_probs
    return float(edges.sum())


def calculate_bets_for_market(
    answer_ids: list[str],
    answer_texts: list[str],
    our_probs: np.ndarray,
    market_probs: np.ndarray,
    allocation: float,
    kelly_mult: float = KELLY_FRACTION,
) -> list[BetRecommendation]:
    """Calculate all bets for a single market.

    Args:
        answer_ids: List of answer IDs from Manifold
        answer_texts: List of answer text labels
        our_probs: Our probability distribution over buckets
        market_probs: Market's probability distribution
        allocation: Total mana allocated to this market
        kelly_mult: Kelly fraction multiplier

    Returns:
        List of bet recommendations
    """
    bets = []
    max_bet = allocation * MAX_POSITION_PCT / KELLY_FRACTION  # Scale with allocation

    for i, (aid, text) in enumerate(zip(answer_ids, answer_texts)):
        our_p = our_probs[i]
        mkt_p = market_probs[i]
        edge = our_p - mkt_p

        if abs(edge) < EDGE_THRESHOLD:
            continue

        if our_p > mkt_p:
            # Bet YES on this bucket
            outcome = "YES"
            kelly = kelly_fraction_for_bet(our_p, mkt_p, kelly_mult)
        else:
            # Bet NO on this bucket
            outcome = "NO"
            kelly = kelly_fraction_for_bet(our_p, mkt_p, kelly_mult)
            edge = -edge  # Make edge positive for display

        bet_amount = min(kelly * allocation, max_bet)

        if bet_amount >= MIN_BET_SIZE:
            bets.append(BetRecommendation(
                answer_id=aid,
                answer_text=text,
                our_prob=our_p,
                market_prob=mkt_p,
                edge=our_p - mkt_p,
                kelly_frac=kelly,
                bet_amount=bet_amount,
                outcome=outcome,
            ))

    return bets


def allocate_bankroll(
    market_edges: dict[str, float],
    total_bankroll: float,
) -> dict[str, float]:
    """Allocate bankroll across markets proportionally to expected edge.

    Args:
        market_edges: Dict of market_key -> expected edge
        total_bankroll: Total mana to allocate

    Returns:
        Dict of market_key -> allocated mana
    """
    total_edge = sum(market_edges.values())
    if total_edge <= 0:
        # Equal allocation if no edge
        n_markets = len(market_edges)
        return {k: total_bankroll / n_markets for k in market_edges}

    allocations = {}
    for market_key, edge in market_edges.items():
        allocations[market_key] = (edge / total_edge) * total_bankroll

    return allocations

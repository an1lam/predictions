#!/usr/bin/env python3
"""Main orchestration for Kelly betting on Manifold Markets."""

import argparse
import json
import csv
from datetime import datetime
from pathlib import Path

import numpy as np

from .api import ManifoldClient, parse_bucket_boundaries
from .config import MARKET_IDS, TOTAL_BANKROLL, KELLY_FRACTION, EDGE_THRESHOLD
from .distributions import fit_distribution, compute_bucket_probs
from .kelly import calculate_bets_for_market, calculate_market_edge, allocate_bankroll, BetRecommendation
from .predictions import PREDICTIONS, Prediction


DATA_DIR = Path(__file__).parent.parent.parent.parent / "data" / "2026_predictions" / "manifold"


def fetch_market_data(client: ManifoldClient, market_id: str) -> dict:
    """Fetch and parse market data from Manifold."""
    market = client.get_market(market_id)
    return market


def parse_market_buckets(market: dict, prediction_key: str) -> list[tuple[str, str, float, tuple[float | None, float | None]]]:
    """Parse market answers into bucket data.

    Returns list of (answer_id, answer_text, market_prob, (lower, upper))
    """
    answers = market.get("answers", [])
    buckets = []

    for ans in answers:
        aid = ans["id"]
        text = ans.get("text", "")
        prob = ans.get("probability", 0.0)
        bounds = parse_bucket_boundaries(text, prediction_key)
        buckets.append((aid, text, prob, bounds))

    return buckets


def process_market(
    client: ManifoldClient,
    prediction_key: str,
    prediction: Prediction,
    verbose: bool = True,
) -> dict:
    """Process a single market and calculate bets.

    Returns dict with market info, our probs, market probs, and recommended bets.
    """
    market_id = MARKET_IDS[prediction_key]
    market = fetch_market_data(client, market_id)

    if verbose:
        print(f"\n{'='*60}")
        print(f"Market: {prediction.name}")
        print(f"ID: {market_id}")
        print(f"Our prediction: {prediction.median} ({prediction.p10}, {prediction.p90}) {prediction.unit}")

    # Parse buckets from market
    bucket_data = parse_market_buckets(market, prediction_key)

    if verbose:
        print(f"\nMarket buckets ({len(bucket_data)}):")
        for aid, text, prob, bounds in bucket_data:
            print(f"  {text}: {prob:.1%} (bounds: {bounds})")

    # Fit our distribution
    dist = fit_distribution(
        median=prediction.median,
        p10=prediction.p10,
        p90=prediction.p90,
        dist_type=prediction.dist_type,
        lower_bound=prediction.lower_bound,
        upper_bound=prediction.upper_bound,
    )

    # Extract bounds for bucket probability calculation
    bucket_bounds = [b[3] for b in bucket_data]
    our_probs = compute_bucket_probs(dist, bucket_bounds)
    market_probs = np.array([b[2] for b in bucket_data])

    if verbose:
        print(f"\nProbability comparison:")
        print(f"  {'Bucket':<25} {'Our':<8} {'Market':<8} {'Edge':<8}")
        print(f"  {'-'*25} {'-'*8} {'-'*8} {'-'*8}")
        for i, (aid, text, mkt_p, bounds) in enumerate(bucket_data):
            our_p = our_probs[i]
            edge = our_p - mkt_p
            edge_str = f"{edge:+.1%}" if abs(edge) >= EDGE_THRESHOLD else f"({edge:+.1%})"
            print(f"  {text[:25]:<25} {our_p:.1%}    {mkt_p:.1%}    {edge_str}")

    # Calculate expected edge for this market
    market_edge = calculate_market_edge(our_probs, market_probs)

    return {
        "prediction_key": prediction_key,
        "market_id": market_id,
        "market_name": prediction.name,
        "market_url": f"https://manifold.markets/questions/{market_id}",
        "bucket_data": bucket_data,
        "our_probs": our_probs,
        "market_probs": market_probs,
        "market_edge": market_edge,
        "distribution": {
            "type": prediction.dist_type,
            "median": prediction.median,
            "p10": prediction.p10,
            "p90": prediction.p90,
        },
    }


def run_dry_run(verbose: bool = True, bankroll: float = TOTAL_BANKROLL) -> dict:
    """Run dry-run analysis for all markets.

    Returns dict with all market analyses and bet recommendations.
    """
    client = ManifoldClient()

    print(f"Kelly Betting Dry Run")
    print(f"Bankroll: {bankroll} mana")
    print(f"Kelly fraction: {KELLY_FRACTION}")
    print(f"Edge threshold: {EDGE_THRESHOLD:.0%}")

    # Process all markets
    market_results = {}
    market_edges = {}

    for pred_key, prediction in PREDICTIONS.items():
        if pred_key not in MARKET_IDS:
            print(f"\nSkipping {pred_key}: No market ID configured")
            continue

        try:
            result = process_market(client, pred_key, prediction, verbose=verbose)
            market_results[pred_key] = result
            market_edges[pred_key] = result["market_edge"]
        except Exception as e:
            print(f"\nError processing {pred_key}: {e}")
            continue

    # Allocate bankroll
    allocations = allocate_bankroll(market_edges, bankroll)

    print(f"\n{'='*60}")
    print("BANKROLL ALLOCATION")
    print(f"{'='*60}")
    for pred_key, alloc in sorted(allocations.items(), key=lambda x: -x[1]):
        edge = market_edges.get(pred_key, 0)
        print(f"  {pred_key}: {alloc:.0f} mana (edge: {edge:.3f})")

    # Calculate bets for each market
    all_bets = []
    for pred_key, result in market_results.items():
        allocation = allocations[pred_key]

        answer_ids = [b[0] for b in result["bucket_data"]]
        answer_texts = [b[1] for b in result["bucket_data"]]

        bets = calculate_bets_for_market(
            answer_ids=answer_ids,
            answer_texts=answer_texts,
            our_probs=result["our_probs"],
            market_probs=result["market_probs"],
            allocation=allocation,
        )

        for bet in bets:
            bet_info = {
                "market_key": pred_key,
                "market_id": result["market_id"],
                "market_name": result["market_name"],
                **vars(bet),
            }
            all_bets.append(bet_info)

    # Sort bets by absolute edge
    all_bets.sort(key=lambda x: -abs(x["edge"]))

    print(f"\n{'='*60}")
    print("RECOMMENDED BETS")
    print(f"{'='*60}")

    total_bet = 0
    for bet in all_bets:
        if bet["bet_amount"] < 1:
            continue
        print(f"\n{bet['market_name']}")
        print(f"  Bucket: {bet['answer_text']}")
        print(f"  Action: {bet['outcome']} for {bet['bet_amount']:.0f} mana")
        print(f"  Our prob: {bet['our_prob']:.1%}, Market: {bet['market_prob']:.1%}, Edge: {bet['edge']:+.1%}")
        total_bet += bet["bet_amount"]

    print(f"\n{'='*60}")
    print(f"TOTAL: {total_bet:.0f} mana across {len([b for b in all_bets if b['bet_amount'] >= 1])} bets")
    print(f"{'='*60}")

    # Prepare output
    output = {
        "timestamp": datetime.now().isoformat(),
        "config": {
            "bankroll": bankroll,
            "kelly_fraction": KELLY_FRACTION,
            "edge_threshold": EDGE_THRESHOLD,
        },
        "allocations": allocations,
        "markets": {k: {
            "market_id": v["market_id"],
            "market_edge": v["market_edge"],
            "distribution": v["distribution"],
            "buckets": [
                {
                    "answer_id": b[0],
                    "text": b[1],
                    "market_prob": b[2],
                    "our_prob": float(v["our_probs"][i]),
                }
                for i, b in enumerate(v["bucket_data"])
            ],
        } for k, v in market_results.items()},
        "bets": all_bets,
        "total_bet": total_bet,
    }

    return output


def save_dry_run(output: dict):
    """Save dry-run output to JSON file."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    output_path = DATA_DIR / "bet_preview.json"

    # Convert numpy types for JSON serialization
    def convert(obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, (np.floating, np.integer)):
            return float(obj)
        return obj

    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, default=convert)

    print(f"\nDry-run saved to: {output_path}")


def execute_bets(bets: list[dict], confirm: bool = False):
    """Execute the recommended bets."""
    if not confirm:
        print("\nTo execute bets, run with --execute --confirm")
        return

    client = ManifoldClient()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    history_path = DATA_DIR / "bet_history.csv"

    # Check if history file exists
    write_header = not history_path.exists()

    with open(history_path, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "timestamp", "market_id", "market_key", "answer_id", "answer_text",
            "outcome", "amount", "our_prob", "market_prob", "edge", "response",
        ])
        if write_header:
            writer.writeheader()

        for bet in bets:
            if bet["bet_amount"] < 1:
                continue

            print(f"\nPlacing bet: {bet['outcome']} {bet['bet_amount']:.0f} on {bet['answer_text']}")

            try:
                response = client.place_bet(
                    market_id=bet["market_id"],
                    answer_id=bet["answer_id"],
                    amount=bet["bet_amount"],
                    outcome=bet["outcome"],
                )
                print(f"  Success: {response}")
                status = "success"
            except Exception as e:
                print(f"  Error: {e}")
                response = str(e)
                status = "error"

            writer.writerow({
                "timestamp": datetime.now().isoformat(),
                "market_id": bet["market_id"],
                "market_key": bet["market_key"],
                "answer_id": bet["answer_id"],
                "answer_text": bet["answer_text"],
                "outcome": bet["outcome"],
                "amount": bet["bet_amount"],
                "our_prob": bet["our_prob"],
                "market_prob": bet["market_prob"],
                "edge": bet["edge"],
                "response": status,
            })

    print(f"\nBet history saved to: {history_path}")


def main():
    parser = argparse.ArgumentParser(description="Kelly betting on Manifold Markets")
    parser.add_argument("--dry-run", action="store_true", help="Preview bets without executing")
    parser.add_argument("--execute", action="store_true", help="Execute bets")
    parser.add_argument("--confirm", action="store_true", help="Confirm execution (required with --execute)")
    parser.add_argument("--bankroll", type=float, default=TOTAL_BANKROLL, help="Override bankroll amount")
    parser.add_argument("--quiet", action="store_true", help="Less verbose output")

    args = parser.parse_args()

    if not args.dry_run and not args.execute:
        args.dry_run = True  # Default to dry-run

    output = run_dry_run(verbose=not args.quiet, bankroll=args.bankroll)
    save_dry_run(output)

    if args.execute:
        execute_bets(output["bets"], confirm=args.confirm)


if __name__ == "__main__":
    main()

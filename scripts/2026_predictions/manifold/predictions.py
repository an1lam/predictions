"""Our 2026 AI predictions with distribution parameters."""

from dataclasses import dataclass
from typing import Literal

DistType = Literal["normal", "lognormal", "truncated_normal"]


@dataclass
class Prediction:
    """A single prediction with uncertainty bounds."""

    key: str
    name: str
    median: float
    p10: float
    p90: float
    dist_type: DistType
    unit: str
    # Bounds for truncated normal
    lower_bound: float | None = None
    upper_bound: float | None = None


# All 10 predictions from the 2026 AI forecast survey
PREDICTIONS: dict[str, Prediction] = {
    "01_metr_horizon": Prediction(
        key="01_metr_horizon",
        name="METR Horizon Doubling Time",
        median=4.5,
        p10=3.0,
        p90=6.5,
        dist_type="normal",
        unit="months",
    ),
    "02_frontiermath_tier4": Prediction(
        key="02_frontiermath_tier4",
        name="FrontierMath Tier 4",
        median=62,  # percentage
        p10=40,
        p90=85,
        dist_type="normal",
        unit="percent",
    ),
    "03_remote_labor_index": Prediction(
        key="03_remote_labor_index",
        name="Remote Labor Index",
        median=18,  # percentage
        p10=8,
        p90=35,
        dist_type="lognormal",
        unit="percent",
    ),
    "04_openai_proof_qa": Prediction(
        key="04_openai_proof_qa",
        name="OpenAI-Proof Q&A",
        median=37,  # percentage
        p10=18,
        p90=55,
        dist_type="normal",
        unit="percent",
    ),
    "05_gsobench": Prediction(
        key="05_gsobench",
        name="GSOBench",
        median=74,  # percentage
        p10=45,
        p90=95,
        dist_type="truncated_normal",
        unit="percent",
        lower_bound=0,
        upper_bound=100,
    ),
    "06_epoch_capabilities": Prediction(
        key="06_epoch_capabilities",
        name="Epoch Capabilities Index",
        median=177,
        p10=160,
        p90=195,
        dist_type="normal",
        unit="index",
    ),
    "07_ai_lab_revenues": Prediction(
        key="07_ai_lab_revenues",
        name="AI Lab Revenues",
        median=60,  # billions USD
        p10=35,
        p90=90,
        dist_type="lognormal",
        unit="billion_usd",
    ),
    "08_public_importance": Prediction(
        key="08_public_importance",
        name="Public Importance (Most Important Problem)",
        median=1.0,  # percentage
        p10=0.3,
        p90=8.0,
        dist_type="lognormal",
        unit="percent",
    ),
    "09_metr_uplift": Prediction(
        key="09_metr_uplift",
        name="METR Uplift Study",
        median=1.4,  # multiplier
        p10=0.90,
        p90=2.2,
        dist_type="lognormal",
        unit="multiplier",
    ),
    "10_yougov_sentiment": Prediction(
        key="10_yougov_sentiment",
        name="YouGov Sentiment (Net Change)",
        median=-14,  # percentage points
        p10=-40,
        p90=15,
        dist_type="normal",  # Can be negative, so normal not lognormal
        unit="pp",  # percentage points
    ),
}


def get_prediction(key: str) -> Prediction:
    """Get a prediction by key."""
    if key not in PREDICTIONS:
        raise KeyError(f"Unknown prediction key: {key}")
    return PREDICTIONS[key]

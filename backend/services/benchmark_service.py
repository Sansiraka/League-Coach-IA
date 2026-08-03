import json
import os
from typing import Dict, Any

class BenchmarkService:
    def __init__(self):
        # Load benchmarks from JSON file
        benchmarks_path = os.path.join(os.path.dirname(__file__), "..", "data", "role_benchmarks.json")
        try:
            with open(benchmarks_path, "r") as f:
                self.benchmarks = json.load(f)
        except Exception as e:
            print(f"Error loading benchmarks: {e}")
            self.benchmarks = {}

    def _get_verdict(self, value: float, good_threshold: float, great_threshold: float, is_lower_better: bool = False) -> str:
        if value is None:
            return "UNKNOWN"
            
        if not is_lower_better:
            if value >= great_threshold:
                return "EXCEEDS_STANDARD"
            elif value >= good_threshold:
                return "MEETS_STANDARD"
            else:
                return "BELOW_STANDARD"
        else:
            if value <= great_threshold:
                return "EXCEEDS_STANDARD"
            elif value <= good_threshold:
                return "MEETS_STANDARD"
            else:
                return "BELOW_STANDARD"

    def evaluate_metrics(self, role: str, metrics: Dict[str, float]) -> Dict[str, Any]:
        """
        Evaluates a set of metrics against the benchmarks for a given role.
        """
        # Ensure role exists in benchmarks, fallback to UNKNOWN
        role_key = role.upper() if role else "UNKNOWN"
        if role_key not in self.benchmarks:
            role_key = "UNKNOWN"
            
        role_benchmarks = self.benchmarks.get(role_key, {})
        evaluation = {}

        for metric_name, value in metrics.items():
            if metric_name in role_benchmarks:
                thresholds = role_benchmarks[metric_name]
                good = thresholds.get("good", 0)
                great = thresholds.get("great", 0)
                
                # CS/min is not relevant for support
                if role_key == "UTILITY" and metric_name == "cs_per_min":
                    continue
                    
                verdict = self._get_verdict(value, good, great)
                
                evaluation[metric_name] = {
                    "value": value,
                    "target_good": good,
                    "target_great": great,
                    "verdict": verdict
                }

        return evaluation

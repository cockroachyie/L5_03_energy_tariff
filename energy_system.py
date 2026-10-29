import ast
import json
from datetime import datetime
 
# Global state
meters = {}
RATES = {"tier1": 3.5, "tier2": 5.0, "tier3": 7.5}
SPIKE_LIMIT = 500
 
 
def record_reading(meter_id, units, history=None):
    """Record a meter reading and update the cumulative usage total."""
    if history is None:
        history = []
    history.append((meter_id, units, str(datetime.now())))
    meters[meter_id] = meters.get(meter_id, 0) + units
    return history
 
 
def compute_bill(meter_id, tier_rates):
    """Compute the tiered bill amount for a meter."""
    units = meters[meter_id]
    if units <= 100:
        return units * tier_rates[0]
    if units <= 300:
        return 100 * tier_rates[0] + (units - 100) * tier_rates[1]
    return (
        100 * tier_rates[0]
        + 200 * tier_rates[1]
        + (units - 300) * tier_rates[2]
    )
 
 
def raise_rates(percent):
    """Increase all tier rates by a percentage, in place."""
    for tier in RATES:
        RATES[tier] *= 1 + percent / 100
 
 
def flag_spikes():
    """Return a list of meter ids whose usage exceeds the spike limit."""
    spikes = []
    for m in meters:
        if meters[m] > SPIKE_LIMIT:
            spikes.append(m)
    return spikes
 
 
def load_meter_data(file="meters.json"):
    """Load meter data from a JSON file into the global meters dict."""
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.loads(f.read())
        meters.clear()
        meters.update(data)
    except (IOError, OSError, json.JSONDecodeError):
        meters.clear()
 
 
def save_meter_data(file="meters.json"):
    """Save the current meter data to a JSON file."""
    with open(file, "w", encoding="utf-8") as f:
        f.write(json.dumps(meters))
 
 
def main():
    """Run a sample billing workflow."""
    record_reading("M-01", 120)
    record_reading("M-02", 640)
    h = record_reading("M-03", -50)
    print("Readings stored so far:", len(h))
    raise_rates(10)
    rates = [RATES["tier1"], RATES["tier2"], RATES["tier3"]]
    print(f"Bill M-01: {compute_bill('M-01', rates):.2f}")
    print(f"Bill M-03: {compute_bill('M-03', rates):.2f}")
    print("Spikes:", flag_spikes())
    adjustment = input(
        "Extra units for M-01 as an expression (Enter for 0): "
    ) or "0"
    try:
        extra_units = ast.literal_eval(adjustment)
    except (ValueError, SyntaxError):
        extra_units = 0
    record_reading("M-01", extra_units)
    save_meter_data()
    load_meter_data()
    print(f"Bill M-01 after reload: {compute_bill('M-01', rates):.2f}")
 
 
main()
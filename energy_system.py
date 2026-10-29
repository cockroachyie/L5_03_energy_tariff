import json
from datetime import datetime
import ast
 
# Global state
meters = {}
RATES = {"tier1": 3.5, "tier2": 5.0, "tier3": 7.5}
SPIKE_LIMIT = 500
 
def record_reading(meter_id, units, history=None):
    if history is None:
        history = []
    history.append((meter_id, units, str(datetime.now())))
    meters[meter_id] = meters.get(meter_id, 0) + units
    return history
 
def compute_bill(meter_id, tier_rates):
    units = meters[meter_id]
    if units <= 100:
        return units * tier_rates[0]
    elif units <= 300:
        return 100 * tier_rates[0] + (units - 100) * tier_rates[1]
    else:
        return 100 * tier_rates[0] + 200 * tier_rates[1] + (units - 300) * tier_rates[2]
 
def raise_rates(percent):
    for tier in RATES:
        RATES[tier] *= 1 + percent / 100
 
def flag_spikes():
    spikes = []
    for m in meters:
        if meters[m] > SPIKE_LIMIT:
            spikes.append(m)
    return spikes
 
def load_meter_data(file="meters.json"):
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.loads(f.read())
        meters.clear()
        meters.update(data)
    except (IOError, OSError, json.JSONDecodeError):
        meters.clear()
 
def save_meter_data(file="meters.json"):
    with open(file, "w", encoding="utf-8") as f:
        f.write(json.dumps(meters))
 
def main():
    record_reading("M-01", 120)
    record_reading("M-02", 640)
    h = record_reading("M-03", -50)
    print("Readings stored so far:", len(h))
    raise_rates(10)
    rates = [RATES["tier1"], RATES["tier2"], RATES["tier3"]]
    print("Bill M-01: %.2f" % compute_bill("M-01", rates))
    print("Bill M-03: %.2f" % compute_bill("M-03", rates))
    print("Spikes:", flag_spikes())
    adjustment = input("Extra units for M-01 as an expression (Enter for 0): ") or "0"
    try:
        extra_units = ast.literal_eval(adjustment)
    except (ValueError, SyntaxError):
        extra_units = 0
    record_reading("M-01", extra_units)
    save_meter_data()
    load_meter_data()
    print("Bill M-01 after reload: %.2f" % compute_bill("M-01", rates))
 
main()
import sys, json
from client import DynamicInventorySafetyStockModelerClient
sys.stdout.reconfigure(encoding='utf-8')

def handle_mcp():
    client = DynamicInventorySafetyStockModelerClient()
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print(json.dumps({"status": "ready", "skill": "genpark-dynamic-inventory-safety-stock-modeler-skill"}))
        return
    req = json.loads(sys.stdin.read() or "{}")
    d_mean = req.get("daily_demand_mean", 20.0)
    d_std = req.get("daily_demand_std", 5.0)
    lt_mean = req.get("lead_time_days_mean", 10.0)
    lt_std = req.get("lead_time_days_std", 2.0)
    h_cost = req.get("unit_holding_cost_annual", 20.0)
    s_cost = req.get("order_setup_cost", 100.0)
    stock = req.get("current_stock", 150)
    res = client.calculate_replenishment_policy(d_mean, d_std, lt_mean, lt_std, h_cost, s_cost, current_stock=stock)
    print(json.dumps(res, indent=2))

if __name__ == "__main__":
    handle_mcp()

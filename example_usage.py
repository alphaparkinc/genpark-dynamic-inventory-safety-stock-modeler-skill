from client import DynamicInventorySafetyStockModelerClient
import json, sys
sys.stdout.reconfigure(encoding='utf-8')

def main():
    client = DynamicInventorySafetyStockModelerClient()
    print("=== DYNAMIC INVENTORY SAFETY STOCK MODELER ===")
    
    # Scenario: High-volume Robot Vacuum hardware SKU
    # 25 units/day (std=6), 14-day lead time (std=2.5 days), holding cost $45/yr, setup cost $250
    res = client.calculate_replenishment_policy(
        daily_demand_mean=25.0,
        daily_demand_std=6.0,
        lead_time_days_mean=14.0,
        lead_time_days_std=2.5,
        unit_holding_cost_annual=45.0,
        order_setup_cost=250.0,
        target_service_level=0.98,
        current_stock=280,
        in_transit_stock=50
    )
    
    print(f"Replenishment Policy (Service Level: {res['target_service_level_pct']}%):")
    print(f"  - Safety Stock: {res['safety_stock_units']} units")
    print(f"  - Reorder Point (ROP): {res['reorder_point_units']} units")
    print(f"  - EOQ Batch: {res['economic_order_quantity_units']} units")
    print(f"  - Current Position: {res['current_inventory_position']} units")
    print(f"  - Reorder Triggered: {res['reorder_triggered']} (Stockout Risk: {res['estimated_stockout_risk_pct']}%)")
    if res['reorder_triggered']:
        print(f"  -> Recommended Purchase Order: {res['recommended_order_quantity']} units")

if __name__ == "__main__":
    main()

import math, sys
sys.stdout.reconfigure(encoding='utf-8')

class DynamicInventorySafetyStockModelerClient:
    """
    Supply chain inventory replenishment modeler. Computes stochastic safety stock,
    reorder point (ROP), Economic Order Quantity (EOQ), and stockout risk probabilities.
    """
    def __init__(self):
        # Standard normal inverse CDF Z values for common service levels
        self.service_z = {
            0.90: 1.282,
            0.95: 1.645,
            0.98: 2.054,
            0.99: 2.326,
            0.995: 2.576
        }

    def get_z_factor(self, service_level):
        for lvl in sorted(self.service_z.keys(), reverse=True):
            if service_level >= lvl:
                return self.service_z[lvl]
        return 1.282

    def calculate_replenishment_policy(
        self,
        daily_demand_mean,
        daily_demand_std,
        lead_time_days_mean,
        lead_time_days_std,
        unit_holding_cost_annual,
        order_setup_cost,
        target_service_level=0.95,
        current_stock=0,
        in_transit_stock=0
    ):
        z = self.get_z_factor(target_service_level)
        
        # Stochastic Safety Stock formula:
        # SS = Z * sqrt( (LT_mean * sigma_D^2) + (D_mean^2 * sigma_LT^2) )
        var_demand_during_lt = (lead_time_days_mean * (daily_demand_std ** 2)) + ((daily_demand_mean ** 2) * (lead_time_days_std ** 2))
        safety_stock = int(math.ceil(z * math.sqrt(max(0.1, var_demand_during_lt))))

        # Reorder Point (ROP) = Mean Demand during Lead Time + Safety Stock
        mean_demand_lead_time = daily_demand_mean * lead_time_days_mean
        reorder_point = int(math.ceil(mean_demand_lead_time + safety_stock))

        # Annual Demand (assuming 365 days)
        annual_demand = daily_demand_mean * 365.0
        
        # Economic Order Quantity: EOQ = sqrt( (2 * D * S) / H )
        eoq = int(math.ceil(math.sqrt((2.0 * annual_demand * order_setup_cost) / max(0.01, unit_holding_cost_annual))))

        # Current Inventory Position = On-hand + In-transit
        inventory_position = current_stock + in_transit_stock
        needs_reorder = inventory_position <= reorder_point
        recommended_order_qty = max(eoq, reorder_point - inventory_position + eoq) if needs_reorder else 0

        # Estimated Stockout Probability given current stock
        shortfall = reorder_point - inventory_position
        stockout_prob = min(0.99, max(0.01, 1.0 - (inventory_position / max(1.0, reorder_point)))) if shortfall > 0 else (1.0 - target_service_level)

        return {
            "status": "success",
            "daily_demand_mean": daily_demand_mean,
            "lead_time_days_mean": lead_time_days_mean,
            "target_service_level_pct": target_service_level * 100.0,
            "safety_stock_units": safety_stock,
            "reorder_point_units": reorder_point,
            "economic_order_quantity_units": eoq,
            "current_inventory_position": inventory_position,
            "reorder_triggered": needs_reorder,
            "recommended_order_quantity": recommended_order_qty,
            "estimated_stockout_risk_pct": round(stockout_prob * 100.0, 2)
        }

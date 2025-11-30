
from typing import Any, Dict, List
from collections import defaultdict
from datetime import timedelta
import config
import utils

def _calculate_cost_analysis(logs: List[Dict[str, Any]], endpoint_stats: List[Dict[str, Any]]) -> Dict[str, Any]:
   
    total_request_cost = len(logs) * config.COST_STRUCTURE["per_request"]
    total_execution_cost = sum(log["response_time_ms"] * config.COST_STRUCTURE["per_ms_execution"] for log in logs)
    
    total_memory_cost = 0.0
    for log in logs:
        size_kb = log["response_size_bytes"] / 1024
        if size_kb <= 1:
            total_memory_cost += config.COST_STRUCTURE["memory_costs"]["small"]
        elif size_kb <= 10:
            total_memory_cost += config.COST_STRUCTURE["memory_costs"]["medium"]
        else:
            total_memory_cost += config.COST_STRUCTURE["memory_costs"]["large"]
    
    total_cost = total_request_cost + total_execution_cost + total_memory_cost
    
    # Calculate per-endpoint costs
    cost_by_endpoint = []
    for stats in endpoint_stats:
        endpoint_logs = [log for log in logs if log["endpoint"] == stats["endpoint"]]
        
        ep_request_cost = len(endpoint_logs) * config.COST_STRUCTURE["per_request"]
        ep_exec_cost = sum(log["response_time_ms"] * config.COST_STRUCTURE["per_ms_execution"] for log in endpoint_logs)
        
        ep_memory_cost = 0.0
        for log in endpoint_logs:
            size_kb = log["response_size_bytes"] / 1024
            if size_kb <= 1:
                ep_memory_cost += config.COST_STRUCTURE["memory_costs"]["small"]
            elif size_kb <= 10:
                ep_memory_cost += config.COST_STRUCTURE["memory_costs"]["medium"]
            else:
                ep_memory_cost += config.COST_STRUCTURE["memory_costs"]["large"]
        
        ep_total = ep_request_cost + ep_exec_cost + ep_memory_cost
        
        cost_by_endpoint.append({
            "endpoint": stats["endpoint"],
            "total_cost": round(ep_total, 2),
            "cost_per_request": round(ep_total / stats["request_count"], 4)
        })
    
    cost_by_endpoint.sort(key=lambda x: x["total_cost"], reverse=True)
    
    # Calculate optimization potential (70% savings on cacheable endpoints)
    optimization_potential_usd = 0.0
    for stats in endpoint_stats:
        endpoint_logs = [log for log in logs if log["endpoint"] == stats["endpoint"]]
        get_count = sum(1 for log in endpoint_logs if log["method"] == "GET")
        get_pct = utils.safe_divide(get_count * 100, len(endpoint_logs))
        
        if get_pct >= 80 and len(endpoint_logs) >= 50:
            ep_cost = next((e["total_cost"] for e in cost_by_endpoint if e["endpoint"] == stats["endpoint"]), 0)
            optimization_potential_usd += ep_cost * 0.7
    
    return {
        "total_cost_usd": round(total_cost, 2),
        "cost_breakdown": {
            "request_costs": round(total_request_cost, 2),
            "execution_costs": round(total_execution_cost, 2),
            "memory_costs": round(total_memory_cost, 2)
        },
        "cost_by_endpoint": cost_by_endpoint,
        "optimization_potential_usd": round(optimization_potential_usd, 2)
    }



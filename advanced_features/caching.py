import config
import utils
from typing import Any, Dict, List
def _analyze_caching_opportunities(logs: List[Dict[str, Any]], endpoint_stats: List[Dict[str, Any]]) -> Dict[str, Any]:
   
    caching_opportunities = []
    total_requests_eliminated = 0
    total_cost_savings_usd = 0.0
    total_performance_improvement_ms = 0.0
    
    for stats in endpoint_stats:
        endpoint_logs = [log for log in logs if log["endpoint"] == stats["endpoint"]]
        get_count = sum(1 for log in endpoint_logs if log["method"] == "GET")
        get_pct = utils.safe_divide(get_count * 100, len(endpoint_logs))
        error_rate = utils.safe_divide(stats["error_count"] * 100, stats["request_count"])
        
        # Check caching criteria
        if (stats["request_count"] >= config.CACHING_CRITERIA["min_request_count"] and
            get_pct >= config.CACHING_CRITERIA["min_get_percentage"] and
            error_rate < config.CACHING_CRITERIA["max_error_rate"]):
            
            # Calculate potential cache hit rate
            potential_cache_hit_rate = min(95, get_pct)
            
            # Calculate potential requests saved
            potential_requests_saved = int(stats["request_count"] * (potential_cache_hit_rate / 100))
            
            # Calculate cost savings
            cost_per_request = (config.COST_STRUCTURE["per_request"] + 
                              stats["avg_response_time_ms"] * config.COST_STRUCTURE["per_ms_execution"])
            estimated_cost_savings_usd = potential_requests_saved * cost_per_request
            
            # Determine confidence level
            if get_pct > 90 and stats["request_count"] > 500:
                recommendation_confidence = "high"
            elif get_pct > 85 and stats["request_count"] > 200:
                recommendation_confidence = "medium"
            else:
                recommendation_confidence = "low"
            
            caching_opportunities.append({
                "endpoint": stats["endpoint"],
                "potential_cache_hit_rate": int(round(potential_cache_hit_rate, 0)),
                "current_requests": stats["request_count"],
                "potential_requests_saved": potential_requests_saved,
                "estimated_cost_savings_usd": round(estimated_cost_savings_usd, 2),
                "recommended_ttl_minutes": config.CACHING_CRITERIA["recommended_ttl_minutes"],
                "recommendation_confidence": recommendation_confidence
            })
            
            # Add to totals
            total_requests_eliminated += potential_requests_saved
            total_cost_savings_usd += estimated_cost_savings_usd
            total_performance_improvement_ms += potential_requests_saved * stats["avg_response_time_ms"]
    
    # Sort by cost savings descending
    caching_opportunities.sort(key=lambda x: x["estimated_cost_savings_usd"], reverse=True)
    
    return {
        "caching_opportunities": caching_opportunities,
        "total_potential_savings": {
            "requests_eliminated": total_requests_eliminated,
            "cost_savings_usd": round(total_cost_savings_usd, 2),
            "performance_improvement_ms": int(round(total_performance_improvement_ms, 0))
        }
    }


from typing import Any, Dict, List, Tuple
from collections import defaultdict
from datetime import datetime
import config
import utils

def _calculate_summary(logs: List[Dict[str, Any]]) -> Dict[str, Any]:
    
    total_requests = len(logs)
    
    # Find time range
    timestamps = [utils.parse_timestamp(log["timestamp"]) for log in logs]
    start_time = min(timestamps)
    end_time = max(timestamps)
    
    # Calculate average response time
    total_response_time = sum(log["response_time_ms"] for log in logs)
    avg_response_time = utils.safe_divide(total_response_time, total_requests)
    
    # Calculate error rate
    error_count = sum(1 for log in logs if utils.is_error_status(log["status_code"]))
    error_rate = utils.safe_divide(error_count * 100, total_requests)
    
    return {
        "total_requests": total_requests,
        "time_range": {
            "start": start_time.isoformat().replace('+00:00', 'Z'),
            "end": end_time.isoformat().replace('+00:00', 'Z')
        },
        "avg_response_time_ms": round(avg_response_time, 1),
        "error_rate_percentage": round(error_rate, 1)
    }
    
def analyse_logs_between(logs: List[Dict[str, Any]], start: datetime, end: datetime) -> List[Dict[str, Any]]:
    logs = [log for log in logs if start <= utils.parse_timestamp(log["timestamp"]) <= end]
    
    
def _calculate_endpoint_stats(logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    
    
    # Group logs by endpoint
    endpoint_logs = defaultdict(list)
    for log in logs:
        endpoint_logs[log["endpoint"]].append(log)
    
    # Calculate stats for each endpoint
    endpoint_stats = []
    for endpoint, endpoint_log_list in endpoint_logs.items():
        stats = _calculate_single_endpoint_stats(endpoint, endpoint_log_list)
        endpoint_stats.append(stats)
    
    # Sort by request count (descending)
    endpoint_stats.sort(key=lambda x: x["request_count"], reverse=True)
    
    return endpoint_stats    

def _detect_performance_issues(
    endpoint_stats: List[Dict[str, Any]], 
    summary: Dict[str, Any]
) -> List[Dict[str, Any]]:
 
    issues = []
    
    for stats in endpoint_stats:
        endpoint = stats["endpoint"]
        avg_time = stats["avg_response_time_ms"]
        request_count = stats["request_count"]
        error_count = stats["error_count"]
        
        # Check for slow endpoints
        severity = utils.calculate_severity(avg_time, config.PERFORMANCE_THRESHOLDS)
        if severity in ["medium", "high", "critical"]:
            issues.append({
                "type": "slow_endpoint",
                "endpoint": endpoint,
                "avg_response_time_ms": avg_time,
                "threshold_ms": config.PERFORMANCE_THRESHOLDS["medium"],
                "severity": severity
            })
        
        # Check for high error rates
        error_rate = utils.safe_divide(error_count * 100, request_count)
        error_severity = utils.calculate_severity(error_rate, config.ERROR_RATE_THRESHOLDS)
        if error_severity in ["medium", "high", "critical"]:
            issues.append({
                "type": "high_error_rate",
                "endpoint": endpoint,
                "error_rate_percentage": round(error_rate, 1),
                "severity": error_severity
            })
    
    # Sort by severity (critical first)
    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    issues.sort(key=lambda x: severity_order.get(x["severity"], 999))
    
    return issues

def _generate_recommendations(
    endpoint_stats: List[Dict[str, Any]], 
    summary: Dict[str, Any],
    logs: List[Dict[str, Any]]
) -> List[str]:
   
    recommendations = []
    
    for stats in endpoint_stats:
        endpoint = stats["endpoint"]
        avg_time = stats["avg_response_time_ms"]
        request_count = stats["request_count"]
        error_count = stats["error_count"]
        error_rate = utils.safe_divide(error_count * 100, request_count)
        
        # Recommendation for slow endpoints
        if avg_time > config.PERFORMANCE_THRESHOLDS["medium"]:
            recommendations.append(
                f"Investigate {endpoint} performance (avg {avg_time:.0f}ms exceeds "
                f"{config.PERFORMANCE_THRESHOLDS['medium']}ms threshold)"
            )
        
        # Recommendation for high error rates
        if error_rate > config.ERROR_RATE_THRESHOLDS["medium"]:
            recommendations.append(
                f"Alert: {endpoint} has {error_rate:.1f}% error rate"
            )
        
        # Recommendation for caching potential
        endpoint_logs = [log for log in logs if log["endpoint"] == endpoint]
        get_count = sum(1 for log in endpoint_logs if log["method"] == "GET")
        get_percentage = utils.safe_divide(get_count * 100, len(endpoint_logs))
        
        if (request_count >= config.CACHING_CRITERIA["min_request_count"] and 
            get_percentage >= config.CACHING_CRITERIA["min_get_percentage"] and
            error_rate < config.CACHING_CRITERIA["max_error_rate"]):
            recommendations.append(
                f"Consider caching for {endpoint} ({request_count} requests, "
                f"{get_percentage:.0f}% cache-hit potential)"
            )
    
    if not recommendations:
        recommendations.append("All endpoints performing within acceptable parameters")
    
    return recommendations

def _calculate_hourly_distribution(logs: List[Dict[str, Any]]) -> Dict[str, int]:
  
    hourly_counts = defaultdict(int)
    
    for log in logs:
        hour_key = utils.get_hour_key(log["timestamp"])
        hourly_counts[hour_key] += 1
    
    # Sort by hour
    return dict(sorted(hourly_counts.items()))

def _calculate_top_users(logs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
   
    user_counts = defaultdict(int)
    
    for log in logs:
        user_counts[log["user_id"]] += 1
    
    # Sort by count and get top N
    top_users = [
        {"user_id": user_id, "request_count": count}
        for user_id, count in sorted(user_counts.items(), key=lambda x: x[1], reverse=True)
    ]
    
    return top_users[:config.TOP_USERS_LIMIT]

def _calculate_single_endpoint_stats(endpoint: str, logs: List[Dict[str, Any]]) -> Dict[str, Any]:
    
    request_count = len(logs)
    
    # Response time statistics
    response_times = [log["response_time_ms"] for log in logs]
    avg_response_time = utils.safe_divide(sum(response_times), request_count)
    slowest_request = max(response_times)
    fastest_request = min(response_times)
    
    # Error statistics
    error_count = sum(1 for log in logs if utils.is_error_status(log["status_code"]))
    
    # Most common status code
    status_counts = defaultdict(int)
    for log in logs:
        status_counts[log["status_code"]] += 1
    most_common_status = max(status_counts.items(), key=lambda x: x[1])[0]
    
    return {
        "endpoint": endpoint,
        "request_count": request_count,
        "avg_response_time_ms": round(avg_response_time),
        "slowest_request_ms": slowest_request,
        "fastest_request_ms": fastest_request,
        "error_count": error_count,
        "most_common_status": most_common_status
    }

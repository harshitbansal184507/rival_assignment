from datetime import datetime
from typing import Any, Dict, List
import config


def is_error_status(status_code: int) -> bool:
    return status_code in config.ERROR_STATUS_CODES


def parse_timestamp(timestamp_str: str) -> datetime:
    """
    Parse ISO format timestamp string to datetime object.
    
    Args:
        timestamp_str: ISO format timestamp (e.g., "2025-01-15T10:30:00Z")
        
    Returns:
        datetime object
        
    Raises:
        ValueError: If timestamp format is invalid
    """
    try:
        if timestamp_str.endswith('Z'):
            timestamp_str = timestamp_str[:-1] + '+00:00'
        return datetime.fromisoformat(timestamp_str)
    except Exception as e:
        raise ValueError(f"Invalid timestamp format: {timestamp_str}") from e


def get_hour_key(timestamp_str: str) -> str:
  
    dt = parse_timestamp(timestamp_str)
    return dt.strftime("%H:00")


def validate_log_entry(log: Dict[str, Any]) -> bool:
   
    required_fields = [
        "timestamp", "endpoint", "method", "response_time_ms",
        "status_code", "user_id", "request_size_bytes", "response_size_bytes"
    ]
    for field in required_fields:
        if field not in log:
            return False
    
    try:
        # Timestamp should be parseable
        parse_timestamp(log["timestamp"])
        
        # Numeric fields should be non-negative
        if log["response_time_ms"] < 0:
            return False
        if log["status_code"] < 100 or log["status_code"] > 599:
            return False
        if log["request_size_bytes"] < 0:
            return False
        if log["response_size_bytes"] < 0:
            return False
            
        # Strings should not be empty
        if not log["endpoint"] or not log["user_id"] or not log["method"]:
            return False
            
        return True
    except (ValueError, TypeError):
        return False


def calculate_severity(value: float, thresholds: Dict[str, float]) -> str:
    
    if value > thresholds.get("critical", float('inf')):
        return "critical"
    elif value > thresholds.get("high", float('inf')):
        return "high"
    elif value > thresholds.get("medium", float('inf')):
        return "medium"
    else:
        return "low"


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
   
    if denominator == 0:
        return default
    return numerator / denominator



def _create_empty_report() -> Dict[str, Any]:
   
    return {
        "summary": {
            "total_requests": 0,
            "time_range": {
                "start": None,
                "end": None
            },
            "avg_response_time_ms": 0.0,
            "error_rate_percentage": 0.0
        },
        "endpoint_stats": [],
        "performance_issues": [],
        "recommendations": ["No valid log entries to analyze"],
        "hourly_distribution": {},
        "top_users_by_requests": []
    }
    
    

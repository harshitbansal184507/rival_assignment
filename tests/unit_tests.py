import pytest
import sys

sys.path.append("C:\\Users\\harshit_work\Desktop\\web projects\\rival_assignment")
from main import analyze_api_logs


def test_summary_calculation():
    logs = [
        {
            "timestamp": "2025-01-15T10:00:00Z",
            "endpoint": "/api/test",
            "method": "GET",
            "response_time_ms": 100,
            "status_code": 200,
            "user_id": "user_001",
            "request_size_bytes": 256,
            "response_size_bytes": 1024
        },
        {
            "timestamp": "2025-01-15T10:05:00Z",
            "endpoint": "/api/test",
            "method": "GET",
            "response_time_ms": 200,
            "status_code": 500,
            "user_id": "user_001",
            "request_size_bytes": 256,
            "response_size_bytes": 1024
        }
    ]
    
    result = analyze_api_logs(logs)
    
    assert result["summary"]["total_requests"] == 2
    assert result["summary"]["avg_response_time_ms"] == 150.0
    assert result["summary"]["error_rate_percentage"] == 50.0

def test_endpoint_stats():
    logs = [
        {
            "timestamp": "2025-01-15T10:00:00Z",
            "endpoint": "/api/users",
            "method": "GET",
            "response_time_ms": 100,
            "status_code": 200,
            "user_id": "user_001",
            "request_size_bytes": 256,
            "response_size_bytes": 1024
        },
        {
            "timestamp": "2025-01-15T10:01:00Z",
            "endpoint": "/api/users",
            "method": "GET",
            "response_time_ms": 200,
            "status_code": 200,
            "user_id": "user_001",
            "request_size_bytes": 256,
            "response_size_bytes": 1024
        }
    ]
    
    result = analyze_api_logs(logs)
    
    assert len(result["endpoint_stats"]) == 1
    stats = result["endpoint_stats"][0]
    
    assert stats["endpoint"] == "/api/users"
    assert stats["request_count"] == 2
    assert stats["avg_response_time_ms"] == 150.0
    assert stats["slowest_request_ms"] == 200
    assert stats["fastest_request_ms"] == 100

def test_performance_issue_detection():
    logs = [
        {
            "timestamp": "2025-01-15T10:00:00Z",
            "endpoint": "/api/slow",
            "method": "GET",
            "response_time_ms": 2500,  # Very slow
            "status_code": 200,
            "user_id": "user_001",
            "request_size_bytes": 256,
            "response_size_bytes": 1024
        }
    ]
    
    result = analyze_api_logs(logs)
    
    assert len(result["performance_issues"]) > 0
    assert any(issue["endpoint"] == "/api/slow" for issue in result["performance_issues"])

def test_error_rate_detection():
    """Test high error rate detection"""
    logs = []
    
    for i in range(10):
        logs.append({
            "timestamp": f"2025-01-15T10:{str(i).zfill(2)}:00Z",
            "endpoint": "/api/errors",
            "method": "POST",
            "response_time_ms": 100,
            "status_code": 500 if i < 8 else 200,  
            "user_id": "user_001",
            "request_size_bytes": 512,
            "response_size_bytes": 256
        })
    
    result = analyze_api_logs(logs)
    
    error_issues = [i for i in result["performance_issues"] if i["type"] == "high_error_rate"]
    assert len(error_issues) > 0

def test_hourly_distribution():
    logs = [
        {
            "timestamp": "2025-01-15T10:00:00Z",
            "endpoint": "/api/test",
            "method": "GET",
            "response_time_ms": 100,
            "status_code": 200,
            "user_id": "user_001",
            "request_size_bytes": 256,
            "response_size_bytes": 1024
        },
        {
            "timestamp": "2025-01-15T10:30:00Z",
            "endpoint": "/api/test",
            "method": "GET",
            "response_time_ms": 100,
            "status_code": 200,
            "user_id": "user_001",
            "request_size_bytes": 256,
            "response_size_bytes": 1024
        },
        {
            "timestamp": "2025-01-15T11:00:00Z",
            "endpoint": "/api/test",
            "method": "GET",
            "response_time_ms": 100,
            "status_code": 200,
            "user_id": "user_001",
            "request_size_bytes": 256,
            "response_size_bytes": 1024
        }
    ]
    
    result = analyze_api_logs(logs)
    
    assert "10:00" in result["hourly_distribution"]
    assert result["hourly_distribution"]["10:00"] == 2
    assert result["hourly_distribution"]["11:00"] == 1

def test_top_users():
    logs = []
    
    for i in range(5):
        logs.append({
            "timestamp": f"2025-01-15T10:{str(i).zfill(2)}:00Z",
            "endpoint": "/api/test",
            "method": "GET",
            "response_time_ms": 100,
            "status_code": 200,
            "user_id": "user_001",
            "request_size_bytes": 256,
            "response_size_bytes": 1024
        })
    
    for i in range(3):
        logs.append({
            "timestamp": f"2025-01-15T10:{str(i+10).zfill(2)}:00Z",
            "endpoint": "/api/test",
            "method": "GET",
            "response_time_ms": 100,
            "status_code": 200,
            "user_id": "user_002",
            "request_size_bytes": 256,
            "response_size_bytes": 1024
        })
    
    result = analyze_api_logs(logs)
    
    assert len(result["top_users_by_requests"]) == 2
    assert result["top_users_by_requests"][0]["user_id"] == "user_001"
    assert result["top_users_by_requests"][0]["request_count"] == 5


def test_cost_analysis():
    logs = [
        {
            "timestamp": "2025-01-15T10:00:00Z",
            "endpoint": "/api/test",
            "method": "GET",
            "response_time_ms": 100,
            "status_code": 200,
            "user_id": "user_001",
            "request_size_bytes": 256,
            "response_size_bytes": 1024
        }
        
    ]
    
    result = analyze_api_logs(logs)
    
    assert "cost_analysis" in result
    assert "total_cost_usd" in result["cost_analysis"]
    assert "cost_breakdown" in result["cost_analysis"]

def test_recommendations_generated():
    logs = [
        {
            "timestamp": "2025-01-15T10:00:00Z",
            "endpoint": "/api/test",
            "method": "GET",
            "response_time_ms": 100,
            "status_code": 200,
            "user_id": "user_001",
            "request_size_bytes": 256,
            "response_size_bytes": 1024
        }
    ]
    
    result = analyze_api_logs(logs)
    
    assert "recommendations" in result
    assert len(result["recommendations"]) > 0
    assert isinstance(result["recommendations"], list)
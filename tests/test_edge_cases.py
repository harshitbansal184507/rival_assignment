"""
Edge case tests
Run: pytest test_edge_cases.py -v
"""
import sys
import pytest
sys.path.append("C:\\Users\\harshit_work\\Desktop\\web projects\\rival_assignment")
from main import analyze_api_logs

def test_empty_array():
    result = analyze_api_logs([])
    
    assert result["summary"]["total_requests"] == 0
    assert result["summary"]["time_range"]["start"] is None
    assert result["summary"]["time_range"]["end"] is None
    assert len(result["endpoint_stats"]) == 0


def test_single_log_entry():
    logs = [
        {
            "timestamp": "2025-01-15T10:00:00Z",
            "endpoint": "/api/test",
            "method": "GET",
            "response_time_ms": 150,
            "status_code": 200,
            "user_id": "user_001",
            "request_size_bytes": 512,
            "response_size_bytes": 1024
        }
    ]
    
    result = analyze_api_logs(logs)
    
    assert result["summary"]["total_requests"] == 1
    assert result["summary"]["avg_response_time_ms"] == 150.0
    assert len(result["endpoint_stats"]) == 1


def test_invalid_input_type():
    """Test with non-list input"""
    with pytest.raises(ValueError):
        analyze_api_logs("not a list")
    
    with pytest.raises(ValueError):
        analyze_api_logs({"key": "value"})
    
    with pytest.raises(ValueError):
        analyze_api_logs(123)


def test_missing_timestamp():
    """Test log missing timestamp field"""
    logs = [
        {
            "endpoint": "/api/test",
            "method": "GET",
            "response_time_ms": 150,
            "status_code": 200,
            "user_id": "user_001",
            "request_size_bytes": 512,
            "response_size_bytes": 1024
        }
    ]
    
    result = analyze_api_logs(logs)
    assert result["summary"]["total_requests"] == 0


def test_missing_endpoint():
    """Test log missing endpoint field"""
    logs = [
        {
            "timestamp": "2025-01-15T10:00:00Z",
            "method": "GET",
            "response_time_ms": 150,
            "status_code": 200,
            "user_id": "user_001",
            "request_size_bytes": 512,
            "response_size_bytes": 1024
        }
    ]
    
    result = analyze_api_logs(logs)
    assert result["summary"]["total_requests"] == 0


def test_missing_response_time():
    """Test log missing response_time_ms field"""
    logs = [
        {
            "timestamp": "2025-01-15T10:00:00Z",
            "endpoint": "/api/test",
            "method": "GET",
            "status_code": 200,
            "user_id": "user_001",
            "request_size_bytes": 512,
            "response_size_bytes": 1024
        }
    ]
    
    result = analyze_api_logs(logs)
    assert result["summary"]["total_requests"] == 0


def test_invalid_timestamp_format():
    """Test with invalid timestamp"""
    logs = [
        {
            "timestamp": "invalid-timestamp",
            "endpoint": "/api/test",
            "method": "GET",
            "response_time_ms": 150,
            "status_code": 200,
            "user_id": "user_001",
            "request_size_bytes": 512,
            "response_size_bytes": 1024
        }
    ]
    
    result = analyze_api_logs(logs)
    assert result["summary"]["total_requests"] == 0


def test_empty_timestamp():
    """Test with empty timestamp"""
    logs = [
        {
            "timestamp": "",
            "endpoint": "/api/test",
            "method": "GET",
            "response_time_ms": 150,
            "status_code": 200,
            "user_id": "user_001",
            "request_size_bytes": 512,
            "response_size_bytes": 1024
        }
    ]
    
    result = analyze_api_logs(logs)
    assert result["summary"]["total_requests"] == 0


def test_negative_response_time():
    """Test with negative response time"""
    logs = [
        {
            "timestamp": "2025-01-15T10:00:00Z",
            "endpoint": "/api/test",
            "method": "GET",
            "response_time_ms": -100,
            "status_code": 200,
            "user_id": "user_001",
            "request_size_bytes": 512,
            "response_size_bytes": 1024
        }
    ]
    
    result = analyze_api_logs(logs)
    assert result["summary"]["total_requests"] == 0


def test_negative_request_size():
    """Test with negative request size"""
    logs = [
        {
            "timestamp": "2025-01-15T10:00:00Z",
            "endpoint": "/api/test",
            "method": "GET",
            "response_time_ms": 150,
            "status_code": 200,
            "user_id": "user_001",
            "request_size_bytes": -512,
            "response_size_bytes": 1024
        }
    ]
    
    result = analyze_api_logs(logs)
    assert result["summary"]["total_requests"] == 0


def test_negative_response_size():
    """Test with negative response size"""
    logs = [
        {
            "timestamp": "2025-01-15T10:00:00Z",
            "endpoint": "/api/test",
            "method": "GET",
            "response_time_ms": 150,
            "status_code": 200,
            "user_id": "user_001",
            "request_size_bytes": 512,
            "response_size_bytes": -1024
        }
    ]
    
    result = analyze_api_logs(logs)
    assert result["summary"]["total_requests"] == 0


def test_invalid_status_code_low():
    """Test with status code too low"""
    logs = [
        {
            "timestamp": "2025-01-15T10:00:00Z",
            "endpoint": "/api/test",
            "method": "GET",
            "response_time_ms": 150,
            "status_code": 50,
            "user_id": "user_001",
            "request_size_bytes": 512,
            "response_size_bytes": 1024
        }
    ]
    
    result = analyze_api_logs(logs)
    assert result["summary"]["total_requests"] == 0


def test_invalid_status_code_high():
    """Test with status code too high"""
    logs = [
        {
            "timestamp": "2025-01-15T10:00:00Z",
            "endpoint": "/api/test",
            "method": "GET",
            "response_time_ms": 150,
            "status_code": 999,
            "user_id": "user_001",
            "request_size_bytes": 512,
            "response_size_bytes": 1024
        }
    ]
    
    result = analyze_api_logs(logs)
    assert result["summary"]["total_requests"] == 0


def test_empty_endpoint_string():
    """Test with empty endpoint"""
    logs = [
        {
            "timestamp": "2025-01-15T10:00:00Z",
            "endpoint": "",
            "method": "GET",
            "response_time_ms": 150,
            "status_code": 200,
            "user_id": "user_001",
            "request_size_bytes": 512,
            "response_size_bytes": 1024
        }
    ]
    
    result = analyze_api_logs(logs)
    assert result["summary"]["total_requests"] == 0


def test_empty_user_id():
    """Test with empty user_id"""
    logs = [
        {
            "timestamp": "2025-01-15T10:00:00Z",
            "endpoint": "/api/test",
            "method": "GET",
            "response_time_ms": 150,
            "status_code": 200,
            "user_id": "",
            "request_size_bytes": 512,
            "response_size_bytes": 1024
        }
    ]
    
    result = analyze_api_logs(logs)
    assert result["summary"]["total_requests"] == 0


def test_mixed_valid_invalid():
    """Test mix of valid and invalid logs"""
    logs = [
        # Valid
        {
            "timestamp": "2025-01-15T10:00:00Z",
            "endpoint": "/api/test",
            "method": "GET",
            "response_time_ms": 150,
            "status_code": 200,
            "user_id": "user_001",
            "request_size_bytes": 512,
            "response_size_bytes": 1024
        },
        # Invalid - negative value
        {
            "timestamp": "2025-01-15T10:01:00Z",
            "endpoint": "/api/test",
            "method": "GET",
            "response_time_ms": -100,
            "status_code": 200,
            "user_id": "user_001",
            "request_size_bytes": 512,
            "response_size_bytes": 1024
        },
        # Valid
        {
            "timestamp": "2025-01-15T10:02:00Z",
            "endpoint": "/api/test",
            "method": "GET",
            "response_time_ms": 200,
            "status_code": 200,
            "user_id": "user_002",
            "request_size_bytes": 512,
            "response_size_bytes": 1024
        }
    ]
    
    result = analyze_api_logs(logs)
    
    # Should process only 2 valid logs
    assert result["summary"]["total_requests"] == 2
    assert result["summary"]["avg_response_time_ms"] == 175.0


def test_zero_values():
    """Test with zero values (valid edge case)"""
    logs = [
        {
            "timestamp": "2025-01-15T10:00:00Z",
            "endpoint": "/api/test",
            "method": "GET",
            "response_time_ms": 0,
            "status_code": 200,
            "user_id": "user_001",
            "request_size_bytes": 0,
            "response_size_bytes": 0
        }
    ]
    
    result = analyze_api_logs(logs)
    
    # Zero is valid
    assert result["summary"]["total_requests"] == 1
    assert result["summary"]["avg_response_time_ms"] == 0.0
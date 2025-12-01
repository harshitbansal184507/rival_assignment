import pytest
import json
import os
import sys
sys.path.append("C:\\Users\\harshit_work\Desktop\\web projects\\rival_assignment")
from main import analyze_api_logs

def test_sample_small():
 
    file_path = "test_data/sample_test_data_small.json"
    
    if not os.path.exists(file_path):
        pytest.skip(f"Sample dataset not found: {file_path}")
    
    with open(file_path, 'r') as f:
        logs = json.load(f)
    
    print(f"\nTesting with {len(logs)} logs from sample_small.json")
    
    result = analyze_api_logs(logs)
    
    assert "summary" in result
    assert "endpoint_stats" in result
    assert "performance_issues" in result
    assert "recommendations" in result
    assert "cost_analysis" in result
    
    assert result["summary"]["total_requests"] == len(logs)
    assert len(result["endpoint_stats"]) > 0
    
    print(f"✅ Processed {result['summary']['total_requests']} requests")
    print(f"✅ Analyzed {len(result['endpoint_stats'])} endpoints")


def test_sample_medium():
   
    
    file_path = "test_data/sample_medium.json"
    
    if not os.path.exists(file_path):
        pytest.skip(f"Sample dataset not found: {file_path}")
    
    with open(file_path, 'r') as f:
        logs = json.load(f)
    
    print(f"\nTesting with {len(logs)} logs from sample_medium.json")
    
    result = analyze_api_logs(logs)
    
    required_keys = [
        "summary", "endpoint_stats", "performance_issues",
        "recommendations", "hourly_distribution", "top_users_by_requests",
        "cost_analysis", "caching_opportunities", 
       
    ]
    
    for key in required_keys:
        assert key in result, f"Missing required key: {key}"
    
    assert result["summary"]["total_requests"] == len(logs)
    assert result["summary"]["avg_response_time_ms"] >= 0
    assert 0 <= result["summary"]["error_rate_percentage"] <= 100
    
    print(f"✅ All {len(required_keys)} output sections present")
    print(f"✅ Avg response time: {result['summary']['avg_response_time_ms']}ms")


def test_sample_large():
   
    
    file_path = "test_data/sample_large.json"
    
    if not os.path.exists(file_path):
        pytest.skip(f"Sample dataset not found: {file_path}")
    
    with open(file_path, 'r') as f:
        logs = json.load(f)
    
    print(f"\nTesting with {len(logs)} logs from sample_large.json")
    
    result = analyze_api_logs(logs)
    
    # Verify processing
    assert result["summary"]["total_requests"] == len(logs)
    
    # With large dataset, should have meaningful analysis
    assert len(result["endpoint_stats"]) > 0
    assert result["cost_analysis"]["total_cost_usd"] > 0
    
    # Print insights
    print(f"\n{'='*60}")
    print(f"Analysis Results:")
    print(f"{'='*60}")
    print(f"Total requests: {result['summary']['total_requests']}")
    print(f"Endpoints: {len(result['endpoint_stats'])}")
    print(f"Performance issues: {len(result['performance_issues'])}")
    print(f"Caching opportunities: {len(result['caching_opportunities'])}")
    print(f"Total cost: ${result['cost_analysis']['total_cost_usd']}")
    print(f"{'='*60}\n")


def test_output_format():
  
    logs = [
        {
            "timestamp": "2025-01-15T10:00:00Z",
            "endpoint": "/api/test",
            "method": "GET",
            "response_time_ms": 150,
            "status_code": 200,
            "user_id": "user_001",
            "request_size_bytes": 512,
            "response_size_bytes": 2048
        }
    ]
    
    result = analyze_api_logs(logs)
    
    required_keys = [
        "summary",
        "endpoint_stats",
        "performance_issues",
        "recommendations",
        "hourly_distribution",
        "top_users_by_requests",
        "cost_analysis",
        "caching_opportunities",
      
    ]
    
    missing_keys = [key for key in required_keys if key not in result]
    assert len(missing_keys) == 0, f"Missing keys: {missing_keys}"
    
    # Verify summary structure
    assert "total_requests" in result["summary"]
    assert "time_range" in result["summary"]
    assert "avg_response_time_ms" in result["summary"]
    assert "error_rate_percentage" in result["summary"]
    
    # Verify cost analysis structure
    assert "total_cost_usd" in result["cost_analysis"]
    assert "cost_breakdown" in result["cost_analysis"]
    assert "cost_by_endpoint" in result["cost_analysis"]
    
  
    
    print("\n✅ Output format verified")
    print("✅ All required fields present")
    print("✅ Structure matches assignment requirements")
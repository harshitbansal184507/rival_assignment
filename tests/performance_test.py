"""
performance test for 10,000 log entries
Run: pytest test_edge_cases.py -s (to also view print output)
"""
import pytest
import json
import time
import os
import sys
sys.path.append("C:\\Users\\harshit_work\Desktop\\web projects\\rival_assignment")
from main import analyze_api_logs

def test_performance_10000_logs():
    
    file_path = "test_data/sample_large.json"
    
    if not os.path.exists(file_path):
        pytest.skip(f"Performance dataset not found at {file_path}")
    
    print(f"\nLoading performance test data from {file_path}...")
    with open(file_path, 'r') as f:
        logs = json.load(f)
    
    log_count = len(logs)
    print(f"Loaded {log_count} log entries")
    
    # Ensure we have at least 10,000 logs
    assert log_count >= 10000, f"Performance test requires 10,000+ logs, found {log_count}"
    
    print(f"Starting performance test with {log_count} logs...")
    print("Target: < 2.0 seconds")
    
    start_time = time.time()
    result = analyze_api_logs(logs)
    end_time = time.time()
    
    execution_time = end_time - start_time
    
    # Print results
    print(f"\n{'='*60}")
    print(f"PERFORMANCE TEST RESULTS")
    print(f"{'='*60}")
    print(f"Log entries processed: {log_count:,}")
    print(f"Execution time: {execution_time:.3f} seconds")
    print(f"Throughput: {log_count/execution_time:,.0f} logs/second")
    print(f"Status: {'✅ PASSED' if execution_time < 2.0 else '❌ FAILED'}")
    print(f"{'='*60}\n")
    
    # Verify the analysis completed correctly
    assert result["summary"]["total_requests"] == log_count
    assert len(result["endpoint_stats"]) > 0
    
    # Performance requirement: < 2 seconds
    assert execution_time < 2.0, f"Performance test failed: {execution_time:.3f}s (required: < 2.0s)"
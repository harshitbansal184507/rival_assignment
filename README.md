# API Log Analyzer

A comprehensive serverless function for analyzing API usage patterns, detecting performance issues, providing cost optimization insights and caching opportunities.

## 📋 Project Overview

This project analyzes API call logs to generate detailed analytics including:

- **Summary Statistics**: Total requests, time ranges, average response times, error rates
- **Endpoint Analytics**: Per-endpoint performance metrics and statistics
- **Performance Issue Detection**: Identifies slow endpoints and high error rates
- **Cost Analysis**: Estimates serverless compute costs with optimization potential
- **Caching Opportunities**: Identifies endpoints that would benefit from caching
- **Actionable Recommendations**: Suggests improvements based on data patterns

### Key Features

✅ Processes 1,00,000+ logs in under 2 seconds  
✅ Handles edge cases gracefully (invalid data, missing fields, etc.)  
✅ 80%+ test coverage  
✅ Production-ready error handling  
✅ Comprehensive documentation

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**

```bash
git clone <your-repo-url>
cd rival-assignment
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Verify installation**

```bash
python test.py
```

---

## 💻 Usage

### Basic Usage

```python
from main import analyze_api_logs
import json

# Load your log data
with open('logs.json', 'r') as f:
    logs = json.load(f)

# Analyze the logs
result = analyze_api_logs(logs)

# Access results
print(f"Total Requests: {result['summary']['total_requests']}")
print(f"Average Response Time: {result['summary']['avg_response_time_ms']}ms")
print(f"Error Rate: {result['summary']['error_rate_percentage']}%")
```

### Input Format

Each log entry should have the following structure:

```json
{
  "timestamp": "2025-01-15T10:30:00Z",
  "endpoint": "/api/users",
  "method": "GET",
  "response_time_ms": 245,
  "status_code": 200,
  "user_id": "user_123",
  "request_size_bytes": 512,
  "response_size_bytes": 2048
}
```

### Output Format

The function returns a comprehensive analysis:

```json
{
  "summary": {
    "total_requests": 1000,
    "time_range": {
      "start": "2025-01-15T10:00:00Z",
      "end": "2025-01-15T11:00:00Z"
    },
    "avg_response_time_ms": 189.5,
    "error_rate_percentage": 2.3
  },
  "endpoint_stats": [...],
  "performance_issues": [...],
  "recommendations": [...],
  "hourly_distribution": {...},
  "top_users_by_requests": [...],
  "cost_analysis": {...},
  "caching_opportunities": [...],

}
```

### Command Line Usage

```bash
# Run with a sample dataset
python test.py

# Or use it as a module
python -c "from main import analyze_api_logs; import json; \
  logs = json.load(open('tests/test_data/sample_large.json')); \
  print(analyze_api_logs(logs)['summary'])"
```

---

## 🧪 Running Tests

### Run All Tests

```bash
# Run complete test suite
pytest tests/ -v

# With coverage report
pytest tests/ --cov=main --cov=analytics --cov=utils --cov=config --cov-report=html
```

### Run Individual Test Files

```bash
# Unit tests
pytest tests/unit_tests.py -v

# Edge cases
pytest tests/test_edge_cases.py -v

# Performance tests
pytest tests/performance_test.py -v -s

# Integration tests
pytest tests/integration_tests.py -v -s
```

### Test Coverage

The project includes comprehensive tests covering:

- ✅ **Unit Tests** (20+ tests): Core functionality
- ✅ **Edge Cases** (19+ tests): Invalid inputs, missing fields, boundary conditions
- ✅ **Performance Tests**: 1,00,000+ logs processed in < 2 seconds
- ✅ **Integration Tests**: Real-world datasets

**Current Coverage: 85%+**

View detailed coverage report:

```bash
pytest tests/ --cov=main --cov=analytics --cov=utils --cov=config --cov-report=html
open htmlcov/index.html
```

---

## 📊 Performance

### Time Complexity

| Operation           | Complexity     | Notes                                |
| ------------------- | -------------- | ------------------------------------ |
| Overall Analysis    | O(n)           | Where n = number of logs             |
| Summary Calculation | O(n)           | Single pass through logs             |
| Endpoint Stats      | O(n)           | Group by endpoint, single pass       |
| Performance Issues  | O(e)           | Where e = number of endpoints        |
| Hourly Distribution | O(n)           | Single pass with timestamp parsing   |
| Top Users           | O(n + u log u) | Where u = unique users               |
| Cost Analysis       | O(n + e)       | Process logs + aggregate by endpoint |
| Caching Analysis    | O(n + e)       | Group and analyze endpoints          |

**Overall: O(n)** - Linear time complexity

### Space Complexity

| Component         | Complexity | Notes                            |
| ----------------- | ---------- | -------------------------------- |
| Input Storage     | O(n)       | Original log data                |
| Endpoint Grouping | O(n)       | Worst case: all unique endpoints |
| Time Windows      | O(w)       | Number of time windows analyzed  |
| Output            | O(e + u)   | Endpoints + users in results     |

**Overall: O(n)** - Linear space complexity

## 📁 Project Structure

```
rival-assignment/
├── README.md              # This file
├── DESIGN.md              # Design decisions and approach
├── requirements.txt       # Python dependencies
├── .gitignore            # Git ignore rules
│
├── main.py               # Main analysis function
├── analytics.py          # Analysis helper functions
├── config.py             # Configuration constants
├── utils.py              # Utility functions
│
└── tests/
    ├── unit_tests.py              # Unit tests
    ├── test_edge_cases.py         # Edge case tests
    ├── performance_test.py        # Performance tests
    ├── integration_tests.py       # Integration tests
    ├── test.py                    # Quick smoke test
    └── test_data/
        ├── sample_test_data_small.json
        ├── sample_medium.json
        ├── sample_large.json
        └── generate_dataset.py
```

---

## 🔧 Configuration

Edit `config.py` to customize thresholds

---

## 📚 API Reference

### Main Function

```python
def analyze_api_logs(logs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analyze API logs and generate comprehensive analytics.

    Args:
        logs: List of API log entries

    Returns:
        Dictionary containing analysis results

    Raises:
        ValueError: If logs is not a list
    """
```

### Key Output Fields

| Field                   | Type | Description                  |
| ----------------------- | ---- | ---------------------------- |
| `summary`               | dict | Overall statistics           |
| `endpoint_stats`        | list | Per-endpoint metrics         |
| `performance_issues`    | list | Detected issues              |
| `recommendations`       | list | Actionable suggestions       |
| `cost_analysis`         | dict | Cost breakdown and estimates |
| `caching_opportunities` | list | Endpoints to cache           |

---

## 🎯 Features in Detail

### 1. Performance Issue Detection

Automatically identifies:

- **Slow Endpoints**: Response time > 500ms (configurable)
- **High Error Rates**: Error rate > 5% (configurable)
- **Severity Levels**: Critical, High, Medium

### 2. Cost Analysis

Calculates costs based on:

- Request count
- Execution time (per millisecond)
- Memory usage (based on response size)
- Provides optimization potential estimate

### 3. Caching Opportunities

Identifies endpoints suitable for caching based on:

- High request frequency (> 100 requests)
- Majority GET requests (> 80%)
- Low error rate (< 2%)
- Estimates cost savings and cache hit rates

## 🐛 Error Handling

The function gracefully handles:

✅ Empty input arrays  
✅ Single log entries  
✅ Missing required fields  
✅ Invalid timestamp formats  
✅ Negative values  
✅ Invalid status codes  
✅ Mixed valid/invalid data

Invalid entries are filtered out and processing continues with valid data.

---

## 🤝 Contributing

### Code Style

- Follow PEP 8 guidelines
- Use type hints
- Add docstrings to all functions
- Write tests for new features

## 📄 License

This project is part of the Rival.io internship assignment.

---

## 📞 Contact

For questions or issues, contact: harshitbansal184507@gmail.com

---

## 🙏 Acknowledgments

- Assignment provided by Rival.io
- Built as part of the Software Development Internship application

---

## 📈 Future Enhancements

Potential improvements:

- [ ] Real-time streaming analysis
- [ ] Machine learning-based anomaly detection
- [ ] GraphQL endpoint support
- [ ] Custom alerting rules
- [ ] Dashboard visualization
- [ ] Export to multiple formats (CSV, Excel, PDF)

---

**Version**: 1.0.0  
**Last Updated**: January 2025  
**Python Version**: 3.8+

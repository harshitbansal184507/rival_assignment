import json
import random
from datetime import datetime, timedelta

def generate_dataset():
    logs = []
    
    endpoints = {
        "/api/users": {"weight": 35, "method": "GET", "time_range": (80, 200), "error_rate": 0.01},
        "/api/products": {"weight": 30, "method": "GET", "time_range": (100, 250), "error_rate": 0.015},
        "/api/payments": {"weight": 15, "method": "POST", "time_range": (700, 1200), "error_rate": 0.12},
        "/api/reports": {"weight": 8, "method": "GET", "time_range": (1800, 2500), "error_rate": 0.02},
        "/api/search": {"weight": 12, "method": "GET", "time_range": (300, 600), "error_rate": 0.03}
    }
    
    users = [f"user_{str(i).zfill(3)}" for i in range(1, 31)]  
    
    # user_001 will be VERY active (anomaly trigger)
    user_weights = [40] + [2] * 29  # user_001 gets 40x weight
    
    base_time = datetime(2025, 1, 15, 10, 0, 0)
    
    # Generate 500 logs over 1 hour
    for i in range(10000):
        # Pick endpoint based on weights
        endpoint = random.choices(
            list(endpoints.keys()),
            weights=[endpoints[e]["weight"] for e in endpoints.keys()],
            k=1
        )[0]
        
        config = endpoints[endpoint]
        
        # Method
        if endpoint in ["/api/users", "/api/products"]:
            method = random.choice(["GET", "GET", "GET", "GET", "GET", "POST"])  # 83% GET
        elif endpoint == "/api/search":
            method = "GET"  # 100% GET
        elif endpoint == "/api/reports":
            method = random.choice(["GET", "GET", "GET", "GET", "POST"])  # 80% GET
        else:
            method = config["method"]
        
        # Pick user (with user_001 being very active)
        user_id = random.choices(users, weights=user_weights, k=1)[0]
        
        # Response time
        response_time = random.randint(config["time_range"][0], config["time_range"][1])
        
        # Timestamp - spread over 60 minutes
        minutes_offset = (i / 500) * 60
        timestamp = base_time + timedelta(minutes=minutes_offset)
        
        # Create request spike for /api/search between 10:20-10:25 (minute 20-25)
        if 20 <= minutes_offset <= 25 and random.random() < 0.6:
            endpoint = "/api/search"
            method = "GET"
            response_time = random.randint(300, 600)
        
        # Create error cluster for /api/payments around 10:35-10:40 (minute 35-40)
        if 35 <= minutes_offset <= 40 and endpoint == "/api/payments":
            status_code = random.choice([500, 500, 500, 503, 503, 200])  # High error rate
        else:
            # Normal error rate
            if random.random() < config["error_rate"]:
                status_code = random.choice([400, 404, 500, 503])
            else:
                if method == "POST" and endpoint != "/api/payments":
                    status_code = 201
                else:
                    status_code = 200
        
        # Create rate limit violations
        # user_002 makes 150+ requests in one minute (minute 45)
        if 45 <= minutes_offset <= 46 and random.random() < 0.3:
            user_id = "user_002"
            endpoint = "/api/products"
            method = "GET"
        
        # Request and response sizes
        if endpoint == "/api/reports":
            request_size = random.randint(256, 1024)
            response_size = random.randint(12288, 20480)  # 12-20KB (large)
        elif endpoint == "/api/users":
            request_size = random.randint(256, 512)
            response_size = random.randint(512, 2048)  # 0.5-2KB
        elif endpoint == "/api/products":
            request_size = random.randint(256, 512)
            response_size = random.randint(1024, 4096)  # 1-4KB
        elif endpoint == "/api/payments":
            request_size = random.randint(1024, 3072)
            response_size = random.randint(256, 1024)
        else:  # search
            request_size = random.randint(512, 2048)
            response_size = random.randint(4096, 12288)  # 4-12KB
        
        log = {
            "timestamp": timestamp.isoformat() + "Z",
            "endpoint": endpoint,
            "method": method,
            "response_time_ms": response_time,
            "status_code": status_code,
            "user_id": user_id,
            "request_size_bytes": request_size,
            "response_size_bytes": response_size
        }
        
        logs.append(log)
    
    # Add extra logs to trigger rate limits more clearly
    # Add 120 more requests from user_002 at minute 45 (rate limit violation)
    spike_time = base_time + timedelta(minutes=45)
    for j in range(120):
        logs.append({
            "timestamp": (spike_time + timedelta(seconds=j * 0.5)).isoformat() + "Z",
            "endpoint": "/api/products",
            "method": "GET",
            "response_time_ms": random.randint(100, 250),
            "status_code": 200,
            "user_id": "user_002",
            "request_size_bytes": 256,
            "response_size_bytes": random.randint(1024, 2048)
        })
    
    # Sort by timestamp
    logs.sort(key=lambda x: x["timestamp"])
    
    return logs

# Generate and save
logs = generate_dataset()


with open('test_data/sample_large.json', 'w') as f:
    json.dump(logs, f, indent=2)

PERFORMANCE_THRESHOLDS = {  #in milliseconds
    "medium": 500,   
    "high": 1000,   
    "critical": 2000  
}

ERROR_RATE_THRESHOLDS = { #in percentage
    "medium": 5.0,  
    "high": 10.0,    
    "critical": 15.0 
}

ERROR_STATUS_CODES = [400, 401, 403, 404, 500, 502, 503, 504]

TOP_USERS_LIMIT = 5

COST_STRUCTURE = {
    "per_request": 0.0001,        
    "per_ms_execution": 0.000002,   
    "memory_costs": {    #based on response_size_bytes
        "small": 0.00001,  
        "medium": 0.00005,  
        "large": 0.0001    
    }
}

CACHING_CRITERIA = {
    "min_request_count": 100,        
    "min_get_percentage": 80.0,      
    "max_error_rate": 2.0,         
    "recommended_ttl_minutes": 15    
}



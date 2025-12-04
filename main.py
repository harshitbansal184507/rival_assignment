from typing import Any, Dict, List, Tuple
from collections import defaultdict
from datetime import datetime
import config
import utils
import analytics
import advanced_features.cost_estimation
import advanced_features.caching


def analyze_api_logs(logs: List[Dict[str, Any]] , starttime : any, endtime: any) -> Dict[str, Any]:
   
    if not isinstance(logs, list):
        raise ValueError("logs must be a list")
    
    if len(logs) == 0:
        return utils._create_empty_report()
    if starttime is not None and endtime is not None:
        starttime = utils.parse_timestamp(starttime)
        endtime = utils.parse_timestamp(endtime)
    valid_logs = []
    
    for log in logs:
        if utils.validate_log_entry(log) :
            
            try :
                log_time = utils.parse_timestamp(log["timestamp"])
                if starttime <= log_time <= endtime:
                    valid_logs.append(log)
                    continue
            except :
                valid_logs.append(log)    
        
    
    if len(valid_logs) == 0:
        return utils._create_empty_report()
    
    summary = analytics._calculate_summary(valid_logs)
    endpoint_stats = analytics._calculate_endpoint_stats(valid_logs)
    performance_issues = analytics._detect_performance_issues(endpoint_stats, summary)
    recommendations = analytics._generate_recommendations(endpoint_stats, summary, valid_logs)
    hourly_distribution = analytics._calculate_hourly_distribution(valid_logs)
    top_users = analytics._calculate_top_users(valid_logs)
    cost_analysis = advanced_features.cost_estimation._calculate_cost_analysis(valid_logs, endpoint_stats)
    caching_analysis = advanced_features.caching._analyze_caching_opportunities(valid_logs, endpoint_stats)
    
    report = {
        "summary": summary,
        "endpoint_stats": endpoint_stats,
        "performance_issues": performance_issues,
        "recommendations": recommendations,
        "hourly_distribution": hourly_distribution,
        "top_users_by_requests": top_users , 
        "cost_analysis": cost_analysis , 
        "caching_opportunities": caching_analysis
    }
    
    return report
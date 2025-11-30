DESIGN.md
Log Analyzer – System Design & Implementation Notes

This document outlines the design decisions, advanced features, trade-offs, scaling approach, and possible improvements for the Log Analyzer.

1. Advanced Features Implemented
   1.1 Cost Analysis

I implemented Cost Analysis to estimate the operational cost of each API endpoint.
Modern APIs often have usage-based pricing, so identifying high-cost endpoints adds immediate business value.

This feature:

Computes total cost per endpoint

Highlights most expensive API routes

Helps prioritize optimization and cost-saving efforts

1.2 Caching Opportunity Detection

Many GET endpoints receive repeated requests. Caching them can significantly reduce server load.

This feature:

Tracks call frequency per endpoint

Surfaces endpoints with high repeat usage

Identifies simple caching opportunities to boost performance

2. Design Choices & Trade-offs
   2.1 In-Memory Aggregation

I used in-memory dictionaries to aggregate metrics such as counts, average latency, and total cost.

Trade-off:

Pros: Fast, simple, easy to implement

Cons: Not ideal for very large datasets since memory usage grows with input size

2.2 Static Cost Mapping

Costs were assigned through predefined static values.

Trade-off:

Pros: Straightforward and easy to extend

Cons: Less realistic than dynamic cloud-based cost integration

2.3 Basic Caching Detection

Caching opportunities are identified based on request frequency.

Trade-off:

Pros: Lightweight and efficient

Cons: Does not include advanced payload-level similarity checks

3. Scaling Strategy

To scale the system to 1 million+ logs, the approach focuses entirely on streaming to maintain stable memory usage.

3.1 Streaming Input

Instead of loading the entire JSON dataset at once, logs are processed incrementally:

Use Python generators to yield logs one by one

Use JSONL format for large offline datasets

For real-time ingestion, integrate with Kafka, Kinesis, or message queues

This ensures the analyzer can handle millions of logs without memory exhaustion.

3.2 Rolling Aggregations

Each log updates small, constant-size counters:

Counts, latencies, cost totals, repeat frequencies

No full logs are cached in memory

Allows the analyzer to scale smoothly with data volume

3.3 Future Streaming Extensions

Streaming makes it easy to later add:

Checkpointing

Partial aggregate flushing

Offset-based recovery

4. What I Would Improve With More Time
   4.1 Real-Time Dashboard

Build a dashboard (Streamlit or Grafana) to visualize:

Latency trends

Cost distribution

Caching opportunities

4.2 Enhanced Cost Modeling

Add support for:

Cloud-specific billing

Per-operation cost (DB calls, CPU time, egress)

4.3 Alerting & Monitoring

Add alerting for:

Latency spikes

Error surges

Unexpected cost anomalies

5. Time Spent

I spent 7–8 hours over 3–4 days on this assignment.
This includes design, coding, testing, and documentation — completed while managing two end-semester exams during the same period.

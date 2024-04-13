# Counter

A counter is a cumulative metric that represents a single numerical value that only ever goes up. A counter is typically used to count requests served, tasks completed, errors occurred, etc. Counters should not be used to expose current counts of items whose number can also go down, e.g. the number of currently running coroutines. Use gauges for this use case.

Examples:
- Number of requests processed
- Number of items that were inserted into a queue
- Total amount of data that a system has processed

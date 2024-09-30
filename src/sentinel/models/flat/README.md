# Partitioning transactions table 

Partitioning the `transactions` table by day is a approach for managing data retention effectively. This way, we can easily remove partitions that are older than your specified retention period (e.g., one month). 

## Steps for Daily Partitioning

### Create Daily Partitions

Create partitions for each day, allowing to drop the entire partition for any day that is older than one month. 

> Note: Partitions can be created in advance

For example, to create partitions for the month of October 2024:

```sql
CREATE TABLE transactions_2024_10_01 PARTITION OF transactions FOR VALUES FROM ('2024-10-01') TO ('2024-10-02');
CREATE TABLE transactions_2024_10_02 PARTITION OF transactions FOR VALUES FROM ('2024-10-02') TO ('2024-10-03');
CREATE TABLE transactions_2024_10_03 PARTITION OF transactions FOR VALUES FROM ('2024-10-03') TO ('2024-10-04');
-- Repeat for each day in the month... 
CREATE TABLE transactions_2024_10_31 PARTITION OF transactions FOR VALUES FROM ('2024-10-31') TO ('2024-11-01');
```

### Managing Partitions

To maintain partitioned structure, we can set up a scheduled job to create new daily partitions as needed. Additionally, we can drop partitions that are older than one month easily.

### Dropping Old Partitions

If we need to drop partitions older than one month, we can use a SQL command like:

```sql
DROP TABLE IF EXISTS transactions_2024_09_30; -- Drop the partition for September 30, 2024
```

To automate this process with a script that runs at the beginning of each month to check and drop partitions older than one month.

### Example Script for Dropping Old Partitions

A function that drops old partitions based on the current date:

```sql
DO $$
DECLARE
    r RECORD;
BEGIN
    FOR r IN SELECT tablename FROM pg_tables
              WHERE tablename LIKE 'transactions_%' AND 
                    tablename < 'transactions_' || to_char(now() - interval '1 month', 'YYYY_MM_DD')
    LOOP
        EXECUTE 'DROP TABLE ' || quote_ident(r.tablename);
    END LOOP;
END $$;
```

class Queries:

  running_queries = '''
    SELECT
      pid,
      state,
      application_name AS source,
      age(now(), xact_start) AS duration,
      waiting,
      query,
      xact_start AS started_at
    FROM
      pg_stat_activity
    WHERE
      query <> '<insufficient privilege>'
      AND state <> 'idle'
      AND pid <> pg_backend_pid()
    ORDER BY
      query_start DESC
  '''

  long_running_queries = '''
    SELECT
      pid,
      state,
      application_name AS source,
      age(now(), xact_start) AS duration,
      waiting,
      query,
      xact_start AS started_at
    FROM
      pg_stat_activity
    WHERE
      query <> '<insufficient privilege>'
      AND state <> 'idle'
      AND pid <> pg_backend_pid()
      AND now() - query_start > interval '5 minutes'
    ORDER BY
      query_start DESC
  '''

  index_hit_rate = '''
    SELECT
      (sum(idx_blks_hit)) / nullif(sum(idx_blks_hit + idx_blks_read),0) AS rate
    FROM
      pg_statio_user_indexes
  '''

  table_hit_rate = ''' 
    SELECT
      sum(heap_blks_hit) / nullif(sum(heap_blks_hit) + sum(heap_blks_read),0) AS rate
    FROM
      pg_statio_user_tables
  '''

  index_usage = '''
    SELECT
      relname AS table,
      CASE idx_scan
        WHEN 0 THEN 'Insufficient data'
        ELSE (100 * idx_scan / (seq_scan + idx_scan))::text
      END percent_of_times_index_used,
      n_live_tup rows_in_table
    FROM
      pg_stat_user_tables
    ORDER BY
      n_live_tup DESC,
      relname ASC
  '''

  missing_indexes = '''
    SELECT
      relname AS table,
      CASE idx_scan
        WHEN 0 THEN 'Insufficient data'
        ELSE (100 * idx_scan / (seq_scan + idx_scan))::text
      END percent_of_times_index_used,
      n_live_tup rows_in_table
    FROM
      pg_stat_user_tables
    WHERE
      idx_scan > 0
      AND (100 * idx_scan / (seq_scan + idx_scan)) < 95
      AND n_live_tup >= 10000
    ORDER BY
      n_live_tup DESC,
      relname ASC
  '''

  unused_tables = '''
    SELECT
      relname AS table,
      n_live_tup rows_in_table
    FROM
      pg_stat_user_tables
    WHERE
      idx_scan = 0
    ORDER BY
      n_live_tup DESC,
      relname ASC
  '''

  unused_indexes = '''
    SELECT
      relname AS table,
      indexrelname AS index,
      pg_size_pretty(pg_relation_size(i.indexrelid)) AS index_size,
      idx_scan as index_scans
    FROM
      pg_stat_user_indexes ui
    INNER JOIN
      pg_index i ON ui.indexrelid = i.indexrelid
    WHERE
      NOT indisunique
      AND idx_scan < 50 AND pg_relation_size(relid) > 5 * 8192
    ORDER BY
      pg_relation_size(i.indexrelid) / nullif(idx_scan, 0) DESC NULLS FIRST,
      pg_relation_size(i.indexrelid) DESC,
      relname ASC
  '''

  relation_sizes = ''' 
    SELECT
      c.relname AS name,
      CASE WHEN c.relkind = 'r' THEN 'table' ELSE 'index' END AS type,
      pg_size_pretty(pg_table_size(c.oid)) AS size
    FROM
      pg_class c
    LEFT JOIN
      pg_namespace n ON (n.oid = c.relnamespace)
    WHERE
      n.nspname NOT IN ('pg_catalog', 'information_schema')
      AND n.nspname !~ '^pg_toast'
      AND c.relkind IN ('r', 'i')
    ORDER BY
      pg_table_size(c.oid) DESC,
      name ASC
  '''

  database_size = ''' 
    SELECT pg_size_pretty(pg_database_size(current_database()))
  '''
  
  slow_queries = ''' 
    SELECT
      query,
      (total_time / 1000 / 60) as total_minutes,
      (total_time / calls) as average_time,
      calls
    FROM
      pg_stat_statements
    INNER JOIN
      pg_database ON pg_database.oid = pg_stat_statements.dbid
    WHERE
      pg_database.datname = current_database()
      AND calls >= 100
      AND (total_time / calls) >= 20
    ORDER BY
      total_minutes DESC
    LIMIT 100
  '''

  query_stats_enabled = '''
    SELECT 
      COUNT(*) AS count 
    FROM pg_extension 
    WHERE extname = 'pg_stat_statements'
  '''

  query_stats_readable = '''
    SELECT has_table_privilege(current_user, 'pg_stat_statements', 'SELECT')
  '''

  enable_query_stats = '''
    CREATE EXTENSION pg_stat_statements
  ''' 
  # TODO: Add query_stats_enabled related queries
  # TODO: Add kill related queries

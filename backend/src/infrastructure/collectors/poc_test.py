"""Proof of Concept script for PostgreSQL query analyzer."""
import asyncio
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.infrastructure.collectors.postgres_collector import PostgresCollector

async def main():
    print("🚀 Starting PostgreSQL Collector PoC...")
    
    # Use the local dev database for testing the collector on itself
    # In a real scenario, this would be the user's target database
    db_url = os.getenv("DATABASE_URL", "postgresql://queryinsight:dev_password_change_me@localhost:5432/queryinsight_dev")
    # Replace asyncpg driver prefix if present for direct connection
    db_url = db_url.replace("+asyncpg", "")
    
    collector = PostgresCollector(db_url)
    
    print(f"Connecting to: {db_url}")
    
    try:
        # 1. Collect slow queries
        print("\n🔍 Collecting slow queries (threshold > 0ms for testing)...")
        slow_queries = await collector.collect_slow_queries(threshold_ms=0.0, limit=5)
        
        if not slow_queries:
            print("No slow queries found. Ensure pg_stat_statements is enabled and you have run some queries.")
            return

        print(f"Found {len(slow_queries)} slow queries.")
        
        for i, q in enumerate(slow_queries):
            print(f"\n[{i+1}] Query ID: {q['query_id']}")
            print(f"    Mean Time: {q['mean_exec_time_ms']:.2f}ms")
            print(f"    SQL Snippet: {q['sql_text'][:100]}...")
            
            # 2. Get EXPLAIN plan for the first one if it's a SELECT
            if i == 0 and q['sql_text'].strip().upper().startswith("SELECT"):
                print("\n📊 Fetching EXPLAIN plan for the top query...")
                plan = await collector.get_explain_plan(q['sql_text'])
                if plan:
                    print("✅ Successfully captured EXPLAIN plan!")
                    # Just print a few keys from the plan to verify
                    print(f"    Node Type: {plan['Plan']['Node Type']}")
                    print(f"    Total Cost: {plan['Plan']['Total Cost']}")
                else:
                    print("❌ Failed to capture EXPLAIN plan (possibly due to placeholders).")

    except Exception as e:
        print(f"❌ Error during PoC: {e}")

if __name__ == "__main__":
    asyncio.run(main())

"""Seed script for Phase 5 Intelligence Layer testing."""
import asyncio
import uuid
from datetime import datetime, timedelta
import random

from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from src.infrastructure.database.models import Base, UserModel, DatabaseModel, QueryModel, MetricModel
from src.domain.entities import DatabaseType, MetricType, PlanTier, QueryStatus
from src.infrastructure.services.sql_normalizer import SqlNormalizer

DATABASE_URL = "postgresql+asyncpg://queryinsight:dev_password_change_me@postgres:5432/queryinsight_dev"

async def seed_intelligence_data():
    engine = create_async_engine(DATABASE_URL)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        # 1. Get or create user
        user_email = "danhnguyen1998@gmail.com"
        result = await session.execute(text(f"SELECT id FROM users WHERE email = '{user_email}'"))
        user_id = result.scalar()
        
        if not user_id:
            user_id = uuid.uuid4()
            user = UserModel(
                id=user_id,
                email=user_email,
                hashed_password="hashed_password",
                full_name="Danh Nguyen",
                plan_tier=PlanTier.PRO
            )
            session.add(user)
            await session.commit()
        
        # 2. Get or create database
        result = await session.execute(text(f"SELECT id FROM databases WHERE user_id = '{user_id}' LIMIT 1"))
        db_id = result.scalar()
        
        if not db_id:
            db_id = uuid.uuid4()
            db = DatabaseModel(
                id=db_id,
                user_id=user_id,
                name="Production Analytics",
                type=DatabaseType.POSTGRES,
                encrypted_connection_string="postgresql://user:pass@host:5432/db",
                is_active=True
            )
            session.add(db)
            await session.commit()

        # 3. Create query patterns with trends
        patterns = [
            "SELECT * FROM users WHERE id = $1",
            "SELECT email, count(*) FROM orders GROUP BY email HAVING count(*) > $1",
            "UPDATE inventory SET stock = stock - $1 WHERE product_id = $2",
            "SELECT p.name, o.total FROM products p JOIN orders o ON p.id = o.product_id WHERE o.created_at > $1"
        ]
        
        # For each pattern, create data points over the last 7 days
        for sql in patterns:
            fingerprint = SqlNormalizer.normalize(sql)
            
            # Baseline (Days 7 to 2) - Fast
            for day in range(2, 8):
                timestamp = datetime.utcnow() - timedelta(days=day)
                # Create 10 entries per day
                for _ in range(10):
                    query = QueryModel(
                        id=uuid.uuid4(),
                        database_id=db_id,
                        sql_text=sql.replace("$1", str(random.randint(1, 1000))),
                        normalized_sql=fingerprint,
                        execution_time_ms=random.uniform(10, 50), # Fast baseline
                        timestamp=timestamp - timedelta(minutes=random.randint(0, 1440)),
                        status=QueryStatus.SLOW
                    )
                    session.add(query)
            
            # Recent (Last 24 hours) - Degraded for some
            is_degraded = random.choice([True, False])
            recent_avg = 150 if is_degraded else 30 # Significant jump if degraded
            
            for _ in range(15):
                timestamp = datetime.utcnow() - timedelta(minutes=random.randint(0, 1440))
                query = QueryModel(
                    id=uuid.uuid4(),
                    database_id=db_id,
                    sql_text=sql.replace("$1", str(random.randint(1, 1000))),
                    normalized_sql=fingerprint,
                    execution_time_ms=random.uniform(recent_avg * 0.8, recent_avg * 1.2),
                    timestamp=timestamp,
                    status=QueryStatus.SLOW
                )
                session.add(query)

        await session.commit()
        print(f"Seeded intelligence data for DB: {db_id}")

if __name__ == "__main__":
    asyncio.run(seed_intelligence_data())

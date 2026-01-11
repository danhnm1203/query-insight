"""Use case for analyzing a query and generating recommendations."""
import logging
from uuid import UUID

from src.application.interfaces.repositories.database_repository import IDatabaseRepository
from src.application.interfaces.repositories.query_repository import IQueryRepository
from src.application.interfaces.repositories.recommendation_repository import IRecommendationRepository
from src.infrastructure.collectors.postgres_collector import PostgresCollector
from src.infrastructure.analyzers.explain_analyzer import ExplainAnalyzer
from src.infrastructure.analyzers.index_analyzer import IndexAnalyzer
from src.infrastructure.analyzers.basic_query_analyzer import BasicQueryAnalyzer
from src.domain.entities.recommendation import Recommendation, RecommendationStatus

logger = logging.getLogger(__name__)

class AnalyzeQueryUseCase:
    """Orchestrates the analysis of a specific slow query."""

    def __init__(
        self,
        db_repo: IDatabaseRepository,
        query_repo: IQueryRepository,
        rec_repo: IRecommendationRepository
    ):
        self.db_repo = db_repo
        self.query_repo = query_repo
        self.rec_repo = rec_repo
        self.explain_analyzer = ExplainAnalyzer()
        self.index_analyzer = IndexAnalyzer()
        self.basic_analyzer = BasicQueryAnalyzer()

    async def execute(self, query_id: UUID) -> None:
        """
        Analyze a query:
        1. Fetch query and database details
        2. Get EXPLAIN plan from target database
        3. Run ExplainAnalyzer and IndexAnalyzer
        4. Save recommendations
        """
        # 1. Fetch data
        query_entity = await self.query_repo.get_by_id(query_id)
        if not query_entity:
            logger.error(f"Query {query_id} not found for analysis")
            return

        database = await self.db_repo.get_by_id(query_entity.database_id)
        if not database:
            logger.error(f"Database {query_entity.database_id} not found for query {query_id}")
            return

        # 2. Get EXPLAIN plan using safe method
        # Note: In production, we'd handle connection strings more securely
        collector = PostgresCollector(database.encrypted_connection_string)
        
        # We only analyze SELECT queries for now to be safe
        if not query_entity.sql_text.strip().upper().startswith("SELECT"):
            logger.info(f"Skipping analysis for non-SELECT query {query_id}")
            return

        # Try to get EXPLAIN plan (handles parameterized queries)
        explain_plan = await collector.get_explain_plan_safe(query_entity.sql_text)
        
        recs_to_save = []
        
        if explain_plan:
            # Update query with EXPLAIN plan
            query_entity.explain_plan = explain_plan
            await self.query_repo.save(query_entity)

            # 3. Analyze with EXPLAIN-based analyzers
            explain_findings = self.explain_analyzer.analyze(explain_plan)
            index_recommendations = self.index_analyzer.analyze(query_entity.sql_text, explain_findings)

            # 4. Save recommendations from EXPLAIN analysis
            # Add explain findings as recommendations (mostly rewrite or schema suggestions)
            for finding in explain_findings:
                # We don't save raw Seq Scan findings if an Index recommendation exists for it
                # IndexAnalyzer already handles high-level index suggestions.
                if finding["type"] != "index":
                    recs_to_save.append(Recommendation(
                        query_id=query_id,
                        rec_type=finding["type"],
                        title=finding["title"],
                        description=finding["description"],
                        estimated_impact=finding["impact"] * 100,
                        confidence=finding["confidence"]
                    ))

            # Add index recommendations
            for rec in index_recommendations:
                recs_to_save.append(Recommendation(
                    query_id=query_id,
                    rec_type=rec["type"],
                    title=rec["title"],
                    description=rec["description"],
                    sql_suggestion=rec["sql_suggestion"],
                    estimated_impact=rec["estimated_impact"],
                    confidence=rec["confidence"]
                ))
        else:
            # No EXPLAIN plan available - use basic pattern-based analysis
            logger.info(f"Using basic analyzer for query {query_id} (no EXPLAIN plan available)")
            basic_recs = self.basic_analyzer.analyze(
                query_entity.sql_text, 
                query_entity.execution_time_ms
            )
            
            for rec in basic_recs:
                recs_to_save.append(Recommendation(
                    query_id=query_id,
                    rec_type=rec["type"],
                    title=rec["title"],
                    description=rec["description"],
                    sql_suggestion=rec.get("sql_suggestion"),
                    estimated_impact=rec["estimated_impact"],
                    confidence=rec["confidence"]
                ))

        if recs_to_save:
            await self.rec_repo.save_all(recs_to_save)
            logger.info(f"Saved {len(recs_to_save)} recommendations for query {query_id}")

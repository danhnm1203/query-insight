"""Unit tests for BasicQueryAnalyzer."""
import sys
sys.path.insert(0, '/app')

import pytest
from src.infrastructure.analyzers.basic_query_analyzer import BasicQueryAnalyzer
from src.domain.entities.recommendation import RecommendationType


class TestBasicQueryAnalyzer:
    """Test suite for BasicQueryAnalyzer."""

    @pytest.fixture
    def analyzer(self):
        """Create analyzer instance."""
        return BasicQueryAnalyzer()

    def test_detect_select_star(self, analyzer):
        """Test detection of SELECT * queries."""
        sql = "SELECT * FROM users WHERE id = 1"
        recommendations = analyzer.analyze(sql, execution_time_ms=100)
        
        assert len(recommendations) > 0
        select_star_rec = next(
            (r for r in recommendations if "SELECT *" in r.title),
            None
        )
        assert select_star_rec is not None
        assert select_star_rec.type == RecommendationType.REWRITE
        assert select_star_rec.confidence > 0

    def test_detect_missing_limit(self, analyzer):
        """Test detection of queries without LIMIT."""
        sql = "SELECT id, name FROM users WHERE active = true"
        recommendations = analyzer.analyze(sql, execution_time_ms=2000)
        
        limit_rec = next(
            (r for r in recommendations if "LIMIT" in r.title),
            None
        )
        assert limit_rec is not None
        assert limit_rec.type == RecommendationType.LIMIT
        assert limit_rec.estimated_impact > 0

    def test_detect_missing_where(self, analyzer):
        """Test detection of queries without WHERE clause."""
        sql = "SELECT id, name FROM users"
        recommendations = analyzer.analyze(sql, execution_time_ms=1500)
        
        where_rec = next(
            (r for r in recommendations if "WHERE" in r.title),
            None
        )
        assert where_rec is not None
        assert "full table scan" in where_rec.description.lower()

    def test_detect_like_wildcard_prefix(self, analyzer):
        """Test detection of LIKE '%...' patterns."""
        sql = "SELECT * FROM products WHERE name LIKE '%phone%'"
        recommendations = analyzer.analyze(sql, execution_time_ms=500)
        
        like_rec = next(
            (r for r in recommendations if "LIKE" in r.title or "full-text" in r.description.lower()),
            None
        )
        assert like_rec is not None

    def test_detect_multiple_or_conditions(self, analyzer):
        """Test detection of multiple OR conditions."""
        sql = "SELECT * FROM users WHERE status = 'active' OR status = 'pending' OR status = 'approved'"
        recommendations = analyzer.analyze(sql, execution_time_ms=300)
        
        or_rec = next(
            (r for r in recommendations if "OR" in r.title or "IN" in r.description),
            None
        )
        assert or_rec is not None

    def test_detect_subquery_in_select(self, analyzer):
        """Test detection of subqueries in SELECT clause."""
        sql = "SELECT id, (SELECT COUNT(*) FROM orders WHERE user_id = users.id) as order_count FROM users"
        recommendations = analyzer.analyze(sql, execution_time_ms=800)
        
        subquery_rec = next(
            (r for r in recommendations if "subquery" in r.title.lower() or "subquery" in r.description.lower()),
            None
        )
        assert subquery_rec is not None

    def test_detect_distinct_without_order_by(self, analyzer):
        """Test detection of DISTINCT without ORDER BY."""
        sql = "SELECT DISTINCT category FROM products"
        recommendations = analyzer.analyze(sql, execution_time_ms=400)
        
        distinct_rec = next(
            (r for r in recommendations if "DISTINCT" in r.title),
            None
        )
        assert distinct_rec is not None

    def test_no_recommendations_for_good_query(self, analyzer):
        """Test that well-optimized queries get no recommendations."""
        sql = "SELECT id, name, email FROM users WHERE id = 1 LIMIT 1"
        recommendations = analyzer.analyze(sql, execution_time_ms=10)
        
        # Should have minimal or no recommendations
        assert len(recommendations) <= 1

    def test_multiple_issues_detected(self, analyzer):
        """Test detection of multiple issues in one query."""
        sql = "SELECT * FROM users"  # SELECT *, no WHERE, no LIMIT
        recommendations = analyzer.analyze(sql, execution_time_ms=3000)
        
        # Should detect at least 2 issues
        assert len(recommendations) >= 2
        
        # Check for SELECT *
        assert any("SELECT *" in r.title for r in recommendations)
        
        # Check for missing LIMIT
        assert any("LIMIT" in r.title for r in recommendations)

    def test_recommendation_properties(self, analyzer):
        """Test that recommendations have all required properties."""
        sql = "SELECT * FROM users"
        recommendations = analyzer.analyze(sql, execution_time_ms=1000)
        
        for rec in recommendations:
            assert rec.type is not None
            assert rec.title is not None
            assert rec.description is not None
            assert rec.estimated_impact >= 0
            assert rec.estimated_impact <= 100
            assert rec.confidence >= 0
            assert rec.confidence <= 1
            assert rec.query_id is None  # Not set yet

    def test_impact_increases_with_execution_time(self, analyzer):
        """Test that impact estimates increase with execution time."""
        sql = "SELECT * FROM users"
        
        fast_recs = analyzer.analyze(sql, execution_time_ms=100)
        slow_recs = analyzer.analyze(sql, execution_time_ms=5000)
        
        # Find matching recommendations
        fast_limit = next((r for r in fast_recs if "LIMIT" in r.title), None)
        slow_limit = next((r for r in slow_recs if "LIMIT" in r.title), None)
        
        if fast_limit and slow_limit:
            assert slow_limit.estimated_impact >= fast_limit.estimated_impact

"""Unit tests for PostgresCollector.get_explain_plan_safe()."""
import sys
sys.path.insert(0, '/app')

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from src.infrastructure.collectors.postgres_collector import PostgresCollector


class TestPostgresCollectorExplainPlan:
    """Test suite for PostgresCollector.get_explain_plan_safe()."""

    @pytest.fixture
    def collector(self):
        """Create collector instance with mocked connection."""
        mock_conn_info = {
            "host": "localhost",
            "port": 5432,
            "database": "testdb",
            "user": "testuser",
            "password": "testpass"
        }
        return PostgresCollector(mock_conn_info)

    @pytest.mark.asyncio
    async def test_get_explain_plan_direct_success(self, collector):
        """Test successful EXPLAIN plan retrieval without parameters."""
        sql = "SELECT id, name FROM users WHERE id = 1"
        
        # Mock the database connection and cursor
        mock_cursor = AsyncMock()
        mock_cursor.fetchall.return_value = [
            {"QUERY PLAN": "Seq Scan on users"},
            {"QUERY PLAN": "  Filter: (id = 1)"}
        ]
        
        mock_conn = AsyncMock()
        mock_conn.cursor.return_value.__aenter__.return_value = mock_cursor
        
        with patch.object(collector, '_get_connection', return_value=mock_conn):
            plan = await collector.get_explain_plan_safe(sql)
        
        assert plan is not None
        assert "Seq Scan" in plan
        mock_cursor.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_explain_plan_with_parameter_substitution(self, collector):
        """Test EXPLAIN plan with parameter substitution fallback."""
        sql = "SELECT id, name FROM users WHERE id = $1 AND status = $2"
        
        # Mock first call to fail (parameterized query error)
        # Mock second call to succeed (with NULL substitution)
        mock_cursor = AsyncMock()
        mock_cursor.execute.side_effect = [
            Exception("bind message supplies 0 parameters, but prepared statement requires 2"),
            None  # Second call succeeds
        ]
        mock_cursor.fetchall.return_value = [
            {"QUERY PLAN": "Seq Scan on users"},
            {"QUERY PLAN": "  Filter: (id IS NULL AND status IS NULL)"}
        ]
        
        mock_conn = AsyncMock()
        mock_conn.cursor.return_value.__aenter__.return_value = mock_cursor
        
        with patch.object(collector, '_get_connection', return_value=mock_conn):
            plan = await collector.get_explain_plan_safe(sql)
        
        assert plan is not None
        assert "Seq Scan" in plan
        # Should have been called twice (first failed, second succeeded)
        assert mock_cursor.execute.call_count == 2

    @pytest.mark.asyncio
    async def test_replace_parameters_with_null(self, collector):
        """Test the _replace_parameters_with_null helper method."""
        sql_with_params = "SELECT * FROM users WHERE id = $1 AND name = $2 AND status = $3"
        expected = "SELECT * FROM users WHERE id = NULL AND name = NULL AND status = NULL"
        
        result = collector._replace_parameters_with_null(sql_with_params)
        assert result == expected

    @pytest.mark.asyncio
    async def test_replace_parameters_preserves_dollar_signs(self, collector):
        """Test that non-parameter dollar signs are preserved."""
        sql = "SELECT price FROM products WHERE price > $1 AND currency = '$$'"
        result = collector._replace_parameters_with_null(sql)
        
        # $1 should be replaced, but $$ should remain
        assert "NULL" in result
        assert "$$" in result

    @pytest.mark.asyncio
    async def test_get_explain_plan_returns_none_on_failure(self, collector):
        """Test that method returns None when both attempts fail."""
        sql = "INVALID SQL QUERY"
        
        mock_cursor = AsyncMock()
        mock_cursor.execute.side_effect = Exception("syntax error")
        
        mock_conn = AsyncMock()
        mock_conn.cursor.return_value.__aenter__.return_value = mock_cursor
        
        with patch.object(collector, '_get_connection', return_value=mock_conn):
            plan = await collector.get_explain_plan_safe(sql)
        
        assert plan is None

    @pytest.mark.asyncio
    async def test_get_explain_plan_handles_empty_result(self, collector):
        """Test handling of empty EXPLAIN result."""
        sql = "SELECT 1"
        
        mock_cursor = AsyncMock()
        mock_cursor.fetchall.return_value = []
        
        mock_conn = AsyncMock()
        mock_conn.cursor.return_value.__aenter__.return_value = mock_cursor
        
        with patch.object(collector, '_get_connection', return_value=mock_conn):
            plan = await collector.get_explain_plan_safe(sql)
        
        # Should return empty string or None for empty results
        assert plan == "" or plan is None

    @pytest.mark.asyncio
    async def test_get_explain_plan_formats_multiline(self, collector):
        """Test that multi-line EXPLAIN plans are properly formatted."""
        sql = "SELECT * FROM users JOIN orders ON users.id = orders.user_id"
        
        mock_cursor = AsyncMock()
        mock_cursor.fetchall.return_value = [
            {"QUERY PLAN": "Hash Join"},
            {"QUERY PLAN": "  Hash Cond: (orders.user_id = users.id)"},
            {"QUERY PLAN": "  ->  Seq Scan on orders"},
            {"QUERY PLAN": "  ->  Hash"},
            {"QUERY PLAN": "        ->  Seq Scan on users"}
        ]
        
        mock_conn = AsyncMock()
        mock_conn.cursor.return_value.__aenter__.return_value = mock_cursor
        
        with patch.object(collector, '_get_connection', return_value=mock_conn):
            plan = await collector.get_explain_plan_safe(sql)
        
        assert plan is not None
        assert "Hash Join" in plan
        assert "Seq Scan" in plan
        # Check that it's properly joined with newlines
        assert "\n" in plan

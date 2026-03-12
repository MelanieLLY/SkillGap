import pytest
from unittest.mock import MagicMock, patch
from server.migrate_roadmap import migrate

def test_migrate_success_postgres():
    """Test migration success on PostgreSQL path."""
    mock_conn = MagicMock()
    with patch("server.migrate_roadmap.engine.connect") as mock_connect:
        mock_connect.return_value.__enter__.return_value = mock_conn
        
        migrate()
        
        assert mock_conn.execute.called
        # Extract the SQL string from the TextClause object
        call_args = mock_conn.execute.call_args_list[0][0][0]
        assert "IF NOT EXISTS" in str(call_args.text)
        assert mock_conn.commit.called

def test_migrate_fallback_sqlite():
    """Test migration fallback to SQLite path when Postgres fails."""
    mock_conn = MagicMock()
    
    # First call to execute (Postgres) raises an exception
    mock_conn.execute.side_effect = [Exception("Postgres failed"), None, None, None]
    
    with patch("server.migrate_roadmap.engine.connect") as mock_connect:
        mock_connect.return_value.__enter__.return_value = mock_conn
        
        migrate()
        
        # Should have called execute at least twice (one failure, one fallback)
        assert mock_conn.execute.call_count >= 2
        
        # In the fallback, the 2nd call (index 1) should be the SQLite ALTER
        call_args = mock_conn.execute.call_args_list[1][0][0]
        assert "ALTER TABLE users ADD COLUMN roadmap JSON" in str(call_args.text)

def test_migrate_all_fail():
    """Test when both Postgres and SQLite migration paths fail."""
    mock_conn = MagicMock()
    
    # Raise exceptions for both paths
    mock_conn.execute.side_effect = Exception("Everything failed")
    
    with patch("server.migrate_roadmap.engine.connect") as mock_connect:
        mock_connect.return_value.__enter__.return_value = mock_conn
        
        migrate()
        
        assert mock_conn.execute.called

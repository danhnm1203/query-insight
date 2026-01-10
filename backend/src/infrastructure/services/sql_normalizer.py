import re
import sqlparse
from sqlparse.sql import Token, TokenList
from sqlparse.tokens import Keyword, Name, Number, String, Punctuation


class SqlNormalizer:
    """Service for normalizing SQL queries into fingerprints."""

    @staticmethod
    def normalize(sql: str) -> str:
        """
        Groups similar queries by replacing literals with placeholders.
        
        Example:
            SELECT * FROM users WHERE id = 10 -> SELECT * FROM users WHERE id = $1
        """
        if not sql:
            return ""

        # 1. Parse the SQL
        parsed = sqlparse.parse(sql)
        if not parsed:
            return sql

        statement = parsed[0]
        
        # 2. Iterate tokens and replace literals
        normalized_tokens = []
        placeholder_count = 1
        
        # We want to replace Numbers and Strings in WHERE/VALUES/etc.
        # but keep them if they are part of the structure (though sqlparse usually handles this)
        
        for token in statement.flatten():
            if token.ttype in (Number.Integer, Number.Float, Number.Hexadecimal):
                normalized_tokens.append(f"${placeholder_count}")
                placeholder_count += 1
            elif token.ttype in String:
                normalized_tokens.append(f"${placeholder_count}")
                placeholder_count += 1
            else:
                normalized_tokens.append(str(token))

        # 3. Clean up whitespace and join
        normalized_sql = "".join(normalized_tokens)
        
        # Further cleanup: collapse multiple spaces
        normalized_sql = re.sub(r'\s+', ' ', normalized_sql).strip()
        
        return normalized_sql

    @staticmethod
    def get_fingerprint(sql: str) -> str:
        """Alias for normalize, providing a clear domain concept."""
        return SqlNormalizer.normalize(sql)

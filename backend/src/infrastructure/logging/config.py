import json
import logging
import sys
from typing import Any

class JSONFormatter(logging.Formatter):
    """JSON log formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        log_obj: dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
        }
        
        # Add request_id if attached to record
        if hasattr(record, "request_id"):
             log_obj["request_id"] = record.request_id
             
        if record.exc_info:
            log_obj["exc_info"] = self.formatException(record.exc_info)
            
        return json.dumps(log_obj)

def configure_logging(level: str = "INFO"):
    """Configure structured logging for the application."""
    logger = logging.getLogger()
    logger.setLevel(level)
    
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    
    # Remove existing handlers to avoid duplication
    logger.handlers = []
    logger.addHandler(handler)
    
    # Configure uvicorn loggers to use our formatter
    for logger_name in ["uvicorn", "uvicorn.access", "uvicorn.error"]:
        log = logging.getLogger(logger_name)
        log.handlers = []
        log.addHandler(handler)
        log.propagate = False

from enum import Enum


class AnalysisStatus(str, Enum):
    PENDING = 'pending'
    RUNNING = 'running'
    COMPLETED = 'completed'
    FAILED = 'failed'


class AnalysisStageName(str, Enum):
    PLANNER = 'planner'
    MARKET_ANALYST = 'market_analyst'
    PRODUCT_MANAGER = 'product_manager'
    CRITIC = 'critic'
    EDITOR = 'editor'

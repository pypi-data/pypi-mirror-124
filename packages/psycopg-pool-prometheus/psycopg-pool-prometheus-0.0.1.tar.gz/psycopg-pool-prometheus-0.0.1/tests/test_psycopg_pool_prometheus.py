"""Tests."""

from unittest.mock import MagicMock

from prometheus_client.core import REGISTRY  # type: ignore
from psycopg_pool import ConnectionPool

import psycopg_pool_prometheus


def test_get_stats() -> None:
    """Test we can read Stats."""
    assert ConnectionPool(min_size=0).get_stats()["pool_size"] == 0


def test_register() -> None:
    """Test we can register a mock pool."""
    pool = MagicMock(spec=ConnectionPool)
    pool.get_stats.return_value = {"foo": 1}
    psycopg_pool_prometheus.register(pool)
    metrics = (m.name for m in REGISTRY.collect())  # pragma: no branch
    assert "psycopg_pool_foo" in metrics

import json
from django.core.cache import cache

CACHE_TTL = 60 * 60  # 1 hour

def get_cached_dashboard(dashboard_uuid):
    """Get cached dashboard data if available."""
    return cache.get(f"dashboard:{dashboard_uuid}")

def set_cached_dashboard(dashboard_uuid, data):
    """Cache dashboard data."""
    cache.set(f"dashboard:{dashboard_uuid}", data, CACHE_TTL)

def invalidate_dashboard_cache(dashboard_uuid):
    """Invalidate cached dashboard data."""
    cache.delete(f"dashboard:{dashboard_uuid}")

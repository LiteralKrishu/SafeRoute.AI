import redis
import pickle
import json
from datetime import timedelta
import streamlit as st

class CacheManager:
    def __init__(self):
        try:
            self.redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=False)
            self.redis_client.ping()
            self.redis_available = True
        except:
            self.redis_available = False
            self.memory_cache = {}
    
    def set(self, key, value, expire_minutes=10):
        \"\"\"Cache data with expiration\"\"\"
        if self.redis_available:
            try:
                self.redis_client.setex(
                    key, 
                    timedelta(minutes=expire_minutes), 
                    pickle.dumps(value)
                )
            except:
                self.memory_cache[key] = {
                    'value': value,
                    'expiry': st.datetime.now() + timedelta(minutes=expire_minutes)
                }
        else:
            self.memory_cache[key] = {
                'value': value,
                'expiry': st.datetime.now() + timedelta(minutes=expire_minutes)
            }
    
    def get(self, key):
        \"\"\"Retrieve cached data\"\"\"
        if self.redis_available:
            try:
                cached = self.redis_client.get(key)
                return pickle.loads(cached) if cached else None
            except:
                return self._get_from_memory(key)
        else:
            return self._get_from_memory(key)
    
    def _get_from_memory(self, key):
        \"\"\"Get from in-memory cache with expiry check\"\"\"
        if key in self.memory_cache:
            cache_entry = self.memory_cache[key]
            if st.datetime.now() < cache_entry['expiry']:
                return cache_entry['value']
            else:
                del self.memory_cache[key]
        return None

class CachedDataIngestion:
    def __init__(self):
        self.cache = CacheManager()
        from utils.database import DatabaseManager
        self.db = DatabaseManager()
    
    def get_cached_hazards(self, bbox, force_refresh=False):
        \"\"\"Get hazards with caching\"\"\"
        cache_key = f\"hazards_{bbox}\"
        
        if not force_refresh:
            cached = self.cache.get(cache_key)
            if cached is not None:
                st.sidebar.info(\"Using cached data\")
                return cached
        
        # Fetch fresh data
        from components.enhanced_data_ingestion import EnhancedDataIngestion
        data_ingestion = EnhancedDataIngestion()
        hazards = data_ingestion.get_real_time_hazards(bbox)
        
        # Cache for 5 minutes
        self.cache.set(cache_key, hazards, expire_minutes=5)
        
        return hazards

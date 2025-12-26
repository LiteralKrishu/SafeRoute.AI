import time
import functools
import streamlit as st

def time_execution(func):
    """Decorator to time function execution"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        execution_time = time.time() - start_time
        
        # Log slow operations
        if execution_time > 2.0:  # More than 2 seconds
            st.sidebar.warning(f" Slow operation: {func.__name__} took {execution_time:.2f}s")
        
        return result
    return wrapper

def retry_on_failure(max_retries=3, delay=1):
    """Retry decorator for API calls"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        st.error(f" Operation failed after {max_retries} attempts: {e}")
                        raise
                    time.sleep(delay * (attempt + 1))
            return None
        return wrapper
    return decorator

class PerformanceMonitor:
    def __init__(self):
        self.metrics = {}
    
    def start_timing(self, operation_name):
        self.metrics[operation_name] = {'start': time.time()}
    
    def end_timing(self, operation_name):
        if operation_name in self.metrics:
            self.metrics[operation_name]['end'] = time.time()
            self.metrics[operation_name]['duration'] = (
                self.metrics[operation_name]['end'] - self.metrics[operation_name]['start']
            )
    
    def get_report(self):
        """Generate performance report"""
        slow_operations = {
            op: data['duration'] 
            for op, data in self.metrics.items() 
            if data.get('duration', 0) > 1.0
        }
        return slow_operations

import sqlite3
import pandas as pd
import json
from datetime import datetime
import streamlit as st
from utils.error_handling import DataValidator

class DatabaseManager:
    def __init__(self):
        self.db_path = "data/safetroute.db"
        self._init_database()
    
    def _init_database(self):
        """Initialize SQLite database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Hazards table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS hazards (
                id TEXT PRIMARY KEY,
                hazard_type TEXT NOT NULL,
                severity INTEGER NOT NULL CHECK(severity >= 1 AND severity <= 5),
                confidence REAL NOT NULL CHECK(confidence >= 0 AND confidence <= 100),
                lat REAL NOT NULL CHECK(lat >= -90 AND lat <= 90),
                lon REAL NOT NULL CHECK(lon >= -180 AND lon <= 180),
                location TEXT,
                description TEXT,
                source TEXT,
                verified BOOLEAN DEFAULT FALSE,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                image_path TEXT,
                reporter_id TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY CHECK(length(username) >= 3),
                password_hash TEXT NOT NULL CHECK(length(password_hash) = 64),
                email TEXT NOT NULL CHECK(email LIKE '%_@__%.__%'),
                role TEXT DEFAULT 'user' CHECK(role IN ('user', 'admin', 'moderator')),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_login DATETIME,
                is_active BOOLEAN DEFAULT TRUE
            )
        ''')
        
        # Routes table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS routes (
                id TEXT PRIMARY KEY,
                start_lat REAL CHECK(start_lat >= -90 AND start_lat <= 90),
                start_lon REAL CHECK(start_lon >= -180 AND start_lon <= 180),
                end_lat REAL CHECK(end_lat >= -90 AND end_lat <= 90),
                end_lon REAL CHECK(end_lon >= -180 AND end_lon <= 180),
                route_data TEXT,
                safety_score INTEGER CHECK(safety_score >= 0 AND safety_score <= 100),
                calculated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                hazards_avoided TEXT
            )
        ''')
        
        # GPT Recommendations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS recommendations (
                id TEXT PRIMARY KEY,
                area TEXT NOT NULL,
                recommendation_data TEXT,
                generated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                implemented BOOLEAN DEFAULT FALSE,
                priority TEXT CHECK(priority IN ('Low', 'Medium', 'High', 'Critical')),
                estimated_cost TEXT,
                implementation_status INTEGER CHECK(implementation_status >= 0 AND implementation_status <= 100)
            )
        ''')
        
        # System logs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS system_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                level TEXT CHECK(level IN ('INFO', 'WARNING', 'ERROR', 'CRITICAL')),
                message TEXT,
                component TEXT,
                user_id TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_hazard(self, hazard_data):
        """Save hazard to database with validation"""
        DataValidator.validate_hazard_data(hazard_data)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT OR REPLACE INTO hazards 
                (id, hazard_type, severity, confidence, lat, lon, location, description, source, verified, timestamp, image_path, reporter_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                hazard_data['id'],
                hazard_data['hazard_type'],
                hazard_data['severity'],
                hazard_data.get('confidence', 50),
                hazard_data['lat'],
                hazard_data['lon'],
                hazard_data.get('location', ''),
                hazard_data.get('description', ''),
                hazard_data.get('source', 'Community'),
                hazard_data.get('verified', False),
                hazard_data.get('timestamp', datetime.now().isoformat()),
                hazard_data.get('image_path', ''),
                hazard_data.get('reporter_id', '')
            ))
            
            conn.commit()
            self._log_event('INFO', f"Hazard {hazard_data['id']} saved", 'database')
            
        except sqlite3.IntegrityError as e:
            self._log_event('ERROR', f"Database integrity error: {e}", 'database')
            raise ValueError(f"Invalid hazard data: {e}")
        except Exception as e:
            self._log_event('ERROR', f"Error saving hazard: {e}", 'database')
            raise
        finally:
            conn.close()
    
    def get_recent_hazards(self, hours=24, limit=1000):
        """Get recent hazards from database"""
        conn = sqlite3.connect(self.db_path)
        query = '''
            SELECT * FROM hazards 
            WHERE datetime(timestamp) >= datetime('now', ?)
            ORDER BY timestamp DESC
            LIMIT ?
        '''
        try:
            df = pd.read_sql_query(query, conn, params=(f'-{hours} hours', limit))
            self._log_event('INFO', f"Retrieved {len(df)} recent hazards", 'database')
            return df
        except Exception as e:
            self._log_event('ERROR', f"Error retrieving hazards: {e}", 'database')
            return pd.DataFrame()
        finally:
            conn.close()
    
    def get_hazard_stats(self):
        """Get hazard statistics for dashboard"""
        conn = sqlite3.connect(self.db_path)
        
        stats = {}
        
        try:
            # Total hazards by type
            type_query = "SELECT hazard_type, COUNT(*) as count FROM hazards GROUP BY hazard_type"
            type_stats = pd.read_sql_query(type_query, conn)
            stats['by_type'] = type_stats.to_dict('records')
            
            # Verification rate
            verification_query = """
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN verified = 1 THEN 1 ELSE 0 END) as verified_count
                FROM hazards
            """
            verification_stats = pd.read_sql_query(verification_query, conn)
            stats['verification_rate'] = (
                verification_stats['verified_count'].iloc[0] / verification_stats['total'].iloc[0] * 100 
                if verification_stats['total'].iloc[0] > 0 else 0
            )
            
            # Recent activity
            recent_query = """
                SELECT COUNT(*) as recent_count 
                FROM hazards 
                WHERE datetime(timestamp) >= datetime('now', '-1 hour')
            """
            recent_stats = pd.read_sql_query(recent_query, conn)
            stats['recent_activity'] = recent_stats['recent_count'].iloc[0]
            
            # Severity distribution
            severity_query = "SELECT severity, COUNT(*) as count FROM hazards GROUP BY severity ORDER BY severity"
            severity_stats = pd.read_sql_query(severity_query, conn)
            stats['by_severity'] = severity_stats.to_dict('records')
            
        except Exception as e:
            self._log_event('ERROR', f"Error getting hazard stats: {e}", 'database')
        finally:
            conn.close()
        
        return stats
    
    def get_user_reports(self, username):
        """Get reports by specific user"""
        DataValidator.validate_user_input(username, "dummy_password")
        
        conn = sqlite3.connect(self.db_path)
        query = """SELECT * FROM hazards WHERE reporter_id = ? ORDER BY timestamp DESC LIMIT 10"""
        try:
            df = pd.read_sql_query(query, conn, params=(username,))
            return df.to_dict('records')
        except Exception as e:
            self._log_event('ERROR', f"Error getting user reports: {e}", 'database')
            return []
        finally:
            conn.close()
    
    def _log_event(self, level, message, component):
        """Log system events"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO system_logs (level, message, component, user_id)
                VALUES (?, ?, ?, ?)
            ''', (
                level,
                message,
                component,
                st.session_state.get('user', {}).get('username', 'system')
            ))
            conn.commit()
        except:
            pass
        finally:
            conn.close()
    
    def cleanup_old_data(self, days_to_keep=30):
        """Clean up old data to prevent database bloat"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            # Delete hazards older than specified days
            cursor.execute('''
                DELETE FROM hazards 
                WHERE datetime(timestamp) < datetime('now', ?)
            ''', (f'-{days_to_keep} days',))
            
            # Delete old logs (keep only 7 days)
            cursor.execute('''
                DELETE FROM system_logs 
                WHERE datetime(timestamp) < datetime('now', '-7 days')
            ''')
            
            deleted_count = cursor.rowcount
            conn.commit()
            self._log_event('INFO', f"Cleaned up {deleted_count} old records", 'database')
            return deleted_count
            
        except Exception as e:
            self._log_event('ERROR', f"Error cleaning up data: {e}", 'database')
            return 0
        finally:
            conn.close()
    
    def get_database_stats(self):
        """Get database statistics"""
        conn = sqlite3.connect(self.db_path)
        stats = {}
        
        try:
            tables = ['hazards', 'users', 'routes', 'recommendations', 'system_logs']
            for table in tables:
                cursor = conn.cursor()
                cursor.execute(f'SELECT COUNT(*) as count FROM {table}')
                stats[table] = cursor.fetchone()[0]
            
            # Database size
            cursor = conn.cursor()
            cursor.execute("SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()")
            stats['database_size_bytes'] = cursor.fetchone()[0]
            
        except Exception as e:
            self._log_event('ERROR', f"Error getting database stats: {e}", 'database')
        finally:
            conn.close()
        
        return stats

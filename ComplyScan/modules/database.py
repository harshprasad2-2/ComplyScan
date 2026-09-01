"""
ComplyScan Database Module
Handles SQLite database initialization, schema, and queries for scan history.
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from modules.config import DATABASE_PATH

class ComplianceScanDB:
    """SQLite database handler for storing and retrieving compliance scans."""
    
    def __init__(self, db_path=DATABASE_PATH):
        """Initialize database connection."""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Create database tables if they don't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Scans table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS scans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_id TEXT UNIQUE NOT NULL,
                timestamp TEXT NOT NULL,
                filename TEXT,
                product_name TEXT,
                verdict TEXT,
                confidence_score REAL,
                image_path TEXT,
                report_path TEXT,
                extracted_fields TEXT,
                violations TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Declarations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS declarations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_id TEXT NOT NULL,
                field_name TEXT,
                extracted_value TEXT,
                confidence REAL,
                detection_method TEXT,
                status TEXT,
                FOREIGN KEY (scan_id) REFERENCES scans(scan_id)
            )
        ''')
        
        # Violations table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS violations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_id TEXT NOT NULL,
                rule_id TEXT,
                rule_description TEXT,
                severity TEXT,
                recommendation TEXT,
                FOREIGN KEY (scan_id) REFERENCES scans(scan_id)
            )
        ''')
        
        # Rules table (config-driven)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                rule_id TEXT UNIQUE,
                rule_description TEXT,
                legal_reference TEXT,
                check_type TEXT,
                parameters TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def save_scan(self, scan_data):
        """
        Save a scan to the database.
        
        Args:
            scan_data (dict): Dictionary containing scan information
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO scans 
            (scan_id, timestamp, filename, product_name, verdict, confidence_score, 
             image_path, report_path, extracted_fields, violations)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            scan_data.get('scan_id'),
            scan_data.get('timestamp'),
            scan_data.get('filename'),
            scan_data.get('product_name'),
            scan_data.get('verdict'),
            scan_data.get('confidence_score'),
            scan_data.get('image_path'),
            scan_data.get('report_path'),
            json.dumps(scan_data.get('extracted_fields', {})),
            json.dumps(scan_data.get('violations', []))
        ))
        
        conn.commit()
        conn.close()
    
    def get_scan_history(self, limit=50):
        """Get recent scans from history."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM scans ORDER BY created_at DESC LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def get_scan_by_id(self, scan_id):
        """Get a specific scan by ID."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM scans WHERE scan_id = ?', (scan_id,))
        row = cursor.fetchone()
        conn.close()
        
        return dict(row) if row else None
    
    def get_dashboard_stats(self):
        """Get statistics for dashboard."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM scans')
        total_scans = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM scans WHERE verdict = ?", ("COMPLIANT",))
        compliant = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM scans WHERE verdict = ?", ("NON-COMPLIANT",))
        non_compliant = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM scans WHERE verdict = ?", ("NEEDS REVIEW",))
        needs_review = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "total_scans": total_scans,
            "compliant": compliant,
            "non_compliant": non_compliant,
            "needs_review": needs_review
        }
    
    def clear_all_scans(self):
        """Clear all scan history (for testing)."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM declarations')
        cursor.execute('DELETE FROM violations')
        cursor.execute('DELETE FROM scans')
        
        conn.commit()
        conn.close()


# Singleton instance
_db_instance = None

def get_db():
    """Get singleton database instance."""
    global _db_instance
    if _db_instance is None:
        _db_instance = ComplianceScanDB()
    return _db_instance

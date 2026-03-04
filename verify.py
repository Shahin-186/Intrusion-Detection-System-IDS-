#!/usr/bin/env python3
"""
Smart Thermal Security System - Verification Script
Tests database connectivity and application initialization
"""

import sqlite3
import os
import sys

def check_file_structure():
    """Verify all required files exist"""
    print("🔍 Checking file structure...")
    
    required_files = [
        'app.py',
        'requirements.txt',
        'templates/base.html',
        'templates/login.html',
        'templates/dashboard.html',
        'templates/history.html',
        'static/style.css',
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print(f"  ✓ {file}")
    
    if missing_files:
        print(f"\n❌ Missing files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files present\n")
    return True

def check_database():
    """Check database connection and schema"""
    print("🔍 Checking database...")
    
    try:
        # Check if database file exists
        if not os.path.exists('security_system.db'):
            print("  ℹ️  Database doesn't exist yet, will be created on first run")
            return True
        
        # Connect to database
        conn = sqlite3.connect('security_system.db')
        cursor = conn.cursor()
        
        # Check events table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='events'")
        if cursor.fetchone():
            print("  ✓ events table exists")
            
            # Check table schema
            cursor.execute("PRAGMA table_info(events)")
            columns = cursor.fetchall()
            expected_columns = ['id', 'timestamp', 'temperature', 'status']
            actual_columns = [col[1] for col in columns]
            
            for col in expected_columns:
                if col in actual_columns:
                    print(f"    ✓ Column '{col}' present")
                else:
                    print(f"    ❌ Column '{col}' missing")
                    return False
            
            # Count events
            cursor.execute("SELECT COUNT(*) FROM events")
            count = cursor.fetchone()[0]
            print(f"  ℹ️  {count} event(s) in database")
        else:
            print("  ℹ️  events table will be created on first run")
        
        conn.close()
        print("✅ Database check passed\n")
        return True
        
    except Exception as e:
        print(f"❌ Database error: {e}\n")
        return False

def check_python_modules():
    """Check if required Python modules are installed"""
    print("🔍 Checking Python modules...")
    
    required_modules = {
        'flask': 'Flask',
        'werkzeug': 'Werkzeug',
    }
    
    missing_modules = []
    for module, name in required_modules.items():
        try:
            __import__(module)
            print(f"  ✓ {name} installed")
        except ImportError:
            missing_modules.append(name)
            print(f"  ❌ {name} not installed")
    
    if missing_modules:
        print(f"\n❌ Missing modules: {', '.join(missing_modules)}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    print("✅ All Python modules installed\n")
    return True

def check_app_import():
    """Test if app.py can be imported"""
    print("🔍 Testing app.py import...")
    
    try:
        # Add current directory to path
        sys.path.insert(0, os.getcwd())
        
        # Try to import app module
        import app
        print("  ✓ app.py imports successfully")
        print(f"  ✓ Admin username: {app.ADMIN_USERNAME}")
        print(f"  ✓ Database: {app.DATABASE}")
        print("✅ Application module check passed\n")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}\n")
        return False

def main():
    """Run all verification checks"""
    print("=" * 60)
    print("Smart Thermal Security System - Verification")
    print("=" * 60)
    print()
    
    checks = [
        ("File Structure", check_file_structure),
        ("Python Modules", check_python_modules),
        ("Application Import", check_app_import),
        ("Database", check_database),
    ]
    
    results = []
    for name, check_func in checks:
        result = check_func()
        results.append((name, result))
    
    # Print summary
    print("=" * 60)
    print("VERIFICATION SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{name}: {status}")
        if not result:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n✅ ALL CHECKS PASSED!")
        print("\nYou can now run the application:")
        print("  python3 app.py")
        print("\nOr use the startup script:")
        print("  ./start.sh")
        print("\nDefault credentials:")
        print("  Username: admin")
        print("  Password: admin123")
        print()
        return 0
    else:
        print("\n❌ SOME CHECKS FAILED")
        print("Please fix the issues above before running the application.\n")
        return 1

if __name__ == '__main__':
    exit(main())

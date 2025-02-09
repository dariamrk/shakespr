# scripts/setup_db.py
import psycopg2
from pathlib import Path
from dotenv import load_dotenv
import os

def setup_databases():
    # Load environment variables
    env_path = Path(__file__).parent.parent / 'config' / '.env'
    load_dotenv(dotenv_path=env_path)
    
    # Connect as postgres superuser
    try:
        conn = psycopg2.connect(
            dbname='postgres',
            user='postgres',
            password='postgres',
            host='localhost',
            port='5432'
        )
        conn.autocommit = True
        
        with conn.cursor() as cur:
            # Create user_data database if it doesn't exist
            cur.execute("SELECT 1 FROM pg_database WHERE datname = 'user_data'")
            if not cur.fetchone():
                cur.execute("CREATE DATABASE user_data")
                print("Created user_data database")
            
            # Create numbeo_data database if it doesn't exist
            cur.execute("SELECT 1 FROM pg_database WHERE datname = 'numbeo_data'")
            if not cur.fetchone():
                cur.execute("CREATE DATABASE numbeo_data")
                print("Created numbeo_data database")
            
            # Create roles if they don't exist
            for role, password in [('bot_admin', '1234'), ('numbeo_admin', '1234')]:
                cur.execute(f"SELECT 1 FROM pg_roles WHERE rolname = '{role}'")
                if not cur.fetchone():
                    cur.execute(f"""
                        CREATE ROLE {role} WITH 
                        LOGIN
                        PASSWORD '{password}'
                        CREATEDB
                        INHERIT
                    """)
                    print(f"Created {role} role")

        conn.close()
        
        # Setup user_data database
        conn = psycopg2.connect(
            dbname='user_data',
            user='postgres',
            password='postgres',
            host='localhost',
            port='5432'
        )
        conn.autocommit = True
        
        with conn.cursor() as cur:
            # Create bot schema
            cur.execute("CREATE SCHEMA IF NOT EXISTS bot")
            
            # Grant permissions to bot_admin
            cur.execute("""
                GRANT ALL ON SCHEMA bot TO bot_admin;
                ALTER DEFAULT PRIVILEGES IN SCHEMA bot GRANT ALL ON TABLES TO bot_admin;
                ALTER DEFAULT PRIVILEGES IN SCHEMA bot GRANT ALL ON SEQUENCES TO bot_admin;
                ALTER DEFAULT PRIVILEGES IN SCHEMA bot GRANT ALL ON FUNCTIONS TO bot_admin;
            """)
            
            # Execute schema initialization
            schema_path = Path(__file__).parent.parent / 'sql' / 'user_data' / 'schema' / 'init.sql'
            with open(schema_path, 'r') as f:
                cur.execute(f.read())
                
            # Execute procedures
            procedures_path = Path(__file__).parent.parent / 'sql' / 'user_data' / 'procedures' / 'user_procedures.sql'
            with open(procedures_path, 'r') as f:
                cur.execute(f.read())
            
            # Grant permissions on existing objects
            cur.execute("""
                GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA bot TO bot_admin;
                GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA bot TO bot_admin;
                GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA bot TO bot_admin;
            """)
            
            print("Initialized user_data database and granted permissions")
            
        conn.close()
        
        # Setup numbeo_data database similarly
        conn = psycopg2.connect(
            dbname='numbeo_data',
            user='postgres',
            password='postgres',
            host='localhost',
            port='5432'
        )
        conn.autocommit = True
        
        with conn.cursor() as cur:
            # Create numbeo schema
            cur.execute("CREATE SCHEMA IF NOT EXISTS numbeo_col")
            
            # Grant permissions to numbeo_admin
            cur.execute("""
                GRANT ALL ON SCHEMA numbeo_col TO numbeo_admin;
                ALTER DEFAULT PRIVILEGES IN SCHEMA numbeo_col GRANT ALL ON TABLES TO numbeo_admin;
                ALTER DEFAULT PRIVILEGES IN SCHEMA numbeo_col GRANT ALL ON SEQUENCES TO numbeo_admin;
                ALTER DEFAULT PRIVILEGES IN SCHEMA numbeo_col GRANT ALL ON FUNCTIONS TO numbeo_admin;
            """)
            
            # Execute schema initialization
            schema_path = Path(__file__).parent.parent / 'sql' / 'numbeo_data' / 'schema' / 'init.sql'
            with open(schema_path, 'r') as f:
                cur.execute(f.read())
                
            # Execute procedures
            procedures_path = Path(__file__).parent.parent / 'sql' / 'numbeo_data' / 'procedures' / 'numbeo_procedures.sql'
            with open(procedures_path, 'r') as f:
                cur.execute(f.read())
            
            # Grant permissions on existing objects
            cur.execute("""
                GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA numbeo_col TO numbeo_admin;
                GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA numbeo_col TO numbeo_admin;
                GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA numbeo_col TO numbeo_admin;
            """)
            
            print("Initialized numbeo_data database and granted permissions")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    setup_databases()

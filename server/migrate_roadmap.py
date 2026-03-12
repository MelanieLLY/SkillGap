from server.database import engine
from sqlalchemy import text


def migrate():
    print("Checking for roadmap column...")
    with engine.connect() as conn:
        try:
            # For PostgreSQL
            conn.execute(
                text("ALTER TABLE users ADD COLUMN IF NOT EXISTS roadmap JSONB;")
            )
            conn.execute(
                text(
                    "ALTER TABLE analysis_history ADD COLUMN IF NOT EXISTS jd_text TEXT;"
                )
            )
            conn.commit()
            print("Successfully updated PostgreSQL tables.")
        except Exception as e:
            print(f"Postgres migration failed or not applicable: {e}")
            try:
                # Fallback for SQLite
                conn.execute(text("ALTER TABLE users ADD COLUMN roadmap JSON;"))
                conn.execute(
                    text("ALTER TABLE analysis_history ADD COLUMN jd_text TEXT;")
                )
                conn.commit()
                print("Successfully updated SQLite tables.")
            except Exception as e2:
                print(f"Columns might already exist or SQLite error: {e2}")


if __name__ == "__main__":
    migrate()

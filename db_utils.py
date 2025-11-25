from typing import Sequence
from sqlalchemy import text
from sqlalchemy.engine import Engine


APPOINTMENT_STATUS_VALUES: Sequence[str] = ("confirm", "decline", "pending", "cancel")
APPOINTMENT_STATUS_CONSTRAINT = "appointment_status_check"


def ensure_appointment_status_constraint(engine: Engine) -> None:
    """
    Make sure the appointment status check constraint allows all expected values.
    This keeps legacy databases in sync without requiring a manual migration.
    """
    allowed_marker = "'cancel'"
    constraint_def_query = text(
        """
        SELECT pg_get_constraintdef(c.oid)
        FROM pg_constraint c
        JOIN pg_class t ON c.conrelid = t.oid
        WHERE t.relname = 'appointment' AND c.conname = :constraint_name
        """
    )
    values_sql = ", ".join(f"'{value}'::character varying" for value in APPOINTMENT_STATUS_VALUES)
    add_constraint_sql = text(
        f"""
        ALTER TABLE appointment
        ADD CONSTRAINT {APPOINTMENT_STATUS_CONSTRAINT}
        CHECK (((status)::text = ANY ((ARRAY[{values_sql}])::text[])))
        """
    )

    with engine.begin() as conn:
        result = conn.execute(
            constraint_def_query,
            {"constraint_name": APPOINTMENT_STATUS_CONSTRAINT}
        ).scalar()
        if result and allowed_marker in result:
            return
        drop_sql = text(
            f"ALTER TABLE appointment DROP CONSTRAINT IF EXISTS {APPOINTMENT_STATUS_CONSTRAINT}"
        )
        conn.execute(drop_sql)
        conn.execute(add_constraint_sql)


"""adding new constraint

Revision ID: 8221adb4c3d5
Revises: 995abc893842
Create Date: 2026-01-21 21:23:31.611750

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8221adb4c3d5'
down_revision: Union[str, Sequence[str], None] = '995abc893842'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Reject empty or whitespace-only title
    op.create_check_constraint(
        "tasks_title_not_empty",
        "tasks",
        "length(trim(title)) > 0"
    )

    # Reject empty or whitespace-only description
    op.create_check_constraint(
        "tasks_description_not_empty",
        "tasks",
        "length(trim(description)) > 0"
    )


def downgrade() -> None:
    op.drop_constraint(
        "tasks_title_not_empty",
        "tasks",
        type_="check"
    )

    op.drop_constraint(
        "tasks_description_not_empty",
        "tasks",
        type_="check"
    )

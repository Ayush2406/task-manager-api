"""empty message

Revision ID: 995abc893842
Revises: a97c678eb2f7
Create Date: 2026-01-20 20:31:02.371864

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '995abc893842'
down_revision: Union[str, Sequence[str], None] = 'a97c678eb2f7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_check_constraint(
        "valid_check_status",
        "tasks",
        "status IN ('pending','in_progress','completed')"
    )

def downgrade() -> None:
    op.drop_constraint(
        "valid_check_status",
        "tasks",
        type_="check"
    )
"""Testing alembic table creation

Revision ID: 0acf2ee7a9f7
Revises: 
Create Date: 2023-12-05 13:44:01.767930

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0acf2ee7a9f7'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

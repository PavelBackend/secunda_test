from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "enable_geo"
down_revision = "89be2d7d20b6"
branch_labels = None
depends_on = None

def upgrade():
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis_topology")

def downgrade():
    pass

from app.db.models import Base


def upgrade(engine):
    """รองรับ CON-TECH-01, DOM-PDPA-01, IF-HIS-01"""
    Base.metadata.create_all(bind=engine)


def downgrade(engine):
    """รองรับ CON-TECH-01, DOM-PDPA-01, IF-HIS-01"""
    return None

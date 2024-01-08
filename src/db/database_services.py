from sqlalchemy.orm import sessionmaker

from src.db import engine
from src.db.models import CourseSection

Session = sessionmaker(bind=engine)


def get_nrcs_from_bd():
    session = Session()
    try:
        nrcs = session.query(CourseSection.nrc).all()
        nrc_list = [nrc[0] for nrc in nrcs]
        return nrc_list
    except Exception as e:
        print(f"Error al obtener nrcs: {e}")
        return []
    finally:
        session.close()


if __name__ == "__main__":
    nrcs = get_nrcs_from_bd()
    print(nrcs)

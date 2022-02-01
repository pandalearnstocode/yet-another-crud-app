from sqlalchemy.orm import Session
from uuid import UUID
from models import Model, ModelSchema

def crud_post(db_session: Session, payload: ModelSchema):
    model = Model(
        title=payload.title,
        description=payload.description,
        status=payload.status,
        country=payload.country,
        email=payload.email,
        user_group=payload.user_group,
    )
    db_session.add(model)
    db_session.commit()
    db_session.refresh(model)
    return model


def crud_get(db_session: Session, id: UUID):
    return db_session.query(Model).filter(Model.id == id).first()


def crud_get_all(db_session: Session):
    return db_session.query(Model).all()


def crud_put(
    db_session: Session,
    model: Model,
    title: str,
    description: str,
    status: str,
    country: str,
    email: str,
    user_group: str,
):
    model.status = status
    if title:
        model.title = title
    if description:
        model.description = description
    if country:
        model.country = country
    if email:
        model.email = email
    if user_group:
        model.user_group = user_group
    db_session.commit()
    return model


def crud_delete(db_session: Session, id: UUID):
    model = db_session.query(Model).filter(Model.id == id).first()
    db_session.delete(model)
    db_session.commit()
    return model
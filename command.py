import asyncio

import typer
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import settings
from src.auth.service import get_password_hash
from src.users.models import User

app = typer.Typer()
engine = create_async_engine(str(settings.db.url))
Session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


@app.command()
async def create_admin_user():
    login = typer.prompt("Введите логин")
    password = typer.prompt("Введите пароль")
    session = Session()
    hashed_password = get_password_hash(password)
    user = User(login=login, password=hashed_password, is_admin=True)
    try:
        session.add(user)
        await session.commit()
        typer.echo(f"Admin user '{user.login}' created successfully!")
    except Exception as e:
        typer.echo(f"Error: {str(e)}")


if __name__ == "__main__":
    asyncio.run(create_admin_user())

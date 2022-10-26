"""Add a user from the command line, optionally make superuser."""
import asyncclick as click
from fastapi import HTTPException

from db import database
from managers.user import UserManager
from models.enums import RoleType


@click.group()
def user_commands():
    """Add a new User to the Database.

    Optionally, make this a Super-user.
    """


@click.command()
@click.option(
    "-e",
    "--email",
    type=str,
    required=True,
    prompt="Enter user's Email Address",
)
@click.option(
    "-f",
    "--first_name",
    type=str,
    required=True,
    prompt="Enter user's First Name",
)
@click.option(
    "-l",
    "--last_name",
    type=str,
    required=True,
    prompt="Enter user's Last Name",
)
@click.option(
    "-p",
    "--password",
    type=str,
    required=True,
    prompt="Enter a strong Password",
)
@click.option(
    "-a",
    "--admin",
    type=str,
    required=True,
    prompt="Should this user be an Admin (y/n)",
    default="n",
)
async def create(email, first_name, last_name, password, admin):
    """Create a new user.

    Values are either taken from the command line options, or interactively for
    any that are missing.
    """
    admin = admin[0].lower()
    if admin == "y":
        role_type = RoleType.admin
    else:
        role_type = RoleType.user

    user_data = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "password": password,
        "role": role_type,
    }

    try:
        await database.connect()
        await UserManager.register(user_data)
        await database.disconnect()
        print(f'\nUser {user_data["email"]} added succesfully.\n')
    except HTTPException as e:
        print(f"\nERROR adding User : {e.detail}\n")
    except Exception as e:
        print(f"\nERROR adding User : {e}\n")


# Add the commands to the group.
user_commands.add_command(create)
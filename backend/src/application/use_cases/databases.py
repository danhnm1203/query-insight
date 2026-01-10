"""Database management use cases."""
from typing import List
from uuid import uuid4, UUID

from src.application.dto.database_dto import DatabaseCreate, DatabaseRead
from src.application.interfaces.repositories.database_repository import IDatabaseRepository
from src.domain.entities.database import Database


class RegisterDatabaseUseCase:
    """UseCase for connecting a new database."""

    def __init__(self, db_repo: IDatabaseRepository):
        self.db_repo = db_repo

    async def execute(self, user_id: UUID, db_create: DatabaseCreate) -> DatabaseRead:
        """Execute database registration."""
        # TODO: Implement connection string encryption
        # For now, we store it as is (plaintext in PoC)
        
        database = Database(
            user_id=user_id,
            name=db_create.name,
            db_type=db_create.type,
            encrypted_connection_string=db_create.connection_string,
            database_id=uuid4()
        )

        saved_db = await self.db_repo.save(database)
        return DatabaseRead.model_validate(saved_db)


class GetDatabasesUseCase:
    """UseCase for retrieving all databases of a user."""

    def __init__(self, db_repo: IDatabaseRepository):
        self.db_repo = db_repo

    async def execute(self, user_id: UUID) -> List[DatabaseRead]:
        """Execute retrieval."""
        databases = await self.db_repo.get_by_user_id(user_id)
        return [DatabaseRead.model_validate(db) for db in databases]


class DeleteDatabaseUseCase:
    """UseCase for deleting a database."""

    def __init__(self, db_repo: IDatabaseRepository):
        self.db_repo = db_repo

    async def execute(self, user_id: UUID, database_id: UUID) -> None:
        """Execute deletion."""
        # Check ownership
        database = await self.db_repo.get_by_id(database_id)
        if not database:
            return  # Idempotent
            
        if database.user_id != user_id:
            raise PermissionError("User does not own this database")
            
        await self.db_repo.delete(database_id)

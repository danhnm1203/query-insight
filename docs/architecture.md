# QueryInsight Architecture

## Overview

QueryInsight follows **Clean Architecture** principles to ensure separation of concerns, testability, and maintainability.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Presentation Layer                        │
│                    (FastAPI REST API, Routes)                     │
└────────────────────────┬──────────────────────────────────────────┘
                         │
┌────────────────────────▼──────────────────────────────────────────┐
│                      Application Layer                            │
│            (Use Cases, DTOs, Interfaces, Services)                │
└────────────────────────┬──────────────────────────────────────────┘
                         │
┌────────────────────────▼──────────────────────────────────────────┐
│                        Domain Layer                                │
│              (Entities, Value Objects, Business Logic)            │
└────────────────────────┬──────────────────────────────────────────┘
                         │
┌────────────────────────▼──────────────────────────────────────────┐
│                    Infrastructure Layer                            │
│     (Database, Redis, Collectors, Analyzers, External Services)   │
└───────────────────────────────────────────────────────────────────┘
```

## Layer Responsibilities

### 1. Domain Layer (`src/domain/`)

The **core business logic** that is independent of external concerns.

**Entities:**
- `Query`: Represents a database query execution
- `Database`: Represents a connected database
- `Metric`: Represents performance metrics
- `Recommendation`: Represents optimization suggestions
- `User`: Represents application users

**Value Objects:**
- Immutable objects representing domain concepts
- Examples: `TimeRange`, `ExecutionPlan`, `IndexSuggestion`

**Rules:**
- No dependencies on outer layers
- Pure business logic
- Framework agnostic

### 2. Application Layer (`src/application/`)

**Orchestrates** the flow of data between layers.

**Use Cases:**
- `CollectMetricsUseCase`: Collects metrics from databases
- `AnalyzeQueryUseCase`: Analyzes slow queries and generates recommendations
- `GetQueryInsightsUseCase`: Retrieves dashboard data

**DTOs (Data Transfer Objects):**
- `QueryDTO`, `DatabaseDTO`, `MetricDTO`
- Used for API requests/responses

**Interfaces:**
- Repository interfaces (e.g., `IQueryRepository`)
- Service interfaces (e.g., `IAnalyzerService`)
- Unit of Work pattern

**Rules:**
- Depends only on Domain layer
- No knowledge of frameworks or infrastructure
- Defines contracts (interfaces) for infrastructure

### 3. Infrastructure Layer (`src/infrastructure/`)

**Implements** the interfaces defined in Application layer.

**Components:**

**Database (`infrastructure/database/`):**
- SQLAlchemy models
- Repository implementations
- PostgreSQL + TimescaleDB interactions

**Cache (`infrastructure/cache/`):**
- Redis implementation
- Caching strategies

**Queue (`infrastructure/queue/`):**
- Celery tasks
- Message queue handling

**Collectors (`infrastructure/collectors/`):**
- `PostgresCollector`: Collects metrics from PostgreSQL
- `MySQLCollector`: Collects metrics from MySQL
- `MongoDBCollector`: Collects metrics from MongoDB

**Analyzers (`infrastructure/analyzers/`):**
- `ExplainAnalyzer`: Parses EXPLAIN plans
- `IndexAnalyzer`: Generates index recommendations
- `PatternDetector`: Detects N+1 queries, missing pagination

**Rules:**
- Implements interfaces from Application layer
- Contains all external dependencies
- Can be replaced without affecting business logic

### 4. Presentation Layer (`src/presentation/`)

**Delivers** the application to users via HTTP API.

**Components:**
- FastAPI routes
- Request/response models (Pydantic)
- Authentication middleware
- Error handling

**API Structure:**
```
/api/v1/
  ├── /databases         # Database management
  ├── /queries           # Query analysis
  ├── /metrics           # Performance metrics
  ├── /recommendations   # Optimization suggestions
  └── /auth              # Authentication
```

**Rules:**
- Depends on Application layer
- Handles HTTP concerns (serialization, validation)
- No business logic

## Data Flow Example

**Analyzing a Slow Query:**

```
1. [Presentation] POST /api/v1/databases/{id}/analyze
   ↓
2. [Application] AnalyzeQueryUseCase.execute()
   ↓
3. [Infrastructure] PostgresCollector.collect_slow_queries()
   ↓
4. [Infrastructure] ExplainAnalyzer.analyze(explain_plan)
   ↓
5. [Infrastructure] IndexAnalyzer.recommend_indexes()
   ↓
6. [Domain] Recommendation entities created
   ↓
7. [Infrastructure] Save to database
   ↓
8. [Application] Send to message queue for processing
   ↓
9. [Presentation] Return recommendations to client
```

## Dependency Rule

**Dependencies point inward:**
- Presentation → Application → Domain
- Infrastructure → Application → Domain
- **Never** the reverse

This ensures:
- Business logic is independent
- Easy to test
- Easy to swap implementations
- Flexible architecture

## Technology Choices

| Layer | Technologies |
|-------|-------------|
| Presentation | FastAPI, Pydantic |
| Application | Python classes, dependency injection |
| Domain | Pure Python (no dependencies) |
| Infrastructure | PostgreSQL, Redis, Celery, SQLAlchemy |

## Testing Strategy

- **Domain Layer**: Unit tests (100% coverage goal)
- **Application Layer**: Unit tests with mocked repositories
- **Infrastructure Layer**: Integration tests with test database
- **Presentation Layer**: API tests with TestClient

## Benefits of This Architecture

1. **Testability**: Easy to mock dependencies
2. **Flexibility**: Swap PostgreSQL for another DB without changing business logic
3. **Maintainability**: Clear separation of concerns
4. **Scalability**: Add new features without breaking existing code
5. **Team Collaboration**: Multiple developers can work on different layers

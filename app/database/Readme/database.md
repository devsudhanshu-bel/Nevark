# Database Configuration

## 1. Overview

The `database.py` module establishes the database connectivity and session-management layer for the Nevark AI backend.

It uses SQLAlchemy as its Object Relational Mapping (ORM) framework and SQLite as its database engine.

The module is responsible for:

- Configuring the SQLite database connection.
- Creating the SQLAlchemy engine.
- Defining a reusable database session factory.
- Initializing the declarative base for ORM models.
- Providing a database session dependency through `get_db()`.

This module centralizes database configuration so that other backend components can access the database without independently creating connections or session factories.

## 2. Dependencies

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
```

| Dependency | Purpose |
|---|---|
| `create_engine` | Creates the SQLAlchemy database engine |
| `declarative_base` | Creates the base class used for defining ORM models |
| `sessionmaker` | Creates a configurable database session factory |

## 3. Database Configuration

```python
DATABASE_URL = "sqlite:///./nevark.db"
```

The module defines the database connection URL.

| Property | Value |
|---|---|
| Database type | SQLite |
| Database name | `nevark.db` |
| Database URL | `sqlite:///./nevark.db` |
| Storage | Local file |
| Relative location | Application working directory |

The `./` indicates that the database file is located relative to the application's current working directory.

This configuration allows Nevark to use a local SQLite database without requiring a separately hosted database server.

## 4. SQLAlchemy Engine Initialization

```python
engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)
```

The `create_engine()` function initializes the SQLAlchemy engine using the configured database URL.

The engine acts as the central interface through which SQLAlchemy communicates with the database.

### SQLite connection configuration

```python
connect_args={
    "check_same_thread": False
}
```

SQLite normally restricts a connection to the thread that created it.

Setting `check_same_thread` to `False` disables that SQLite thread check.

This is commonly used in FastAPI applications where database operations may occur across different execution threads.

**Important:** This setting does not make SQLAlchemy sessions automatically thread-safe. Individual sessions should still be managed appropriately.

## 5. Database Session Factory

```python
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
```

The `sessionmaker()` function creates a reusable factory for generating SQLAlchemy database sessions.

The resulting factory is stored in `SessionLocal`.

Whenever a component needs database access, it can create a session by calling:

```python
db = SessionLocal()
```

### Session configuration

| Parameter | Value | Purpose |
|---|---|---|
| `autocommit` | `False` | Disables automatic transaction commits |
| `autoflush` | `False` | Disables automatic flushing before queries |
| `bind` | `engine` | Associates sessions with the configured database engine |

### Autocommit

With `autocommit=False`, database transactions are not automatically committed through the session's normal operations.

Changes generally need to be committed explicitly:

```python
db.add(record)
db.commit()
```

### Autoflush

With `autoflush=False`, SQLAlchemy does not automatically flush pending changes before every query.

A flush can be explicitly requested when required:

```python
db.flush()
```

### Bind

The `bind=engine` parameter associates sessions created by this factory with the SQLite database engine.

## 6. Declarative Base Initialization

```python
Base = declarative_base()
```

The declarative base provides the foundation for defining SQLAlchemy ORM models.

Database model classes can inherit from `Base` to declare their corresponding database tables.

For example, an illustrative model structure would look like:

```python
class ExampleModel(Base):
    __tablename__ = "example"

    # Model columns are defined here.
```

The actual table definitions are maintained separately in the database model module.

The shared `Base` allows ORM models to use the same SQLAlchemy metadata registry.

## 7. Core Function: `get_db()`

```python
def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()
```

The `get_db()` function provides a database session to calling components.

It uses Python's `yield` statement to provide the session and retain control of cleanup after the caller finishes using it.

### Step 1: Create a database session

```python
db = SessionLocal()
```

A new SQLAlchemy session is created using the configured session factory.

This session is used for database operations performed by the calling component.

### Step 2: Provide the session

```python
try:
    yield db
```

The session is yielded to the caller.

In a FastAPI application, this function can be used as a dependency to provide database access to route handlers.

For example:

```python
from fastapi import Depends

@router.get("/example")
def example_route(db = Depends(get_db)):
    # Perform database operations using db
    ...
```

This is an illustrative integration pattern.

### Step 3: Close the session

```python
finally:
    db.close()
```

The `finally` block executes when the dependency's execution context finishes, including when an exception occurs after the session has been yielded.

The session is closed to release its associated database resources.

This helps prevent database sessions from remaining open after request processing.

## 8. Database Session Lifecycle

The session lifecycle follows this sequence:

1. A route or backend component requests database access.
2. `get_db()` creates a session through `SessionLocal`.
3. The session is yielded to the calling component.
4. The component performs its database operations.
5. The caller completes or raises an exception.
6. The `finally` block executes.
7. The database session is closed.

Each invocation of `get_db()` creates a separate session.

## 9. Integration with Other Database Components

The module provides three important objects for the rest of the database layer.

| Object | Responsibility |
|---|---|
| `engine` | Database connectivity |
| `SessionLocal` | Database session creation |
| `Base` | ORM model declaration |

Other database components can import these objects instead of defining their own database configuration.

The intended separation is:

- `database.py` manages connectivity and sessions.
- `models.py` defines database table structures.
- `schemas.py` defines data validation and serialization structures.

The actual implementation of models and schemas is documented separately.

## 10. Current Implementation Scope

The module currently provides:

- SQLite database configuration.
- SQLAlchemy engine initialization.
- SQLite thread-check configuration.
- Reusable session factory.
- Explicit transaction configuration.
- Declarative ORM base initialization.
- Database session dependency.
- Session cleanup through a `finally` block.

The module does not currently implement:

- Database table definitions.
- Database migrations.
- Database initialization or table creation.
- Connection pooling customization.
- Multiple database connections.
- Database backup or recovery.
- Database authentication.
- Explicit transaction-management utilities.

These responsibilities are not defined in the supplied source file.

## 11. Summary

The `database.py` module provides the database foundation for the Nevark AI backend.

It configures a local SQLite database through SQLAlchemy, initializes the engine, creates a reusable session factory, and provides the `get_db()` dependency for controlled database access.

By separating database connectivity and session management from ORM models and API routes, the module provides a centralized database configuration layer for the application.
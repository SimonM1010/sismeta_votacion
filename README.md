-- Active: 1786760236879@@localhost@3306
# Sistema de Votaciones - API

API REST de votaciones construida con **FastAPI**, **SQL Server** y **JWT**, siguiendo
**arquitectura limpia** (Clean Architecture).

---

## Arquitectura

La regla es una sola: **las dependencias apuntan hacia adentro**. El dominio no conoce a
nadie; la infraestructura conoce al dominio, nunca al reves.

```
                 +---------------------------------------+
                 |          PRESENTATION (FastAPI)       |
                 |   endpoints, DI, manejo de errores    |
                 +------------------+--------------------+
                                    | usa
                 +------------------v--------------------+
                 |        APPLICATION (casos de uso)     |
                 |      orquesta reglas, DTOs Pydantic   |
                 +------------------+--------------------+
                                    | depende de interfaces
                 +------------------v--------------------+
                 |          DOMAIN (nucleo puro)         |
                 |  entidades, puertos (ABC), errores    |
                 +------------------^--------------------+
                                    | implementa
                 +------------------+--------------------+
                 |    INFRASTRUCTURE (SQLAlchemy/pyodbc) |
                 |   modelos ORM, repositorios, engine   |
                 +---------------------------------------+
```

Consecuencia practica: para cambiar SQL Server por PostgreSQL solo se tocan
`app/infrastructure/` y la cadena de conexion. Los casos de uso no se enteran.

---

## Estructura de carpetas

```
sismeta_votacion/
├── main.py                     # Punto de entrada (uvicorn main:app)
├── requirements.txt            # Dependencias de produccion
├── .env                        # Credenciales reales (NO se sube a git)
├── venv/                       # Entorno virtual
│
└── app/
    ├── core/                           # Configuracion transversal
    │   ├── config.py                   # Settings desde .env + cadena de conexion
    │   └── security.py                 # Hash bcrypt + emision/lectura de JWT
    │
    ├── domain/                         # NUCLEO: sin dependencias externas
    │   ├── entities/                   # Candidate, Voter, Vote, User (dataclasses)
    │   ├── repositories/               # Puertos: interfaces ABC de persistencia
    │   └── exceptions.py               # NotFoundError, ConflictError, AuthenticationError
    │
    ├── application/                    # Casos de uso
    │   ├── dto/                        # Contratos de entrada/salida (Pydantic)
    │   └── use_cases/                  # Una clase por operacion de negocio
    │
    ├── infrastructure/                 # Detalles tecnicos
    │   ├── database/
    │   │   ├── connection.py           # engine, SessionLocal, Base, init_db
    │   │   └── models/                 # Modelos ORM (tablas de SQL Server)
    │   └── repositories/               # Implementaciones SQLAlchemy de los puertos
    │
    └── presentation/                   # Capa web
        ├── app.py                      # create_app(): routers, CORS, error handlers
        └── api/
            ├── dependencies.py         # Inyeccion de dependencias (el "cableado")
            └── v1/
                ├── router.py           # Agregador de routers
                └── endpoints/          # auth, voters, candidates, votes, health
```

---

## Puesta en marcha

### 1. Activar el entorno virtual

```powershell
.\venv\Scripts\Activate.ps1
```

> Si PowerShell bloquea el script:
> `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`

### 2. Instalar dependencias (ya instaladas, por si recreas el venv)

```powershell
pip install -r requirements.txt
```

### 3. Crear la base de datos en SQL Server

```sql
CREATE DATABASE sismeta_votacion;
```

Las **tablas se crean solas** al arrancar la API (`init_db()` en el startup).

### 4. Configurar el `.env`

```env
DB_USER=                                    # vacio = autenticacion de Windows
DB_PASS=
DB_HOST=localhost
DB_PORT=1433
DB_DATABASE=sismeta_votacion
DB_DRIVER=ODBC Driver 17 for SQL Server

JWT_SECRET_KEY=<generar>
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=60
```

| Escenario | Como configurarlo |
|-----------|-------------------|
| Instancia por defecto + Windows | `DB_HOST=localhost`, `DB_PORT=1433`, `DB_USER` vacio |
| Instancia con nombre | `DB_HOST=localhost\SQLEXPRESS` y **`DB_PORT=`** (vacio) |
| Autenticacion SQL | llenar `DB_USER` y `DB_PASS` |
| Driver 18 instalado | `DB_DRIVER=ODBC Driver 18 for SQL Server` |

Genera una clave JWT de verdad antes de usar esto en serio:

```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 5. Levantar la API

```powershell
uvicorn main:app --reload
```

Documentacion interactiva: **http://127.0.0.1:8000/docs**

---

## Endpoints

Prefijo base: `/api/v1` (configurable con `API_V1_PREFIX` en el `.env`).

| Metodo | Ruta | Descripcion | Token |
|--------|------|-------------|:-----:|
| GET | `/` | Informacion de la API | No |
| GET | `/api/v1/health` | Estado de la API y de la base | No |
| POST | `/api/v1/auth/register` | Crear usuario del sistema | No * |
| POST | `/api/v1/auth/login` | Obtener el JWT | No |
| POST | `/api/v1/voters` | Registrar votante | Si |
| GET | `/api/v1/voters` | Lista de votantes | Si |
| GET | `/api/v1/voters/{id}` | Un votante | Si |
| DELETE | `/api/v1/voters/{id}` | Eliminar votante | Si |
| POST | `/api/v1/candidates` | Registrar candidato | Si |
| GET | `/api/v1/candidates` | Lista de candidatos | Si |
| GET | `/api/v1/candidates/{id}` | Un candidato | Si |
| DELETE | `/api/v1/candidates/{id}` | Eliminar candidato | Si |
| POST | `/api/v1/votes` | Emitir un voto | Si |
| GET | `/api/v1/votes` | Votos emitidos | Si |
| GET | `/api/v1/votes/statics` | Estadisticas de la votacion | Si |

\* `/auth/register` esta abierto para poder crear el primer usuario. Cuando ya tengas tu
admin, protegelo agregando `current_user: CurrentUser` a la firma en
`app/presentation/api/v1/endpoints/auth.py`.

---

## Como probar en 1 minuto

1. Abre **http://127.0.0.1:8000/docs**
2. `POST /auth/register` -> `{"username": "admin", "password": "admin123"}`
3. Boton verde **Authorize** (arriba a la derecha) -> mismo usuario y contrasena
4. Ya puedes ejecutar cualquier endpoint desde la misma pagina.

Con PowerShell:

```powershell
# 1. Registrar usuario
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/api/v1/auth/register `
  -ContentType "application/json" `
  -Body '{"username":"admin","password":"admin123"}'

# 2. Obtener token (login usa formulario, no JSON)
$token = (Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/api/v1/auth/login `
  -Body @{ username = "admin"; password = "admin123" }).access_token
$headers = @{ Authorization = "Bearer $token" }

# 3. Cargar datos y votar
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/api/v1/candidates `
  -Headers $headers -ContentType "application/json" -Body '{"name":"Ana Torres"}'
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/api/v1/voters `
  -Headers $headers -ContentType "application/json" -Body '{"name":"Juan Perez"}'
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/api/v1/votes `
  -Headers $headers -ContentType "application/json" -Body '{"voter_id":1,"candidate_id":1}'

# 4. Ver estadisticas
Invoke-RestMethod -Uri http://127.0.0.1:8000/api/v1/votes/statics -Headers $headers |
  ConvertTo-Json -Depth 5
```

Ejemplo de respuesta de `/votes/statics`:

```json
{
  "total_votes": 3,
  "total_voters": 3,
  "total_candidates": 2,
  "participation_percentage": 100.0,
  "results": [
    { "candidate_id": 1, "candidate_name": "Ana Torres", "votes": 2, "percentage": 66.67 },
    { "candidate_id": 2, "candidate_name": "Luis Gomez", "votes": 1, "percentage": 33.33 }
  ]
}
```

---

## Tablas

Base minima. Agrega tus columnas en `app/infrastructure/database/models/` y el campo
equivalente en `app/domain/entities/`.

| Tabla | Columnas |
|-------|----------|
| `Candidate` | `Id` (PK, identity), `Name` |
| `Voter` | `Id` (PK, identity), `Name` |
| `Vote` | `Id` (PK, identity), `VoterId` (FK -> Voter.Id, UNIQUE), `CandidateId` (FK -> Candidate.Id) |
| `Users` | `Id` (PK, identity), `Username` (UNIQUE), `HashedPassword` |

- `Vote.VoterId` es **UNIQUE**: la base garantiza "un votante, un voto". Si no quieres esa
  regla, quita el `UniqueConstraint` en `vote_model.py`.
- `Users` se llama asi porque `USER` es palabra reservada en T-SQL.

---

## Reglas de negocio ya implementadas

Estan en los casos de uso (`app/application/use_cases/`), no en los endpoints, para que
se puedan cambiar sin tocar la capa web.

| Regla | Donde | Respuesta si se viola |
|-------|-------|-----------------------|
| El votante y el candidato deben existir para votar | `CastVoteUseCase` | 404 |
| Un votante solo puede votar una vez | `CastVoteUseCase` + UNIQUE en la tabla | 409 |
| No se elimina un votante que ya voto | `DeleteVoterUseCase` | 409 |
| No se elimina un candidato que ya tiene votos | `DeleteCandidateUseCase` | 409 |
| No se repite el `Username` | `RegisterUserUseCase` + UNIQUE | 409 |

Las dos reglas de borrado evitan votos huerfanos que descuadren el conteo. Si prefieres
borrado en cascada, quita la verificacion del caso de uso y agrega `ON DELETE CASCADE` a
las FK de `Vote`.

---

## Como agregar un campo nuevo (ejemplo: `Party` en candidato)

Toca 4 archivos, siempre en el mismo orden:

1. `app/domain/entities/candidate.py` -> agrega `party: str`
2. `app/infrastructure/database/models/candidate_model.py` -> agrega la columna
3. `app/infrastructure/repositories/candidate_repository_impl.py` -> mapealo en `_to_entity` y en `create`
4. `app/application/dto/candidate_dto.py` -> agregalo al DTO de entrada y/o de salida

---

## Codigos de respuesta

| Codigo | Cuando |
|--------|--------|
| 200 / 201 / 204 | Operacion exitosa |
| 401 | Sin token, token invalido/expirado, o credenciales incorrectas |
| 404 | El recurso no existe (`NotFoundError`) |
| 409 | Regla de negocio violada (`ConflictError`): ver tabla de reglas |
| 422 | El body no cumple el DTO (validacion de Pydantic) |
| 503 | SQL Server no responde |

---

## Pendientes antes de produccion

- [ ] Cambiar `JWT_SECRET_KEY` por un valor generado y fuera del repositorio
- [ ] Restringir `allow_origins` del CORS en `app/presentation/app.py`
- [ ] Proteger o eliminar `POST /auth/register`
- [ ] Reemplazar `init_db()` por migraciones (Alembic)
- [ ] Agregar tests con `pytest` (`pip install -r requirements-dev.txt`)
#   s i s m e t a _ v o t a c i o n  
 #   s i s m e t a _ v o t a c i o n  
 
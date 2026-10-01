# Mini E-Commerce Order API

A robust, database-backed RESTful backend API built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL (Neon DB)** for managing products and order lifecycles. 

Features include client input validation, server-side price calculation using exact decimal precision, order status state-machine lifecycle enforcement, and relational persistence.

---

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Database Schema & Architecture](#database-schema--architecture)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Database Setup (Neon DB)](#database-setup-neon-db)
  - [Environment Configuration](#environment-configuration)
  - [Running the Application](#running-the-application)
- [API Documentation & Endpoints](#api-documentation--endpoints)
  - [Product Endpoints](#product-endpoints)
  - [Order Endpoints](#order-endpoints)
- [Order Lifecycle State Machine](#order-lifecycle-state-machine)
- [Monetary Calculation Precision](#monetary-calculation-precision)
- [Testing the API](#testing-the-api)

---

## Features

- **Product Management:** Create and list products with positive price enforcement.
- **Order Processing:** Place orders with multi-item validation and existence checks.
- **Server-Side Pricing:** Total amounts and subtotals are computed dynamically on the server using Python's `Decimal` type to eliminate floating-point rounding errors.
- **Strict Order Lifecycle:** Enforces sequential status transitions (`PLACED` → `PROCESSING` → `SHIPPED` → `DELIVERED`).
- **PostgreSQL / Neon DB Integration:** Relational database storage with SQLAlchemy ORM and transactional session management.
- **Interactive OpenAPI Documentation:** Built-in Swagger UI and ReDoc interface.

---

## Tech Stack

- **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
- **ASGI Server:** [Uvicorn](https://www.uvicorn.org/)
- **Database:** [PostgreSQL](https://www.postgresql.org/) (Hosted on [Neon DB](https://neon.tech/))
- **ORM:** [SQLAlchemy 2.0](https://www.sqlalchemy.org/)
- **Data Validation:** [Pydantic v2](https://docs.pydantic.dev/)
- **Database Driver:** `psycopg2-binary`

---

## Database Schema & Architecture

The database consists of three entities: `products`, `orders`, and `order_items` (junction entity preserving line-item snapshot data).

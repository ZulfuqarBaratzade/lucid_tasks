# FastAPI MySQL Authentication API

This project provides a **REST API** that allows users to register, log in, and manage their posts (create, delete). The API is built with **FastAPI** and uses **MySQL** as the database. **JWT (JSON Web Token)** is used for authentication.

## Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Installation](#installation)
  - [Required Dependencies](#required-dependencies)
  - [Running the Application](#running-the-application)
- [API Usage](#api-usage)
  - [Sign Up](#sign-up)
  - [Login](#login)
  - [Add Post](#add-post)
  - [Delete Post](#delete-post)
  - [Get Posts](#get-posts)
- [Tests](#tests)

---

## About the Project

This project provides an API built with **FastAPI** that allows users to authenticate via **JWT**, create, view, and delete posts. The application uses **SQLAlchemy** for ORM-based database interactions with **MySQL**.

### Technologies Used:

- **FastAPI**: A modern web framework for building APIs.
- **SQLAlchemy**: ORM for handling database interactions.
- **MySQL**: Relational database management system.
- **JWT (JSON Web Token)**: Used for user authentication.
- **bcrypt**: For hashing and verifying passwords securely.
- **Pymysql**: MySQL connector for Python.

---

## Features

- User Registration (Sign Up)
- User Login
- Post Creation
- Post Deletion
- Post Listing
- JWT token-based authentication

---

## Installation

### Required Dependencies

To run the project, you need **Python 3.7+** and the required dependencies listed in the `requirements.txt` file.

1. Install the dependencies with the following command:

```bash
pip install -r requirements.txt
```

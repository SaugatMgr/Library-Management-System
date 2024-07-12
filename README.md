# Library Management System

## Introduction

The Library Management System is a web application designed to manage the operations of a library. It provides functionalities such as adding, updating, and deleting books, managing user accounts, and keeping track of book borrow. Also this project is live/deployed at: [here](https://lib-hub-proj.me) but since only backend is implemented for this project, you would need admin email and password for
accessing the admin panel.

## Project Structure

The main Django project is managed inside the `core/project_name` directory. The `manage.py` file also resides in the `core/` directory. To run commands, use `python -m core.manage <command_name>` or `make command_name` instead of `python manage.py <command_name>`. The `command_name` for make is inside `Makefile`. This structure is designed to organize project files effectively and improve maintainability.

## Purpose of Using Makefile

To streamline project development and management, a Makefile is included with custom command names. This simplifies executing commands related to Django management, such as running the development server, applying migrations, and installing dependencies.

## Installation

To install and run the Library Management System, follow these steps:
1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/library-management-system.git
    ```

2. **Navigate to the project directory:**

    ```bash
    cd the-project-directory
    ```

3. **Create a virtual environment:**

    ```bash
    python -m venv .venv
    ```

4. **Activate the virtual environment:**

    On Windows:

    ```bash
    .\.venv\Scripts\activate
    ```

    On Unix or MacOS:

    ```bash
    source .venv/bin/activate
    ```

5. **Install Poetry:**

    ```bash
    pip install poetry
    ```

6. **Install project dependencies:**

    ```bash
    poetry install
    ```

7. **Set up environment variables:**

    Create a `.env` file in the project root directory and add the following variables:

    ```
    DEBUG=True
    SECRET_KEY=your_secret_key_here
    DATABASE_URL=postgres://db_user:db_password@localhost:db_port_number/db_name
    ALLOWED_HOSTS="localhost,127.0.0.1" or "*"
    ```

8. **Apply migrations:**

    ```bash
    python manage.py migrate
    ```

9. **Run the project:**

    Ensure Makefile is installed:
    - For Windows users, download and add Make to environment variables [here](https://gnuwin32.sourceforge.net/packages/make.htm).
    - For Linux/Ubuntu users:

    ```bash
    sudo apt install make
    ```

    Now, run the project:

    ```bash
    make runserver
    ```

10. **Access the project:**

    Open a web browser and go to [http://localhost:8000](http://localhost:8000) to view the project.

## Contributing

If you would like to contribute to the Library Management System, follow these steps:

1. Fork the repository on GitHub.
2. Create a new branch for your feature or bug fix.
3. Make the necessary changes and commit them.
4. Push your changes to your forked repository.
5. Submit a pull request to the main repository.

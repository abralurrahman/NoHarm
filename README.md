# NoHarm Project Setup Guide

This guide will walk you through setting up and running the NoHarm survey web application. You will learn how to create a virtual environment, install necessary dependencies, run the server, and view survey results.

## Prerequisites

- **Python**: Ensure Python 3.8+ is installed. Download it from [python.org](https://www.python.org/downloads/).
- **pip**: Python’s package installer, included with Python.

## Step 1: Setting Up the Virtual Environment

1. Open Command Prompt or Terminal.
2. Navigate to your desired directory where you want to set up the project:
    ```bash
    cd path/to/your/project/directory
    ```
3. Create a virtual environment:
    ```bash
    python -m venv venv
    ```
4. Activate the virtual environment:
    - **Windows (PowerShell)**:
      ```bash
      .\venv\Scripts\Activate.ps1
      ```
    - **Windows (CMD)**:
      ```cmd
      .\venv\Scripts\activate
      ```
    - **Mac/Linux**:
      ```bash
      source venv/bin/activate
      ```

   When activated, you should see `(venv)` at the beginning of your command prompt.

## Step 2: Installing Flask and Dependencies

1. Install Flask using pip:
    ```bash
    pip install Flask
    ```
2. Verify the Flask installation:
    ```bash
    flask --version
    ```
   You should see the Flask version information confirming the installation.

## Step 3: Setting Up the Project Structure

1. Create the project directory if not already done:
    ```bash
    mkdir NoHarm
    cd NoHarm
    ```
2. Inside the `NoHarm` directory, ensure you have the following structure:
    - `app.py` for the Flask application.
    - `templates/index.html` for the survey form.
    - `templates/results.html` for displaying the survey results.

## Step 4: Initializing the SQLite Database

1. Create a script (`init_db.py`) to initialize the database.
2. Run the script to create the database and tables:
    ```bash
    python init_db.py
    ```
   This creates a `database.db` file with the necessary tables for storing survey responses.

## Step 5: Running the Flask Server

1. Start the Flask app:
    ```bash
    python app.py
    ```
2. Open your web browser and navigate to:
    ```
    http://127.0.0.1:5000/
    ```
   This is the homepage where you can fill out and submit the survey.

## Step 6: Viewing Survey Results

1. After submitting a survey response, view the stored data by navigating to:
    ```
    http://127.0.0.1:5000/results
    ```
2. This page displays a table with all the survey responses collected so far.

## Summary of Commands

1. Navigate to the project directory:
    ```bash
    cd path/to/NoHarm
    ```
2. Create and activate the virtual environment:
    ```bash
    python -m venv venv
    .\venv\Scripts\Activate.ps1  # Windows PowerShell
    source venv/bin/activate      # Mac/Linux
    ```
3. Install Flask:
    ```bash
    pip install Flask
    ```
4. Initialize the database:
    ```bash
    python init_db.py
    ```
5. Run the server:
    ```bash
    python app.py
    ```
6. Access the app in your web browser:
    - Survey form: `http://127.0.0.1:5000/`
    - Survey results: `http://127.0.0.1:5000/results`

This guide should help you set up and run the NoHarm project from start to finish, enabling you to run the server and view survey results efficiently.

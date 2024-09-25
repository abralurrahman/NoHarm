# NoHarm Survey Project Setup Guide

This guide will walk you through setting up and running the NoHarm survey web application. It includes steps for creating a virtual environment, installing necessary dependencies, running the server, and viewing survey results. Just so you know, for now, each developer will have their local server, but we aim to deploy the project on a shared server soon.

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
4. For PowerShell users, if you encounter execution policy restrictions, run the following command to allow script execution:
    ```bash
    Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
    ```
5. Activate the virtual environment:
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
   This URL is specific to your local machine and indicates that the server is running locally. It will open the homepage where you can fill out and submit the survey.

   **Note:** The URL `http://127.0.0.1:5000/` is a loopback address that points to your own computer. This means each developer will use the same address to access their own local instance of the server. Since we haven't deployed this application to a public server yet, the address will change once we have a dedicated server.

## Step 6: Viewing Survey Results

1. After submitting a survey response, view the stored data by navigating to:
    ```
    http://127.0.0.1:5000/results
    ```
2. This page displays a table with all the survey responses collected on your local instance.

   **Note:** The data displayed here will only include responses submitted on your machine. Other developers will see their data on their local instance.

---

### Future Server Setup

We aim to deploy this project on a dedicated server soon, where everyone will be able to interact with the same instance of the application. For now, each developer will have their own local environment, and the server will be different for each machine.


# HLX-Native State Server

This directory contains a Flask-based state server for the HLX system. It manages the runtime state, including contract definitions and handle resolution, using a content-addressable storage (CAS) system.

## Setup

1.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

2.  **Activate the virtual environment:**
    ```bash
    source venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## Running the Server

1.  **Activate the virtual environment (if not already activated):**
    ```bash
    source venv/bin/activate
    ```

2.  **Run the Flask application:**
    ```bash
    python app.py
    ```

The server will start on `http://0.0.0.0:5002`. It will automatically create a `cas/` directory for the content-addressable storage if it doesn't exist.

## API Endpoints

*   `GET /hlx/state/query?handle=<handle>`: Retrieves the current value for a given handle.
*   `POST /hlx/state/update`: Updates the value for a given handle.
    *   **Body (JSON):** `{"handle": "<handle>", "value": <json_payload>}`
*   `GET /hlx/state/resolve?handle=<handle>`: Resolves a handle to its content-addressed value (functionally the same as `/query`).
*   `GET /hlx/state/collapse?handle=<handle>`: Lowers a state to its canonical form (returns its content hash).

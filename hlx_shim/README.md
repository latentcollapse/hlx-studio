# HLX Shim Layer

This directory contains a Flask-based shim layer for the HLX system. It provides endpoints for encoding, decoding, and validating HLX payloads.

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

The server will start on `http://0.0.0.0:5001`.

## Endpoints

*   `POST /hlx/shim/encode`: Encodes a JSON payload to LC-T format.
*   `POST /hlx/shim/decode`: Decodes an LC-T/LC-B payload to a structured format.
*   `POST /hlx/shim/validate`: Validates an LC-T/LC-B payload against its schema and a BLAKE3 hash. The hash must be provided in the `X-HLX-Hash` header.

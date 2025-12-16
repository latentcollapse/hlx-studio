# HLX Deterministic Toolchain

This directory contains a Flask-based deterministic toolchain for the HLX system. It provides endpoints for encoding, decoding, validating, and hashing HLX payloads.

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

The server will start on `http://0.0.0.0:5003`.

## API Endpoints

*   `POST /hlx/tool/encode?mode=<LC-T|LC-B>`: Encodes a JSON payload.
    *   **Body (JSON):** The HLX-Lite object to encode.
    *   **Mode `LC-T` (default):** Returns a JSON object with the encoded data as a string.
    *   **Mode `LC-B`:** Returns a deterministic ZIP file (`payload.zip`).

*   `POST /hlx/tool/decode?mode=<LC-T|LC-B>`: Decodes an HLX payload.
    *   **Body:** The raw LC-T string or LC-B ZIP file.
    *   **Mode `LC-T` (default):** Expects a raw string body.
    *   **Mode `LC-B`:** Expects a `application/zip` body.

*   `POST /hlx/tool/validate`: Validates an HLX payload against runtime conformance rules.
    *   **Body:** The raw payload to validate.
    *   **Returns:** `{"status": "PASS"}` or `{"status": "FAIL"}` with a descriptive message.

*   `POST /hlx/tool/hash`: Computes an authoritative BLAKE3 hash for any given data.
    *   **Body:** The raw data to be hashed.
    *   **Returns:** A JSON object with the computed hash.

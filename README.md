# Voice Isolator

A Python application that uses the ElevenLabs API to isolate the voice from an audio file.

## Description

This tool provides a simple command-line interface to process audio files. You place your audio files in an `input` directory, run the script, and the voice-isolated versions will be saved in the `output` directory.

## Project Structure

The project is structured as follows:

-   `main.py`: The main entry point of the application.
-   `src/`: Contains the source code, organized by feature.
-   `input/`: Directory for input audio files (ignored by git).
-   `output/`: Directory for processed output files (ignored by git).
-   `.github/workflows/ci.yml`: GitHub Actions workflow for continuous integration.
-   `requirements.txt`: Production dependencies.
-   `requirements-dev.txt`: Development dependencies.

## Getting Started

### Prerequisites

-   Python 3.9 or higher
-   An ElevenLabs API key

### Installation

1.  **Clone the repository.**

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up your API key:**
    Create a file named `.env` in the root of the project and add your ElevenLabs API key to it:
    ```
    elevenlabs_api_key=YOUR_API_KEY
    ```

## Usage

1.  Place the audio files you want to process into the `input` directory. Supported formats are `.mp3`, `.wav`, `.flac`, and `.m4a`.

2.  Run the application:
    ```bash
    python main.py
    ```

3.  If multiple audio files are found in the `input` directory, you will be prompted to select one.

4.  The processed file, with the voice isolated, will be saved in the `output` directory with `_isolated.mp3` appended to the original filename.

## For Developers

### Development Setup

To set up the project for development, install the development dependencies:

```bash
pip install -r requirements-dev.txt
```

### Code Style and Linting

-   **Style Guide**: This project follows the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide.
-   **Linting**: We use `ruff` for linting. To check the code, run:
    ```bash
    ruff check .
    ```
-   **Type Checking**: We use `mypy` for static type checking. To check the types, run:
    ```bash
    mypy .
    ```

### Running Tests

The tests are written using Python's built-in `unittest` framework and are co-located with the code.

To run the test suite, use the following command, which will discover and run all tests in the `src` directory:

```bash
python -m unittest discover src
```

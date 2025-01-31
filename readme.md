# Wine Recommendation Web App

## Overview

This project is a web application built with Python 3 and Django that helps users find wines that match their preferences. The application provides recommendations based on user input and displays the results on a web page.

## Features

- **Flask-based Web Server**: Handles user interactions and API requests.
- **Wine Recommendation System**: Matches user preferences with stored wine data.
- **Session Handling**: Stores recommendations temporarily for displaying results.
- **CORS Support**: Enables cross-origin requests.

## Installation

### Prerequisites

Ensure you have the following installed:

- Python 3.x
- Flask
- Flask-CORS

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```
2. Install dependencies:
   ```bash
   pip install flask flask-cors
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. The app will be available at `http://localhost:5000`

## File Structure

```
├── app.py             # Flask application entry point
├── recommend.py       # Wine recommendation logic
├── static/
│   ├── data/
│   │   ├── wine.txt   # JSON data file for wine recommendations
│   ├── css/
│   ├── js/
├── templates/
│   ├── main.html      # Homepage template
│   ├── result.html    # Result page template
```

## API Endpoints

### `GET /`

- Renders the main page (`main.html`).

### `POST /recommend`

- Accepts JSON input containing user preferences.
- Returns a redirect response to `/result`.

### `GET /result`

- Displays the recommended wine based on user input.

## Wine Recommendation Logic

1. Loads wine data from `static/data/wine.txt`.
2. Checks user input against predefined conditions.
3. Returns the best-matching wine or a default message if no match is found.

## Notes

- Ensure `wine.txt` exists and contains valid JSON data.
- If no exact match is found, a default response is provided.

## License

This project is open-source and available under the MIT license.

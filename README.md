# X-Ray Feature Backend

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Directory Structure](#directory-structure)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Data Flow Overview](#data-flow-overview)
- [Troubleshooting](#troubleshooting)
- [Additional Notes](#additional-notes)
- [License](#license)

## Introduction

This backend application replicates a simplified version of Amazon Prime Video's X-Ray feature. It processes uploaded videos to recognize faces in different scenes and identifies known actors using facial recognition and classification models. The application provides a FastAPI-based API for video uploading, processing, and retrieving processed results.

## Features

- Face Detection: Detects faces in video scenes using face_recognition and OpenCV.
- Face Recognition: Matches detected faces against a database of known actors.
- Scene Processing: Processes videos based on provided scene timestamps.
- API Endpoints: FastAPI application with endpoints for video uploading and results retrieval.
- Data Storage: Stores actor information and processing results in JSON files.
- Extensibility: Modular code structure for easy expansion and customization.

## Prerequisites

- Python: Version 3.7 or higher.
- CMake: Required for building dlib, which is a dependency of face_recognition.
- Git: For cloning the repository (optional).

## Installation

1. Clone the Repository

   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. Create a Virtual Environment

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Unix or macOS
   venv\Scripts\activate  # On Windows
   ```

3. Install Dependencies

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Install CMake (if not already installed)
   - Windows: Download from the official CMake website
   - Ubuntu/Debian: `sudo apt-get install cmake`
   - macOS: `brew install cmake`

## Directory Structure

```
project/
├── main.py
├── models/
│   ├── face_recognition.py
│   └── face_classification.py
├── data/
│   ├── known_actors/
│   ├── actors.json
│   ├── known_faces.pkl
│   ├── uploaded_videos/
│   └── results/
├── requirements.txt
├── .gitignore
└── README.md
```

## Configuration

1. Prepare Known Actors Data
2. Create actors.json
3. Generate Known Faces Database

For detailed configuration steps, refer to the full documentation.

## Usage

1. Set up the Known Actors Database
2. Run the FastAPI Server:
   ```bash
   uvicorn main:app --reload
   ```
3. Test the API endpoints

For detailed usage instructions, refer to the full documentation.

## API Endpoints

- POST /upload_video
- GET /results

For detailed API documentation, refer to the full documentation.

## Data Flow Overview

1. Video Uploading
2. Face Detection and Recognition
3. Results Generation
4. Response to Client
5. Cleanup

## Troubleshooting

- CMake Not Found Error
- dlib Installation Issues
- Face Recognition Accuracy
- Empty Results
- Server Errors

For detailed troubleshooting steps, refer to the full documentation.

## Additional Notes

- Security Considerations
- Performance Optimization
- Extending the Application
- Data Privacy

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Libraries Used: FastAPI, Uvicorn, face_recognition, OpenCV, Pydantic
- Inspiration: Amazon Prime Video's X-Ray feature

Feel free to contribute to this project by submitting issues or pull requests. If you have any questions or need further assistance, please contact the project maintainer.

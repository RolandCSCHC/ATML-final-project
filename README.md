# Analítica Textual con Machine Learning - Proyecto Final

## Michael Jackson AI Chatbot - Flask Application

A Flask web application that provides an interactive chatbot interface for the Michael Jackson AI model trained on GPT-2.

## Setup Instructions

### 1. Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 2. Download the Model from Google Drive

The model needs to be downloaded from Google Drive and placed in the repository:

1. Navigate to your Google Drive folder:

   - Path: `Analítica Textual con Machine Learning/Proyecto/michael_jackson_model/best_model`

2. Download the entire `best_model` folder (or its contents) from Google Drive

3. Place the model files in the following directory structure:

   ```
   models/
   └── michael_jackson_model/
       └── best_model/
           ├── config.json
           ├── model.safetensors (or pytorch_model.bin)
           ├── tokenizer_config.json
           ├── vocab.json
           ├── merges.txt
           └── other config files...
   ```

   **Important:** Make sure to download the `model.safetensors` file (or `pytorch_model.bin`) from Google Drive. This is a large file (several GB) that contains the actual model weights. The config files alone are not sufficient.

   The final path should be: `models/michael_jackson_model/best_model/`

### 3. Run the Flask Application

#### Option A: Run with Docker (Recommended)

1. **Build and run with Docker Compose:**

   ```bash
   docker-compose up --build
   ```

   The application will be available at `http://localhost:5001`

2. **Or build and run with Docker directly:**

   ```bash
   # Build the image
   docker build -t mj-chatbot .

   # Run the container
   docker run -p 5001:5001 -v $(pwd)/models:/app/models mj-chatbot
   ```

#### Option B: Run Locally

Start the Flask server:

```bash
python app.py
```

The application will be available at `http://localhost:5001`

## Project Structure

```
.
├── app.py                 # Main Flask application
├── chatbot.py            # MichaelJacksonChatbot class
├── templates/
│   └── index.html        # Chatbot web interface (dark theme)
├── static/               # Static files (images, etc.)
│   └── Michael Jackson.png  # Profile image for the chatbot
├── models/               # Model files directory (to be populated)
│   └── michael_jackson_model/
│       └── best_model/
├── requirements.txt      # Python dependencies
├── Dockerfile            # Docker image configuration
├── docker-compose.yml    # Docker Compose configuration
└── README.md            # This file
```

## Usage

1. Open your web browser and navigate to `http://localhost:5001`
2. Type your message in the input field
3. Click "Send" or press Enter to get a response from the Michael Jackson AI chatbot

## Features

- **Dark Theme UI**: Modern dark gray/black interface for comfortable chatting
- **Michael Jackson Profile Image**: Visual identity with Michael Jackson's image in the header
- **Real-time Chat**: Interactive chat interface with message history
- **Model Status Indicator**: Visual feedback showing whether the model is loaded successfully
- **Responsive Design**: Works on desktop and mobile devices

## Docker Commands

### Using Docker Compose

- **Start the application:**

  ```bash
  docker-compose up
  ```

- **Start in detached mode (background):**

  ```bash
  docker-compose up -d
  ```

- **Stop the application:**

  ```bash
  docker-compose down
  ```

- **View logs:**

  ```bash
  docker-compose logs -f
  ```

- **Rebuild after code changes:**
  ```bash
  docker-compose up --build
  ```

## Notes

- The model will be loaded once when the Flask application starts
- If the model is not found, the application will display a detailed error message indicating what's missing
- The chatbot uses GPT-2 with custom special tokens (`<|michael|>`, `<|startoftext|>`, etc.) for Michael Jackson-style responses
- When using Docker, the `models/` and `static/` directories are mounted as volumes, so you can add files without rebuilding the image
- The application runs on port **5001** by default (changed from 5000 to avoid conflicts)
- For production deployment, consider removing the volume mounts for app files in `docker-compose.yml` to use the built-in code

## Troubleshooting

### Model Not Loading

If you see "Model not loaded" error:

1. Verify that `model.safetensors` (or `pytorch_model.bin`) exists in `models/michael_jackson_model/best_model/`
2. Check the file size - the model weight file should be several GB
3. Restart the Flask application after adding the model file
4. Check the terminal/console for detailed error messages

### Image Not Showing

If Michael Jackson's image doesn't appear:

1. Ensure `static/Michael Jackson.png` exists (or update the filename in `templates/index.html`)
2. Restart the Flask application
3. Clear your browser cache and refresh

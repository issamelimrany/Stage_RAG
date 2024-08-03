# PDF Document Analysis with LLMs

This project uses a combination of LangChain, Groq, Streamlit, and HuggingFace to create a web application that allows users to upload PDF documents and ask questions about the content. The application processes the PDF, splits it into chunks, stores the chunks in a vector store, and uses a large language model (LLM) to answer user queries based on the document's content.

## Features

- Upload PDF documents and analyze their content.
- Ask questions about the uploaded document and receive accurate answers.
- Uses Groq's LLM for generating responses.
- Processes documents using LangChain's text splitters.
- Stores document chunks in a vector store for efficient retrieval.
- Interactive user interface built with Streamlit.

## Installation

To run this project locally, follow these steps:

1. **Clone the repository:**

    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Create a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the required dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set your Groq API key as an environment variable:**

    ```sh
    export GROQ_API_KEY="your_groq_api_key"   # On Windows, use `set GROQ_API_KEY=your_groq_api_key`
    ```

## Usage

1. **Run the Streamlit app:**

    ```sh
    streamlit run app.py
    ```

2. **Upload a PDF file** using the web interface.

3. **Ask questions** about the uploaded document through the chat interface.

## Code Overview

### `app.py`

- **Imports and Environment Setup:** Imports necessary libraries and sets the Groq API key.
- **Function Definitions:**
  - `initialize_groq_client()`: Initializes the Groq client.
  - `create_directories()`: Creates directories for storing files and vector stores if they don't exist.
  - `initialize_session_state()`: Initializes Streamlit session state for various components.
  - `get_groq_response(client, user_query, context)`: Fetches a response from the Groq LLM based on the user query and context.
  - `main()`: Main function to run the Streamlit app.
- **Streamlit Interface:**
  - Allows users to upload PDF files.
  - Processes the uploaded files and stores document chunks in a vector store.
  - Provides a chat interface for users to ask questions and get responses.

## Example

Here's an example of how to use the application:

1. Run the Streamlit app:

    ```sh
    streamlit run app.py
    ```

2. Upload a PDF document using the web interface.

3. Enter a question related to the uploaded document in the chat input.

4. Receive a response from the assistant based on the document's content.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.


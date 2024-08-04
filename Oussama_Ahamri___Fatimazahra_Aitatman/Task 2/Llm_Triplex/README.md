# PDF Document Analysis with LLMs

This project uses a combination of LangChain, Ollama_Triplex , Gradio, and HuggingFace to create a web application that allows users to upload PDF documents and ask questions about the content. The application processes the PDF, splits it into chunks, stores the chunks in a vector store, and uses a large language model (LLM) to answer user queries based on the document's content.

## Features

- Upload PDF documents and analyze their content.
- Ask questions about the uploaded document and receive accurate answers.
- Uses Ollama_LLM for generating responses.
- Processes documents using LangChain's text splitters.
- Stores document chunks in a vector store for efficient retrieval.
- Interactive user interface built with Gradio.

## Installation

To run this project locally, follow these steps:


1. **Create a virtual environment:**

    ```sh
    python -m venv venv
    source venv/bin/activate   # On Windows, use `venv\Scripts\activate`
    ```

2. **Install the required dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Run the Gradio app:**

    ```sh
    python app.py
    ```

2. **Upload a PDF file** using the web interface.

3. **Ask questions** about the uploaded document through the chat interface.


## Example

Here's an example of how to use the application:

1. Run the Gradio app:

    ```sh
    python app.py
    ```

2. Upload a PDF document using the web interface.

3. Enter a question related to the uploaded document in the chat input.

4. Receive a response from the assistant based on the document's content.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.


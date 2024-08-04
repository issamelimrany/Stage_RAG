
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

1. **Run the Streamlit app:**

    **app by llama3**
    ```sh
    chainlit run app.py  
    ```
    **app by gemma**
    ```sh
    chainlit run app2.py 
    ```

2. **Upload a PDF file** using the web interface.

3. **Ask questions** about the uploaded document through the chat interface.

## Example

Here's an example of how to use the application:

1. Run the Chainlit app:

    ```sh
    chainlit run app.py
    ```
    ```sh
    chainlit run app2.py
    ```

2. Upload a PDF document using the web interface.

3. Enter a question related to the uploaded document in the chat input.

4. Receive a response from the assistant based on the document's content.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.


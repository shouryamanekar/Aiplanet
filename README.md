
# Chat with your PDF using Llama 2 and Llama Index

This is a Streamlit application that allows you to chat with a PDF document using Llama 2 and Llama Index. You can upload a PDF file, process it, and interact with the content through a chatbot interface powered by OpenAI's GPT model.

## Features

- Upload and process PDF files.
- Interact with the content of the uploaded PDF via chat.
- Powered by OpenAI's GPT model and Llama Index for efficient querying.
- Built with Streamlit for a simple and user-friendly interface.

## Requirements

Before running this application, ensure you have the following dependencies installed:

- Python 3.7 or higher
- Streamlit
- Cassandra
- LlamaIndex
- OpenAI API key
- `python-dotenv` for loading environment variables

### Install Dependencies

You can install the required dependencies using the following command:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the root directory of the project with the following content:

```
OPENAI_API_KEY=<Your OpenAI API Key>
```

Make sure to replace `<Your OpenAI API Key>` with your actual OpenAI API key.

### Secure Connect Bundle

- Download the secure connect bundle from [Datastax Astra](https://astra.datastax.com/).
- Place the `secure-connect-aiplanet.zip` file in the project directory.

### Authentication Token

Ensure you have an authentication token stored in `aiplanet_astra_test_token.json` with the following structure:

```json
{
  "clientId": "<Your Client ID>",
  "secret": "<Your Client Secret>"
}
```

Replace `<Your Client ID>` and `<Your Client Secret>` with your credentials.

## Running the Application

1. Make sure the environment variables and dependencies are properly set up.
2. Run the application using Streamlit:

```bash
streamlit run app.py
```

3. Visit the URL provided by Streamlit (typically `http://localhost:8501`) in your browser.

## Usage

1. Upload a PDF file using the file uploader on the sidebar.
2. Click the "Process" button to process the document.
3. After processing, you can ask questions about the content of the PDF through the chat interface.
4. The assistant will respond with relevant information from the document.

## Contributing

Feel free to fork the repository, raise issues, and submit pull requests. Contributions are always welcome!

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

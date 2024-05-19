# LangChain ChatBot Project

This project demonstrates how to build a simple chatbot using LangChain that can answer questions based on the contents of an uploaded text file (e.g. `Facts.txt`). It utilizes Vector DB and Retrieval-Augmented Generation (RAG) to extract relevant data and respond to queries.

## Features

- Load data from a text file.
- Use LangChain's OpenAI integration to process and respond to queries.
- Simple command-line interface for specifying the input file.

## Prerequisites

- Python 3.11+
- An OpenAI API key
- a LangChain API key

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/langchain-chatbot.git
    cd langchain-chatbot
    ```

2. **Create and activate a virtual environment (optional but recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages:**

    ```bash
    pip install -r requirements.txt
    or
    pipenv install
    pipienv shell
    ```

4. **Set up environment variables:**

    Create a `.env` file in the root directory of your project and add your OpenAI API key:

    ```plaintext
    OPENAI_API_KEY=your_openai_api_key
    LANGCHAIN_TRACING_V2=true
    LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
    LANGCHAIN_API_KEY=your_langchain_api_key
    ```

## Usage

1. **Prepare your data:**

    Ensure you have a File in the same directory as your script. This file should contain the information that the chatbot will use to answer questions.
    
2. **Run the script:**

    ```bash
    python main.py [-f filename]
    ```

    You can also specify a different file:

    ```bash
    python main.py -f path/to/yourfile.txt
    ```

3. **Interacting with the chatbot:**

    The script will load the data from the specified file and use LangChain's OpenAI integration to process queries.

## Example

An example `Facts.txt` might look like:

```plaintext
Fact 1: The Eiffel Tower is located in Paris, France.
Fact 2: The Great Wall of China is over 13,000 miles long.
Fact 3: The human body has 206 bones.
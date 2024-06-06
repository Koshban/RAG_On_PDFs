# LangChain ChatBot Project

This project demonstrates how to build a simple chatbot using LangChain that can answer questions based on the contents of an uploaded text file (e.g. `Facts.txt`). It utilizes Vector DB and Retrieval-Augmented Generation (RAG) to extract relevant data and respond to queries.

## Features

- Load data from a text file.
- Use LangChain's OpenAI integration to process and respond to queries.
- Simple command-line interface for specifying the input file.

## NOTE

The AI and Langchain landscape is changing so fats, that even within 1 month of coding this, some of the APIs might change/get deprecated.
If you do get errors for such or deprecated warnings , please follow langchain documentation on whats the latest iteration of those Classes and Functions.
https://api.python.langchain.com/en/latest/langchain_api_reference.html

## Prerequisites

- Python 3.11+
- An OpenAI API key
- a LangChain API key

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Koshban/RAG_On_PDFs.git
    cd RAG_On_PDFs
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
    pipenv shell
    ```
    Note : You might need to install MicroSoft C++ Build tools + Visual Studio Community ( with Python installations ) + Windows 10/11 SDK to get CHromaDB to install using pip.
4. **Set up environment variables:**

    Create a `.env` file in the root directory of your project and add your API keys. I have added a .env_copy file to make it easier. Rename it as .env and fill in the details.


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
1. The Eiffel Tower is located in Paris, France.
2. The Great Wall of China is over 13,000 miles long.
3. The human body has 206 bones.
4. "Dreamt" is the only English word that ends with the letters "mt."
5. An ostrich's eye is bigger than its brain.
6. Honey is the only natural food that is made without destroying any kind of life.
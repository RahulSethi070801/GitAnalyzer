# GitAnalyzer

GitAnalyzer is an analytical chatbot development framework dedicated to GitHub.
GitAnalyzer's goal is to increase the productivity and efficiency of development by helping shorten the time and effort to study through chatbot applications.

It is an AI-powered semantic search and code analysis system for GitHub repositories using LangChain and large language models (LLMs). Key challenges include efficient data retrieval, preprocessing diverse code files, implementing semantic search algorithms, and leveraging LLMs for intelligent code analysis. Our system will not only locate relevant code but also generate insights and answer queries, bridging traditional information retrieval with advanced natural language processing (NLP) techniques.

### Why GitAnalyzer

ChatGPT cannot learn the latest framework without web access extensions. So we created an application that can complement that.
Using Langchain, which deals with Large Language Model(LLM). You can ask and answer specialized questions about the repository you entered.
Store and retrieve data at high speed. Use FAISS, which is a Langchain vector store.

### Target Group
Anyone who is interested in programming looks at the GitHub repository.
However, if there is too much content in the Repository, or if there is not enough explanation about the code, it's difficult to understand what it is. Or if you're new to coding, you're at a loss where to start looking at which files.

### Features
GitAnalyzer is not just a chit-chat chatbot, provides file structure, code analysis, and summarization within the repository to make the content of the GitHub repository of interest easier to learn.

### Setup

To set up GitAnalyzer, follow these steps:

1. **Clone the Repository**  
    Clone the GitAnalyzer repository to your local machine:
    ```bash
    git clone https://github.com/your-username/GitAnalyzer.git
    cd GitAnalyzer
    ```

2. **Create a Virtual Environment and Install Dependencies**  
    Ensure you have Python 3.8 or higher installed. Then, create a virtual environment to install the required dependencies:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Set Up Environment Variables**  
    Create a `.env` file in the root directory and add the following environment variables:
    ```env
    OPENAI_API_KEY=your_openai_api_key
    GITHUB_TOKEN=your_github_token
    ```

4. **Run the Application**  
    Start the application by running the `CS_410_project.ipynb` file located in the `code` folder:
    

5. **Access the Application**  
    An interactive chatbot interface will open, allowing you to query and explore the GitHub repository with ease.


You're now ready to use GitAnalyzer!

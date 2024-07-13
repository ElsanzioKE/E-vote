# E-vote

E-vote is a simple polling application built with Flask.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

- Python 3.x
- Virtualenv

### Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/ElsanzioKE/E-vote.git
    ```
2. **Navigate into the project directory**:
    ```sh
    cd E-vote
    ```
3. **Set up a virtual environment**:
    ```sh
    python -m venv venv
    ```
4. **Activate the virtual environment**:
    - On Windows:
      ```sh
      venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```sh
      source venv/bin/activate
      ```
5. **Install the required packages**:
    ```sh
    pip install -r requirements.txt
    ```
6. **Set up the database**:
    ```sh
    flask db init
    flask db migrate
    flask db upgrade
    ```

### Running the Application

1. **Run the Flask application**:
    ```sh
    flask run
    ```

The application should now be running on `http://127.0.0.1:5000`.

### Additional Information

- Make sure you have a running instance of RabbitMQ if you are using Celery for task management. 

Enjoy using E-vote!

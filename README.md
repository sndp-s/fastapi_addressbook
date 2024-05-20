# Addressbook API
This is an address book application built using the FastAPI framework. It provides APIs to create, update, delete, and retrieve addresses. The addresses contain coordinates and are saved to an SQLite database. User can also retrieve addresses within a given distance from specific location coordinates. This application uses SQLAlchemy ORM for database interactions and provides a standardized response structure.


## Installation (For linux/Mac OS)
1. Clone the repository
```bash
git clone https://github.com/sndp-s/fastapi_addressbook.git
cd fastapi_addressbook
```

2. Create a Virtual Environment
```bash
python -m venv .venv
source venv/bin/activate
```

3. Install Dependencies
```bash
pip install -r requirements.txt
```

4. Run the Application
```bash
uvicorn main:app --reload
```

5. Access the API Documentation
Open your browser and go to http://127.0.0.1:8000/docs to access the Swagger UI for API documentation and testing.


## License

This project is licensed under the [Project Name] License. For more details, see the [LICENSE](LICENSE) file.

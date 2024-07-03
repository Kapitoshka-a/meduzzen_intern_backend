You can run my application using this commands
- **Building docker image**:  docker build -t quiz-app . 
- **Testing**:  pytest -v app/tests
- **Running the Application**: docker run -d -p 8000:8000 quiz-app 

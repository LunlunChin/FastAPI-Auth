![image](https://github.com/LunlunChin/FastAPI-Auth/assets/36696204/be35417e-fac0-4b9a-90e2-def9e0ff8eae)
# FastAPI Auth System

This project demonstrates a simple authentication system using FastAPI for the backend and a basic HTML/JavaScript frontend. It uses JWT (JSON Web Tokens) for handling secure authentication.

## Features
- Backend API built with FastAPI.
- JWT Authentication with a 30-minute expiration.
- Mock database with a single user for demonstration.
- Frontend form handling and token storage.
- SQLite to track user login

## Getting Started

Follow these steps to get the project up and running on your local machine.

### Prerequisites
- Python 3.6+
- Live Server Extension in VSCode


### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/LunlunChin/FastAPI-Auth
   ```

2. **Navigate to the Directory**

   ```bash
   cd FastAPI-Auth
   ```

3. ** Set up and activatevirtual env**
    ```bash
    python3 -m venv venv
    ```

    ```bash
    .\venv\Scripts\activate
    ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Server**

   Launch the FastAPI server using Uvicorn:

   ```bash
   uvicorn main:app --reload
   ```


6. **Set Up the Frontend**

   Open the `index.html` file using the Live Server extension in Visual Studio Code. [Guide to setting up Live Server](https://www.geeksforgeeks.org/how-to-enable-live-server-on-visual-studio-code/).

7. **Access the Application**

   Visit the URL provided by Live Server, typically `http://127.0.0.1:5500/index.html`.

### Usage

1. Open the web application in your browser.

2. Enter the following credentials:
   - **Username:** admin
   - **Password:** admin

3. Click the **Login** button.

4. Upon successful login, the JWT token will be logged in the browser's console.

5. To view the stored JWT token, press `F12` to open the Developer Tools, go to the `Application` tab, and look under `Session Storage`.

![image](https://github.com/LunlunChin/FastAPI-Auth/assets/36696204/540d195f-56ed-4f65-97ca-bfe6a7abcf17)



6.go to the /logins endpoint to get the SQLite Db data that contains the list of username and login_time
http://127.0.0.1:8000/logins/

![image](https://github.com/LunlunChin/FastAPI-Auth/assets/36696204/69cd7bfd-8d97-4c93-8013-f90df1968651)




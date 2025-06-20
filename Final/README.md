# 🎬 Movieggest: AI Movie Recommender

A simple movie recommendation engine built with Python and Flask. This project uses a content-based filtering model to suggest movies based on their similarity in genre, cast, and plot.

 
![alt text](image.png)

---

## 🚀 How to Run

### **Prerequisites**
- Python 3.8+
- Git
- VS Code with the "Live Server" extension

### **1. Clone & Setup**
```bash
# Clone the repository
git clone https://github.com/[Your-Username]/movie-recommender.git
cd movie-recommender

# Download the dataset from Kaggle: https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata
# Place the two .csv files into the 'data/' folder.

2. Run Backend
Generated bash
      
# Navigate to the backend folder
cd backend

# Create virtual environment and install dependencies
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Start the server
python app.py

 The backend will be running at http://127.0.0.1:5001


 3. Run Frontend

    Open the project folder in VS Code.

    Right-click frontend/index.html.

    Select "Open with Live Server".

    Your browser will open to the application, ready to use!
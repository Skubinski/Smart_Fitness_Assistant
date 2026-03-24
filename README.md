# Smart Fitness Assistant
Smart Fitness Assistant is a modular desktop application built with Python and wxPython, designed to provide personalized fitness and nutrition recommendations using machine learning.

# Features
   - Personalized diet and workout recommendations
   - Machine Learning integration for predictions
   - Clean and interactive GUI built with wxPython
   - Data persistence using SQLite
   - Tracks user history and progress
   - Modular and extensible architecture
   - Architecture Overview
   - The application follows a modular architecture with the following components:
      - User Interface (UI) – Handles user input and displays results
      - Application Logic – Processes and validates data
      - Machine Learning Models – Generate recommendations
      - Database (SQLite) – Stores user data and history
      - Data flows from the UI → Logic Layer → ML Models → Database → UI.
    
# Technologies Used
   - Python
   - wxPython
   - SQLite
   - scikit-learn
   - joblib
   - pandas
   - matplotlib
   
# Getting Started
1. Clone the repository
git clone https://github.com/Skubinski/Smart_Fitness_Assistant.git

2. Navigate to the project (cd Smart_Fitness_Assistant/)

3. Install dependencies
pip install -r requirements.txt

4. Run the application
python main.py

# Project Structure
Smart_Fitness_Assistant/
│
├── Database/              # SQLite database
├── Dataset/               # Used datasets
├── Logic/                 # Dataset operations
├── Models/                # ML models
├── UI/                    # wxPython interface
├── Gallery/               # Gallery
├── main.py                # Entry point
├── requirements.txt       # Required libraries
└── README.md              # Application information

# Future Improvements
   - Integration with wearable devices
   - Advanced analytics and progress charts
   - Mobile or web version
   - More accurate ML models
     
# Contact
For questions or collaboration:
kubinskisergey@gmail.com

# License
This project is licensed under the MIT License.

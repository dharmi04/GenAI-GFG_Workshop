# Python Virtual Environment Setup

This repository contains a Python project that utilizes a virtual environment for dependency management. Follow the instructions below to set up and run the project in your local environment.

## Prerequisites

- Python 3.x installed on your system
- `virtualenv` package installed (if not installed, you can install it via `pip install virtualenv`)

## Setup

1. Clone this repository to your local machine.

```
git clone "https://github.com/dharmi04/GenAI-GFG_Workshop.git"
cd GenAI-GFG_Workshop
```

2. Create a virtual environment inside the project directory.

```
python3 -m venv venv
```

3. Activate the virtual environment.

On macOS/Linux:
```
source venv/bin/activate
```

On Windows:
```
venv\Scripts\activate
```

4. Install project dependencies.

```
pip install -r requirements.txt
```

## Running the Project

Once the virtual environment is set up and activated, you can run the Python scripts or start the application.

```
python simple.py
streamlit run Onthatday.py
```

## Deactivating the Virtual Environment

When you're done working on the project, you can deactivate the virtual environment.

```
deactivate
```

## Additional Notes

- Make sure to activate the virtual environment every time you work on the project to ensure that you're using the correct dependencies.
- It's recommended to keep your virtual environment folder (`venv` in this case) out of version control by adding it to your `.gitignore` file.

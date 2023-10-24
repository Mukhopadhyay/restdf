import uvicorn
from .app import app


# Main method
def main() -> None:
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")


# Nohup run: nohup python3 -m restdf /absolute/path/to/df > stdlog.txt 2>&1 &
# More test data: https://github.com/cs109/2014_data/
if __name__ == "__main__":
    main()

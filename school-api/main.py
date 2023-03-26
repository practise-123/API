import logging
import uvicorn
from fastapi import FastAPI

logging.basicConfig(filename="tasks-api.log", filemode='w+', level=logging.DEBUG
                    , format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)
# logger.addHandler(logging.StreamHandler(sys.stdout))
logger.info("API Started")

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
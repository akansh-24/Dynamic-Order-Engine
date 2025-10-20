import logging
import asyncio
from fastapi import FastAPI
from .database import SessionLocal
from .db_service import check_and_update_inventory
from .kafka_service import consumer
from .migration_utils import run_flyway_migration
from .routes import router as inventory_routes

logger = logging.getLogger(__name__)

app = FastAPI()

app.include_router(inventory_routes)

def kafka_consumer():
    for message in consumer:
        logger.info(f'received message: {message}')
        order_data = message.value
        db = SessionLocal()
        try:
            check_and_update_inventory(db, order_data)
        finally:
            db.close()

def run_flyway_with_retry(retries=5, delay=3):
    import time
    for i in range(retries):
        try:
            run_flyway_migration()
            logger.info("Flyway migration applied successfully")
            return
        except Exception as e:
            logger.warning(f"Flyway migration failed (attempt {i+1}/{retries}): {e}")
            time.sleep(delay)
    raise Exception("Flyway migration failed after multiple attempts")    

@app.on_event("startup")
async def startup_event():
    logger.info("Trying to start....")
    # Run Flyway migrations safely with retry
    run_flyway_with_retry()

    # Start Kafka consumer in a background thread (non-blocking)
    asyncio.create_task(asyncio.to_thread(kafka_consumer))

    logger.info("Connected main is running properly")
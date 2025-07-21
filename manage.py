# manage.py
from fastapi import FastAPI
from adapters.assembly import Container
import blueprints.main
import logging

logging.basicConfig(level=logging.INFO)

container = Container()
container.wire(modules=[blueprints.main])  # Passa o módulo, não o nome como string


app = FastAPI()
app.include_router(blueprints.main.main)  # Ou use o nome router se preferir


# Se quiser rodar localmente:
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)

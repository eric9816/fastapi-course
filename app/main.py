from fastapi import FastAPI


app = FastAPI()

@app.get('/hotels/{id}')
def get_hotels(id: int, tv: str):
    return [id, tv, 'ура']
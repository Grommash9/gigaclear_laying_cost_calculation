import tempfile
from fastapi import FastAPI, UploadFile, File
from igraph import Graph
from main import count_graph_realisation_price
from fastapi.responses import JSONResponse

app = FastAPI()


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.graphml'):
        return JSONResponse(status_code=500, content={"error": "wrong file type! please use only graphml"})

    content = await file.read()
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(content)
    temp_file.close()
    try:
        graph_data = Graph.Read_GraphML(temp_file.name)
        result = count_graph_realisation_price(graph_data)
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": f"{e}"})

    return JSONResponse(status_code=200, content={"error": "ok", 'result': result})


from fastapi import FastAPI
import sz_sysinfo

app = FastAPI()

@app.get("/")
def read_root():
    return {"meta": {"version": "0.0.1",
                     "name": "System Info API",}}
@app.get("/sysinfo")
def read_sysinfo():
    return sz_sysinfo.get_sysinfo()
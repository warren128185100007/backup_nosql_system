import subprocess
import os
import shutil
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
   CORSMiddleware,
   allow_origins=["*"],
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)

@app.get("/")
async def root():
   return {"message": "Database Backup Server is Running"}

@app.get("/download-student-backup")
async def backup_student_db():
   dump_tool = r"C:\Program Files\MongoDB\Database Tools\bin\mongodump.exe"

   if not os.path.exists(dump_tool):
       raise HTTPException(status_code=500, detail="mongodump.exe not found in path")

   backup_filename = "student_backup.gz"
   full_path = os.path.join(os.getcwd(), backup_filename)

   if os.path.exists(full_path):
       os.remove(full_path)

   command = [
       dump_tool,
       "--db", "student",
       f"--archive={full_path}",
       "--gzip"
   ]

   subprocess.run(command, check=True)

   return FileResponse(
       path=full_path,
       filename="student_backup.gz",
       media_type="application/gzip"
   )
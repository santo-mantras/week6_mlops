FROM python:3.10-slim

# 2. Set working directory
WORKDIR /app

# 3. Copy all files from the project folder to the /app directory
COPY . /app

# 4. Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# 5. Expose port 8000 (standard for Gunicorn)
EXPOSE 8000

# 6. Command to run the Gunicorn server a production-ready server that runs the app.
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "iris_fastapi:app", "--bind", "0.0.0.0:8000"]

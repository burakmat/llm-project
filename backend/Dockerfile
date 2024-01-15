FROM python:3.9.18-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000
ENTRYPOINT [ "python", "manage.py", "runserver"]
CMD [ "0.0.0.0:8000" ]
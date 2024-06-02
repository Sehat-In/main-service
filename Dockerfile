FROM python:3.12

WORKDIR /code

ARG AUTH_API_URL
ARG PROGRESS_API_URL
ARG FORUM_API_URL
ARG MEAL_WORKOUT_API_URL

ENV AUTH_API_URL ${AUTH_API_URL}
ENV PROGRESS_API_URL ${PROGRESS_API_URL}
ENV FORUM_API_URL ${FORUM_API_URL}
ENV MEAL_WORKOUT_API_URL ${MEAL_WORKOUT_API_URL}

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . .

EXPOSE 8000

CMD ["fastapi", "run", "main.py", "--port", "8000"]
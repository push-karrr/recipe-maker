FROM python3.13-slim as builder

WORKDIR /app

COPY requirements.txt /install/requirements.txt



FROM python3.13-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local

ENV PATH=/root/.local/bin:$PATH

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
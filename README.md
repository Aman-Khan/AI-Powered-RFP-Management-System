# AI-Powered-RFP-Management-System

docker run -d \
  --name rfp_postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=rfp_db \
  -p 5432:5432 \
  postgres:15


prisma db push --force-reset
prisma generate

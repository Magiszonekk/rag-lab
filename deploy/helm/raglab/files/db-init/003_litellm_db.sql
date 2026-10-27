-- osobna baza dla bramki LiteLLM (klucze wirtualne, budżety) w tym samym Postgresie RAG Lab (D11)
SELECT 'CREATE DATABASE litellm' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'litellm')\gexec

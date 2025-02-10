# Expects image with tag "ai-service" to be built
docker run --rm -p 5000:5000 -it -v ~/gensim-data:/root/gensim-data -v ./models:/app/models ai-service

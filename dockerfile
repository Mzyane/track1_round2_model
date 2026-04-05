# Dockerfile
# Base image provided by competition
FROM 10.200.99.202:15080/zero2x002/competition-base:ubuntu22.04-py310.19

# Set working directory
WORKDIR /workspace

# Copy requirements first (to leverage Docker layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt -i https://repo.huaweicloud.com/repository/pypi/simple

# Copy all project files into the container
COPY . .

# Ensure run.sh is executable
RUN chmod +x run.sh

# Default command (the CI/CD pipeline will override with START_CMD)
CMD ["./run.sh"]

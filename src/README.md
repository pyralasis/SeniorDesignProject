# senòr design

## Development

For reproducible development, we recommend using [Docker](https://www.docker.com/).
You can build the Docker image with the following command (make sure you are in the `src` directory):

```bash
docker build -t sdp .
```

You can then run the Docker container with the following command:

```bash
docker run -it --rm  -v $(pwd):/app -w /app sdp
```

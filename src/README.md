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

### Dev Container

I have included a `.devcontainer` directory that can be used with [Visual Studio Code](https://code.visualstudio.com/). This will allow you to develop in a containerized environment. You can find more information on how to use this [here](https://code.visualstudio.com/docs/remote/containers).

### Running the app

To run the app, make sure all the dependencies are installed. Then, from the `src` directory, run the following command:

```bash
QUART_DEBUG=1 python backend/run.py
```

This will start the Quart server and you can access the app at `http://localhost:7777`. You can also see all the routes by setting the `QUART_DEBUG` environment variable to `1` (as shown above).


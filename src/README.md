# senòr design

## Installation

For reproducible development, we recommend using [Docker](https://www.docker.com/).
You can build the Docker image with the following command **(make sure you are in the `src` directory for all of the following commands)**:

### Bare Machine

Make sure you have Python 3.10 installed, and that you have `pip` and `npm` installed.

Then, run the following commands:

```bash
npm install # install
npm start # start the frontend and backend concurrently
```

### Docker

Alternatively, you can build the Docker image with the following command:

```bash
docker build -t sdp .
```

Building in docker will restrict dependencies to the container, so you will not need to install any dependencies on your host machine.
You can then run the Docker container with the following command:

```bash
docker run -it --rm  -v $(pwd):/app -w /app sdp
```

Once you are in the container, you can run the following command to start the frontend and backend:

```bash
npm start
```

### Dev Container

I have included a `.devcontainer` directory that can be used with [Visual Studio Code](https://code.visualstudio.com/). This will allow you to develop in a containerized environment. You can find more information on how to use this [here](https://code.visualstudio.com/docs/remote/containers).

### Running the app

To run the app, make sure all the dependencies are installed. Then, from the `src` directory, run the following command:

```bash
QUART_DEBUG=1 python backend/run.py
```

This will start the Quart server and you can access the app at `http://localhost:7777`. You can also see all the routes by setting the `QUART_DEBUG` environment variable to `1` (as shown above).


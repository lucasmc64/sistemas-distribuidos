![Relist](./readme/cover.png)

# 🔑 Valkyrie

## 🎯 Goal

A multi-version key-value storage hybrid architecture system to experience first-hand the anxieties and pleasures of the Distributed Systems area.

## :scroll: Some details

This project was created using Python, MQTT and gRPC technologies.

> **Note**: Pay attention to the minimum version of Python required by [gRPC](https://grpc.io/). It is currently version 3.7 but this requirement may change in the future.

## :thinking: How do I run the project on my machine?

The first step is to clone the project, either via terminal or GitHub Desktop, or even by downloading the compressed file (.zip). After that, go ahead.

### :hammer_and_wrench: Requirements

- [Python](https://www.python.org/)

  > Was used `venv` to create a virtual environment to encapsulate the dependencies. This feature requires python 3.10 and maybe will be necessary install some package like `python3.10-venv` as was in Pop!_OS 22.04. 
- [MQTT](https://mqtt.org/)

### :mag: Installing dependencies

With Python and MQTT installed, access the project directory via terminal and run the `./compile.sh` script to install the required packages, create the virtual environment and compile the .proto files.

### ⚙️ Accessing virtual environment

Before running the project in your virtual environment first you’ll need to activate it.

```bash
source ./pyenv/bin/activate
```

> If you want, for any reason, to exit the virtual environment, simply run the `deactivate` command.

### :sparkles: Running project

Encapsulating server and client execution is a way of abstracting some responsibilities and steps that must be performed, providing a CLI for configurations that can be parameterized.

To run the server, simply run the following file:

> If the `--port` flag is not used, the server will default to port `12345` and try to use it.

```bash
./server.sh
```

To run the client, run the following script:

> If the `--port` flag is not given, the client will assume that the server is running on port `12345` and will try to connect to it.

```bash
./client.sh
```

### :tada: If everything went well...

Now you are running the project beautifully!

## :memo: License

This project is under the GNU General Public License v2.0 license. See the [LICENSE](LICENSE) for more information.

---

Made with 🖤 by [Lucas Vieira](https://www.linkedin.com/in/lucas-mattos-vieira-247950187/) and [Lucas Coutinho](https://www.linkedin.com/in/lucasmc64/). :wave: Get in touch!

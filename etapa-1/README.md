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

  > Python `venv` was used to create a virtual environment to encapsulate the dependencies. This feature requires python 3.10 and maybe it will be necessary to install a package like `python3.10-venv` like it was in Pop!_OS 22.04. 
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
# Without specify a custom port
./server.sh

# Specifying a custom port
./server.sh --port=1224
```

To run the client, run the following script:

> If the `--port` flag is not given, the client will assume that the server is running on port `12345` and will try to connect to it.

```bash
# Without specify a custom port
./client.sh

# Specifying a custom port
./client.sh --port=1224
```

### :tada: If everything went well...

Now you are running the project beautifully!

## 💁 Examples

### 🤲 `Get`

Returns value for the key and version immediately less than or equal to the one entered.

> The version can be left blank (or less than or equal to 0) to get newer value.

```bash
--- Key Value Store ---
 1. Get
 2. GetRange
 3. GetAll
 4. Put
 5. PutAll
 6. Del
 7. DelRange
 8. DellAll
 9. Trim
10. Exit

Select operation: 1

Key: a
Ver: 

> Response:
(key=a, ver=1695519359437)

Select operation: 1

Key: b
Ver: 1695514564199

> Response:

(key=b, val=2, ver=1695514564199)
```

### 🤲 `GetRange`

Returns values in the range between the two keys entered.

> The version can be left blank (or less than or equal to 0) to get newer value.
>
> If either version is actually reported. the largest of them is chosen and returns values and versions immediately smaller or equal to this version.

```bash
--- Key Value Store ---
 1. Get
 2. GetRange
 3. GetAll
 4. Put
 5. PutAll
 6. Del
 7. DelRange
 8. DellAll
 9. Trim
10. Exit

Select operation: 2

From key: b
From ver: 
To key: d
To ver: 

> Response:

(key=b, val=2, ver=1695514564199)
(key=c, val=3, ver=1695514564199)
(key=d, val=4, ver=1695514564200)

Select operation: 2

From key: b
From ver: 1695514564199
To key: d
To ver: 

> Response:

(key=b, val=2, ver=1695514564199)
(key=c, val=3, ver=1695514564199)
(key=d, ver=1695514564199)

Select operation: 2

From key: b
From ver: 
To key: d
To ver: 1695514564199

> Response:

(key=b, val=2, ver=1695514564199)
(key=c, val=3, ver=1695514564199)
(key=d, ver=1695514564199)

Select operation: 2

From key: b
From ver: 1695514564199
To key: d
To ver: 1695514564200

> Response:

(key=b, val=2, ver=1695514564199)
(key=c, val=3, ver=1695514564199)
(key=d, val=4, ver=1695514564200)
```

### 🤲 `GetAll`

Returns values for set of unordered given keys.

> The version can be left blank (or less than or equal to 0) to get newer value.
>
> If either version is actually reported. the largest of them is chosen and returns values and versions immediately smaller or equal to this version.

```bash
--- Key Value Store ---
 1. Get
 2. GetRange
 3. GetAll
 4. Put
 5. PutAll
 6. Del
 7. DelRange
 8. DellAll
 9. Trim
10. Exit

Select operation: 3

> Enter an empty key to finish request!

Key: a
Version: 

Key: b
Version: 1695514564199

Key: 

> Response:

(key=a, ver=1695519359437)
(key=b, val=2, ver=1695514564199)
```

### ✍️ `Put`

Updates/inserts entered value and key, returning value for previous key and version, as well as the new assigned version.

```bash
--- Key Value Store ---
 1. Get
 2. GetRange
 3. GetAll
 4. Put
 5. PutAll
 6. Del
 7. DelRange
 8. DellAll
 9. Trim
10. Exit

Select operation: 4

Key: a
Val: 1

> Response:

(key=a, old_ver=1695519359437, ver=1695520601457)

Select operation: 4

Key: o
Val: 8

> Response:

(key=o, ver=1695520624176)

Select operation: 4

Key: a
Val: 2

> Response:

(key=a, old_val=1, old_ver=1695520601457, ver=1695520689147)
```

### ✍️ `PutAll`

Updates/inserts entered values and keys, returning, for each key, the previous value and version, as well as the new assigned version.

```bash
--- Key Value Store ---
 1. Get
 2. GetRange
 3. GetAll
 4. Put
 5. PutAll
 6. Del
 7. DelRange
 8. DellAll
 9. Trim
10. Exit

Select operation: 5

Keys: a b p l
Vals: 1 2 9 8

> Response:

(key=a, old_val=1, old_ver=1695520721822, ver=1695520747144)
(key=b, old_val=2, old_ver=1695520721822, ver=1695520747145)
(key=p, ver=1695520747145)
(key=l, ver=1695520747145)
```

### 👎️ `Del`

Removes all values associated with the key and returns value for key and most current version or empty values if the key does not exist.

```bash
--- Key Value Store ---
 1. Get
 2. GetRange
 3. GetAll
 4. Put
 5. PutAll
 6. Del
 7. DelRange
 8. DellAll
 9. Trim
10. Exit

Select operation: 6

Key: a

> Response:

(key=a, val=1, ver=1695520747144)

Select operation: 1

Key: a
Ver: 

> Response:

(key=a)
```

### 👎️ `DelRange`

Removes values in the range between the two keys entered, returning the most current values for these keys or empty values for keys that do not exist.

```bash
--- Key Value Store ---
 1. Get
 2. GetRange
 3. GetAll
 4. Put
 5. PutAll
 6. Del
 7. DelRange
 8. DellAll
 9. Trim
10. Exit

Select operation: 7

From key: f
To key: z

> Response:

(key=f, ver=1695519396936)
(key=g, ver=1695519502073)
(key=t, val=4, ver=1695519711452)
(key=o, val=8, ver=1695520624176)
(key=p, val=9, ver=1695520747145)
(key=l, val=8, ver=1695520747145)
```

### 👎️ `DelAll`

Removes values for the given set of keys and returns more current values or empty values for keys that do not exist.

```bash
--- Key Value Store ---
 1. Get
 2. GetRange
 3. GetAll
 4. Put
 5. PutAll
 6. Del
 7. DelRange
 8. DellAll
 9. Trim
10. Exit

Select operation: 8

Keys: b c d

> Response:

(key=b, val=4, ver=1695520915710)
(key=c, val=3, ver=1695520721823)
(key=d, val=4, ver=1695514564200)
```

### 🤏 `Trim`

Removes all values associated with the key except the most recent version and returns value and version for the key or empty values if key does not exist.

```bash
--- Key Value Store ---
 1. Get
 2. GetRange
 3. GetAll
 4. Put
 5. PutAll
 6. Del
 7. DelRange
 8. DellAll
 9. Trim
10. Exit

Select operation: 4

Key: w
Val: 0

> Response:

(key=w, ver=1695520979585)

Select operation: 4

Key: w
Val: 90

> Response:

(key=w, old_val=0, old_ver=1695520979585, ver=1695521004688)

Select operation: 9

Key: w

> Response:

(key=w, val=90, ver=1695521004688)
```

## 🧪 Tests

The client we created is interactive, that is, it presents a menu with all the possible options and the user can execute several of them in sequence in just a single execution of the file.

Therefore, due to the way it was designed, for stress testing it is necessary to use a file that contains all the entries (number of operations and data that would normally be entered in the CLI) sequentially separated by line breaks.

We create a base file called `test.txt` which is at the root of the project. You could use it in the following way:

```bash
./client.sh < ./test.txt
```

## :memo: License

This project is under the MIT License v2.0 license. See the [LICENSE](LICENSE) for more information.

---

Made with 🖤 by [Lucas Vieira](https://www.linkedin.com/in/lucas-mattos-vieira-247950187/) and [Lucas Coutinho](https://www.linkedin.com/in/lucasmc64/). :wave: Get in touch!

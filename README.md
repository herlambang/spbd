# SPBD

ReST based audio converter prototype.

## Tech Stacks
- Python 3.11
- PostgreSQL
- Fastapi (https://fastapi.tiangolo.com/)
- FFmpeg (https://www.ffmpeg.org/)

## How to run using docker  

1. Create file `.env.compose`. 

2. Add these environment variable with preferred values  
    DB_USER=theuser  
    DB_PASSWORD=pwd123  
    DB_NAME=thedb  
    DB_PORT=5433  
    APP_PORT=8000  
    ENV_=prod

    > Sample also can be found in env.example

3. Build image and start the containers
    ```sh
    $ docker compose --env-file .env.compose -f docker/docker-compose.yaml up -d --build
    ```

4. Check if application is ready
    ```sh
    $ curl http://localhost:8000/version
    {"version":"0.1.0"}
    ```

5. Stop containers
    ```sh
    $ docker compose --env-file .env.compose -f docker/docker-compose.yaml stop
    ```

## Add and Fetch Data

When running the rest container, a fixture script will be executed to add user and phrase data with ID 1 and 2 on each entities.  
Also the migration script run to create defined schema prior to the fixture insertion.

### Adding data
```sh
$ curl -v --request POST http://localhost:8000/v1/audio/user/1/phrase/1 -F "audio_file=@<path to m4a file>"
{"id":1,"path":"wav/audio_1_1.wav","user_id":1,"phrase_id":1}
```

This request should run successfully since user with id 1 and phrase with id 1 already exist.

Sending wrong parameters will result in error response. Such as:

- Adding a record that already exists, for instance resubmit request already succeed:
    ```sh
    $ curl -v --request POST http://localhost:8000/v1/audio/user/1/phrase/1 -F "audio_file=@song.m4a"
    {"detail":"audio already exists"}
    ```

- Sending user or phrase that doesn't exist
    ```sh
    $ curl -v --request POST http://localhost:8000/v1/audio/user/1/phrase/12 -F "audio_file=@song.m4a"
    {"detail":"phrase not found"}
    ```

- Sending wrong file type
    ```sh
    $ curl -v --request POST http://localhost:8000/v1/audio/user/1/phrase/1 -F "audio_file=@song.jpg"
    {"detail":"jpg is not acceptable format"
    ```

### Fetching (download) audio data

```sh
$ curl "http://localhost:8000/v1/audio/user/1/phrase/1/m4a" -o downloaded.m4a
% Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  100k  100  100k    0     0  6931k      0 --:--:-- --:--:-- --:--:-- 7165k
```

This request will download the audio file of user 1 and phrase 1 to file named downloaded.m4a

Sending wrong parameters will result in error response. Such as:

```sh
curl -v "http://localhost:8000/v1/audio/user/1/phrase/21/m4a"
*   Trying [::1]:8000...
* Connected to localhost (::1) port 8000
> GET /v1/audio/user/1/phrase/21/m4a HTTP/1.1
> Host: localhost:8000
> User-Agent: curl/8.4.0
> Accept: */*
>
< HTTP/1.1 404 Not Found
< date: Tue, 28 Jan 2025 14:49:43 GMT
< server: uvicorn
< content-length: 28
< content-type: application/json
<
* Connection #0 to host localhost left intact
{"detail":"audio not found"}
```
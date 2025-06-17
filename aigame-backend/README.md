# AIGame Backend

AIGame is a backend API for generating mini-games using AI. This project is built with Rust and powered by the Actix-web framework.

## Features
- AI-powered game generation
- RESTful API design
- High-performance backend with Actix-web
- Secure and scalable architecture

## Getting Started

### Prerequisites
Ensure you have the following installed:
- Rust (latest stable version)
- Cargo (Rust's package manager)

### Installation
Clone the repository:
```sh
$ git clone <private-repo-url>
$ cd AIGame
```

### Running the Server
Use Cargo to run the application:
```sh
$ API_LOG=info cargo run
```
The server will start on `http://127.0.0.1:8080` by default.

## API Endpoints

### Health Check
```http
GET /status
```
**Response:**
```json
{"status": "ok"}
```


## Configuration
Environment variables:
- `PORT`: Server port (default: 8080)
- `API_LOG`: Logging level (default: `info`)


## Tests
```sh
cd tests/
hurl --variable server=http://127.0.0.1:8080 api.hurl  --test 
```
if you want a report, add `--report-html .` to the command.

## License
This is a private repository. Unauthorized distribution is prohibited.

## Contributors
- Maintainer: [coding@dfine.tech]

For more information, please contact the repository owner.



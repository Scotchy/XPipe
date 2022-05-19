export var PROTOCOL = "http";

// "prod" or "dev"
export var ENV = "dev";

// The port of the backend API that will be used if ENV=="dev". 
// It allows you to use "npm start" and connect to the React server while using another port for the backend.
// In production environment, the React app is served by the Flask server on a port (5000 for example).
// The Flask server also handle the backend API on the same port.
export const DEV_PORT = 5000;
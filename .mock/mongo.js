/**
 * LOCAL DEVELOPMENT ONLY!
 * DO NOT USE PRODUCTION DATA HERE!
 *
 * Mongo init script mounted via docker-compose.yml into /docker-entrypoint-initdb.d, 
 * so it runs automatically on the container's first start to create the API's DB user.
 */

/* API User at MongoDB */
db.createUser({
    user: "fast-app-api",
    pwd: "123456",
    roles: [{role: "readWrite", db: "fastAppDB"}]
});

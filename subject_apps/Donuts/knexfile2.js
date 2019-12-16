module.exports = {
/**
   development: {
      client: 'pg',
      connection: 'postgres://localhost/donuts',
      migrations: {
          directory: __dirname + '/db/migrations',
        },
      seeds: {
          directory: __dirname + '/db/seeds',
        },
    },
  production: {
      client: 'pg',
      connection: process.env.DATABASE_URL,
      migrations: {
          directory: __dirname + '/db/migrations',
        },
      seeds: {
          directory: __dirname + '/db/seeds/production',
        },
    },
**/
 development: {
    client: 'sqlite3',
    connection: {
     // filename: ':memory:'
      filename: __dirname +'/drug.sqlite3'
    },
      migrations: {
          directory: __dirname + '/db/migrations',
        },
      seeds: {
          directory: __dirname + '/db/seeds/production',
        },
  }


};

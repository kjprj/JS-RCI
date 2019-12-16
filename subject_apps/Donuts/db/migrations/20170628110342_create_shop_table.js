
exports.up = function(knex, Promise) {
  return knex.schema.createTable('shops', function(table) {
  table.increments();
  table.string('name').notNullable();
  table.string('city').notNullable();
});
};

exports.down = function(knex, Promise) {
  return knex.schema.createTable('shops');

};

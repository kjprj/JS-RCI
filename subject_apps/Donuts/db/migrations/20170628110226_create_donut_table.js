
exports.up = function(knex, Promise) {
  return knex.schema.createTable('donuts', function(table) {
  table.increments();
  table.string('name').notNullable();
  table.string('topping');
  table.integer('price').notNullable();
});
};

exports.down = function(knex, Promise) {
  return knex.schema.createTable('donuts');
};

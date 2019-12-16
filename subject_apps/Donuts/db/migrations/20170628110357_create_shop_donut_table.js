
exports.up = function(knex, Promise) {
  return knex.schema.createTable('shop_donut', function(table) {

  table.increments();
  table.integer('shop_id').references('id').inTable('shops');
  table.integer('donut_id').references('id').inTable('donuts');
  });
};

exports.down = function(knex, Promise) {
  return knex.schema.createTable('shop_donut');

};

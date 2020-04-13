exports.up = function(knex, Promise) {
  return knex.schema.createTable('shops', function(table) {
      table.increments();
      table.string('name');
      table.string('city');
    })
    .createTable('donuts', function(table) {
      table.increments();
      table.string('donuts_name');
      table.string('topping');
      table.integer('price');
    })
    .createTable('shop_donuts', function(table) {
      table.increments();
      table.integer('shop_id').references('id').inTable('shops');
      table.integer('donut_id').references('id').inTable('donuts');
    })
    .createTable('employees', function(table) {
      table.increments();
      table.string('first_name');
      table.string('last_name');
      table.integer('favorite_donut').references('id').inTable('donuts');
      table.integer('store_id').references('id').inTable('shops');
    })
};

exports.down = function(knex, Promise) {

};

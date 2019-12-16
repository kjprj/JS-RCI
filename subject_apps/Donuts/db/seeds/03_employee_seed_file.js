
exports.seed = function(knex, Promise) {
  // Deletes ALL existing entries
  return knex('employee').del()
    .then(function () {
      // Inserts seed entries
      return knex('employee').insert([
        {first_name: 'Vinnii', last_name: 'Otchkov',favorite_donut:3, shop_id:3},
        {first_name: 'Race', last_name: 'Carpenter',favorite_donut:2, shop_id:2},
        {first_name: 'Stephen', last_name: 'Eversole',favorite_donut:1, shop_id:1}
      ]);
    });
};

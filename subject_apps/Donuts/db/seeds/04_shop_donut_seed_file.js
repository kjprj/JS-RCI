
exports.seed = function(knex, Promise) {
  // Deletes ALL existing entries
  return knex('shop_donut').del()
    .then(function () {
      // Inserts seed entries
      return knex('shop_donut').insert([
        {shop_id: 1, donut_id:1},
        {shop_id: 2, donut_id:2},
        {shop_id: 3, donut_id:3}
      ]);
    });
};

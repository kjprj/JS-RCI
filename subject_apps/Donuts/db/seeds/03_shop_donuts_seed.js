exports.seed = function(knex, Promise) {
  // Deletes ALL existing entries
  return knex('shop_donuts').del()
    .then(function() {
      // Inserts seed entries
      return knex('shop_donuts').insert([{
          shop_id: 1,
          donut_id: 2
        },
        {
          shop_id: 2,
          donut_id: 1
        },
        {
          shop_id: 3,
          donut_id: 3
        },
        {
          shop_id: 4,
          donut_id: 5
        },
        {
          shop_id: 4,
          donut_id: 2
        },
        {
          shop_id: 1,
          donut_id: 4
        },
        {
          shop_id: 2,
          donut_id: 5
        },
        {
          shop_id: 3,
          donut_id: 4
        },
        {
          shop_id: 2,
          donut_id: 4
        },
      ]);
    });
};

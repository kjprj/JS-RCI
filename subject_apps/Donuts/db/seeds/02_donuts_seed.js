exports.seed = function(knex, Promise) {
  // Deletes ALL existing entries
  return knex('donuts').del()
    .then(function() {
      // Inserts seed entries
      return knex('donuts').insert([{
          donuts_name: 'Maple',
          topping: 'Maple Frosting',
          price: 3
        },
        {
          donuts_name: 'Sugar',
          topping: 'Sugar covering',
          price: 2
        },
        {
          donuts_name: 'Cinnamon',
          topping: 'Cinnamon covering',
          price: 2
        },
        {
          donuts_name: 'Jelly',
          topping: 'Jelly filling',
          price: 3
        },
        {
          donuts_name: 'Glazed',
          topping: 'Frosting',
          price: 2
        }
      ]);
    });
};

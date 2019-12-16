
exports.seed = function(knex, Promise) {
  // Deletes ALL existing entries
  return knex('donuts').del()
    .then(function () {

      // Inserts seed entries
      return knex('donuts').insert([
        {name: 'Glazed', topping: null, price:2},
        {name: 'Long John', topping: 'Maple', price:3},
        {name: 'Frosted', topping: 'Strawberry', price:2},
        {name: 'Donut Holes', topping: 'Powdered Sugar', price:1}

      ]);
    });
};

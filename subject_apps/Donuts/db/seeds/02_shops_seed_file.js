
exports.seed = function(knex, Promise) {
  // Deletes ALL existing entries
  return knex('shops').del()
    .then(function () {
      // Inserts seed entries
      return knex('shops').insert([
        {name:'Dillas Donuts', city: 'Detroit'},
        {name:'Dunkin Donuts', city: 'Phoenix'},
        {name:'Doh! Nuts', city: 'San Diego'}
      ]);
    });
};

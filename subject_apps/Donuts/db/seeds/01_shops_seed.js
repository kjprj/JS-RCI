exports.seed = function(knex, Promise) {
  // Deletes ALL existing entries
  return knex('shops').del()
    .then(function() {
      // Inserts seed entries
      return knex('shops').insert([{
          name: 'Roundys',
          city: 'Fat, USA'
        },
        {
          name: 'Cloggys',
          city: 'Obese Beach, USA'
        },
        {
          name: 'Fattys',
          city: 'New Butt City, USA'
        },
        {
          name: 'Slappys',
          city: 'Lardville, USA'
        }
      ]);
    });
};

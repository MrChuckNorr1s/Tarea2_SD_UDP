const cats = [
  {
    age: 2,
    breed: 'Siamese',
    gender: 'Male',
    name: 'Simba',
  },
  {
    age: 4,
    breed: 'Bengal',
    gender: 'Female',
    name: 'Luna',
  },
  {
    age: 3,
    breed: 'Persian',
    gender: 'Male',
    name: 'Felix',
  },
  {
    age: 1,
    breed: 'Sphynx',
    gender: 'Female',
    name: 'Nala',
  },
  {
    age: 5,
    breed: 'Maine Coon',
    gender: 'Male',
    name: 'Thor',
  },
  {
    age: 2,
    breed: 'Ragdoll',
    gender: 'Female',
    name: 'Bella',
  },
  {
    age: 6,
    breed: 'Siamese',
    gender: 'Male',
    name: 'Zeus',
  },
  {
    age: 1,
    breed: 'Scottish Fold',
    gender: 'Female',
    name: 'Mia',
  },
  {
    age: 3,
    breed: 'Siberian',
    gender: 'Male',
    name: 'Leo',
  },
  {
    age: 7,
    breed: 'Burmese',
    gender: 'Female',
    name: 'Cleo',
  },
  {
    age: 4,
    breed: 'Siberian',
    gender: 'Female',
    name: 'Loreto',
  },
  {
    age: 3,
    breed: 'Black and White',
    gender: 'Male',
    name: 'Pancho',
  },
  {
    age: 2,
    breed: 'Maine Coon',
    gender: 'Female',
    name: 'Sofia',
  },
  {
    age: 5,
    breed: 'Carey',
    gender: 'Male',
    name: 'TomÃ¡s',
  },
  {
    age: 3,
    breed: 'Siamese',
    gender: 'Male',
    name: 'Cesar',
  },
  {
    age: 6,
    breed: 'Persian',
    gender: 'Male',
    name: 'Diego',
  },
  {
    age: 1,
    breed: 'Scottish Fold',
    gender: 'Female',
    name: 'Mona',
  },
  {
    age: 4,
    breed: 'Bengal',
    gender: 'Male',
    name: 'Tito',
  },
  {
    age: 2,
    breed: 'Sphynx',
    gender: 'Female',
    name: 'Lola',
  },
  {
    age: 7,
    breed: 'Ragdoll',
    gender: 'Male',
    name: 'Max',
  },
];

cats.forEach(async (cat) => {
  try {
    console.log(JSON.stringify(cat));
    await fetch('http://localhost:3000/api/cats', {
      method: 'POST',
      body: JSON.stringify(cat),
      headers: {
        'Content-Type': 'application/json',
      },
    });
  } catch (error) {
    console.log('Something went wrong sendind this cat:', cat, error);
  }
});

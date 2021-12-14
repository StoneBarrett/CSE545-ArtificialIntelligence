"use strict";

const permutations = require("./tables/permutations");
const eval_fitness = require("./eval_fitness");

const Cube = require("rubiks-cube");

const cut = (arr, size) => arr.slice(0, Math.floor(arr.length / size)); // cut array to a size

const rand_perm = () => {
  return permutations[Math.floor(Math.random() * permutations.length)]; // gen a random perm from perms
};

const rand_ori = () => {
  const oris = ["z", "z'", "z2"];
  return oris[Math.floor(Math.random() * oris.length)]; // gen rand orientation
};

const rand_rot = () => {
  const rots = ["x", "x'", "x2", "y", "y'", "y2"];
  return rots[Math.floor(Math.random() * rots.length)]; // gen rand rotation
};

const mutate = (perms) => {
  const new_perms = [...perms];

  // decide which mutation
  switch (Math.floor(Math.random() * 6)) {
    case 0:
      new_perms.push(rand_perm()); // one perm
      break;
    case 1:
      new_perms.push(rand_perm()); // two perms to cover more sides
      new_perms.push(rand_perm());
      break;
    case 2:
      new_perms.push(rand_rot()); // rot and perm to cover stickers not in perms
      new_perms.push(rand_perm());
      break;
    case 3:
      new_perms.push(rand_ori()); // ori and perm to cover stickers not in perms
      new_perms.push(rand_perm());
      break;
    case 4:
      new_perms.push(rand_rot()); // double up on the above
      new_perms.push(rand_ori());
      new_perms.push(rand_perm());
      break;
    case 5:
      new_perms.push(rand_ori()); // double up on the above
      new_perms.push(rand_rot());
      new_perms.push(rand_perm());
      break;
  }

  return new_perms;
};

const crossover = (parent) => {
  // cross over by mutating a parent => new child
  const new_perms = mutate(parent.perms);
  return { perms: new_perms, fitness: Infinity };
};

const breed = (population, elitism) => {
  // breed by taking top performers and crossing them over asexually
  const new_pop = cut(population, elitism);
  const top_pop = [...new_pop];

  for (let i = 0; new_pop.length < population.length; i++) {
    const rand = Math.floor(Math.random() * top_pop.length);
    new_pop.push(crossover(top_pop[rand]));
  }

  return new_pop;
};

const create_population = (pop_size) => {
  // create array of individuals (ie. population) filled with one rand perm each
  const population = new Array(pop_size);
  for (let i = 0; i < pop_size; i++) {
    population[i] = { perms: [rand_perm()], fitness: Infinity };
  }
  return population;
};

module.exports = (scramble, pop_size, num_gens, elitism) => {
  const cube = Cube.identity().scramble(scramble); // create a cube based on given scramble

  let population;

  const fitness_avgs = []; // array of avergae population fitness across generations

  for (let gens = 0; true; gens++) {
    if (gens % num_gens == 0) {
      // keep track of resets
      population = create_population(pop_size);
    }

    for (let i = 0; i < pop_size; i++) {
      const cube_perm = Cube.scramble(population[i].perms.join(" ")); // create a cube from the indviduals perms
      const cur_cube = new Cube(cube).multiply(cube_perm); // apply above scramble to the given starting cube

      population[i].fitness = eval_fitness(cur_cube); // clac fitness of individual and store
    }

    population.sort((a, b) => a.fitness - b.fitness); // sort pop by fitness

    // store fitness avg of pop
    const fitness_avg =
      population.reduce((acc, cur) => (acc += cur.fitness), 0) / pop_size;
    fitness_avgs.push(fitness_avg);

    // check to see if best performer is a solved cube, return if so
    if (population[0].fitness == 0) {
      population[0].perms = population[0].perms.join(" ").split(" ").join(" ");
      return {
        best: population[0],
        start: scramble,
        gens,
        fitness_avgs,
      };
    }

    population = breed(population, elitism); // breed population
  }
};

"use strict";

const Cube = require("rubiks-cube");

const compare = (arr1, arr2) => {
  // simple array comaprsion
  let fitness = 0;
  for (let i = 0; i < arr1.length; i++) {
    if (arr1[i] != arr2[i]) {
      fitness++;
    }
  }
  return fitness;
};

module.exports = (cube) => {
  if (cube.isSolved()) {
    return 0; // if solved, fitness is 0
  }

  let fitness = 1; // start with one bc above failed
  const goal = Cube.identity(); // solved cube
  cube = cube.orient(); // orient the cube to eval

  // comapre all stickers
  fitness += compare(goal.co, cube.co);
  fitness += compare(goal.cp, cube.cp);
  fitness += compare(goal.ep, cube.ep);
  fitness += compare(goal.eo, cube.eo);
  fitness += compare(goal.c, cube.c);

  return fitness;
};

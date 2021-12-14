"use strict";

const rubikGA = require("./src/rubikGA");
const fs = require("fs");

const start = (scramble, pop_size, num_gens, elitism, woc) => {
  const rubik = rubikGA(scramble, pop_size, num_gens, elitism);
  if (woc != undefined) {
    process.send(JSON.stringify(rubik));
  } else {
    fs.writeFileSync("./tmp.txt", JSON.stringify(rubik));
    console.log(rubik);
  }
};

start(...process.argv.slice(2));

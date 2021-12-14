"use strict";

const { performance } = require("perf_hooks");
const { fork } = require("child_process");
const { readFileSync, writeFileSync } = require("fs");

const start = () => {
  const rubik = `${__dirname}/../rubik/index.js`;

  const cmds = JSON.parse(readFileSync("./cmdFile.json"));

  // go thru each of the params in cmdFile and create a rubik child
  for (let i = 0; i < cmds.params.length; i++) {
    const cmd = cmds.params[i]; // get commands

    const start_time = performance.now(); // log start time

    // create the fork
    const child = fork(rubik, [
      cmd.scramble,
      cmd.pop_size,
      cmd.num_gens,
      cmd.elitism,
      "true",
    ]);

    console.log(`Rubik ${i} running...`);

    child.on("close", (code) => console.log(`Rubik ${i} finish! ${code}`)); // log that a rubik has finished

    // recieve messages from child
    child.on("message", (msg) => {
      const data = JSON.parse(msg); // get message data
      data.timeMs = performance.now() - start_time; // calculate time it took to finish, add to data
      console.log(`Rubik ${i} data:`); // log the data
      console.log(data); // ditto
      writeFileSync(`./output${i}.json`, msg); // also write the data to a file
    });
  }
};

start(process.argv.slice(2));

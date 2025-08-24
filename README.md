## brute-force combination generator
this program generates every single possible character combination in the ASCII character set with the specified character length(s), and stores all in a text file.  
---
## What happens
### Phase 1:
user inputs minimum and maximum length
benchmark feature asks if to run or not
### Phase 2:
if it runs, it gets time and dividies by number of combinations generated (100 multiplied by number of lengths, eg 1-5 is 5 lengths. 500 combinations total)
this gets the speed.
### Phase 3:
now inside the main function, the total combination count is divided by both speeds, yielding two estimated times, for performance and live display mode.
it displays both, and asks the user if they would like to generate.
### Benchmarking Feature
so in order for max accuracy the benchmarking feature runs AFTER max and min length are inputted.
for the benchmark to not take as long as the full generation, a **boolean** named benchmark must be added to the normal bruteforce function as a parameter to specify, which makes it only generate 100 combinations or so, per length.
then the function takes the max and minimum length as parameters and runs the brute force function with the added parameter of benchmark
eg. for benchmark of generation minimum length 1, max 5, the function brute_force(1,5,True) is ran, and it calculates and returns the final speed. in the main function the total amount of combinations is divided by

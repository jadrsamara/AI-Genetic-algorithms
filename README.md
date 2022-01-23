# AI-Genetic-algorithms
An Artificial intelligence project for Distributing Graduation Projects using Genetic algorithms

## implementation
Genetic algorithms look at the problem as natural selections, and the solution as a gene with the population as a set of genes (solutions). Genetic algorithms are comprised of five phases which are: the generation of the initial population, the Fitness function to differentiate between the different genes, the selection method to select the genes to crossover, the crossover method and finally the mutation.

### Initial Population
We start the creation of the initial population by creating a set number of random genomes. Creating a random genome goes like this:
The genome is a list with length equals to the number of groups, with the first element in the list representing the first group, the second element represents the second group, and so on for the rest of the groups. Now if you’re using Python to generate a random genome you can utilize the `random.sample` function included in the `random` library. The command looks like this:

```python
random.sample(list(range(1, values)), length)
```

`list(range(1, values))` :  this gives you a list of all the numbers between 1 and values which are in our case 38, And this list represents all the projects.

`Length` :                  this represents the length of the genome, meaning the number of groups.

Then you can do this many times and save all of the results into a list in order to have a new random initial population.

### Fitness Function
The fitness function is a function that basically calculates how good is a genome. (a solution)
```python
for gene in genome_under_testing:
  if int(gene) == int(ideal_list_1[counter]):
    score += 100 
    s_1 += 1 
  elif int(gene) == int(ideal_list_2[counter]): 
    score += 10 
    s_2 += 1 
  elif int(gene) == int(ideal_list_3[counter]): 
    score += 1 
    s_3 += 1 
  else: 
    # number of unmatched choices 
    score2 += 1 
    # number of groups 
  counter += 1
  
result = (counter - score2) * 1000 + score
```
we check the solution group by group and see if the group’s distribution matches one of their three choices or not, if it’s the first choice we add 100 to the score, if it’s the second we add 10 and if it’s the last we only add 1. And in the end after checkibng all the groups we get the number of satisfied groups (i.e., they have gotten one of their choices) and add that multiplied by 1000.
Then we have a score most dependent on the number of satisfied groups, then if two solutions have the same number of satisfied groups the score is then bias to the solution following the closer solution to the groups first, second then third choices.
The solution with its Fitness looks like this:

[35, 11, 12, 25, 31, 3, 26, 9, 13, 23, 29, 15, 8, 32, 37, 2, 7, 21, 30, 34, 1, 5, 16, 38, 20, 27, 14, 22, 17, 24, 6, 10, 28, 19, 18, 36]

-> 29675:(28, [16, 7, 5])

With 28 as the number of satisfied groups, 16 as the number of groups who got their first choice, 7 as the second choice and finally, 5 as the last choice.

### Selection
Before the selection process we sort the population based on Fitness, the better the fitness the lower the index for the solution in the population. (The better are first, and the worst are the last)

```python
population = sorted(
    population,
    key=lambda genome: fitness(genome),
    reverse=True
)
```

we sort using the `sorted` function, with the population (list of solutions-genomes) and the result is a sorted list based on fitness from better fitness to worst fitness.
Then we take the better half of the population and choose 2 distinct random parents.

Then we take the better half of the population and choose 2 distinct random parents.

```python
def pair_selector(population: Population) -> Population:
    p = random.sample(range(0, len(population) // 2), 2)
    return [population[p[0]], population[p[1]]]
```

now have 2 genomes that we can crossover.

### Crossover
Before we make the crossover, we need to choose a random point to cross the two genomes.
```python
cross_point_list = random.choices(list(range(1, len(parent_1))))
cross_point = cross_point_list[0]
```
the function `random.choices` returns a list containing a random element of the list inputted. We enter a list of numbers from 1 to the length of the genome to make the function return a point to which the crossover will be done on. The return type of the function even if its only one value is a list, so we take the first value of the list and make it the crossover point. 

Now the result of the crossover is two children, the first part of each child is simple the first part of each parent until the crossover point.

```python
res_1 = parent_1[0:cross_point]
res_2 = parent_2[0:cross_point]
```

the second part of the child is the second part of the other parent. (i.e., the part after the cross point)
to avoid replicated projects in the second part of the child, we check each new value of the gene if its already in the first part of the child, if yes then a new value is randomly chosen and tested from a list containing all the projects, and if its not in the first part then it’s appended to the first part.

```python
for i in parent_2[cross_point:]:
    if i not in res_1:
        res_1.append(i)
    else:
        for e in new_wanted_list:
            if e not in res_1:
                res_1.append(e)
                break
```
the same is done for the second child.
```python
return res_1, res_2
```
then the new children are returned.

### Mutation
Similar to the process of choosing a crossover point, we choose two points from the genome to be switched, we switched instead of choosing a random value in order to skip the repetition check process.
```python
mute_points = random.choices(list(range(1, len(genome_to_be_mutated))), k=2)
temp = genome_to_be_mutated[mute_points[0]]
genome_to_be_mutated[mute_points[0]] = genome_to_be_mutated[mute_points[1]]
genome_to_be_mutated[mute_points[1]] = temp
return genome_to_be_mutated
```
then the genome is returned after the switch is done.

## Running the Program
First of all, to run the python program without the console, we run the program with the `.pyw` extension.

![Image](https://raw.githubusercontent.com/jadrsamara/AI-Genetic-algorithms/main/assets/pyw.PNG)	

When we run it, we are greeted with this window:

![Image](https://raw.githubusercontent.com/jadrsamara/AI-Genetic-algorithms/main/assets/1.png)	

We have two files to import which are the file containing the students’ selections, and the file containing all the projects and their information.

To run the program at least the students’ selections file is needed.


### Setting the algorithm's options
There are many settings you can adjust, some for the algorithm itself like:

`Generations` :       the number of generations (iterations) for the evolution process.

`Population Size` :   the population size.

And some for the program like:

`Iterations` :	which is how many times to run the algorithm – in order to better our chance to find a good result.
This is followed by a checkmark with Infinite by it, when checked the program runs forever.

`Fitness Stop value` :	which tells the program to stop if a solution with that fitness is found.

`Not Ranked` :	selects what solutions to show based on fitness (the number of satisfied groups).

these choices: 

![Image](https://raw.githubusercontent.com/jadrsamara/AI-Genetic-algorithms/main/assets/2_cropped.png) 

Are some optimizations. 

The first one has two choices: 

![Image](https://raw.githubusercontent.com/jadrsamara/AI-Genetic-algorithms/main/assets/3.png) 

`Random` :	means the random projects chosen initially are random from 1 – 38.

`Random – Diff.` :	this is basically the same, but the difference between the number of groups and number of projects 
(in our case =|36-38| = 2) will then be the number of unwanted projects (projects no group has chosen) 
that we can discard from the random process.
The random process is in the initial population generation and in the crossover correction. (When a project is repeated after a crossover)

The second has three choices: 

![Image](https://raw.githubusercontent.com/jadrsamara/AI-Genetic-algorithms/main/assets/4.png) 

this controlls the Fitness function used by the algorithm.

`Satisfied groups favorable` :	calculates the fitness based on all of the three choices favoring the number of satisfied groups, 
followed by the number of groups with their first choice, then the number of groups with their second, 
and lastly, the number of groups with their third choice.

`First choice favorable` :	calculates the fitness only based on the number of groups with their first choice.

`Not Ranked` :	calculates the fitness only based on the number of satisfied groups (any of the three choices). The choice Satisfied groups favorable is the best of two worlds.

The option: 

![Image](https://raw.githubusercontent.com/jadrsamara/AI-Genetic-algorithms/main/assets/5.png) 

selects how many processes you wish to run at the same time for each run (`Iteration`) of the program.


### Running the algorithm
When importing the data, a window pops with only .csv files viewable to ease finding the right file.

![Image](https://raw.githubusercontent.com/jadrsamara/AI-Genetic-algorithms/main/assets/6.png)

And to run the program after importing the data, click the green Start bar at the bottom.

![Image](https://raw.githubusercontent.com/jadrsamara/AI-Genetic-algorithms/main/assets/7.png)

The *Stop* button can be clicked at any time to stop the current operation. 

The program running normally:

![Image](https://raw.githubusercontent.com/jadrsamara/AI-Genetic-algorithms/main/assets/8.png)

The program with `Show by fitness` set to 28:

![Image](https://raw.githubusercontent.com/jadrsamara/AI-Genetic-algorithms/main/assets/9.png)

The program result when it finishes: (when the projects file is imported)

![Image](https://raw.githubusercontent.com/jadrsamara/AI-Genetic-algorithms/main/assets/10.png)

The program result when it finishes: (when the projects file is **NOT** imported)

![Image](https://raw.githubusercontent.com/jadrsamara/AI-Genetic-algorithms/main/assets/11.png)










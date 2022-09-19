# Reflection: Mice finding the exit in a maze

The process of reading [this](https://tonytruong.net/solving-a-2d-maze-game-using-a-genetic-algorithm-and-a-search-part-2/) about the problem and writing the code was fairly simple to do. The problem arose when the code was finished and i ran the algorithm only to find out that mice though they were at a really good position quite early in the maze and inorder to continue from this position, they hade to take some path that would temporarly give them a worse fitness value but later pay off since they would eventually find the goal. I could not solve this problem although i know the reason behind it and will try to illustrade it with an image.

![](https://www.mathsisfun.com/algebra/images/function-max-min.svg)

So my analysiz of why the mice suddenly stops quite early in the maze is due to the first local maximum. They think that they are close to the goal although they're not even close. Inorder for the mice to escape from the local maximum and go to another local maximum is to first go down to the local minimum and then up towards the next local maximum again. One solution to this would be to mutate the mice enough so that they would go further away from the first local maximum and by doing that they would eventually find another local maximum. 

I included two mazes and you can try each one of them. The one calld ZeroMaze is a smaller maze where the mice easily finds the exit and FinalMaze is the large one included in the assignment.
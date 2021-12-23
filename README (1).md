
# Sudoku Solver with computer vision

## Installation

Install the libraries used to try out the code

```bash
  pip install opencv
  pip install pygame
  pip install keras
  pip install tensorflow
  pip install pytesseract
```

## How it works ?

This program allows the user to play sudoku with three levels of difficulty. During the game the user can place hypotheses of numbers in the boxes and only when he is sure he presses enter and validates as the final answer.

![Captura de ecrã 2021-12-23 164107](https://user-images.githubusercontent.com/76222459/147269155-175276c2-6c7c-436a-8f82-aea2f1b41d4b.png)

After the user makes a mistake three times in the sudoku game, it is possible to see the backtracking algorithm working as following...

![sudoku-2021-12-23-16-36-48-trim-8fvnknhh_NNNeLgzs](https://user-images.githubusercontent.com/76222459/147272884-1deaba09-98a8-4197-aa83-48a3afad387f.gif)

In case the user chooses to take a photo of a sudoku to obtain the solution, several image processing functions had to be implemented first for then that image was sent to a neural network to extract the digits of the grid. So for this option the user must click on the scan option

So, for example to solve the sudoku for the image bellow.

![oi2](https://user-images.githubusercontent.com/76222459/147271151-1979e9fb-0958-48c1-9581-e002c27c3ea6.png)

With the help of the openCv library it is possible to treat the image so that it looks like this:

![oi3](https://user-images.githubusercontent.com/76222459/147271300-e5ed655e-38b9-4846-9738-1b76bb86c05f.png)

With the pre-processed image, now the image will be ready to go to the neural network that will guess the digits contained in the image. The results of the neural network will be presented on a grid as shown:

![oi40](https://user-images.githubusercontent.com/76222459/147273016-aa737de8-13eb-4821-9f31-a575102c2824.png)

After that, it is possible to play just like in the level modes described earlier, so after the user makes three mistakes the backtracking will solve the sudoku of the image that the user took photo in first place.
## Installation

Install my-project with npm

```bash
  npm install my-project
  cd my-project
```
    
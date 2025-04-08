"""
Programa que simula el problema de los filósofos resuelto por turnos.

- Integrantes del equipo
Iván Alfredo López Barrera - 217628305
Zuzuky Guadalupe Gascón González - 300272566
"""

import os
import time
import random

PHILOSOPHERS = 5  # The amount of philosophers (set between 4 and 9)
MAX_FOOD = 6  # The maximum foods of each philosopher (set between 1 and 9)
FIRST_TIME_SLEEP = 1  # The duration of the first iteration (in seconds)
TIME_SLEEP = 3  # The duration of the rest of iterations (in seconds)

class Draw:
    _colors = {
        "green": "\033[92m",
        "orange": "\033[93m",
        "default": "\033[0m",
    }

    def drawTable(self, foods:list,
                  colors:list = ["default"] * PHILOSOPHERS) -> None:
        """
        Draws the food's table.
        """

        # Title and top of the table header
        print("Tabla de comidas por filósofo")
        print(" " + "_____" * (PHILOSOPHERS - 1) + "____")

        # Ids of the philosophers
        print("|", end="")
        for i in range(PHILOSOPHERS):
            print(self._colors[colors[i]], end="")  # Set the color
            print(f" F{i+1} ", end="")
            print(self._colors['default'], end="")  # Reset the color
            print("|", end="")

        # Bottom of the table header
        print("\n|" + "____|" * PHILOSOPHERS)

        # Body of the table content
        print("|", end="")
        for i in range(PHILOSOPHERS):
            print(self._colors[colors[i]], end="")  # Set the color
            print(f" 0{foods[i]} ", end="")
            print(self._colors['default'], end="")  # Reset the color
            print("|", end="")

        # Bottom of the table content
        print("\n|" + "____|" * PHILOSOPHERS + "\n")

    def _drawSingleCell(self, number:int, spaces:int = 0,
                        color:str = "default") -> None:
        """
        Private method that draws a single cell with a color.
        """

        # Initializes the color
        print(self._colors[color])

        # Print the cell with the spaces
        print(" " * spaces + " ____ ")
        print(" " * spaces + f"| F{number} |")
        print(" " * spaces + "|____|")

        # Set again the default color
        print(self._colors["default"])

    def _drawCoupleCells(self, number1:int, number2:int, distance:int,
                         color1:str = "default", color2:str = "default",
                         spaces:int = 0,) -> None:
        """
        Private method that draws a couple of cell with colors.
        """

        # Top of the cells (" _____ ")
        print(" " * spaces + f"{self._colors[color1]} ____ " +
              " " * distance + f"{self._colors[color2]} ____ ")

        # Body of the cells ("| F# |")
        print(" " * spaces + f"{self._colors[color1]}| F{number1} |" +
              " " * distance + f"{self._colors[color2]}| F{number2} |")

        # Footer of the cells ("|____|")
        print(" " * spaces + f"{self._colors[color1]}|____|" +
              " " * distance + f"{self._colors[color2]}|____|")

        print(self._colors["default"])  # Reset the color

    def drawScheme(self, colors:list) -> None:
        """
        Draws the philosophers scheme
        """

        print("Diagrama de filósofos")
        self._drawSingleCell(1, 12, colors[0])

        for i in range(1, PHILOSOPHERS//2):
            self._drawCoupleCells(i+1, PHILOSOPHERS-i+1, 18, colors[i], colors[-i])

        i += 1
        if PHILOSOPHERS % 2:
            self._drawCoupleCells(i+1, PHILOSOPHERS-i+1, 8, colors[i], colors[-i], 5)
        else:
            self._drawSingleCell(i+1, 12, colors[i])

class Simulation:
    _foods:list = [0] * PHILOSOPHERS
    _end:bool = False
    _first:bool = True
    _draw:Draw = Draw()
    _plays:list = []

    def _sleep(self) -> None:
        """
        Private method that controls the sleep
        """

        if self._first:
            time.sleep(FIRST_TIME_SLEEP)
            self._first = False
        else:
            time.sleep(TIME_SLEEP)

    def _getPossiblePhilosophers(self) -> list:
        """
        Private method that return the possible indices of philosophers to
        choose from based on their foods
        """

        philosophers:list = []

        for idx, food in enumerate(self._foods):
            if food != MAX_FOOD:
                philosophers.append(idx)

        return philosophers

    def _getColors(self, chosen_ones) -> list:
        """
        Private method that return the list of color based on:
        If the philosopher hasn't eaten -> default color
        If the philosopher has eaten -> orange
        If the philosopher has consumed the maximum amount of food -> green
        """

        colors:list = []

        for food in self._foods:
            color = "green" if food == MAX_FOOD else "default"
            colors.append(color)

        for chosen in chosen_ones:
            colors[chosen] = "orange"

        return colors

    def _verifyEnd(self) -> None:
        """
        Private method that verifies if it's the end of the simulation
        """

        for food in self._foods:
            if food != MAX_FOOD:
                return

        self._end = True

    def __init__(self):
        # First draw
        os.system("cls")
        self._draw.drawTable([0] * PHILOSOPHERS)
        self._draw.drawScheme(["default"] * PHILOSOPHERS)

        while not self._end:
            # Before a repetition wait and clear the screen
            self._sleep()
            os.system("cls")

            # Get the possible philosophers to choose some
            philosophers:list = self._getPossiblePhilosophers()
            chosen_ones:list = []

            # Select philosophers randomly
            while len(philosophers) > 0:
                chosen:int = random.choice(philosophers)
                chosen_ones.append(chosen)

                before = PHILOSOPHERS - 1 if chosen - 1 < 0 else chosen - 1
                after = 0 if chosen + 1 > PHILOSOPHERS - 1 else chosen + 1

                for i in range(PHILOSOPHERS):
                    if i in philosophers and i in [chosen, before, after]:
                        philosophers.remove(i)

            # Increase the foods of the chosen philosophers
            for chosen in chosen_ones:
                self._foods[chosen] += 1

            # Draw the table and the scheme
            self._draw.drawTable(self._foods, self._getColors(chosen_ones))
            self._draw.drawScheme(self._getColors(chosen_ones))

            # Show the philosophers that they have eaten
            print("Comieron los siguientes filósofos: ", end="")
            chosen_ones.sort()
            self._plays.append(chosen_ones)
            for idx, chosen in enumerate(chosen_ones):
                text = f"{chosen+1}" if idx == 0 else f", {chosen+1}"
                print(text, end="")

            # Verify if it's the end
            self._verifyEnd()

        # End of the simulation
        self._sleep()
        os.system("cls")
        self._draw.drawTable([MAX_FOOD] * PHILOSOPHERS, ["green"] * PHILOSOPHERS)
        self._draw.drawScheme(["green"] * PHILOSOPHERS)
        print("Fin de la simulación")
        print("\n\nHistorial:")
        for play in self._plays:
            print(f"- {play}")


def main():
    Simulation()

main()

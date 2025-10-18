package calculator;

import java.util.InputMismatchException;
import java.util.Scanner;

public class InputHandler {

    private final Scanner scanner;

    public InputHandler() {
        scanner = new Scanner(System.in);
    }

    public double getNumberInput(String prompt) {
        double number;
        while (true) {
            System.out.print(prompt);
            try {
                number = scanner.nextDouble();
                scanner.nextLine(); // Consume newline
                return number;
            } catch (InputMismatchException e) {
                System.out.println("Invalid input. Please enter a number.");
                scanner.nextLine(); // Clear invalid input from scanner
            }
        }
    }

    public void close() {
        scanner.close();
    }
}


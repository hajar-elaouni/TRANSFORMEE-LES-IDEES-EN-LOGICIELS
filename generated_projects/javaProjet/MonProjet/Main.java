package calculator;

import java.util.InputMismatchException;
import java.util.Scanner;

public class Main {

    public static void main(String[] args) {
        Calculator calculator = new Calculator();
        InputHandler inputHandler = new InputHandler();
        OutputHandler outputHandler = new OutputHandler();
        Scanner scanner = new Scanner(System.in);


        while (true) {
            System.out.println("\nSelect operation:");
            System.out.println("1. Add");
            System.out.println("2. Subtract");
            System.out.println("3. Multiply");
            System.out.println("4. Divide");
            System.out.println("5. Exit");

            System.out.print("Enter choice(1/2/3/4/5): ");
            int choice;
            try {
                choice = scanner.nextInt();
            } catch (InputMismatchException e) {
                System.out.println("Invalid input. Please enter a validnumber.");
                scanner.next();
                continue;
            }


            if (choice == 5) break;

            if (choice < 1 || choice > 4) {
                System.out.println("Invalid choice. Please try again.");
                continue;
            }

            double num1 = inputHandler.getNumberInput("Enter first number: ");
            double num2 = inputHandler.getNumberInput("Enter second number: ");

            double result;
            try {
                switch (choice) {
                    case 1:
                        result = calculator.add(num1, num2);
                        break;
                    case 2:
                        result = calculator.subtract(num1, num2);
                        break;
                    case 3:
                        result = calculator.multiply(num1, num2);
                        break;
                    case 4:
                        result = calculator.divide(num1, num2);
                        break;
                    default:
                        throw new IllegalStateException("Unexpected value: " + choice);
                }
                outputHandler.displayResult(result);
            } catch (ArithmeticException e) {
                outputHandler.displayError(e.getMessage());
            }
        }
        inputHandler.close();
        scanner.close();
        System.out.println("Exiting calculator...");
    }
}

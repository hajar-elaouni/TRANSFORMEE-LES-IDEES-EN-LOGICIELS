package calculator;

public class OutputHandler {

    public void displayResult(double result) {
        System.out.println("Result: " + result);
    }

    public void displayError(String message) {
        System.err.println("Error: " + message);
    }
}


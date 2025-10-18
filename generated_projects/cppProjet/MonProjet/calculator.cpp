#include "calculator.h"
#include <cmath> // for pow function if needed later.
#include <iostream>
#include <limits> // Required for numeric_limits


double getInput(double& op1, double& op2, char& op) {
    std::cout << "Enter first operand: ";
    std::cin >> op1;

    //Error handling for non-numeric input
    while (std::cin.fail()) {
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        std::cerr << "Invalid input. Please enter a number: ";
        std::cin >> op1;
    }

    std::cout << "Enter second operand: ";
    std::cin >> op2;
    while (std::cin.fail()) {
        std::cin.clear();
        std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
        std::cerr << "Invalid input. Please enter a number: ";
        std::cin >> op2;
    }

    std::cout << "Enter operator (+, -, *, /): ";
    std::cin >> op;
    while (op != '+' && op != '-' && op != '*' && op != '/') {
        std::cerr << "Invalid operator. Please enter +, -, *, or /: ";
        std::cin >> op;
    }
    return 0;
}


double performOperation(double op1, double op2, char op) {
    switch (op) {
        case '+': return op1 + op2;
        case '-': return op1 - op2;
        case '*': return op1 * op2;
        case '/':
            if (op2 == 0) {
                throw std::runtime_error("Division by zero!");
            }
            return op1 / op2;
        default: throw std::runtime_error("Invalid operator");
    }
}

void displayResult(double result) {
    std::cout << "Result: " << result << std::endl;
}

void handleErrors(const std::exception& e) {
    std::cerr << "Error: " << e.what() << std::endl;
}

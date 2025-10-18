#include "calculator.h"
#include <iostream>


int main() {
    double op1, op2;
    char op;
    double result;

    try {
        getInput(op1, op2, op);
        result = performOperation(op1, op2, op);
        displayResult(result);
    } catch (const std::exception& e) {
        handleErrors(e);
    }

    return 0;
}
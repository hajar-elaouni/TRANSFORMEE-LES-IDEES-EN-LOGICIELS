#ifndef CALCULATOR_H
#define CALCULATOR_H

#include <string>
#include <iostream>
#include <stdexcept>
#include <limits>


double getInput(double& op1, double& op2, char& op);
double performOperation(double op1, double op2, char op);
void displayResult(double result);
void handleErrors(const std::exception& e);

#endif

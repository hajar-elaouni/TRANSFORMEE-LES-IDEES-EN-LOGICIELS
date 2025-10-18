package calculator;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

public class CalculatorTest {

    @Test
    void testAdd() {
        Calculator calculator = new Calculator();
        assertEquals(5, calculator.add(2, 3));
        assertEquals(0, calculator.add(-2, 2));
        assertEquals(10.5, calculator.add(5.5, 5));
    }

    @Test
    void testSubtract() {
        Calculator calculator = new Calculator();
        assertEquals(-1, calculator.subtract(2, 3));
        assertEquals(4, calculator.subtract(6, 2));
        assertEquals(0.5, calculator.subtract(5.5, 5));
    }

    @Test
    void testMultiply() {
        Calculator calculator = new Calculator();
        assertEquals(6, calculator.multiply(2, 3));
        assertEquals(0, calculator.multiply(-2, 0));
        assertEquals(27.5, calculator.multiply(5.5, 5));
    }

    @Test
    void testDivide() {
        Calculator calculator = new Calculator();
        assertEquals(2, calculator.divide(6, 3));
        assertThrows(ArithmeticException.class, () -> calculator.divide(5, 0));
        assertEquals(1.1, calculator.divide(5.5, 5));
    }
}
class TestDivide(TestCase):
    def test_both_positive(self):
        self.assertEqual(divide(4, 2), 2)

    def test_negative_positive_division(self):
        self.assertEqual(divide(-4, 2), -2)

    def test__positive_negative_division(self):
        self.assertEqual(divide(4, -2), -2)

    def test_both_negative_division(self):
        self.assertEqual(divide(-4, -2), 2)

    def test_both_equal(self):
        self.assertEqual(divide(1, 1), 1)

    def test_zero_numerator(self):
        self.assertEqual(divide(1, 2), 0.5)

    def test_division_by_zero(self):
        answer = "Can't divide by zero"
        self.assertEqual(divide(4, 0), answer)

    def test_zero_divided(self):
        self.assertEqual(divide(0, 4), 0)

    def test_both_zero(self):
        answer = "Can't divide by zero"
        self.assertEqual(divide(0, 0), answer)

    def test_first_big(self):
        answer = 10**15
        self.assertEqual(divide(10**16, 10), answer)

    def test_second_big(self):
        answer = 10**-15
        self.assertEqual(divide(10, 10**16), answer)

    def test_both_big(self):
        self.assertEqual(divide(10**16, 10**15), 10)

    def test_first_small(self):
        self.assertAlmostEqual(divide(10**-16, 10), 10**-17, places=10) //

    def test_second_small(self):
        self.assertEqual(divide(10, 10**-16), 10**17)

    def test_both_small(self):
        self.assertAlmostEqual(divide(10**-16, 10**-15), 10**-1, places=10)

    def test_big_and_small(self):
        self.assertAlmostEqual(divide(10**16, 10**-15), 10**31, places=10)

    def test_small_and_big(self):
        self.assertAlmostEqual(divide(10**-16, 10**15), 10**-31, places=10)

    def test_first_fractional(self):
        self.assertEqual(divide(0.5, 2), 0.25)

    def test_second_fractional(self):
        self.assertEqual(divide(2, 0.5), 4)

    def test_both_fractional(self):
        self.assertEqual(divide(0.5, 0.25), 2)

    def test_non_numeric_input(self):
        with self.assertRaises(TypeError):
            divide("a", 5)
        with self.assertRaises(TypeError):
            divide(5, "b")
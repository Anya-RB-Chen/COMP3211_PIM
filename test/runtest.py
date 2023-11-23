import unittest
import coverage

test_dir = './'
discover = unittest.defaultTestLoader.discover(test_dir, pattern='test*.py')

if __name__ == '__main__':
    """ 
    This method is to use coverage API to generate coverage report.
    However, the function header will not be counted as executed line when using this method.
    """
    cov = coverage.coverage()
    cov.start()
    unittest.TextTestRunner().run(discover)
    cov.stop()
    cov.save()
    cov.report()
    cov.html_report(directory='covhtml')
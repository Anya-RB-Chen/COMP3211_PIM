import unittest
import coverage

test_dir = './'
discover = unittest.defaultTestLoader.discover(test_dir, pattern='test*.py')

if __name__ == '__main__':
    cov = coverage.coverage()
    cov.start()
    unittest.TextTestRunner().run(discover)
    cov.stop()
    cov.save()
    cov.report()
    cov.html_report(directory='covhtml')
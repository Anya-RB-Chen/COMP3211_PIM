import unittest
import coverage

test_dir = './'
discover = unittest.defaultTestLoader.discover(test_dir, pattern='test*.py')

if __name__ == '__main__':
    cov = coverage.coverage()
    # 开始分析
    cov.start()
    unittest.TextTestRunner().run(discover)
    # 结束分析
    cov.stop()
    # 结果保存
    cov.save()
    # 命令行模式展示结果
    cov.report()
    # 生成HTML覆盖率报告
    cov.html_report(directory='covhtml')
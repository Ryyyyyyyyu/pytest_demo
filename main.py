import os
import pytest
import time
from common.handle_path import report_path

if __name__ == '__main__':
    # pytest.main(['-sv', '-k', 'testcase'])
    now = time.strftime('%Y.%m.%d-%H_%M_%S-')
    report_dir = now + 'reports'
    report_path = os.path.join(report_path, report_dir)
    print(report_dir, report_path)
    pytest.main(['--alluredir={}'.format(report_path)])
    os.system('allure serve {}'.format(report_path))

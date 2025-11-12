"""
基础测试用例
确保CI/CD流程能够正常运行

注意：这是简化版测试，只验证pytest能正常运行
完整的集成测试需要配置MCP服务器环境
"""

import pytest
import sys
from pathlib import Path


def test_python_version():
    """测试Python版本"""
    assert sys.version_info >= (3, 10), "需要Python 3.10或更高版本"


def test_pytest_working():
    """验证pytest正常工作"""
    assert True, "pytest基本功能正常"


def test_path_exists():
    """测试项目路径存在"""
    current_file = Path(__file__)
    assert current_file.exists(), "测试文件应该存在"
    
    # 测试项目根目录
    project_root = current_file.parent.parent
    assert project_root.exists(), "项目根目录应该存在"


def test_import_pytest():
    """测试pytest模块可导入"""
    import pytest
    assert hasattr(pytest, 'main'), "pytest应该有main函数"


def test_import_standard_lib():
    """测试标准库导入"""
    import json
    import os
    import sys
    
    assert json is not None
    assert os is not None
    assert sys is not None


def test_basic_functionality():
    """测试基本功能"""
    assert 1 + 1 == 2
    assert "test" == "test"
    assert True is True


@pytest.mark.parametrize("input,expected", [
    (1, 1),
    (2, 2),
    (10, 10),
])
def test_parametrized(input, expected):
    """参数化测试示例"""
    assert input == expected


class TestBasicClass:
    """测试类示例"""
    
    def test_method_1(self):
        """测试方法1"""
        assert True
    
    def test_method_2(self):
        """测试方法2"""
        result = [1, 2, 3]
        assert len(result) == 3
        assert 1 in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])



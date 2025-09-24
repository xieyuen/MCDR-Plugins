import unittest
from datetime import datetime
from unittest.mock import mock_open, patch

from migration import SimpleLogger


class TestSimpleLogger(unittest.TestCase):

    def setUp(self):
        # 为所有测试准备一个固定的当前时间
        self.fixed_time = datetime(2023, 1, 1, 12, 0, 0)

    # 测试 __init__ 方法
    def test_init(self):
        """测试初始化方法"""
        logger = SimpleLogger()
        self.assertEqual(logger.format_str, '[{time}] [{level}] {msg}')

    # 测试 __enter__ 方法
    @patch("builtins.open", new_callable=mock_open)
    def test_enter(self, mock_file):
        """测试上下文管理器入口"""
        logger = SimpleLogger()
        with logger as l:
            # 验证返回的是同一个实例
            self.assertIs(logger, l)
            # 验证文件已被打开
            mock_file.assert_called_once_with("migration.log", "w")

    # 测试 __exit__ 方法
    @patch("builtins.open", new_callable=mock_open)
    def test_exit(self, mock_file):
        """测试上下文管理器退出"""
        mock_file_handle = mock_file.return_value
        logger = SimpleLogger()

        with logger:
            pass

        # 验证文件已被关闭
        mock_file_handle.close.assert_called_once()

    # 测试 _log 方法（文件未打开情况）
    @patch('migration.datetime')
    @patch('builtins.print')
    def test_log_without_file(self, mock_print, mock_datetime):
        """测试日志记录方法（无文件）"""
        mock_datetime.now.return_value = self.fixed_time
        logger = SimpleLogger()

        logger._log("测试消息", "INFO")

        expected_output = "[2023-01-01 12:00:00] [INFO] 测试消息"
        mock_print.assert_called_once_with(expected_output)

    # 测试 _log 方法（文件已打开情况）
    @patch('migration.datetime')
    @patch('builtins.print')
    @patch("builtins.open", new_callable=mock_open)
    def test_log_with_file(self, mock_file, mock_print, mock_datetime):
        """测试日志记录方法（有文件）"""
        mock_datetime.now.return_value = self.fixed_time
        mock_file_handle = mock_file.return_value
        logger = SimpleLogger()

        # 手动模拟文件已打开的状态
        logger.log_file = mock_file_handle

        logger._log("测试消息", "INFO")

        expected_output = "[2023-01-01 12:00:00] [INFO] 测试消息"
        # 验证打印调用
        mock_print.assert_called_once_with(expected_output)
        # 验证文件写入调用
        mock_file_handle.write.assert_called_once_with(expected_output + '\n')
        # 验证刷新调用
        mock_file_handle.flush.assert_called_once()

    # 测试 info 方法
    @patch.object(SimpleLogger, '_log')
    def test_info(self, mock_log):
        """测试INFO级别日志"""
        logger = SimpleLogger()
        logger.info("信息消息")
        mock_log.assert_called_once_with("信息消息", "INFO")

    # 测试 warning 方法
    @patch.object(SimpleLogger, '_log')
    def test_warning(self, mock_log):
        """测试WARNING级别日志"""
        logger = SimpleLogger()
        logger.warning("警告消息")
        mock_log.assert_called_once_with("警告消息", "WARNING")

    # 测试 error 方法
    @patch.object(SimpleLogger, '_log')
    def test_error(self, mock_log):
        """测试ERROR级别日志"""
        logger = SimpleLogger()
        logger.error("错误消息")
        mock_log.assert_called_once_with("错误消息", "ERROR")

    # 测试 catch 方法（正常执行路径）
    @patch.object(SimpleLogger, 'error')
    def test_catch_normal_execution(self, mock_error):
        """测试catch装饰器（正常执行）"""
        logger = SimpleLogger()

        @logger.catch
        def normal_function(x, y):
            return x + y

        result = normal_function(1, 2)

        # 验证函数正常执行并返回正确结果
        self.assertEqual(result, 3)
        # 验证没有记录错误
        mock_error.assert_not_called()

    # 测试 catch 方法（异常处理路径）
    @patch.object(SimpleLogger, 'error')
    def test_catch_exception_handling(self, mock_error):
        """测试catch装饰器（异常处理）"""
        logger = SimpleLogger()

        @logger.catch
        def faulty_function():
            raise ValueError("出错了")

        # 验证异常被重新抛出
        with self.assertRaises(ValueError) as context:
            faulty_function()

        self.assertEqual(str(context.exception), "出错了")
        # 验证记录了错误日志
        mock_error.assert_called_once_with("An error occurred: 出错了")


if __name__ == '__main__':
    unittest.main()

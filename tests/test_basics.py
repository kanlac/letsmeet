import unittest
from flask import current_app
from app import create_app, db


class BasicsTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # 测试函数一，确保应用实例存在
    def test_app_exists(self):
        self.assertFalse(current_app is None)

    # 测试函数二，确保使用的是测试配置
    def test_app_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])

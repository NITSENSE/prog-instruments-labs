import unittest
import os

import tudo.controller as controller
import tudo.store as store


class TestTudoMethods(unittest.TestCase):
    """Тесты для функциональности управления задачами."""
    
    def setUp(self):
        """Создает новый экземпляр хранилища для каждого теста."""
        self.store = store.TasksStore("test_db.db")
        self.store.reset()

    def tearDown(self):
        """Удаляет тестовую базу данных после каждого теста."""
        if os.path.exists("test_db.db"):
            os.remove("test_db.db")

    def test_add(self):
        """Тест добавления задачи."""
        controller.add(self.store, ["Do Homework"])
        # self.assertEqual(main.list_tasks()[-1], "Do Homework")
        self.assertTrue(len(controller.list_tasks(self.store)) == 1)

    def test_list(self):
        """Тест получения списка задач."""
        self.assertTrue(len(controller.list_tasks(self.store)) == 0)


if __name__ == "__main__":
    unittest.main()

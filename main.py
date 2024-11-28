from core.Core import Core


class Main:
    """
        Основной класс для запуска приложения
    """
    @staticmethod
    def run():
        try:
            app = Core.openController("home")
            app.main()
        except Exception as e:
            print(str(e))

if __name__ == '__main__':
    Main.run()
import rand
import unittest
from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CONFIG_BASE_URL = 'http://localhost:3000'
PAGE_SIGNIN_URL = f'{CONFIG_BASE_URL}/signin'
PAGE_SIGNUP_URL = f'{CONFIG_BASE_URL}/signup'
PAGE_HOME_URL = f'{CONFIG_BASE_URL}/?page=1'
PAGE_FAVORITES_URL = f'{CONFIG_BASE_URL}/favorites'

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 3)


# @unittest.skip('')
class Authorization(unittest.TestCase):

    def _fill_form_fields(self, email, password):
        self.email_field.clear()
        self.email_field.send_keys(email)
        self.pass_field.send_keys(password)
        # self.submit_btn.click

    def _prepare_form_fields(self):
        self.email_field = driver.find_element(By.NAME, "email")
        self.pass_field = driver.find_element(By.NAME, "password")
        self.submit_btn = driver.find_element(
            By.CSS_SELECTOR, "form [type=submit]")

    # Сетап сайта и подвязка переменных к соответсвующим формам

    @classmethod
    def setUpClass(self):
        print('Тест-Сьют №1: Авторизация \n')
        self.driver = driver
        self.driver.get(PAGE_SIGNIN_URL)

    def setUp(self):
        print('\n\nsetup')
        self.driver.get(PAGE_SIGNIN_URL)
        try:
            wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, "form-wrapper")))
            self._prepare_form_fields()
        except:
            print("The form wasn't initiated properly")

    # Проверка успешной авторизации

    def test_auth(self):
        print('test_auth')
        self._fill_form_fields("super.neyt@yandex.ru", "180175Ilya")
        self.submit_btn.click()
        try:
            wait.until(EC.element_to_be_clickable(
                (By.CLASS_NAME, "header__catalog-link")))
            self.driver.find_element(
                By.CLASS_NAME, "header__catalog-link").click()
            self.assertEqual(self.driver.current_url, PAGE_HOME_URL)
        except:
            print("TimeOut")

    def test_bad_auth_email(self):
        '''
        # Проверка валидации поля "E-Mail" /Неверный формат/
        '''
        print('test_badAuth_eMail')
        self._fill_form_fields("super.neyt@", "180175Ilya")
        self.submit_btn.click()
        try:
            wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, "error")))
            usrErr = self.driver.find_element(By.CLASS_NAME, "error")
            self.assertEqual(usrErr.text, "Invalid email address")
        except:
            print("No errors found!")

    # Проверка валидации поля "E-Mail" /Несуществующий/

    def test_badAuth_eMail_notExist(self):
        print('test_badAuth_eMail_notExist')
        generated_email = rand.generate_random_email(5)
        self._fill_form_fields(generated_email, "180175Ilya")
        self.submit_btn.click()
        try:
            wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, "error")))
            usrErr = self.driver.find_element(By.CLASS_NAME, "error")
            self.assertEqual(usrErr.text, "User with this email not found")
        except:
            print("No errors found!")

    # Проверка валидации поля "Пароль"

    def test_badAuth_pass(self):
        print('test_badAuth_pass')
        self._fill_form_fields("super.neyt@yandex.ru", "180175Ily")
        self.submit_btn.click()
        try:
            wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, "error")))
            usrErr = self.driver.find_element(By.CLASS_NAME, "error")
            self.assertEqual(usrErr.text, "Wrong password")
        except:
            print("No errors found!")

    # Проверка ввода пробела в начале поля "Пароль"

    def test_using_space_in_pass_field(self):
        print("using_space_in_pass_field")
        self._fill_form_fields("super.neyt@yandex.ru", " 180175Ilya")
        self.submit_btn.click()
        self.assertNotEqual(self.driver.current_url, PAGE_HOME_URL)

    # Проверка сохранения данных после перезагрузки страницы

    def test_refresh_page_with_data(self):
        print("test_refreshPage_withData")
        self._fill_form_fields("super.neyt@yandex.ru", "180175Ilya")
        self.driver.refresh()
        try:
            wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, "form-wrapper")))
            self._prepare_form_fields()
            self.submit_btn.click()
        except:
            print("The form wasn't initiated properly")
        try:
            wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, "error")))
            usrErr = self.driver.find_element(By.CLASS_NAME, "error")
            self.assertEqual(usrErr.text, "Required")
        except:
            print("No errors found!")

    # Закрытие браузера после каждой итерации

    def tearDown(self):
        print('tearDown\n')
        # self.driver.close()


# @unittest.skip('')
class Registration(unittest.TestCase):
    '''
    '''

    def _fill_reg_form_fields(self, email, password, passwordRep):
        self.email_field.clear()
        self.email_field.send_keys(email)
        self.pass_field.send_keys(password)
        self.pass_repeat.send_keys(passwordRep)

    def _prepare_reg_form_fields(self):
        self.email_field = driver.find_element(By.NAME, "email")
        self.pass_field = driver.find_element(By.NAME, "password")
        self.pass_repeat = driver.find_element(By.NAME, "passwordRepeat")
        self.submit_btn = driver.find_element(
            By.CSS_SELECTOR, "form [type=submit]")

    @classmethod
    def setUpClass(self):
        print('\n\nТест-Сьют№2: Регистрация \n')
        self.driver = driver
        self.driver.get(PAGE_SIGNIN_URL)

    def setUp(self):
        print('\n\nsetup')
        self.driver = driver
        self.driver.get(PAGE_SIGNUP_URL)
        self.wait = WebDriverWait(driver, 10)
        try:
            wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, "form-wrapper")))
            self._prepare_reg_form_fields()
        except:
            print("The form wasn't initiated properly")

    # Проверка успешной регистрации

    def test_asuccesfull_registration(self):
        print("succesfull_registration")
        self._fill_reg_form_fields(
            rand.generate_random_email(6), "180175Ilya", "180175Ilya")
        self.submit_btn.click()
        try:
            wait.until(EC.element_to_be_clickable(
                (By.CLASS_NAME, "header__catalog-link"))).click()
            self.assertEqual(self.driver.current_url, PAGE_HOME_URL)
        except:
            print("TimeOut")

    # Проверка валидации поля "E-Mail" /Неверный формат/

    def test_bad_registration_wrong_email_format(self):
        print("bad_registration_wrong_email_format")
        self._fill_reg_form_fields(
            rand.generate_random_wrong_email(10), '180175Ilya', "180175Ilya")
        self.submit_btn.click()
        try:
            wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, "error")))
            usrErr = self.driver.find_element(By.CLASS_NAME, "error")
            self.assertEqual(usrErr.text, "Invalid email address")
        except:
            print("No errors found!")

    # Проверка валидации поля "Пароль" /Использовать пробел вначале/

    def test_bad_registration_wrong_pass_space(self):
        print("bad_registration_wrong_pass_space")
        self._fill_reg_form_fields(
            rand.generate_random_email(7), ' 180175Ilya', " 180175Ilya")
        self.submit_btn.click()
        self.assertNotEqual(self.driver.current_url, PAGE_HOME_URL)

        # Проверка валидации поля "Подтверждение пароля" /Использовать другой пароль

    def test_bad_registration_wrong_pass_anotherPass(self):
        print("bad_registration_wrong_pass_anotherPass")
        self._fill_reg_form_fields(
            rand.generate_random_email(8), '180175Ilya', "180175Ily")
        self.submit_btn.click()
        try:
            wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, "error")))
            usrErr = self.driver.find_element(By.CLASS_NAME, "error")
            self.assertEqual(usrErr.text, "Both passwords need to be the same")
        except:
            print("No errors found!")

        # Проверка сохранения данных в полях после перезагрузки страницы с формой

    def test_bad_registration_reload_page_wData(self):
        print("bad_registration_reload_page_wData")
        self._fill_reg_form_fields(
            rand.generate_random_email(5), "180175Ilya", "180175Ilya")
        self.driver.refresh()
        try:
            wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, "form-wrapper")))
            self._prepare_reg_form_fields()
            self.submit_btn.click()
        except:
            print("The form wasn't initiated properly")
        try:
            wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, "error")))
            usrErr = self.driver.find_element(By.CLASS_NAME, "error")
            self.assertEqual(usrErr.text, "Required")
        except:
            print("No errors found!")

    def tearDown(self):
        print('tearDown')


class BookFavorite(unittest.TestCase):

    def _prepare_auth_form_fields(self):
        self.email_field = driver.find_element(By.NAME, "email")
        self.pass_field = driver.find_element(By.NAME, "password")
        self.submit_btn = driver.find_element(
            By.CSS_SELECTOR, "form [type=submit]")

    def _fill_auth_form_fields(self, email, password):
        self.email_field.send_keys(email)
        self.pass_field.send_keys(password)

    @classmethod
    def setUpClass(self):
        print('\n\n Тест-Сьют №3\n')
        self.driver = driver
        self.driver.get(PAGE_SIGNIN_URL)

    def setUp(self):
        print('\n\nsetup')

    def test_adding_a_Favorite_book(self):
        print('adding_a_Favorite_book')
        try:
            wait.until(EC.element_to_be_clickable((By.NAME, "email")))
            self._prepare_auth_form_fields()
            self._fill_auth_form_fields("super.neyt@yandex.ru", "180175Ilya")
            self.submit_btn.click()
        except:
            print("The form wasn't initiated properly")
        try:
            wait.until(EC.element_to_be_clickable(
                (By.CLASS_NAME, 'book__favorite')))
            self.assertEqual(self.driver.current_url, PAGE_HOME_URL)
            # Проверка нажатия кнопки Favorite
            self.driver.find_element(By.CLASS_NAME, "book__favorite").click()
        except:
            print("No books added to Favorite!")
        self.driver.get(PAGE_FAVORITES_URL)
        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "book")))
        except:
            pass

    def test_removing_from_favorites(self):
        print("removing_from_favorites")
        self.driver.get(PAGE_FAVORITES_URL)
        try:
            wait.until(EC.element_to_be_clickable(
                (By.CLASS_NAME, 'book__favorite'))).click()
        except:
            print("Book was not added!")
        try:
            wait.until_not(EC.presence_of_element_located(
                (By.CLASS_NAME, 'book')))
        except:
            print("The book is still here")
        self.driver.refresh
        try:
            wait.until_not(EC.presence_of_element_located(
                (By.CLASS_NAME, 'book')))
        except:
            print("The book is still here")
        with self.assertRaises(NoSuchElementException):
            self.driver.find_element(By.CLASS_NAME, "book")

    def test_zlEAVE_A_COMMENT(self):
        print("LEAVE_A_COMMENT")
        self.driver.get(PAGE_HOME_URL)
        try:
            wait.until(EC.element_to_be_clickable(
                (By.CLASS_NAME, "book__link"))).click()
        except:
            print("Unable to find any books!")
        try:
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "textarea"))).send_keys(
                rand.generate_random_wrong_email(80))
            self.driver.find_element(
                By.CSS_SELECTOR, "form [type=submit]").click()
        except:
            print("Unable to leave a comment!")
        self.driver.find_element(By.CLASS_NAME, "header__catalog-link").click()

    def tearDown(self):
        print("tearDown")
    #################


tc1 = unittest.TestLoader().loadTestsFromTestCase(Authorization)
tc2 = unittest.TestLoader().loadTestsFromTestCase(Registration)
tc3 = unittest.TestLoader().loadTestsFromTestCase(BookFavorite)

signInSuite = unittest.TestSuite(tc1)
signUpSuite = unittest.TestSuite(tc2)
favBook = unittest.TestSuite(tc3)

unittest.TextTestRunner(verbosity=2).run(signInSuite)
unittest.TextTestRunner(verbosity=2).run(signUpSuite)
unittest.TextTestRunner(verbosity=2).run(favBook)

# if __name__ == "__main__":
#   unittest.main()

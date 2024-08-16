import API_test as API
import requests
from time import sleep
import random_file_generator as RFG
import rand
import unittest
from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
print('++++++++++++++++1')
print('++++++++++++++++3')

CONFIG_BASE_URL = 'http://localhost:3000'
API_BASE_URL = 'http://localhost:4000'
PAGE_SIGNIN_URL = f'{CONFIG_BASE_URL}/signin'
PAGE_SIGNUP_URL = f'{CONFIG_BASE_URL}/signup'
PAGE_HOME_URL = f'{CONFIG_BASE_URL}/?page=1'
PAGE_FAVORITES_URL = f'{CONFIG_BASE_URL}/favorites'
USER_PAGE_URL = f'{CONFIG_BASE_URL}/me'
USER_UPLOAD_AVATAR = f'{API_BASE_URL}/user/upload-avatar'
USER_PROFILE_AUTH = f'{API_BASE_URL}/user/1'

token = None
refresh_token = None

second_driver = webdriver.Chrome()
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 3)


@unittest.skip('')
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
            usr_err = self.driver.find_element(By.CLASS_NAME, "error")
            self.assertEqual(usr_err.text, "Invalid email address")
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
            usr_err = self.driver.find_element(By.CLASS_NAME, "error")
            self.assertEqual(usr_err.text, "User with this email not found")
        except:
            print("No errors found!")

    # Проверка валидации поля "Пароль"

    def test_bad_auth_pass(self):
        print('test_badAuth_pass')
        self._fill_form_fields("super.neyt@yandex.ru", "180175Ily")
        self.submit_btn.click()
        try:
            wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, "error")))
            usr_err = self.driver.find_element(By.CLASS_NAME, "error")
            self.assertEqual(usr_err.text, "Wrong password")
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
            usr_err = self.driver.find_element(By.CLASS_NAME, "error")
            self.assertEqual(usr_err.text, "Required")
        except:
            print("No errors found!")

    # Закрытие браузера после каждой итерации

    def tearDown(self):
        print('tearDown\n')
        # self.driver.close()


@unittest.skip('')
class Registration(unittest.TestCase):
    '''
    '''

    def _fill_reg_form_fields(self, email, password, password_rep):
        self.email_field.clear()
        self.email_field.send_keys(email)
        self.pass_field.send_keys(password)
        self.pass_repeat.send_keys(password_rep)

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
            usr_err = self.driver.find_element(By.CLASS_NAME, "error")
            self.assertEqual(usr_err.text, "Invalid email address")
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
            usr_err = self.driver.find_element(By.CLASS_NAME, "error")
            self.assertEqual(
                usr_err.text, "Both passwords need to be the same")
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
            usr_err = self.driver.find_element(By.CLASS_NAME, "error")
            self.assertEqual(usr_err.text, "Required")
        except:
            print("No errors found!")

    def tearDown(self):
        print('tearDown')


class BookFavorite(unittest.TestCase):

    def _initializing_a_sec_driver(self):
        try:
            wait.until(EC.element_to_be_clickable((By.NAME, "email")))
            self._prepare_second_auth_form_fields()
        except:
            print("The form wasn't initiated properly")
        sleep(1)

    def _prepare_second_auth_form_fields(self):
        self.sec_email_field = second_driver.find_element(
            By.NAME, "email").send_keys("super,neyt@yandex.r")
        self.sec_pass_field = second_driver.find_element(
            By.NAME, "password").send_keys("180175Ilya")
        self.sec_submit_btn = second_driver.find_element(
            By.CSS_SELECTOR, "form [type=submit]").click()

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
        self.second_driver = second_driver
        self.second_driver.get("http://localhost:3000/product/1")
        self.driver = driver
        self.driver.get(PAGE_SIGNIN_URL)

    def setUp(self):
        print('\n\nsetup')

    def test_01_adding_a_Favorite_book(self):
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

    def test_02_removing_from_favorites(self):
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

    def test_03_leave_a_comment(self):
        print("LEAVE_A_COMMENT")
        self.driver.get(PAGE_HOME_URL)
        try:
            wait.until(EC.element_to_be_clickable(
                (By.CLASS_NAME, "book__link"))).click()
        except:
            print("Unable to find any books!")
        try:
            wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, "textarea")))
            self.driver.find_element(By.CLASS_NAME, 'textarea').send_keys(
                rand.generate_random_string(15))
            self.driver.find_element(
                By.CSS_SELECTOR, "form [type=submit]").click()
        except Exception as ex:
            print("Unable to leave a comment!", ex)

    def test_04_uploading_a_photo(self):
        print("test_04_uploading_a_photo")
        self.driver.get(USER_PAGE_URL)
        random_photo = RFG.get_a_random_file()
        body = {"email": "super.neyt@yandex.ru", "password": "180175Ilya"}
        response = requests.post(API.BASE_API_SIGNIN, json=body)
        response_json = response.json()
        token = response_json["token"]
        self.response = requests.get(USER_PROFILE_AUTH, headers={
                                     'Authorization': f'Bearer {token}'})
        self.first_result = self.response.json().get(
            "data", {}).get("user", {}).get("avatar")
        print(self.first_result)
        try:
            sabaka = wait.until(EC.element_to_be_clickable((By.ID, 'ava')))
            sabaka.send_keys(random_photo)
            sleep(1)
        except Exception as ex:
            print('pizdec', ex)

        wait.until(EC.element_to_be_clickable((By.ID, 'ava')))
        self.response = requests.get(USER_PROFILE_AUTH, headers={
                                     'Authorization': f'Bearer {token}'})
        self.second_result = self.response.json().get(
            "data", {}).get("user", {}).get("avatar")
        print(self.second_result)
        assert self.first_result != self.second_result
        
        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "Toastify__toast")))
            toast = driver.find_element(By.CLASS_NAME,'Toastify__toast')
        except Exception as ex:
            print('No toasts found!')
        self.assertEqual(toast.text, "Avatar has been updated")
         


    def test_05_trying_to_post_not_a_picture(self):
        self.driver.get(USER_PAGE_URL)
        random_file = RFG.get_a_random_wrong_file()
        
        try:
            sabaka = wait.until(EC.element_to_be_clickable((By.ID, 'ava')))
            sabaka.send_keys(random_file)
            sleep(5)
        except Exception as ex:
            print('pizdec', ex)
        
        try:
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "Toastify__toast")))
            toast = driver.find_element(By.CLASS_NAME,'Toastify__toast')
        except Exception as ex:
            print('No toasts found!')
            
        self.assertEqual(toast.text, "Sorry, we were unable to upload the avatar now...")



    def test_06_check_comment_appearance(self):
        print("test_05_check_comment_appearance")
        self.driver.get('http://localhost:3000/product/1')
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'comments')))
        
        try:
            wait.until(EC.presence_of_element_located(
                (By.CLASS_NAME, 'comments')))
        except Exception as ex:
            print('No comments over here!')
            raise(ex)
        
        find_comments_overall = self.second_driver.find_element(
            By.CLASS_NAME, 'comments')
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'comment')))
        find_comment = find_comments_overall.find_elements(
            By.CLASS_NAME, 'comment')[-1]
        comment_box = find_comment.find_element(By.CLASS_NAME, 'text')
        comment_text = comment_box.text
        try:
            wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "textarea")))
            self.driver.find_element(By.CLASS_NAME, "textarea").send_keys(
                rand.generate_random_string(15))
            self.driver.find_element(
                By.CSS_SELECTOR, "form [type=submit]").click()
        except:
            print("Unable to leave a comment!")
        sleep(0.2)
        second_find_comments_overall = self.second_driver.find_element(
            By.CLASS_NAME, 'comments')
        second_find_comment = second_find_comments_overall.find_elements(
            By.CLASS_NAME, 'comment')[-1]
        second_comment_box = second_find_comment.find_element(
            By.CLASS_NAME, 'text')
        second_comment_text = second_comment_box.text
        sleep(2)
        self.assertNotEqual(comment_text, second_comment_text)

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

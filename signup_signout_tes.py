from multiprocessing.spawn import prepare
import unittest
from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import rand


def getFormElements(self):
  email_field = driver.find_element(By.NAME, "email") 
  pass_field = driver.find_element(By.NAME, "password")
  submit_btn = driver.find_element(By.CSS_SELECTOR, "form [type=submit]")
  sleep(1)
  return email_field, pass_field, submit_btn

driver = webdriver.Chrome()

print("#################Тест-Сьют 1: Проверка формы 'Sign In'#################")

class Authorization(unittest.TestCase):

    
  # def __init__(self, q ) -> None:
  #     super().__init__()
  #     print('q', q)
  #     self.email_field = None
  #     self.pass_field = None
  #     self.submit_btn = None
  #     self.driver = webdriver.Chrome()
  def _fill_form_fields(self, email, password):
    self.email_field.clear()
    self.email_field.send_keys(email)
    self.pass_field.send_keys(password)
    # self.submit_btn.click
    
  
  def _prepare_form_fields(self):
    self.email_field = driver.find_element(By.NAME, "email") 
    self.pass_field = driver.find_element(By.NAME, "password")
    self.submit_btn = driver.find_element(By.CSS_SELECTOR, "form [type=submit]")




  # Сетап сайта и подвязка переменных к соответсвующим формам

  def setUp(self):
    print('\n\nsetup')
    self.driver = driver
    self.driver.get('http://localhost:3000/signin')
    sleep(1.5)
    self._prepare_form_fields()

  #Проверка успешной авторизации

  def test_auth(self):
    print('test_auth')
    self._fill_form_fields("super.neyt@yandex.ru", "180175Ilya")
    self.submit_btn.click()
    sleep(1)
    self.assertEqual(self.driver.current_url, "http://localhost:3000/?page=1")
    self.driver.find_element(By.CLASS_NAME, "header__catalog-link").click()

  # Проверка валидации поля "E-Mail" /Неверный формат/

  def test_badAuth_eMail(self):
    print('test_badAuth_eMail')
    self._fill_form_fields("super.neyt@", "180175Ilya")
    self.submit_btn.click()
    sleep(1)
    usrErr = self.driver.find_element(By.CLASS_NAME,"error")
    self.assertEqual(usrErr.text,"Invalid email address")

  # Проверка валидации поля "E-Mail" /Несуществующий/

  def test_badAuth_eMail_notExist(self):
    print('test_badAuth_eMail_notExist')
    self._fill_form_fields(rand.generate_random_email(5),"180175Ilya")
    self.submit_btn.click()
    sleep(1)
    usrErr = self.driver.find_element(By.CLASS_NAME,"error")
    self.assertEqual(usrErr.text,"User with this email not found")

  # Проверка валидации поля "Пароль"

  def test_badAuth_pass(self):
    print('test_badAuth_pass')
    self._fill_form_fields("super.neyt@yandex.ru", "180175Ily")
    self.submit_btn.click()
    sleep(1)
    usrErr = self.driver.find_element(By.CLASS_NAME,"error")
    self.assertEqual(usrErr.text,"Wrong password")

  # Проверка ввода пробела в начале поля "Пароль"

  def test_using_space_in_pass_field(self):
    print("using_space_in_pass_field")
    self._fill_form_fields("super.neyt@yandex.ru"," 180175Ilya")
    self.submit_btn.click()
    sleep(1)
    usrErr = self.driver.find_element(By.CLASS_NAME,"error")
    self.assertEqual(usrErr.text,"Wrong password")

  # Проверка сохранения данных после перезагрузки страницы


  def test_refreshPage_withData(self):
    print("test_refreshPage_withData")
    self._fill_form_fields("super.neyt@yandex.ru", "180175Ilya")
    self.driver.refresh()
    sleep(0.2)
    self._prepare_form_fields()
    self.submit_btn.click()
    sleep(1)
    self.assertEqual(self.driver.current_url, "http://localhost:3000/signin")


  # Закрытие браузера после каждой итерации

  def tearDown(self):
    print('tearDown')
    # self.driver.close()
  



print('#################Тест-Сьют 2: Проверка формы "Sign Up"#################')



class Registration(unittest.TestCase):


  def _fill_reg_form_fields(self, email, password, passwordRep):
    self.email_field.clear()
    self.email_field.send_keys(email)
    self.pass_field.send_keys(password)
    self.pass_repeat.send_keys(passwordRep)


  def _prepare_reg_form_fields(self):
    self.email_field = driver.find_element(By.NAME, "email") 
    self.pass_field = driver.find_element(By.NAME, "password")
    self.pass_repeat = driver.find_element(By.NAME, "passwordRepeat")
    self.submit_btn = driver.find_element(By.CSS_SELECTOR, "form [type=submit]")


  def setUp(self):
    print('\n\nsetup')
    self.driver = driver
    self.driver.get('http://localhost:3000/signup')
    sleep(1)
    self._prepare_reg_form_fields()
    

  
  # Проверка успешной регистрации
  
  def test_asuccesfull_registration(self):
    print("succesfull_registration")
    self._fill_reg_form_fields(rand.generate_random_email(6),"180175Ilya","180175Ilya")
    self.submit_btn.click()
    sleep(1.5)
    self.assertEqual(driver.current_url,"http://localhost:3000/?page=1")
    logoutButton = driver.find_element(By.CLASS_NAME,"header__catalog-link").click()
    sleep(1)
    

  # Проверка валидации поля "E-Mail" /Неверный формат/

  def test_bad_registration_wrong_email_format(self):
    print("bad_registration_wrong_email_format")
    self._fill_reg_form_fields(rand.generate_random_wrong_email(10),'180175Ilya',"180175Ilya")
    self.submit_btn.click()
    sleep(1.5)
    usrErr = self.driver.find_element(By.CLASS_NAME,"error")
    self.assertEqual(usrErr.text,"Invalid email address")
    

  # Проверка валидации поля "Пароль" /Использовать пробел вначале/

  def test_bad_registration_wrong_pass_space(self):
    print("bad_registration_wrong_pass_space")
    self._fill_reg_form_fields(rand.generate_random_email(7),' 180175Ilya'," 180175Ilya")
    self.submit_btn.click()
    sleep(1.5)
    usrErr = self.driver.find_element(By.CLASS_NAME,"error")
    self.assertEqual(usrErr.text,"Invalid Password")
    

    #Проверка валидации поля "Подтверждение пароля" /Использовать другой пароль


  def test_bad_registration_wrong_pass_anotherPass(self):
    print("bad_registration_wrong_pass_anotherPass")
    self._fill_reg_form_fields(rand.generate_random_email(8),'180175Ilya',"180175Ily")
    self.submit_btn.click()
    sleep(1.5)
    usrErr = self.driver.find_element(By.CLASS_NAME,"error")
    self.assertEqual(usrErr.text,"Both passwords need to be the same")


  def test_bad_registration_reload_page_wData(self):
    print("bad_registration_reload_page_wData")
    self._fill_reg_form_fields(rand.generate_random_email(5), "180175Ilya", "180175Ilya")
    self.driver.refresh()
    sleep(0.2)
    self._prepare_reg_form_fields()
    self.submit_btn.click()
    sleep(1)
    self.assertEqual(self.driver.current_url, "http://localhost:3000/signup")
    usrErr = self.driver.find_element(By.CLASS_NAME,"error")
    self.assertEqual(usrErr.text,"Required")


  def tearDown(self):
    print('tearDown')
    
  
  
  
  #################



if __name__ == "__main__":
  unittest.main()
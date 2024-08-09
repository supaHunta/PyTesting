from multiprocessing.spawn import prepare
import unittest
from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import rand
from selenium.common.exceptions import NoSuchElementException



driver = webdriver.Chrome()



def getFormElements(self):
  email_field = driver.find_element(By.NAME, "email") 
  pass_field = driver.find_element(By.NAME, "password")
  submit_btn = driver.find_element(By.CSS_SELECTOR, "form [type=submit]")
  sleep(1)
  return email_field, pass_field, submit_btn







class BookFavorite(unittest.TestCase):

    

    def _prepare_auth_form_fields(self):
     self.email_field = driver.find_element(By.NAME, "email") 
     self.pass_field = driver.find_element(By.NAME, "password")
     self.submit_btn = driver.find_element(By.CSS_SELECTOR, "form [type=submit]")

    def _fill_Auth_form_fields(self, email, password):
     self.email_field.send_keys(email)
     self.pass_field.send_keys(password)





    def setUp(self):
     print('\n\nsetup')
     self.driver = driver
     self.driver.get('http://localhost:3000/signin')
     sleep(1.5)
     


    def test_adding_a_Favorite_book(self):
     print('adding_a_Favorite_book')
     self._prepare_auth_form_fields()
     sleep(0.2)
     self._fill_Auth_form_fields("super.neyt@yandex.ru", "180175Ilya")
     self.submit_btn.click()
     sleep(1)
     self.assertEqual(self.driver.current_url, "http://localhost:3000/?page=1")
     self.driver.find_element(By.CLASS_NAME, "book__favorite").click()  #Проверка нажатия кнопки Favorite
     sleep(1)
     self.driver.get("http://localhost:3000/favorites")
     sleep(5)
     
    def test_removing_from_favorites(self):
      print("removing_from_favorites")
      self.driver.get("http://localhost:3000/favorites")
      sleep(1)
      self.driver.find_element(By.CLASS_NAME, "book__favorite").click()  #Проверка изъятия из избранного
      sleep(0.2)
      self.driver.refresh
      sleep(3)
      with self.assertRaises(NoSuchElementException):
        self.driver.find_element(By.CLASS_NAME,"book")


    def tearDown(self):
     print("tearDown")


if __name__ == "__main__":
  unittest.main()


















  
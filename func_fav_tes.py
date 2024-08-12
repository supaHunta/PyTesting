from multiprocessing.spawn import prepare
import unittest
from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import rand
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



driver = webdriver.Chrome()
wait = WebDriverWait(driver, 3)


def getFormElements(self):
  email_field = driver.find_element(By.NAME, "email") 
  pass_field = driver.find_element(By.NAME, "password")
  submit_btn = driver.find_element(By.CSS_SELECTOR, "form [type=submit]")
  return email_field, pass_field, submit_btn







class BookFavorite(unittest.TestCase):

    

    def _prepare_auth_form_fields(self):
     self.email_field = driver.find_element(By.NAME, "email") 
     self.pass_field = driver.find_element(By.NAME, "password")
     self.submit_btn = driver.find_element(By.CSS_SELECTOR, "form [type=submit]")

    def _fill_auth_form_fields(self, email, password):
     self.email_field.send_keys(email)
     self.pass_field.send_keys(password)

    @classmethod
    def setUpClass(self):
      print('set all this staff ========================= \n')
      self.driver = driver
      self.driver.get('http://localhost:3000/signin')


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
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'book__favorite')))
        self.assertEqual(self.driver.current_url, "http://localhost:3000/?page=1")
        self.driver.find_element(By.CLASS_NAME, "book__favorite").click()  #Проверка нажатия кнопки Favorite
      except:
        print("No books added to Favorite!")
      self.driver.get("http://localhost:3000/favorites")
      wait.until(EC.presence_of_element_located((By.CLASS_NAME,"book")))
      
     
    def test_removing_from_favorites(self):
      print("removing_from_favorites")
      self.driver.get("http://localhost:3000/favorites")
      try:
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'book__favorite'))).click()
      except:
        print("Book was not added!")
      try:
        wait.until_not(EC.presence_of_element_located((By.CLASS_NAME, 'book')))
      except:
        print("The book is still here")
      self.driver.refresh
      try:
        wait.until_not(EC.presence_of_element_located((By.CLASS_NAME, 'book')))
      except:
        print("The book is still here")
      with self.assertRaises(NoSuchElementException):
        self.driver.find_element(By.CLASS_NAME,"book")
      


    def test_zlEAVE_A_COMMENT(self):
      print("LEAVE_A_COMMENT")
      self.driver.get("http://localhost:3000/?page=1")
      try:
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "book__link"))).click()
      except:
        print("Unable to find any books!")
      try:
        wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "textarea"))).send_keys(rand.generate_random_wrong_email(80))
        self.driver.find_element(By.CSS_SELECTOR, "form [type=submit]").click()
      except:
        print("Unable to leave a comment!")
      self.driver.find_element(By.CLASS_NAME, "header__catalog-link").click()


    def tearDown(self):
     print("tearDown")


if __name__ == "__main__":
  unittest.main()


















  
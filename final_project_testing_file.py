from final_project_working_file import *
import unittest

class TestScrap(unittest.TestCase):
    def test_destination_lst(self):
        self.assertIsNotNone(destination_name_lst)

    def test_destination_lst_num(self):
        self.assertEqual(len(destination_name_lst), 25)

    def test_destination_lst_value(self):
        self.assertIn("Paris, France", destination_name_lst)
        self.assertIn("Sydney, Australia", destination_name_lst)
        self.assertNotIn("Musee d'Orsay", destination_name_lst)


    def test_city_lst(self):
        self.assertIsNotNone(city_name_lst)

    def test_destination_lst_num(self):
        self.assertEqual(len(city_name_lst), 25)

    def test_destination_lst_value(self):
        self.assertIn("Paris", city_name_lst)
        self.assertIn("London", city_name_lst)
        self.assertNotIn("France", city_name_lst)


class TestApi(unittest.TestCase):
    def setUp(self):
        self.home_city = "Boston"
        self.destination_city = "New York City"

    def test_return_code_for_city(self):
        self.assertEqual(CityInfo(self.home_city).return_code_for_city(), "BOS-sky")
        self.assertEqual(CityInfo(self.destination_city).return_code_for_city(), "JFK-sky")

    def test_return_airport_name(self):
        self.assertEqual(CityInfo(self.home_city).return_airport_name(), "Boston Logan International")
        self.assertEqual(CityInfo(self.destination_city).return_airport_name(), "New York John F. Kennedy")

    def test_return_date_price(self):
        self.assertIsNotNone(SkyscannerApiInput(self.home_city,self.destination_city).return_date_price())
        self.assertEqual(type(SkyscannerApiInput(self.home_city,self.destination_city).return_date_price()), type({}))

    def test_return_date_price_value(self):
        for value in SkyscannerApiInput(self.home_city,self.destination_city).return_date_price().values():
            self.assertEqual(type(value), type(float()))

    def test_sort_lowest_price(self):
        self.assertEqual(type(sort_lowest_price(SkyscannerApiInput(self.home_city,self.destination_city).return_date_price())), type(""))


    def test_get_gps_for_airport(self):
        self.assertEqual(type(get_gps_for_airport("Boston Logan International")), type(""))

    def test_get_gps_for_airport_value(self):
        self.assertEqual(get_gps_for_airport("Boston Logan International"), "42.3656132,-71.0095602")


class TestMapping(unittest.TestCase):
    def setUp(self):
        self.home_city = "Boston"
        self.destination_city = "New York City"

    def test_plot_sites_for_cities(self):
        try:
            plot_sites_for_cities(self.home_city,self.destination_city)
        except:
            self.fail()



if __name__ == '__main__':
    unittest.main()

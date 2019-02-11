from django.core.management.base import BaseCommand
from website.models import City
from bs4 import BeautifulSoup
from mechanize import Browser


class Command(BaseCommand):
    help = 'Imports the top 100 US Cities into database'

    def handle(self, *args, **options):
        mech = Browser()
        url = "https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population"
        page = mech.open(url)
        html = page.read()
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find_all("table", {"class":"wikitable"})[1]
        if table is None:
            self.stderr.write("Unable to find table")
        City.objects.all().delete()

        for row in table.tbody.find_all("tr")[1:101]:
            city = row.find_all("td")[1].text
            index = city.find("[")
            if index != -1:
                city = city[0:index]
            new_city = City(name=city)
            new_city.save()
        self.stdout.write("Successfully added cities")

import pywikibot

class SearchEngine:

    def __init__(self, site='wikipedia', lang='en'):
        """
        Creates an instance of the SearchEngine object to search a given site for specific pages
        :param site (optional): The name (or link) to a given website. Pass url if site is other than Wikipedia
        :param lang (optional): The language to be used by the SearchEngine on the given site
        """

        self.lang = lang
        self.site = site
        self.source = pywikibot.Site(lang, site)


    # To get a single page, do search("searchterm", 1, 'nearmatch')
    def search(self, keyterm:str, max_pages_grabbed=-1, search_by='title'):
        """
        Searches a site for pages based on a given keyterm
        :param keyterm: A string that we want to search for on the site in order to receive relevant pages
        :param max_pages_grabbed (optional): The maximum number of pages to be returned
        :param search_by (optional): Pages can either searched by "title", "text", or "nearmatch". The "title" search is best for finding pages with a similar title
        :return: A list of pywikibot.Page objects corresponding to the found pages
        """
        pageList = []
        #Namespaces[0] searches all Wikipedia pages (there are other namespaces such as PageFiles that we do not want to search)
        page_generator = self.source.search(keyterm, where=search_by, namespaces=[0])
        page_generator.set_maximum_items(max_pages_grabbed)
        for page in page_generator:
            pageList.append(page)
        return pageList

    def getByPageID(self, page_ids:[]):
        """
        Searches a site for a page based on the page_id
        :param page_id: An integer corresponding to the page_id of the provided page
        :return: A pywikibot.Page object corresponding to provided page_id
        """
        #page_generator = self.source.load_pages_from_pageids(page_ids)
        #print(list(page_generator))
        raise NotImplementedError


    def getByCategory(self, category:str):
        """
        Creates list of pages from one category on a site
        :param category: A string corresponding to a page category
        :return: A list of pywikibot.Page objects corresponding to the given category
        """
        categoryPage = pywikibot.Category(self.source, title=category)
        return categoryPage.articles()


    def pullMultipleCategories(self, categories:[]):
        """
        Creates list of pages from multiple categories
        :param categories: List of page categories on a site
        :return: A list of lists that each contain pywikibot.Page objects corresponding to each category
        """
        pageList = []
        for category in categories:
            pageList.append(list(self.getByCategory(category)))
        return pageList

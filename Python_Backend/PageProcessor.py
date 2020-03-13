import pywikibot, mwparserfromhell
import RevisionPuller as RP
import SearchEngine as SE

class PageProcessor:


    def getSections(self, page:pywikibot.page.Page, headers=None, flat=True):
        """[summary]
        
        Arguments:
            page {pywikibot.page.Page} -- [description]
            headers {list of strings} -- Only extracts sections with specified headers. None extracts all the sections. 
            We also add edit term as many old articles has the word in headers. Users should add the synonyms.
            flat {boolean} -- flattens the sections.
        """

        text = page.text
        wikiCode = mwparserfromhell.parse(text)

        if headers is None:
            sections = wikiCode.get_sections(include_headings=True, flat=flat)
        else:
            headers_edit = [i + 'Edit' for i in headers]
            #then merge those two lists together
            all_possibles = headers + headers_edit
            headersRegex = '|'.join(all_possibles)
            sections = wikiCode.get_sections(matches=headersRegex, include_headings=True, flat=flat)
    
        return sections
    

    def naiveStrip(self, wikiCode:mwparserfromhell.wikicode.Wikicode):
        """removes the code delimiter, keeps the text. Accepts pages and sections in Wikicode format
        
        Arguments:
            wikiCode {mwparserfromhell.wikicode.Wikicode} -- wikicode for a page or a section.
        """
        return wikiCode.strip_code()

    def getReadableText(self, wikiText:str):
        """ Performs a naiveStrip on a string of wikiText and then passes the text through mwparserfromhell
        to be returned

        :param wikiText: A string containing WikiText
        :return: A string of the parsed text
        """
        wikiCode = mwparserfromhell.parse(wikiText)
        return self.naiveStrip(wikiCode)

    def getLeadSection(self, page:pywikibot.page.Page):
        raise NotImplementedError

    def getInfoBox(self, page:pywikibot.page.Page):
        raise NotImplementedError

    def getCategories(self, page:pywikibot.page.Page):
        raise NotImplementedError
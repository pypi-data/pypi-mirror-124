"""Google api class.
"""

import time
import json
import urllib

from datahunters.shared.selenium_scraper import SeleniumScraper
from datahunters.search.common import ImgSearchResult


class GoogleSearchAPI(SeleniumScraper):
  """Class for google image search api.
  """
  base_url = "https://www.google.com/search"

  def __init__(self, use_headless=True):
    super().__init__(use_headless)
    print("Google image api initialized")

  def convert_elem_to_obj(self, img_elem):
    """Convert page element to image object.
    """
    cur_res = ImgSearchResult()
    # check thumbnail link.
    src_val = img_elem.get_attribute("src")
    if src_val is not None:
      link = urllib.parse.unquote(src_val)
      cur_res.thumbnail_url = link
    else:
      src_val = img_elem.get_attribute("data-src")
      if src_val:
        cur_res.thumbnail_url = src_val
    # load image detail page.
    img_elem.click()
    time.sleep(0.5)
    elems = self.find_elements("a[rlhc] > img.n3VNCb")
    for elem in elems:
      link = elem.get_attribute("src")
      if link and "http" in link:
        cur_res.img_url = link
        break
    # cur_res.img_url = link[link.find("imgurl=") +
    #                        7:link.find("&imgrefurl")].rstrip(".")
    return cur_res

  def img_search(self, keywords, get_all=False):
    """Collect images from google search results.

    Args:
      keywords: search input.
      item_num: number of items to retrieve.
      get_all: if get all available results or just first page.

    Returns:
      list of image items.
    """
    all_res = []
    try:
      startt = time.time()
      print("start scraping '{}' using Google".format(keywords))
      formatted_keywords = keywords.strip().replace(" ", "+")
      req_url = "{}?q={}&source=lnms&tbm=isch&sa=X&ei=0eZEVbj3IJG5uATalICQAQ&ved=0CAcQ_AUoAQ&biw=939&bih=591".format(
          self.base_url, formatted_keywords)
      print(req_url)
      # check default page.
      print("checking default data")
      if not get_all:
        self.visit_url(req_url, "img.Q4LuWd")
        elems = self.find_elements("img.Q4LuWd")
      else:
        elems = self.scrape_inf_scroll(req_url,
                                       "img.Q4LuWd",
                                       None,
                                       load_btn_selector="input#smb")
      print("total fetched items: {}".format(len(elems)))
      for elem in elems:
        try:
          cur_res = self.convert_elem_to_obj(elem)
          if cur_res:
            all_res.append(cur_res)
        except Exception as ex:
          print("error in processing item: {}".format(ex))
          continue
      print(
          "Google image scraping finished: time cost: {}s".format(time.time() -
                                                                  startt))
      return all_res
    except Exception as ex:
      print("error in Google image scraper: {}".format(ex))
      return all_res


if __name__ == "__main__":
  engine = GoogleSearchAPI()
  all_imgs = engine.img_search("cats", True)
  print(len(all_imgs))
  img_json = [x.to_json() for x in all_imgs]
  with open("./samples.json", "w") as f:
    json.dump(img_json, f)
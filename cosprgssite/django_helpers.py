__author__ = "Jeremy Nelson"
import json,sys
from Friends.models import *
from location.models import Address
from django.contrib.auth.models import User
import settings,datetime
from docutils.core import publish_string
from bs4 import BeautifulSoup
import os,sys,re

advice_re = re.compile(r"advice")
biz_re = re.compile(r"business")
finance_re = re.compile(r"finance")
house_re = re.compile(r"house|home")
mo_re = re.compile(r"ministry")
nominating_re = re.compile(r"nominating")
special_re = re.compile(r"special|called")
query_re = re.compile(r"query|queries")


def associate_addresses(addresses_filename):
    print("Associate addresses with Friends")
    addr_json = json.load(open(addresses_filename,'r'))
    for row in addr_json:
        try:
            addr_query = Address.objects.filter(md5_key=row["addr"])
            addr = addr_query[0]
            friends = get_friends(row["friends"])
            for friend in friends:
                friend.address = addr
                friend.save()
                print("\t{0} address set to {1}, {2}".format(friend.short_name,
                                                             addr.street,
                                                             addr.city))
        except:
            print("Failed assocication for {0}, error={1}".format(row,
                                                                  sys.exc_info()[0]))
    print("Finished associating addresses with Friends")


def associate_categories(categories_filename):
    print("Associate categories with Friends")
    categories_json = json.load(open(categories_filename,'r'))
    for row in categories_json:
        new_category = FriendCategory(code=row["code"],
                                      label=row["label"])
        new_category.save()
        new_category.friends = get_friends(row["friends"])
        new_category.save()
    print("Finished associating categories")

def build_loader(year_loader,directory):
    month_walker = os.walk(directory)
    next(month_walker)
    for row in month_walker:
        path,filenames = row[0],row[2]
        month = os.path.split(path)[1]
        year_loader[month] = {"meetings":dict(),
                              "committees":dict()}
        for filename in filenames:
            raw_file = open(os.path.join(path,filename),'rb')
            raw_rst = raw_file.read()
            raw_file.close()
            print("Trying to load {0}{1}".format(path,filename))
            rst_contents = publish_string(raw_rst,
                                          writer_name="html")
            rst_soup = BeautifulSoup(rst_contents)
            main_contents = rst_soup.find("div",attrs={"class":"document"})
            meta_date = rst_soup.find("meta",attrs={"name":"date"})
            if meta_date is not None:
                rst_date = datetime.datetime.strptime(meta_date.attrs["content"],"%Y-%m-%d")
            else:
                print("MISSING Date {0}".format(meta_date))
            rst_category = guess_rst(filename)
            pretty_html = main_contents.prettify()
            if rst_category.has_key("meeting"):
                year_loader[month]['meetings'][rst_category.get("meeting")] = {"html":pretty_html,
                                                                               "date":rst_date}
            if rst_category.has_key("committee"):
                year_loader[month]['committees'][rst_category.get("committee")] = {"html":pretty_html,
                                                                                   "date":rst_date}
    return year_loader
    
def get_friends(friend_keys):
    friends = []
    for friend_key in friend_keys:
        try:
            friend_query = Friend.objects.filter(md5_key=friend_key)
            friends.append(friend_query[0])
        except:
            print("Failed to retrieve friend md5={0} from datastore\n\tError {1}".format(friend_key,
                                                                                         sys.exc_info()[0]))
    return friends

def guess_rst(filename):
    query = filename.lower()
    advice_result = advice_re.search(query)
    if advice_result is not None:
        return {"meeting":"advice"}
    business_meeting_result = biz_re.search(query)
    if business_meeting_result is not None:
        return {"meeting":"business"}
    fiance_committee_result = finance_re.search(query)
    if fiance_committee_result is not None:
        return {"committee":"finance"}
    house_result = house_re.search(query)
    if house_result is not None:
        return {"committee":"meetinghouse"}
    ministry_oversight_result = mo_re.search(query)
    if ministry_oversight_result is not None:
        return {"committee":"ministryandoversight"}
    nominating_result = nominating_re.search(query)
    if nominating_result is not None:
        return {"committee":"nominating"}
    query_result = query_re.search(query)
    if query_result is not None:
        return {"meeting":"query"}
    special_result = special_re.search(query)
    if special_result is not None:
        return {"meeting":"special"}
    return {}



def load_base(ADDR_JSON,CATEGORY_JSON):
    associate_addresses(ADDR_JSON)
    associate_categories(CATEGORY_JSON)
    # Sets admin to correct values
    jeremy = User.objects.get(pk=1)
    jeremy.first_name = 'Jeremy'
    jeremy.last_name = 'Nelson'
    jeremy.save()

def load_windows():
    ADDR_JSON = 'H:\\jermsmemory\\ColoradoSpringsMeeting\\2012\\friend-addresses.json'
    CATEGORY_JSON = 'H:\\jermsmemory\\ColoradoSpringsMeeting\\2012\\friend-categories.json'
    load_base(ADDR_JSON,CATEGORY_JSON)

def load_linux():
    ADDR_JSON = '/home/jpnelson/jermsmemory/ColoradoSpringsMeeting/2012/friend-addresses.json'
    CATEGORY_JSON = '/home/jpnelson/jermsmemory/ColoradoSpringsMeeting/2012/friend-categories.json'
    load_base(ADDR_JSON,CATEGORY_JSON)



def get_year(year):
    year_path = os.path.join(settings.PROJECTBASE_DIR,year)
    if os.path.exists(year_path):
        return build_loader(dict(),year_path)
    
if __name__ == '__main__':
    pass

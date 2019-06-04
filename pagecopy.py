# -*- coding: utf-8 -*-
# Make sure you rename config.py.example to config.py and fill it out before trying to run this!
# Get our config variables.
import config
# Used to be a nice API user. Max 240 req/min.
from time import sleep
# Used to talk to the wikidot API.
from xmlrpclib import ServerProxy
# used to check arguments for performing various jobs
from sys import argv

if "--help" in argv or len(argv) == 1:
    print "Usage: pagecopy.py sluglist"
    print "sluglist is a list of page slugs, with no spaces, separated with commas"

else:
    # Let's make our connection to Wikidot.
    s = ServerProxy(
        'https://' + config.wikidot_username + ':' + config.wikidot_api_key + "@www.wikidot.com/xml-rpc-api.php")

    slugs = argv[1]
    sluglist = slugs.split(",")
    for article in sluglist:
        # Get the actual page content and full metadata set.
        print "Pulling " + article
        page = s.pages.get_one({"site": config.wikidot_site, "page": article})
        # Obey the speed limit.
        sleep(0.25)
        print "Saving page to wikidot."
        newpage = s.pages.save_one({"site": config.cafe_site, "page": page["fullname"], "title": page["title_shown"],
                                    "content": page["content"], "tags": page["tags"]})
        sleep(0.25)
        print "Getting list of files associated with " + article + "."
        oldfiles = s.files.select({"site": config.wikidot_site, "page": page["fullname"]})
        sleep(0.25)
        for filename in oldfiles:
            print "Getting " + filename + "."
            attachment = s.files.get_one({"site": config.wikidot_site, "page": page["fullname"], "file": filename})
            sleep(0.25)
            print "Uploading " + filename + " to cafe wiki."
            upload = s.files.save_one(
                {"site": config.cafe_site, "page": page["fullname"], "file": filename, "content": attachment["content"],
                 "comment": attachment["comment"], "revision_comment": "Uploaded with cafetools."})
            sleep(0.25)

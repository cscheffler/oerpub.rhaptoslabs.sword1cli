"""
Command line client using SWORD version 1 to push content to
Connexions.

Author: Carl Scheffler
Copyright (C) 2011 Katherine Fletcher.

Funding was provided by The Shuttleworth Foundation as part of the OER
Roadmap Project.

If the license this software is distributed under is not suitable for
your purposes, you may contact the copyright holder through
oer-roadmap-discuss@googlegroups.com to discuss different licensing
terms.

This file is part of oerpub.rhaptoslabs.sword1cli

Sword1CLI is free software: you can redistribute it and/or modify it
under the terms of the GNU Lesser General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Sword1CLI is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with Sword1Cnx.  If not, see <http://www.gnu.org/licenses/>.
"""
from __future__ import division
import oerpub.rhaptoslabs import sword1cnx
import os

PARAMS = {
    'username': raw_input("Enter Connexions username: "),
    'password': raw_input("Enter Connexions password: "),
}

print 'Retrieving service document...'
conn = sword1cnx.Connection("http://cnx.org/sword",
                            user_name=PARAMS['username'],
                            user_pass=PARAMS['password'],
                            download_service_document=True)

swordCollections = sword1cnx.parse_service_document(conn.sd)

formFields = {
    "url":          None,
    "title":        None,
    "abstract":     None,
    "keywords":     None,
    "language":     "en",
    "keepUrl":      True,
    "keepTitle":    False,
    "keepAbstract": False,
    "keepKeywords": True,
}

print 'Deposit location:'
for i in range(len(swordCollections)):
    print ' %i. %s [%s]'%(i+1, swordCollections[i]['title'],
                          swordCollections[i]['url'])
formFields['url'] = swordCollections[int(raw_input())-1]['url']

formFields['title'] = raw_input('Title: ').strip()
formFields['abstract'] = raw_input('Summary: ').strip()
formFields['keywords'] = raw_input('Keywords (comma-separated): ')
formFields['language'] = raw_input('Language code: ').strip()

filenames = []
while True:
    filenames.append(raw_input('Files to upload (empty to stop): '))
    if filenames[-1] == '':
        del filenames[-1]
        break

# Send zip file to SWORD interface
print 'Posting new module to Connexions...'
conn = sword1cnx.Connection(formFields['url'],
                            user_name=PARAMS['username'],
                            user_pass=PARAMS['password'],
                            download_service_document=False)
response = sword1cnx.upload_multipart(
    conn, formFields['title'], formFields['abstract'], formFields['language'],
    ",".split(formFields['keywords']), [{os.path.basename(filename): open(filename,'rb')} for filename in filenames])

print 'Response:'
print response

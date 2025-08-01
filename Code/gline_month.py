import sqlite3
import time
import zlib

conn = sqlite3.connect('index.sqlite')
cur = conn.cursor()

cur.execute('SELECT id, sender FROM Senders')
senders = dict()
for message_row in cur :
    senders[message_row[0]] = message_row[1]

cur.execute('SELECT id, guid,sender_id,subject_id,sent_at FROM Messages')
messages = dict()
for message_row in cur :
    messages[message_row[0]] = (message_row[1],message_row[2],message_row[3],message_row[4])

print("Loaded messages=",len(messages),"senders=",len(senders))

sendorgs = dict()
for (message_id, message) in list(messages.items()):
    sender = message[1]
    pieces = senders[sender].split("@")
    if len(pieces) != 2 : continue
    dns = pieces[1]
    sendorgs[dns] = sendorgs.get(dns,0) + 1

# pick the top schools
orgs = sorted(sendorgs, key=sendorgs.get, reverse=True)
orgs = orgs[:10]
print("Top 10 Oranizations")
print(orgs)

counts = dict()
years = list()
# cur.execute('SELECT id, guid,sender_id,subject_id,sent_at FROM Messages')
for (message_id, message) in list(messages.items()):
    sender = message[1]
    pieces = senders[sender].split("@")
    if len(pieces) != 2 : continue
    dns = pieces[1]
    if dns not in orgs : continue
    year = message[3][:4]
    if year not in years : years.append(year)
    key = (year, dns)
    counts[key] = counts.get(key,0) + 1

years.sort()
# print counts
# print months

fhand = open('gline_month.js','w')
fhand.write("gline_month = [ ['Year'")
for org in orgs:
    fhand.write(",'"+org+"'")
fhand.write("]")

for year in years:
    fhand.write(",\n['"+year+"'")
    for org in orgs:
        key = (year, org)
        val = counts.get(key,0)
        fhand.write(","+str(val))
    fhand.write("]");

fhand.write("\n];\n")
fhand.close()

print("Output written to gline_month.js")
print("Open gline_month.htm to visualize the data")

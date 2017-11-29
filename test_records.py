import chemdataextractor
import ast
import pprint

#Loads the document from 'filepath'
html = "C2CP23894B.html"
print(html + " is being extracted for debugging.")
filepath = "TestingDocuments/" + html

#Run document through chemdataextractor
doc = chemdataextractor.Document.from_file(open(filepath, "rb"))
print("Loaded doc correctly. Proceeding to retrieve records...")
records = doc.records.serialize()

#Writes results to 'debug.txt'
print("Records retrieved successfully")
pp = pprint.PrettyPrinter(indent=2)
json = ast.literal_eval(str(records))
with open("debug.txt", "w") as f:
    f.write(pp.pformat(json))




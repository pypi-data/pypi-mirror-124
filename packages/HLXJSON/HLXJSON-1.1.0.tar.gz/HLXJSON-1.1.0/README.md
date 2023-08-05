# HLXJSON
Easily read and write JSON files in Python!
examples:
```
import hlxjson
hlxjson.start("test.json")
hlxjson.add("test.json","testname","testval")
hlxjson.divstart("test.json","testdiv")
hlxjson.add("test.json","testname","testval")
hlxjson.divend("test.json","testdiv")
hlxjson.add("test.json","testnameAfterADiv","testval")
hlxjson.end("test.json")
hlxjson.readdiv("test.json","testdiv","testnameindiv")
hlxjson.read("test.json","testproperty")
```
meanwhile test.json :
```
{ 
"testname":"testval",
"testdiv":{ 
"testnameindiv":"testvalindiv",
},
"testnameAfterADiv":"testvalafterduv",
}
```

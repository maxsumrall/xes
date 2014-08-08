__author__ = 'Jonathan Sumrall'

class XESDocument():
    def __init__(self):
        self.header = """<?xml version="1.0" encoding="UTF-8" ?>
<!-- This file has been generated with the OpenXES library. It conforms -->
<!-- to the XML serialization of the XES standard for log storage and -->
<!-- management. -->
<!-- XES standard version: 1.0 -->
<!-- OpenXES library version: 1.0RC7 -->
<!-- OpenXES is available from http://www.openxes.org/ -->
<log xes.version="1.0" xes.features="nested-attributes" openxes.version="1.0RC7" xmlns="http://www.xes-standard.org/">
	<extension name="Lifecycle" prefix="lifecycle" uri="http://www.xes-standard.org/lifecycle.xesext"/>
	<extension name="Organizational" prefix="org" uri="http://www.xes-standard.org/org.xesext"/>
	<extension name="Time" prefix="time" uri="http://www.xes-standard.org/time.xesext"/>
	<extension name="Concept" prefix="concept" uri="http://www.xes-standard.org/concept.xesext"/>
	<extension name="Semantic" prefix="semantic" uri="http://www.xes-standard.org/semantic.xesext"/>
	<global scope="trace">
		<string key="concept:name" value="__INVALID__"/>
	</global>
	<global scope="event">
		<string key="concept:name" value="__INVALID__"/>
		<string key="lifecycle:transition" value="complete"/>
	</global>
	"""
        self.footer = "\n</log>"
        self.attributes = []
        self.traces = []

    def addAttribute(self, attr):
        self.attributes.append(attr)

    def addTrace(self, trace):
        self.traces.append(trace)

    def toXES(self):
        xes = ""
        xes += self.header
        for attribute in self.attributes:
            xes += attribute.toXES() + "\n"
        for trace in self.traces:
            xes += trace.toXES() + "\n"
        xes += self.footer

        return xes
    def __str__(self):
        return self.toXES()



class Event():
    def __init__(self):
        self.attributes = []

    def addAttribute(self, attr):
        self.attributes.append(attr)
        return self

    def toXES(self):
        xes = "\t<event>\n"
        for attr in self.attributes:
            xes += "\t\t" + attr.toXES() + "\n"
        xes += "\t</event>"
        return xes
    def __str__(self):
        return self.toXES()


class Attribute():
    def __init__(self, type="not set", key="not set", value="not set"):
        self.type = str(type)
        self.key = str(key)
        self.value = str(value)

    def toXES(self):
        xes = "<" + self.type + " key=\"" + self.key + "\" value= \"" + self.value + "\"/>"
        return xes
    def __str__(self):
        return self.toXES()


class Trace():
    def __init__(self):
        self.events = []
        self.attributes = []

    def addAttribute(self, attr):
        self.attributes.append(attr)

    def addEvent(self, event):
        self.events.append(event)

    def toXES(self):
        xes = "<trace>\n"
        for attr in self.attributes:
            xes += attr.toXES() + "\n"
        for event in self.events:
            xes = xes + event.toXES() + "\n"
        xes += "</trace>"
        return xes
    def __str__(self):
        return self.toXES()


def main():
    doc = XESDocument()

    trace1 = Trace()
    trace1.addAttribute(Attribute("string","concept:name", "1"))
    trace1.addEvent(Event().addAttribute(Attribute("string", "org:resource","Rose")))
    trace1.addEvent(Event().addAttribute(Attribute("string","lifecycle:transition","start")))

    trace2 = Trace()
    trace2.addAttribute(Attribute("string", "concept:name", "2"))
    trace2.addEvent(Event().addAttribute(Attribute("string", "org:resource","Bob")))
    trace2.addEvent(Event().addAttribute(Attribute("string","lifecycle:transition","start")))

    doc.addAttribute(Attribute("something", "or", "other"))
    doc.addTrace(trace1)
    doc.addTrace(trace2)

    print doc





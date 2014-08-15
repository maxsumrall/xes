__author__ = 'Jonathan Sumrall'
import xml.etree.ElementTree as ET
from xml.dom import minidom

class Log():
    """ An XES log class for adding traces to.
    """
    def __init__(self):
        self.CREATOR = "Python XES v1.2"
        self.log = ET.Element("log")
        self.log.set("xes.version", "1.0")
        self.log.set("xmlns", "http://www.xes-standard.org")
        self.log.set("xes.creator", self.CREATOR)

        self.attributes = []
        self.traces = []
        self.extensions = []
        self.classifiers = []
        self.global_event_attributes = []
        self.global_trace_attributes = []
        self.infer_global_attributes = True
        self.use_default_extensions = True


    def add_global_event_attribute(self, attr):
        self.global_event_attributes.append(attr)

    def add_global_trace_attributes(self, attr):
        self.global_trace_attributes.append(attr)

    def add_attribute(self, attr):
        if isinstance(attr, Attribute):
            self.attributes.append(attr)

    def add_trace(self, trace):
        if isinstance(trace, Trace):
            self.traces.append(trace)

    def add_extension(self, extension):
        if isinstance(extension, Extension):
            self.extensions.append(extension)

    def add_default_extensions(self):
        self.extensions = [
            Extension(name="Concept",
                      prefix="concept",
                      uri="http://www.xes-standard.org/concept.xesext"),
	        Extension(name="Lifecycle",
                      prefix="lifecycle",
                      uri="http://www.xes-standard.org/lifecycle.xesext"),
	        Extension(name="Time",
                      prefix="time",
                      uri="http://www.xes-standard.org/time.xesext"),
	        Extension(name="Organizational",
                      prefix="org",
                      uri="http://www.xes-standard.org/org.xesext")
        ]

    def infer_attributes(self):
        for trace in self.traces:
            for attr in trace.attributes:
                contained = False
                for global_attr in self.global_trace_attributes:
                    if attr.key == global_attr.key:
                        contained = True
                if not contained:
                    self.add_global_trace_attributes(
                        Attribute(type=attr.type, key=attr.key, value="string")
                    )
            for event in trace.events:
                for attr in event.attributes:
                    contained = False
                    for global_attr in self.global_event_attributes:
                        if attr.key == global_attr.key:
                            contained = True
                    if not contained:
                        self.add_global_event_attribute(
                            Attribute(type=attr.type, key=attr.key, value="string")
                        )

    def build_log(self):
        if len(self.classifiers) == 0:
            print "XES Warning! Classifiers not set. \n"

        if self.infer_global_attributes:
            self.infer_attributes()

        if self.use_default_extensions:
            self.add_default_extensions()

        for extension in self.extensions:
            self.log.append(extension.xml)

        globalTraceElement = ET.SubElement(self.log, "global")
        globalTraceElement.set("scope", "trace")
        for attr in self.global_trace_attributes:
            globalTraceElement.append(attr.xml)

        globalEventElement = ET.SubElement(self.log, "global")
        globalEventElement.set("scope", "event")
        for attr in self.global_event_attributes:
            globalEventElement.append(attr.xml)

        for classifier in self.classifiers:
            self.log.append(classifier.xml)

        self.attributes.append(Attribute(type="string", key="creator", value=self.CREATOR))
        for attr in self.attributes:
            self.log.append(attr.xml)


        for trace in self.traces:
            for event in trace.events:
                event.build_event()
            trace.build_trace()
            self.log.append(trace.xml)


    def __str__(self):
        self.build_log()
        stuff = minidom.parseString(ET.tostring(self.log, "utf-8"))
        c1 = stuff.createComment("Created by Python XES https://pypi.python.org/pypi/xes")
        c2 = stuff.createComment("(c) Jonathan Sumrall - http://www.sumrall.nl")
        stuff.insertBefore(c2,stuff.childNodes[0])
        stuff.insertBefore(c1,stuff.childNodes[0])

        return stuff.toprettyxml("  ")
class Event():
    """
    An event class. Add attributes to an event.
    """
    def __init__(self):
        self.xml = ET.Element("event")
        self.attributes = []

    def add_attribute(self, attr):
        self.attributes.append(attr)
        return self

    def build_event(self):
        for attribute in self.attributes:
            self.xml.append(attribute.xml)

    def __str__(self):
        return ET.dump(self.xml)


class Attribute():
    """
    An Attribute object. Set the type, key, and value of the attribute and add this attribute to a trace or the log.
    """
    def __init__(self,
                 type="not set",
                 key="not set",
                 value="not set"):
        self.type = type
        self.key = key
        self.value = value

        self.xml = ET.Element(self.type)
        self.xml.set("key", key)
        self.xml.set("value", value)

    def __str__(self):
        return ET.dump(self.xml)


class Trace():
    """
    A Trace which has Events.
    """
    def __init__(self):
        self.xml = ET.Element("trace")
        self.events = []
        self.attributes = []

    def add_attribute(self, attr):
        self.attributes.append(attr)

    def add_event(self, event):
        self.events.append(event)

    def build_trace(self):
        for event in self.events:
            self.xml.append(event.xml)

    def __str__(self):
        return ET.dump(self.xml)




class Extension():
    """
    An Extension. Used for the Log.
    """
    def __init__(self,
                 name="not set",
                 prefix="not set",
                 uri="not set"):
        self.name = name
        self.prefix = prefix
        self.uri = uri

        self.xml = ET.Element("extension")
        self.xml.set("name", name)
        self.xml.set("prefix", prefix)
        self.xml.set("uri", uri)

    def __str__(self):
        return ET.dump(self.xml)


class Classifier():
    """
    Classifier. Used by the Log. Should be the main attributes of events you want to classify by.
    """
    def __init__(self, name="not set", keys="not set"):
        self.name = name
        self.keys = keys

        self.xml = ET.Element("classifier")
        self.xml.set("name", name)
        self.xml.set("keys", keys)

    def __str__(self):
        return ET.dump(self.xml)


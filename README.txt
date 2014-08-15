===========
XES
===========

This project is on Github: https://github.com/jsumrall/xes



This is a simple library which has methods for generating XES files.
With this library you will be able to take your raw event data and
generate an XES file with a standard header. From the XES-Standard web page,
"XES is an XML-based standard for event logs. Its purpose is to provide a
generally-acknowledged format for the interchange of event log data between
tools and application domains. Its primary purpose is for process mining,
i.e. the analysis of operational processes based on their event logs."

As usual, examples are the best way to see what this does.

Typical usage often looks like this::

    #!/usr/bin/env python

    import xes

    document = xes.XESDocument()
    processed_traces = []

    for raw_trace in raw_data_traces:
        xesTrace = xes.Trace()
        for raw_event in raw_trace.events:
            xesEvent = xes.Event()
            xesEvent.attributes = [
                xes.Attribute(type="string", key="lifecycle:transition", value="start"),
                xes.Attribute(type="string", key="org:resource", value=raw_event["resource"]),
                xes.Attribute(type="date", key="time:timestamp", value=raw_event["timestamp"]),
            ]
        xesTrace.addEvent(xesEvent)
        document.addTrace(xesTrace)

    open("xeslog.xes","w").write(document.toXES())



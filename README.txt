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

Example usage looks like this::

    #!/usr/bin/env python

    import xes

    traces = [
        [
            {"concept:name" : "Register", "org:resource" : "Bob"},
            {"concept:name" : "Negotiate", "org:resource" : "Sally"},
            {"concept:name" : "Negotiate", "org:resource" : "Sally"},
            {"concept:name" : "Sign", "org:resource" : "Dan"},
            {"concept:name" : "Sendoff", "org:resource" : "Mary"}
        ],
        [
            {"concept:name" : "Register", "org:resource" : "Bob"},
            {"concept:name" : "Negotiate", "org:resource" : "Sally"},
            {"concept:name" : "Sign", "org:resource" : "Dan"},
            {"concept:name" : "Sendoff", "org:resource" : "Mary"}
        ],
        [
            {"concept:name" : "Register", "org:resource" : "Bob"},
            {"concept:name" : "Negotiate", "org:resource" : "Sally"},
            {"concept:name" : "Sign", "org:resource" : "Dan"},
            {"concept:name" : "Negotiate", "org:resource" : "Sally"},
            {"concept:name" : "Sendoff", "org:resource" : "Mary"}
        ],
        [
            {"concept:name" : "Register", "org:resource" : "Bob"},
            {"concept:name" : "Sign", "org:resource" : "Dan"},
            {"concept:name" : "Sendoff", "org:resource" : "Mary"}
        ]
    ]


    log = xes.Log()
    for trace in traces:
        t = xes.Trace()
        for event in trace:
            e = xes.Event()
            e.attributes = [
                xes.Attribute(type="string", key="concept:name", value=event["concept:name"]),
                xes.Attribute(type="string", key="org:resource", value=event["org:resource"])
            ]
            t.add_event(e)
        log.add_trace(t)
    log.classifiers = [
        xes.Classifier(name="org:resource",keys="org:resource"),
        xes.Classifier(name="concept:name",keys="concept:name")
    ]

    open("example.xes", "w").write(str(log))




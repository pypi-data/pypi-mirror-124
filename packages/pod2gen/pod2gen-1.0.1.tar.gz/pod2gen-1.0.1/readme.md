pod2gen (forked from python-podgen)
===================================

[![Build Status](https://gitlab.com/caproni-podcast-publishing/pod2gen/badges/master/pipeline.svg?key_text=build)](https://gitlab.com/caproni-podcast-publishing/pod2gen/badges/master/pipeline.svg?key_text=build)
[![Documentation Status](https://readthedocs.org/projects/pod2gen/badge/?version=latest)](http://pod2gen.readthedocs.io/en/latest/?badge=latest)


This module can be used to generate podcast feeds in RSS format, and is
compatible with Python 3.6+.

It is licensed under the terms of both, the FreeBSD license and the LGPLv3+.
Choose the one which is more convenient for you. For more details have a look
at license.bsd and license.lgpl.

More details about the project:

- Repository:            https://gitlab.com/caproni-podcast-publishing/pod2gen
- Documentation:         https://pod2gen.caproni.fm
- Python Package Index:  https://pypi.python.org/pypi/pod2gen/


See the documentation link above for installation instructions and
guides on how to use this module.

RSS Namespace Extension for Podcasting
--------------------------

pod2gen is a fork from python-podgen that adds on top of it a support for 
[RSS Namespace Extension for Podcasting](https://podcastindex.org/namespace/1.0),
a wholistic RSS namespace for podcasting that is meant to synthesize the fragmented 
world of podcast namespaces. 

All the tags described in the document 
[RSS Namespace Extension for Podcasting](https://podcastindex.org/namespace/1.0) 
are implemented in pod2gen.

Known bugs and limitations
--------------------------

* The updates to Apple's podcasting guidelines since 2016 have not been
  implemented. This includes the ability to mark episodes
  with episode and season number, and the ability to mark the podcast as
  "serial". It is a goal to implement those changes in a future release.
* We do not follow the RSS recommendation to encode &amp;, &lt; and &gt; using
  hexadecimal character reference (eg. `&#x3C;`), simply because lxml provides
  no documentation on how to do that when using the text property.

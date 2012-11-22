NoWiki is a wiki made wrong

# Goals

This aims to be the most minimal wiki engine ever written.

EVER.

It is especially optimized for high-latency connections (Tor, proxy, satellite,
tcp over pidgeons).

# Tech

It is just a _single_ editable page. Every resource is inside the page, so
there are fewer http requests. It tries to use JavaScript as much as it can, so
to minimize useless pagereloads.

Authentication is handled through htaccess

If JS is not enabled in browser, it will still be possible to see the page,
but not edit it.
However, updating via curl should be easy

In future, more than one page will be supported. By now, we can live without
it.

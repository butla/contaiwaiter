Contaiwaiter - the container awaiter
====================================

Waits until systems in containers really come on-line and then signals it.
The purpose is to use this in tests, as a single URL to wait for for the whole system
spread across multiple containers.

There are many simple projects like this
(see `here <https://hub.docker.com/r/waisbrot/wait/>`_
or `here <https://hub.docker.com/r/n3llyb0y/wait/>`_,
but you can find many more than these), but they only wait for ports or URLs,
which is insufficient, from my experience.
So this application will wait for URLs to start returning proper HTTP responses,
wait for SQL servers to be responsive, check that you can talk with Redis, etc.

I'll add to this project over time, when need arises, functions
to wait for a specific system to become operational.
But hey, contributions are welcome.

TODO: plugin system, so that you inherit the image, add a python file and config,
and it works magically.

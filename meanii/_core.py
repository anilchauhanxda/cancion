# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import asyncio
import traceback
import os
from datetime import datetime
from meanii import util


DELETE_TIMEOUT = 5


@songsxd.on(util.admin_cmd(pattern="load (?P<shortname>\w+)$"))  # pylint:disable=E0602
async def load_reload(event):
    await event.delete()
    shortname = event.pattern_match["shortname"]
    try:
        if shortname in songsxd._plugins:  # pylint:disable=E0602
            songsxd.remove_plugin(shortname)  # pylint:disable=E0602
        songsxd.load_plugin(shortname)  # pylint:disable=E0602
        msg = await event.respond(f"Successfully (re)loaded plugin {shortname}")
        await asyncio.sleep(DELETE_TIMEOUT)
        await msg.delete()
    except Exception as e:  # pylint:disable=C0103,W0703
        trace_back = traceback.format_exc()
        # pylint:disable=E0602
        logger.warn(f"Failed to (re)load plugin {shortname}: {trace_back}")
        await event.respond(f"Failed to (re)load plugin {shortname}: {e}")


@songsxd.on(util.admin_cmd(pattern="(?:unload|remove) (?P<shortname>\w+)$"))  # pylint:disable=E0602
async def remove(event):
    await event.delete()
    shortname = event.pattern_match["shortname"]
    if shortname == "_core":
        msg = await event.respond(f"Not removing {shortname}")
    elif shortname in songsxd._plugins:  # pylint:disable=E0602
        songsxd.remove_plugin(shortname)  # pylint:disable=E0602
        msg = await event.respond(f"Removed plugin {shortname}")
    else:
        msg = await event.respond(f"Plugin {shortname} is not loaded")
    await asyncio.sleep(DELETE_TIMEOUT)
    await msg.delete()



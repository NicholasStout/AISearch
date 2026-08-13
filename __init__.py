"""The searxng integration."""

from homeassistant.config_entries import ConfigEntry
#from homeassistant.const import Platform
from homeassistant.exceptions import ConfigEntryNotReady
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import aiohttp
from . import SearXNGApi

type SearXNGConfigEntry = ConfigEntry[SearXNGApi]  # noqa: F821


async def async_setup_entry(hass: HomeAssistant, entry: SearXNGConfigEntry) -> bool:
    """Set up searxng from a config entry."""
    # 1. Create API instance
    api = SearXNGApi(entry.data["url"], async_get_clientsession(hass))

    # 2. Validate the API connection (and authentication)
    try:
        await api.async_validate()
    except:
        raise ConfigEntryNotReady

    # 3. Store an API object for your platforms to access
    entry.runtime_data = api

    #await hass.config_entries.async_forward_entry_setups(entry, _PLATFORMS)

    return True


# TODO Update entry annotation
async def async_unload_entry(hass: HomeAssistant, entry: SearXNGConfigEntry) -> bool:
    """Unload a config entry."""
    return
    #return await hass.config_entries.async_unload_platforms(entry, _PLATFORMS)

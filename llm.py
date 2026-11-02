from typing import Any

from homeassistant.components import llm
from homeassistant.helpers.llm import LLMContext, ToolInput
from homeassistant.core import HomeAssistant, callback

from . import SearXNGApi


class SearXNGSearchTool(llm.Tool):
    """Tool for searching the web using SearXNG."""

    name = "searxng_search"

    description = (
        "Use this as a search engine for general information and unit conversions."
    )

    parameters = {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The query to send to the search engine.",
            },
        },
        "required": ["query"],
    }

    async def async_call(
        self,
        hass: HomeAssistant,
        tool_input: ToolInput,
        llm_context: LLMContext,
    ) -> dict[str, Any]:
        """Execute a SearXNG search."""

        entries = hass.config_entries.async_entries("searxng")

        if not entries:
            return {
                "error": "SearXNG is not configured."
            }

        entry = entries[0]
        api: SearXNGApi = entry.runtime_data

        query = tool_input.tool_args["query"]

        return await api.search(query)


#@llm.hass_config_entry
@callback
async def async_get_tools(
    hass: HomeAssistant,
    llm_context: LLMContext,
    api_id: str,
) -> llm.LLMTools | None:
    """Return the tools to expose to the LLM."""

    return llm.LLMTools(
        tools=[SearXNGSearchTool()],
        prompt=(
            "Use SearXNGSearchTool to submit a concise search engine query for general information and unit conversions."
        ),
    )

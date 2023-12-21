from aiohttp import web
import json
import server 
from .nodes import reset_registry


@server.PromptServer.instance.routes.post("/easygrids/reset/{node_id}")
async def ResetLoop(request):
    try:
        node_id = request.match_info["node_id"]
        if node_id == "all":
            for node_id in reset_registry:
                reset_registry[node_id].reset()
            return web.json_response(status=200)
        elif node_id in reset_registry:
            reset_registry[node_id].reset()
            return web.json_response(status=200)
        else:
            return web.json_response(dict(error="Node not found"), status=404)
    except Exception as e:
        return web.json_response(dict(error=str(e)), status=500)
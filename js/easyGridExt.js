import { app } from "../../scripts/app.js";
import { api } from "../../scripts/api.js"

// Copied from widgetInputs.js because AFAICT it doesn't seem to export these
function hideWidget(node, widget, suffix = "") {
	widget.origType = widget.type;
	widget.origComputeSize = widget.computeSize;
	widget.origSerializeValue = widget.serializeValue;
	widget.computeSize = () => [0, -4]; // -4 is due to the gap litegraph adds between widgets automatically
	widget.type = CONVERTED_TYPE + suffix;
	widget.serializeValue = () => {
		// Prevent serializing the widget if we have no input linked
		if (!node.inputs) {
			return undefined;
		}
		let node_input = node.inputs.find((i) => i.widget?.name === widget.name);

		if (!node_input || !node_input.link) {
			return undefined;
		}
		return widget.origSerializeValue ? widget.origSerializeValue() : widget.value;
	};

	// Hide any linked widgets, e.g. seed+seedControl
	if (widget.linkedWidgets) {
		for (const w of widget.linkedWidgets) {
			hideWidget(node, w, ":" + widget.name);
		}
	}
}

function showWidget(widget) {
	widget.type = widget.origType;
	widget.computeSize = widget.origComputeSize;
	widget.serializeValue = widget.origSerializeValue;

	delete widget.origType;
	delete widget.origComputeSize;
	delete widget.origSerializeValue;

	// Hide any linked widgets, e.g. seed+seedControl
	if (widget.linkedWidgets) {
		for (const w of widget.linkedWidgets) {
			showWidget(w);
		}
	}
}

app.registerExtension({
    name: "easygrids",
    async nodeCreated(node, app) {
        if (node.__proto__.comfyClass === "ImageGridCommander")
        {
            node.addWidget( "button", "Queue Full Grid", "QueueButton", () => 
            {
                const x_widget = node.widgets.find((w) => w.name === "x_count");
                const y_widget = node.widgets.find((w) => w.name === "y_count");
                let batch_size = x_widget.value * y_widget.value;
                app.queuePrompt(0, batch_size);
            });
            node.addWidget( "button", "Reset Grid Loop", "ResetButton", () =>
            {
                let req_url = "easygrids/reset/" + node.id.toString(); 
                // I have no idea if this is the right way to do this, but it seems to work!
                api.fetchApi(req_url, {
                    method: "POST",
                    body: "",
                }).then( (resp) =>
                {
                    if (resp.status != 200)
                    {
                        console.error("Failed to reset grid loop.");
                    }
                });
            });
            node.addWidget( "button", "Reset All Loop Nodes", "ResetAllButton", () => 
            {
                let req_url = "easygrids/reset/all"; 
                api.fetchApi(req_url, {
                    method: "POST",
                    body: "",
                }).then( (resp) =>
                {
                    if (resp.status != 200)
                    {
                        console.error("Failed to reset all loop nodes.");
                    }
                });
            });
        }
        else if (node.__proto__.comfyClass === "SaveImageGrid")
        {
            node.addWidget( "button", "Clear Stored Images", "ResetButton", () => 
            {
                let req_url = "easygrids/reset/" + node.id.toString(); 
                // i do not understand promises
                api.fetchApi(req_url, {
                    method: "POST",
                    body: "",
                }).then( (resp) =>
                {
                    if (resp.status != 200)
                    {
                        console.error("Failed to clear accumulated images.");
                    }
                });
            });
        }
    },
});
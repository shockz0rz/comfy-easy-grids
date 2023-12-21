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
                for ( let queue_x = 1; queue_x <= x_widget.value; queue_x++ )
                {
                    for ( let queue_y = 1; queue_y <= y_widget.value; queue_y++ )
                    {
                        app.queuePrompt(1, 1);
                    }
                }
            });
            node.addWidget( "button", "Reset Grid Loop", "ResetButton", () =>
            {
                let req_url = "easygrids/reset/" + node.id.toString();
                const resp = api.fetchApi(req_url, {
					method: "POST",
					body: "",
                } );
                if ( resp.status !== 200 )
                {
                    console.error( "Failed to reset grid loop" );
                }
            });
        }
    },
});
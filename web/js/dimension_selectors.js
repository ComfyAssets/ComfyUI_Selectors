import { app } from "../../scripts/app.js";

console.log("ComfyUI Selectors extension loading...");

// Register extension for ComfyUI
app.registerExtension({
    name: "ComfyAssets.DimensionSelectors",
    
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        console.log("Processing node:", nodeData.name);
        
        // Only target our WidthHeightNode
        if (nodeData.name === "WidthHeightNode") {
            console.log("Found WidthHeightNode, adding handlers...");
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            
            nodeType.prototype.onNodeCreated = function() {
                const result = onNodeCreated?.apply(this, arguments);
                
                // Add preset change handler
                this.addPresetChangeHandler();
                
                return result;
            };
            
            // Add method to handle preset changes
            nodeType.prototype.addPresetChangeHandler = function() {
                const self = this;
                console.log("Setting up preset change handler for node:", this);
                
                // Find the preset widget
                const presetWidget = this.widgets?.find(w => w.name === "preset");
                const widthWidget = this.widgets?.find(w => w.name === "width");
                const heightWidget = this.widgets?.find(w => w.name === "height");
                const swapWidget = this.widgets?.find(w => w.name === "swap_dimensions");
                
                console.log("Found widgets:", { presetWidget, widthWidget, heightWidget, swapWidget });
                
                if (!presetWidget || !widthWidget || !heightWidget) {
                    console.warn("Could not find required widgets for WidthHeightNode");
                    console.log("Available widgets:", this.widgets?.map(w => w.name));
                    return;
                }
                
                // Store original callback
                const originalCallback = presetWidget.callback;
                
                // Define preset mappings
                const presetMappings = {
                    "1024x1024 (1:1 Square)": { width: 1024, height: 1024 },
                    "1152x896 (9:7 Slightly wide landscape)": { width: 1152, height: 896 },
                    "896x1152 (7:9 Portrait)": { width: 896, height: 1152 },
                    "1216x832 (3:2 Standard landscape)": { width: 1216, height: 832 },
                    "832x1216 (2:3 Standard portrait)": { width: 832, height: 1216 },
                    "1344x768 (7:4 Wide landscape)": { width: 1344, height: 768 },
                    "768x1344 (4:7 Tall portrait)": { width: 768, height: 1344 },
                    "1536x640 (12:5 Ultra-wide cinematic)": { width: 1536, height: 640 },
                    "640x1536 (5:12 Ultra-tall)": { width: 640, height: 1536 }
                };
                
                // Swap mappings for when swap is enabled
                const swapMappings = {
                    "1024x1024 (1:1 Square)": "1024x1024 (1:1 Square)",
                    "1152x896 (9:7 Slightly wide landscape)": "896x1152 (7:9 Portrait)",
                    "896x1152 (7:9 Portrait)": "1152x896 (9:7 Slightly wide landscape)",
                    "1216x832 (3:2 Standard landscape)": "832x1216 (2:3 Standard portrait)",
                    "832x1216 (2:3 Standard portrait)": "1216x832 (3:2 Standard landscape)",
                    "1344x768 (7:4 Wide landscape)": "768x1344 (4:7 Tall portrait)",
                    "768x1344 (4:7 Tall portrait)": "1344x768 (7:4 Wide landscape)",
                    "1536x640 (12:5 Ultra-wide cinematic)": "640x1536 (5:12 Ultra-tall)",
                    "640x1536 (5:12 Ultra-tall)": "1536x640 (12:5 Ultra-wide cinematic)"
                };
                
                // Update dimensions based on preset and swap state
                function updateDimensions() {
                    const preset = presetWidget.value;
                    const isSwapped = swapWidget?.value || false;
                    
                    if (preset !== "custom" && presetMappings[preset]) {
                        let dimensions;
                        
                        if (isSwapped && swapMappings[preset]) {
                            // Use swapped preset dimensions
                            const swappedPreset = swapMappings[preset];
                            dimensions = presetMappings[swappedPreset];
                        } else {
                            dimensions = presetMappings[preset];
                        }
                        
                        if (dimensions) {
                            widthWidget.value = dimensions.width;
                            heightWidget.value = dimensions.height;
                            
                            // Trigger visual update
                            self.setDirtyCanvas(true);
                        }
                    }
                }
                
                // Override preset widget callback
                presetWidget.callback = function(value) {
                    console.log("Preset changed to:", value);
                    updateDimensions();
                    originalCallback?.apply(this, arguments);
                };
                
                // Also handle swap changes
                if (swapWidget) {
                    const originalSwapCallback = swapWidget.callback;
                    swapWidget.callback = function(value) {
                        updateDimensions();
                        originalSwapCallback?.apply(this, arguments);
                    };
                }
            };
        }
        
        // Handle individual Width and Height nodes too
        if (nodeData.name === "WidthNode" || nodeData.name === "HeightNode") {
            const onNodeCreated = nodeType.prototype.onNodeCreated;
            
            nodeType.prototype.onNodeCreated = function() {
                const result = onNodeCreated?.apply(this, arguments);
                
                // Add preset change handler for individual nodes
                this.addIndividualPresetHandler();
                
                return result;
            };
            
            nodeType.prototype.addIndividualPresetHandler = function() {
                const self = this;
                const isWidthNode = nodeData.name === "WidthNode";
                
                const presetWidget = this.widgets?.find(w => w.name === "preset");
                const valueWidget = this.widgets?.find(w => w.name === (isWidthNode ? "width" : "height"));
                
                if (!presetWidget || !valueWidget) {
                    return;
                }
                
                const originalCallback = presetWidget.callback;
                
                presetWidget.callback = function(value) {
                    if (value !== "custom") {
                        // Extract number from preset string (e.g., "640 (5:12 Ultra-tall)" -> 640)
                        const match = value.match(/^(\d+)/);
                        if (match) {
                            valueWidget.value = parseInt(match[1]);
                            self.setDirtyCanvas(true);
                        }
                    }
                    originalCallback?.apply(this, arguments);
                };
            };
        }
    }
});
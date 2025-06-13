import { app } from "/scripts/app.js";

// Register extension for ComfyUI
app.registerExtension({
    name: "ComfyAssets.DimensionSelectors",
    
    async beforeRegisterNodeDef(nodeType, nodeData, app) {
        // Only target our WidthHeightNode
        if (nodeData.name === "WidthHeightNode") {
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
                
                // Find the preset widget
                const presetWidget = this.widgets?.find(w => w.name === "preset");
                const widthWidget = this.widgets?.find(w => w.name === "width");
                const heightWidget = this.widgets?.find(w => w.name === "height");
                const swapWidget = this.widgets?.find(w => w.name === "swap_dimensions");
                
                if (!presetWidget || !widthWidget || !heightWidget) {
                    return;
                }
                
                // Store original callback
                const originalCallback = presetWidget.callback;
                
                // Define preset mappings
                const presetMappings = {
                    "1024x1024": { width: 1024, height: 1024 },
                    "1152x896": { width: 1152, height: 896 },
                    "896x1152": { width: 896, height: 1152 },
                    "1216x832": { width: 1216, height: 832 },
                    "832x1216": { width: 832, height: 1216 },
                    "1344x768": { width: 1344, height: 768 },
                    "768x1344": { width: 768, height: 1344 },
                    "1536x640": { width: 1536, height: 640 },
                    "640x1536": { width: 640, height: 1536 }
                };
                
                // Swap mappings
                const swapMappings = {
                    "1024x1024": "1024x1024", // Square stays the same
                    "1152x896": "896x1152",
                    "896x1152": "1152x896",
                    "1216x832": "832x1216", 
                    "832x1216": "1216x832",
                    "1344x768": "768x1344",
                    "768x1344": "1344x768",
                    "1536x640": "640x1536",
                    "640x1536": "1536x640"
                };
                
                // Update dimensions based on current state
                function updateDimensions() {
                    const preset = presetWidget.value;
                    
                    if (preset !== "custom" && presetMappings[preset]) {
                        const dimensions = presetMappings[preset];
                        
                        widthWidget.value = dimensions.width;
                        heightWidget.value = dimensions.height;
                        
                        // Trigger visual update
                        self.setDirtyCanvas(true);
                    }
                }
                
                // Handle swap button click
                function handleSwap() {
                    const preset = presetWidget.value;
                    
                    if (preset !== "custom") {
                        // Get current dimensions from the preset
                        let currentDimensions = null;
                        if (presetMappings[preset]) {
                            currentDimensions = presetMappings[preset];
                        } else {
                            // Fallback: use current widget values
                            currentDimensions = {
                                width: widthWidget.value,
                                height: heightWidget.value
                            };
                        }
                        
                        // Temporarily disable the callback to prevent recursion
                        const originalCallback = presetWidget.callback;
                        presetWidget.callback = null;
                        
                        // Set preset to custom to avoid validation issues
                        presetWidget.value = "custom";
                        
                        // Swap the dimensions
                        widthWidget.value = currentDimensions.height;
                        heightWidget.value = currentDimensions.width;
                        
                        // Re-enable callback
                        presetWidget.callback = originalCallback;
                        
                        // Trigger visual update
                        self.setDirtyCanvas(true);
                        
                    } else {
                        // Handle custom dimensions swap
                        const currentWidth = widthWidget.value;
                        const currentHeight = heightWidget.value;
                        widthWidget.value = currentHeight;
                        heightWidget.value = currentWidth;
                        
                        // Trigger visual update
                        self.setDirtyCanvas(true);
                    }
                }
                
                // Override preset widget callback
                presetWidget.callback = function(value) {
                    updateDimensions();
                    originalCallback?.apply(this, arguments);
                };
                
                // Handle swap changes
                if (swapWidget) {
                    const originalSwapCallback = swapWidget.callback;
                    
                    swapWidget.callback = function(value) {
                        handleSwap();
                        originalSwapCallback?.apply(this, arguments);
                    };
                    
                    // Also try hooking into mouse events as backup
                    if (swapWidget.element) {
                        swapWidget.element.addEventListener('click', function() {
                            setTimeout(() => {
                                handleSwap();
                            }, 10);
                        });
                    }
                }
            };
        }
    }
});
// ComfyUI_Selectors - Width Height Node with Swap Button
import { app } from "../../scripts/app.js";

app.registerExtension({
  name: "comfyassets.WidthHeightSwap",
  async beforeRegisterNodeDef(nodeType, nodeData, _app) {
    if (nodeData.name === "WidthHeightNode") {
      const onNodeCreated = nodeType.prototype.onNodeCreated;
      nodeType.prototype.onNodeCreated = function () {
        if (onNodeCreated) onNodeCreated.apply(this, []);
        
        // Hide the swap_dimensions widget
        const swapWidget = this.widgets?.find(w => w.name === "swap_dimensions");
        if (swapWidget) {
          swapWidget.type = "hidden";
          swapWidget.hidden = true;
        }
        
        // Add swap functionality
        this.swapDimensions = function() {
          const widthWidget = this.widgets.find(w => w.name === "width");
          const heightWidget = this.widgets.find(w => w.name === "height");
          const presetWidget = this.widgets.find(w => w.name === "preset");
          
          if (widthWidget && heightWidget && presetWidget) {
            // Handle preset swapping first
            if (presetWidget.value !== "custom") {
              const currentPreset = presetWidget.value;
              const [w, h] = currentPreset.split('x').map(v => parseInt(v));
              const swappedPreset = `${h}x${w}`;
              
              // Check if the swapped preset exists in the options
              const presetOptions = [
                "custom", "512x512", "768x512", "1024x768", "1152x896", 
                "1216x832", "1344x768", "1408x704", "1472x704", "1536x640",
                "640x1536", "704x1472", "704x1408", "768x1344", "832x1216", 
                "896x1152", "768x1024", "512x768"
              ];
              
              if (presetOptions.includes(swappedPreset)) {
                // Swapped preset exists, use it
                presetWidget.value = swappedPreset;
                if (presetWidget.callback) {
                  presetWidget.callback(swappedPreset, this, presetWidget);
                }
              } else {
                // Swapped preset doesn't exist, switch to custom and swap manual values
                presetWidget.value = "custom";
                widthWidget.value = h;
                heightWidget.value = w;
                
                if (presetWidget.callback) {
                  presetWidget.callback("custom", this, presetWidget);
                }
                if (widthWidget.callback) {
                  widthWidget.callback(h, this, widthWidget);
                }
                if (heightWidget.callback) {
                  heightWidget.callback(w, this, heightWidget);
                }
              }
            } else {
              // Custom preset - just swap the width and height values
              const tempWidth = widthWidget.value;
              widthWidget.value = heightWidget.value;
              heightWidget.value = tempWidth;
              
              // Trigger widget change events
              if (widthWidget.callback) {
                widthWidget.callback(widthWidget.value, this, widthWidget);
              }
              if (heightWidget.callback) {
                heightWidget.callback(heightWidget.value, this, heightWidget);
              }
            }
            
            // Mark the graph as changed
            this.graph?.setDirtyCanvas(true, true);
          }
        };
      };

      const onDrawForeground = nodeType.prototype.onDrawForeground;
      nodeType.prototype.onDrawForeground = function (ctx) {
        if (onDrawForeground) {
          onDrawForeground.apply(this, arguments);
        }
        
        if (this.flags.collapsed) return;
        
        // Draw swap button in bottom right corner
        const swapButtonSize = 24;
        const margin = 6;
        const swapButtonX = this.size[0] - swapButtonSize - margin;
        const swapButtonY = this.size[1] - swapButtonSize - margin;
        
        // Button background
        ctx.fillStyle = "rgba(100,100,100,0.8)";
        ctx.beginPath();
        ctx.roundRect(swapButtonX, swapButtonY, swapButtonSize, swapButtonSize, 2);
        ctx.fill();
        
        // Button border
        ctx.strokeStyle = "rgba(200,200,200,0.9)";
        ctx.lineWidth = 1;
        ctx.stroke();
        
        // Draw swap icon (clean stacked arrows like mxToolkit)
        ctx.strokeStyle = "rgba(255,255,255,0.9)";
        ctx.lineWidth = 2;
        ctx.lineCap = "round";
        
        const centerX = swapButtonX + 12;
        const centerY = swapButtonY + 12;
        
        // Top arrow (pointing right)
        ctx.beginPath();
        ctx.moveTo(centerX - 6, centerY - 3);
        ctx.lineTo(centerX + 6, centerY - 3);
        ctx.stroke();
        
        // Top arrow head
        ctx.beginPath();
        ctx.moveTo(centerX + 6, centerY - 3);
        ctx.lineTo(centerX + 3, centerY - 5);
        ctx.moveTo(centerX + 6, centerY - 3);
        ctx.lineTo(centerX + 3, centerY - 1);
        ctx.stroke();
        
        // Bottom arrow (pointing left)
        ctx.beginPath();
        ctx.moveTo(centerX + 6, centerY + 3);
        ctx.lineTo(centerX - 6, centerY + 3);
        ctx.stroke();
        
        // Bottom arrow head
        ctx.beginPath();
        ctx.moveTo(centerX - 6, centerY + 3);
        ctx.lineTo(centerX - 3, centerY + 1);
        ctx.moveTo(centerX - 6, centerY + 3);
        ctx.lineTo(centerX - 3, centerY + 5);
        ctx.stroke();
      };

      const onMouseDown = nodeType.prototype.onMouseDown;
      nodeType.prototype.onMouseDown = function (e) {
        // Check if click is on swap button
        const swapButtonSize = 24;
        const margin = 6;
        const swapButtonX = this.pos[0] + this.size[0] - swapButtonSize - margin;
        const swapButtonY = this.pos[1] + this.size[1] - swapButtonSize - margin;
        
        if (
          e.canvasX >= swapButtonX &&
          e.canvasX <= swapButtonX + swapButtonSize &&
          e.canvasY >= swapButtonY &&
          e.canvasY <= swapButtonY + swapButtonSize
        ) {
          this.swapDimensions();
          return true;
        }
        
        // Call original onMouseDown if not clicking swap button
        if (onMouseDown) {
          return onMouseDown.apply(this, arguments);
        }
      };
    }
  },
});
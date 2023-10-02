document.addEventListener('DOMContentLoaded', function () {


    const toolbox = {
        "kind":"categoryToolbox",
        "contents":[
            {
                "kind":"category",
                "name":"Robot Control",
                "contents":[
                    {
                        "kind":"block",
                        "type":"move"
                    },
                    {
                        "kind":"block",
                        "type":"waypoint"
                    },
                    {
                        "kind":"block",
                        "type":"waypoint_control"
                    },
                    {
                        "kind":"block",
                        "type":"coordinate_input"
                    },

                ]
            }
        ]
    }

    Blockly.Blocks['move'] = {
        init: function() {
            this.appendDummyInput()
                .appendField("Move");
            this.appendStatementInput('WAYPOINT')
                .setCheck('waypoint')
                .appendField('Waypoint:');
            this.setPreviousStatement(true, null);
            this.setNextStatement(true, null);
            this.setColour(160); // Change the color to a different value
            this.setTooltip('Moves the robot through the inserted waypoints');
        }
    };
    
    Blockly.Blocks['waypoint'] = {
        init: function() {
            this.appendDummyInput()
                .appendField("Waypoint");
            this.appendValueInput('COORDINATES')
                .setCheck('waypoint_destination')
                .appendField('Coordinates to move to:');
            this.appendValueInput('WAYPOINT_CONTROLS')
                .setCheck(['waypoint_controls'])
                .appendField('Optional Controls:');
            this.setPreviousStatement(true, 'waypoint');
            this.setNextStatement(true, 'waypoint');
            this.setColour(210); // Change the color to a different value
            this.setTooltip('Create a waypoint with X, Y, and Z coordinates and optional control blocks.');
        }
    };
    
    Blockly.Blocks['waypoint_control'] = {
        init: function() {
            this.appendDummyInput()
                .appendField('Linear Acceleration:')
                .appendField(new Blockly.FieldNumber(0), 'ACCELERATION')
                .setAlign(Blockly.ALIGN_RIGHT);
            this.appendDummyInput()
                .appendField('Joint Acceleration:')
                .appendField(new Blockly.FieldNumber(0), 'ACCELERATION')
                .setAlign(Blockly.ALIGN_RIGHT);
            this.appendDummyInput()
                .appendField('Speed:')
                .appendField(new Blockly.FieldNumber(0), 'SPEED')
                .setAlign(Blockly.ALIGN_RIGHT);
            this.setOutput(true, 'waypoint_controls');
            this.setColour(260); // Change the color to a different value
            this.setTooltip('Set acceleration and speed for the waypoint.');
        }
    };
    
    Blockly.Blocks['coordinate_input'] = {
        init: function() {
            this.appendDummyInput()
                .appendField("Coords:")
                .appendField("X:")
                .appendField(new Blockly.FieldNumber(0), 'X')
                .appendField("Y:")
                .appendField(new Blockly.FieldNumber(0), 'Y')
                .appendField("Z:")
                .appendField(new Blockly.FieldNumber(0), 'Z');
            this.setOutput(true, 'waypoint_destination');
            this.setColour(120); // Change the color to a different value
            this.setTooltip('Specify X, Y, and Z coordinates.');
        }
    };
    
      


    const workspace = Blockly.inject('blocklyDiv', {
        media: '../lib/blockly/media/',
        toolbox: toolbox,
    });

});

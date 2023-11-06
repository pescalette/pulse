document.addEventListener('DOMContentLoaded', function () {


    const toolbox = {
        "kind": "categoryToolbox",
        "contents": [
            {
                "kind": "category",
                "name": "Main Robot Control",
                "contents": [
                    {
                        "kind": "block",
                        "type": "program_root"
                    },
                    {
                        "kind": "block",
                        "type": "motor_name"
                    },
                    {
                        "kind": "block",
                        "type": "move"
                    },
                    {
                        "kind": "block",
                        "type": "waypoint"
                    },
                    {
                        "kind": "block",
                        "type": "coordinate_input"
                    },
                    {
                        "kind": "block",
                        "type": "waypoint_control"
                    },
                ]
            },
            {
                "kind": "category",
                "name": "Logic",
                "contents": [
                    {
                        "kind": "block",
                        "type": "controls_repeat_custom"
                    },
                ]
            },
            {
                "kind": "category",
                "name": "LED Control",
                "contents": [
                {
                "kind": "block",
                "type": "led_control"
                }
        ]
            }
        ]
    }

    Blockly.Blocks['program_root'] = {
        init: function () {
            this.appendDummyInput()
                .appendField('Initialization')
            this.appendStatementInput('MOTORS')
                .setCheck('motor_name')
                .appendField('Motor Names:');
            this.appendStatementInput('MAIN_PROGRAM')
                .setCheck(null)
                .appendField('Main Program');
            this.setColour(160); // You can set a custom color for your block
            this.setTooltip('Root block for the program');
            this.setHelpUrl(''); // Set the URL for documentation if needed
        }
    };

    Blockly.Blocks['motor_name'] = {
        init: function () {
            this.appendDummyInput()
                .appendField('Motor Name:')
                .appendField(new Blockly.FieldTextInput('motor_name'), 'MOTOR_NAME');
            this.setOutput(true, 'motor_name');
            this.setPreviousStatement(true, "motor_name");
            this.setNextStatement(true, "motor_name");
            this.setColour(210); // You can set a custom color for this block
            this.setTooltip('Add a motor name');
            this.setHelpUrl(''); // Set the URL for documentation if needed
        }
    };


    Blockly.Blocks['controls_repeat_custom'] = {
        init: function () {
            this.appendDummyInput()
                .appendField("Repeat")
                .appendField(new Blockly.FieldNumber(0), "TIMES")
                .appendField("times");
            this.appendStatementInput("DO")
                .appendField("Do:")
                .setCheck("move"); // Replace with your desired block type
            this.setInputsInline(true);
            this.setPreviousStatement(true, ["controls_repeat_custom", "move"]);
            this.setNextStatement(true, ["controls_repeat_custom", "move"]);
            this.setColour(20);
            this.setTooltip("Repeat a set of actions a specified number of times.");
            this.setHelpUrl("");
        }
    };


    Blockly.Blocks['move'] = {
        init: function () {
            this.appendDummyInput()
                .appendField("Move to");
            this.appendStatementInput('WAYPOINT')
                .setCheck('waypoint')
                .appendField('Waypoint:');
            this.setPreviousStatement(true, "move");
            this.setNextStatement(true, "move");
            this.setColour(40);
            this.setTooltip('Moves the robot through the inserted waypoints');
        }
    };

    Blockly.Blocks['waypoint'] = {
        init: function () {
            this.appendDummyInput()
                .appendField("Waypoint");
            this.appendValueInput('COORDINATES')
                .setCheck('waypoint_destination')
                .appendField('Coordinates to move to:');
            this.appendValueInput('WAYPOINT_CONTROLS')
                .setCheck('waypoint_controls')
                .appendField('Optional Speed Parameters:');
            this.setPreviousStatement(true, 'waypoint');
            this.setNextStatement(true, 'waypoint');
            this.setColour(60);
            this.setTooltip('Create a waypoint with X, Y, and Z coordinates and optional control blocks.');
        }
    };

    Blockly.Blocks['coordinate_input'] = {
        init: function () {
            this.appendDummyInput()
                .appendField("Coords:")
                .appendField("X:")
                .appendField(new Blockly.FieldNumber(0), 'X')
                .appendField("Y:")
                .appendField(new Blockly.FieldNumber(0), 'Y')
                .appendField("Z:")
                .appendField(new Blockly.FieldNumber(0), 'Z');
            this.setOutput(true, 'waypoint_destination');
            this.setColour(80);
            this.setTooltip('Specify X, Y, and Z coordinates.');
        }
    };

    Blockly.Blocks['waypoint_control'] = {
        init: function () {
            this.appendDummyInput()
                .appendField('Acceleration:')
                .appendField(new Blockly.FieldNumber(0), 'ACCELERATION')
                .setAlign(Blockly.ALIGN_RIGHT);
            this.appendDummyInput()
                .appendField('Speed:')
                .appendField(new Blockly.FieldNumber(0), 'SPEED')
                .setAlign(Blockly.ALIGN_RIGHT);
            this.setOutput(true, 'waypoint_controls');
            this.setColour(80);
            this.setTooltip('Set acceleration and speed for the waypoint.');
        }
    };

    Blockly.Blocks['led_control'] = {
        init: function () {
            this.appendDummyInput()
                .appendField("LED Control:")
                .appendField(new Blockly.FieldDropdown([
                    ["ON", "TRUE"], 
                    ["OFF", "FALSE"]
                ]), "STATE")
                .appendField("Color")
                .appendField(new Blockly.FieldColour("#ff0000"), "COLOR");
            this.setPreviousStatement(true, null);
            this.setNextStatement(true, null);
            this.setColour(120);
            this.setTooltip("Turn an LED on or off and set its color.");
            this.setHelpUrl("");
        }
    };
    
    Blockly.Python['led_control'] = function (block) {
        var state = block.getFieldValue('STATE') === 'TRUE' ? 'True' : 'False';
        var color = block.getFieldValue('COLOR');
        // Assuming a function setLED exists to control the LED
        var pythonCode = `setLED(${state}, '${color}')\n`;
        return pythonCode;
    };




    const workspace = Blockly.inject('blocklyDiv', {
        media: '../lib/blockly/media/',
        toolbox: toolbox,
        toolboxPosition: 'start',
    });



    function generatePythonCode() {
        const code = python.pythonGenerator.workspaceToCode(workspace);

        // Add import statements and robot initialization
        let pythonCode = 'import webots\n\n';
        pythonCode += 'robot = webots.Robot()\n';

        pythonCode += '\n';

        // Concatenate the generated Python code
        pythonCode += code;
        document.getElementById('generated-code').innerText = pythonCode;
    }

    Blockly.Python['program_root'] = function (block) {
        var motorCode = Blockly.Python.statementToCode(block, 'MOTORS');
        var mainCode = Blockly.Python.statementToCode(block, 'MAIN_PROGRAM');
        var code = motorCode + mainCode;
        return code;
    };

    Blockly.Python['motor_name'] = function (block) {
        var motorName = block.getFieldValue('MOTOR_NAME');
        var pythonCode = `motor_${motorName} = robot.getMotor("${motorName}")\n`;
        return pythonCode;
    };

    Blockly.Python['controls_repeat_custom'] = function (block) {
        const times = block.getFieldValue('TIMES');
        const doCode = Blockly.Python.statementToCode(block, 'DO');

        return `for i in range(${times}):\n${doCode}\n`;
    };

    Blockly.Python['move'] = function (block) {
        const waypointsCode = Blockly.Python.statementToCode(block, 'WAYPOINT');
        return waypointsCode;
    };

    Blockly.Python['waypoint'] = function (block) {
        const coordinatesCode = Blockly.Python.valueToCode(block, 'COORDINATES', Blockly.Python.ORDER_ATOMIC);
        const waypointControlsCode = Blockly.Python.valueToCode(block, 'WAYPOINT_CONTROLS', Blockly.Python.ORDER_ATOMIC);

        const code = 'motor.setPosition(' + coordinatesCode + ')\n';

        return code;
    };

    Blockly.Python['coordinate_input'] = function (block) {
        const x = block.getFieldValue('X');
        const y = block.getFieldValue('Y');
        const z = block.getFieldValue('Z');

        return ['webots.Vector3(' + x + ', ' + y + ', ' + z + ')', Blockly.Python.ORDER_ATOMIC];
    };

    Blockly.Python['waypoint_control'] = function (block) {
        const acceleration = block.getFieldValue('ACCELERATION');
        const speed = block.getFieldValue('SPEED');

        return [`# Set acceleration and speed: Acceleration: ${acceleration}, Speed: ${speed}`, Blockly.Python.ORDER_ATOMIC];
    };


    // Attach the code generation function to the button click event
    document.getElementById('generateCodeButton').addEventListener('click', generatePythonCode);
    document.getElementById('saveCodeButton').addEventListener('click', savePythonCodeToFile);

    function savePythonCodeToFile() {
        const code = python.pythonGenerator.workspaceToCode(workspace);
        const pythonCode = 'import webots\n\n' +
            'robot = webots.Robot()\n' +
            'motor = robot.getMotor("motor_name")\n\n' +
            code;

        const blob = new Blob([pythonCode], { type: 'text/plain' });
        const fileName = 'generated_code.py';

        // Create a temporary link to trigger the download
        const a = document.createElement('a');
        a.href = window.URL.createObjectURL(blob);
        a.download = fileName;
        a.style.display = 'none';

        // Append the link to the document and trigger the download
        document.body.appendChild(a);
        a.click();

        // Clean up by removing the link
        document.body.removeChild(a);
    }


    // keep submenu open
    workspace.toolbox_.flyout_.autoClose = false;
});

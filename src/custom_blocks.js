document.addEventListener('DOMContentLoaded', function () {
    var move_block_index = 0;


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
            }
        ]
    }

    Blockly.Blocks['program_root'] = {
        init: function () {
            this.appendDummyInput()
                .appendField('Start Here');
            this.appendDummyInput()
                .appendField('Robot Name:')
                .appendField(new Blockly.FieldDropdown([["BlockArm", "BlockArm"]]), "ROBOT_NAME");
            this.appendStatementInput('MAIN_PROGRAM')
                .setCheck(['controls_repeat_custom', 'move'])
                .appendField('Main Program');
            this.setColour(160);
            this.setTooltip('Root block for the program');
            this.setHelpUrl('');
            this.appendDummyInput()
                .appendField('Program Loops Infinitely')
                .appendField(new Blockly.FieldCheckbox(), "PROGRAM_DOES_LOOP")
        }
    };


    Blockly.Blocks['controls_repeat_custom'] = {
        init: function () {
            this.appendDummyInput()
                .appendField("Repeat")
                .appendField(new Blockly.FieldNumber(1), "TIMES")
                .appendField("times");
            this.appendStatementInput("DO")
                .appendField("Do:")
                .setCheck("move");
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
                .appendField('Speed:')
                .appendField(new Blockly.FieldNumber(0), 'SPEED')
                .setAlign(Blockly.ALIGN_RIGHT);
            this.setOutput(true, 'waypoint_controls');
            this.setColour(80);
            this.setTooltip('Set speed for the waypoint.');
        }
    };

    const workspace = Blockly.inject('blocklyDiv', {
        media: '../lib/blockly/media/',
        toolbox: toolbox,
        toolboxPosition: 'start',
    });

    // Override indentation to handle it myself
    Blockly.Python.INDENT = '';

    function generatePythonCode() {
        const code = python.pythonGenerator.workspaceToCode(workspace);

        // Add import statements and robot initialization
        let pythonCode = 
`import os
import sys

# Current script directory
current_script_directory = os.path.dirname(os.path.abspath(__file__))
# Path to the 'controllers' folder
controllers_directory = os.path.abspath(os.path.join(current_script_directory, os.pardir))

# Add 'controllers' directory to sys.path
if controllers_directory not in sys.path:
    sys.path.append(controllers_directory)

from robot_control import instruction, _controller
from collections import deque

`;

        // Concatenate the generated Python code
        pythonCode += code;
        move_block_index = 0
        return pythonCode;
    }

    Blockly.Python['program_root'] = function (block) {
        const robot_name = block.getFieldValue('ROBOT_NAME');
        const program_loops = block.getFieldValue('PROGRAM_DOES_LOOP') === 'TRUE';
        // Initialize the robot and devices from the given name
        let code =
`controller = _controller.RobotController('${robot_name}')
execution_queue = deque()

`;
        var mainCode = Blockly.Python.statementToCode(block, 'MAIN_PROGRAM');
        code += mainCode;
        code += 
`
while execution_queue:
    instruction = execution_queue.popleft()
    instruction_complete = instruction.execute(controller)
    if not instruction_complete:
        execution_queue.appendleft(instruction)
    controller.step_simulation()
`;
        if (program_loops) {
            code += 
`    execution_queue.append(instruction)
`;  // End of circular execution loop
        }

        return code;
    };


    Blockly.Python['controls_repeat_custom'] = function (block) {
        const times = block.getFieldValue('TIMES');
        let doCode = Blockly.Python.statementToCode(block, 'DO');
        doCode = addIndentation(doCode, 1);

        return `for i in range(${times}):\n${doCode}\n`;
    };


    Blockly.Python['move'] = function (block) {
        move_block_index += 1
        const index = move_block_index
        const waypointsCode = Blockly.Python.statementToCode(block, 'WAYPOINT');
        const cleanedWaypointsCode = waypointsCode.replace(/,\s*$/, ""); // Remove trailing comma and whitespace
        let code =
`move_instruction_${index} = instruction.Move("move${index}")
waypoints_${index} = [${cleanedWaypointsCode}]
for waypoint in waypoints_${index}:
    wp_options = {'coords': waypoint['coordinates']}
    if 'speed' in waypoint:
        wp_options['speed'] = waypoint['speed']
    wp = instruction.Waypoint(**wp_options)

    move_instruction_${index}.add_waypoint(wp)

execution_queue.append(move_instruction_${index})

`;
    
        return code;
    };

    Blockly.Python['waypoint'] = function (block) {
        const coordinatesCode = Blockly.Python.valueToCode(block, 'COORDINATES', Blockly.Python.ORDER_ATOMIC);
        const waypointControlsCode = Blockly.Python.valueToCode(block, 'WAYPOINT_CONTROLS', Blockly.Python.ORDER_ATOMIC);

        // let waypointcontrols decide if the entry for controls will exist for later error checking
        let code = `{ 'coordinates': ${coordinatesCode}, ${waypointControlsCode} }, `;

        return code;
    };

    Blockly.Python['coordinate_input'] = function (block) {
        const x = block.getFieldValue('X');
        const y = block.getFieldValue('Y');
        const z = block.getFieldValue('Z');

        return ['[' + x + ', ' + y + ', ' + z + ']', Blockly.Python.ORDER_ATOMIC];
    };

    Blockly.Python['waypoint_control'] = function (block) {
        const speed = block.getFieldValue('SPEED');

        // Only create an entry in the dictionary or speed is greater than 0
        let controlsCode = '';
        if (speed > 0) {
            controlsCode += `'speed': ${speed}, `;
        }

        return [controlsCode, Blockly.Python.ORDER_ATOMIC];
    };

    function addIndentation(code, indentLevel) {
        const indent = '    '; 
        const lines = code.split('\n');
        const indentedLines = lines.map(line => line ? indent.repeat(indentLevel) + line : line); 
        return indentedLines.join('\n');
    }

    // Attach the code generation function to the button click event
    document.getElementById('generateCodeButton').addEventListener('click', showGeneratedCode);
    document.getElementById('saveCodeButton').addEventListener('click', savePythonCodeToFile);

    function showGeneratedCode() {
        let pythonCode = generatePythonCode();
        document.getElementById('generated-code').innerText = pythonCode;
    }

    function savePythonCodeToFile() {
        let pythonCode = generatePythonCode();

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

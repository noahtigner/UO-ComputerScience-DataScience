"""
Graphical display of the duck machine state. 
"""

from mvc import MVCEvent
from cpu import CPU, CPUStep
from memory import MemoryEvent, MemoryRead, MemoryWrite
from memory import Memory

import graphics.graphics
from graphics.graphics import GraphWin, Rectangle, Point, Text

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

class MachineStateView(object):
    """View of the CPU and memory state"""

    def __init__(self, model: CPU,
                     width: int, height: int):
        """Create a view width x height"""
        self.width = width
        self.height = height
        self.model = model
        model.register_listener(self)
        model.memory.register_listener(self)

        self.window = graphics.graphics.GraphWin("Duck Machine", width, height)

        # CPU in left 1/3 of window
        cpu_region = Rectangle(Point(5,5),
                               Point(0.3 * self.width - 5, self.height - 5))
        cpu_region.setFill("#fafaff")
        cpu_region.draw(self.window)

        # 16 registers, whose display we'll keep in a list,
        # with display as 8 rows of 2 columns
        self.registers = [ ]
        self._draw_registers()

        # Current instruction word above registers, in top
        # 1/5 of window
        instr_word_display = Rectangle(Point(10,10),
                                       Point(0.3 * self.width -10, 0.2 * self.height - 5))
        instr_word_display.draw(self.window)
        self._draw_instruction(instr_word_display)

        # Memory in right 2/3 of window
        self._draw_memory()

    def _draw_instruction(self, in_rect):
        x_center = (in_rect.p1.x + in_rect.p2.x)/2.0
        height = in_rect.p2.y - in_rect.p1.y
        y_line_1 = in_rect.p1.y + 0.33 * height
        y_line_2 = in_rect.p1.y + 0.66 * height
        self.instr_raw = Text(Point(x_center, y_line_1), "_")
        self.instr_raw.setSize(18)
        self.instr_raw.draw(self.window)
        self.instr_decoded = Text(Point(x_center, y_line_2), "_")
        self.instr_decoded.setSize(16)
        self.instr_decoded.draw(self.window)


    def _draw_registers(self):
        reg_region_y_min = self.height * 0.2 + 5
        reg_region_y_max = self.height - 5
        reg_region_x_min = 5
        reg_region_x_max = 0.3 * self.width - 10
        self.reg_region = (reg_region_x_min, reg_region_y_min,
                           reg_region_x_max, reg_region_y_max)

        log.debug("Registers will display from {},{} to {},{}"
                  .format(reg_region_x_min,reg_region_y_min,
                          reg_region_x_max, reg_region_y_max))


        for reg_pair in range(8):
            self._draw_reg(reg_pair, 0)
            self._draw_reg(reg_pair, 1)

    def _draw_reg(self, row, col ):
        x_min, y_min, x_max, y_max = self.reg_region
        height = y_max - y_min
        width = x_max - x_min
        llx = x_min + col * 0.5 * width + 5
        lly = y_min + row * (height / 8)
        urx = x_min + (col + 1) * 0.5 * width  -10
        ury = y_min + (row + 1) * (height / 8)
        reg_display = Rectangle(Point(llx,lly), Point(urx,ury))
        reg_display.draw(self.window)
        reg_center = Point((llx+urx)/2, (lly+ury)/2)
        label = Text(reg_center,"_")
        label.setSize(24)
        label.draw(self.window)
        reg_display.label = label
        self.registers.append(reg_display)
        log.debug("Displayed register {} at {}".format(row*2 + col, reg_display))

    def _draw_memory(self):
        mem_region_y_min = 5
        mem_region_y_max = self.height - 5
        mem_region_x_min = 0.3 * self.width + 5
        mem_region_x_max = self.width - 5
        self.mem_region = (mem_region_x_min, mem_region_y_min,
                           mem_region_x_max, mem_region_y_max)

        self.mem_cells = [ ]
        for row in range(32):
            for col in range(8):
                self._draw_memory_cell(row, col)

    def _draw_memory_cell(self, row, col):
        x_min, y_min, x_max, y_max = self.mem_region
        width = x_max - x_min
        height = y_max - y_min
        cell_height = height/32
        cell_width = width/8
        llx = x_min + col * cell_width + 1
        lly = y_min + row * cell_height + 1
        urx = llx + cell_width - 2
        ury = lly + cell_height - 2
        mem_cell = Rectangle(Point(llx,lly), Point(urx,ury))
        mem_cell.setFill("#dddddd")
        mem_cell.draw(self.window)
        center = Point((llx + urx)/2, (lly+ury)/2)
        label = Text(center, ".")
        label.draw(self.window)
        mem_cell.label = label
        self.mem_cells.append(mem_cell)

    def notify(self, event: MVCEvent):
        """Something to depict"""
        if isinstance(event, CPUStep):
            self._cpu_step(event)
        elif isinstance(event, MemoryEvent):
            self._memory_event(event)

    def _cpu_step(self, event: CPUStep):
        self.instr_raw.setText(str(event.instr_word))
        self.instr_decoded.setText(str(event.instr))
        for reg_index in range(16):
            # Index both the display and the model registers
            reg_value = self.model.registers[reg_index].get()
            reg_display = self.registers[reg_index]
            reg_display.label.setText(str(reg_value))

    def _memory_event(self, event):
        """Memory was accessed"""
        log.debug("Memory event: {}".format(event))
        memory = event.subject
        address = event.addr
        value = event.value
        if address >= len(self.mem_cells):
            return
        cell_display = self.mem_cells[address]
        if isinstance(event, MemoryRead):
            cell_display.setFill("#DDFFDD")
        elif isinstance(event,MemoryWrite):
            cell_display.setFill("#DDDDFF")
        cell_display.label.setText(str(value))








    
            

            
            
        
            

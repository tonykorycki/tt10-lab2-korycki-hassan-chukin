# Defaults
SIM ?= icarus
TOPLEVEL_LANG ?= verilog
SRC_DIR = $(PWD)/../src
TEST_DIR = $(PWD)/test

# Verilog source files
PROJECT_SOURCES = project.v priority_encoder.v bitwise_majority.v

# Testbenches
TESTBENCHES = tb_project.v tb_priority_encoder.v tb_bitwise_majority.v

# Check if we are running gate-level simulation
ifneq ($(GATES),yes)
    # RTL simulation
    SIM_BUILD = sim_build/rtl
    VERILOG_SOURCES += $(addprefix $(SRC_DIR)/,$(PROJECT_SOURCES))
else
    # Gate-level simulation
    SIM_BUILD = sim_build/gl
    COMPILE_ARGS += -DGL_TEST -DFUNCTIONAL -DUSE_POWER_PINS -DSIM -DUNIT_DELAY=\#1
    VERILOG_SOURCES += $(PDK_ROOT)/sky130A/libs.ref/sky130_fd_sc_hd/verilog/primitives.v
    VERILOG_SOURCES += $(PDK_ROOT)/sky130A/libs.ref/sky130_fd_sc_hd/verilog/sky130_fd_sc_hd.v
    VERILOG_SOURCES += $(PWD)/gate_level_netlist.v
endif

# Include testbench sources
VERILOG_SOURCES += $(addprefix $(TEST_DIR)/,$(TESTBENCHES))

# Set top-level module
TOPLEVEL = tb_project  # Default, will be overridden per test
MODULE = test

# Define test targets
test_project:
	$(MAKE) SIM=$(SIM) TOPLEVEL=tb MODULE=test PROJECT_SOURCES=project.v run

test_priority_encoder:
	$(MAKE) SIM=$(SIM) TOPLEVEL=tb_priority_encoder MODULE=test PROJECT_SOURCES=priority_encoder.v run

test_bitwise_majority:
	$(MAKE) SIM=$(SIM) TOPLEVEL=tb_bitwise_majority MODULE=test PROJECT_SOURCES=bitwise_majority.v run

# Run all tests
test_all: test_project test_priority_encoder test_bitwise_majority

# Include cocotb’s make rules
include $(shell cocotb-config --makefiles)/Makefile.sim
